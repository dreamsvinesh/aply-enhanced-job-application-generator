#!/usr/bin/env python3
"""
Enhanced Job Description Parser with LLM Integration
Replaces rule-based keyword matching with intelligent LLM analysis for accurate job classification.
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import logging

# Import existing modules
from llm_service import LLMService
from database_manager import DatabaseManager

class EnhancedJobDescriptionParser:
    """
    Enhanced JD parser that uses LLM for intelligent analysis instead of keyword matching.
    
    Key improvements over original parser:
    - LLM-based role classification (eliminates substring matching bug)
    - Profile-aware analysis with credibility scoring
    - Comprehensive requirement extraction
    - Cultural and company context understanding
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        self.db_manager = DatabaseManager()
        self.logger = logging.getLogger(__name__)
        
        # Load user profile for profile-aware analysis
        self.user_profile = self._load_user_profile()
        
    def _load_user_profile(self) -> Dict:
        """Load user profile for profile-aware analysis."""
        try:
            profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load user profile: {e}")
            return {}
    
    def analyze_with_profile_awareness(self, jd_text: str, country: str) -> Tuple[Dict, bool]:
        """
        Analyze job description with profile awareness and credibility gating.
        
        Args:
            jd_text: Job description text
            country: Target country for cultural adaptation
            
        Returns:
            Tuple of (analysis_result, should_proceed)
            should_proceed is False if credibility score < 6/10
        """
        try:
            # Build comprehensive analysis prompt
            analysis_prompt = self._build_analysis_prompt(jd_text, country)
            
            # Call LLM for analysis
            analysis_response = self.llm_service.call_llm(
                prompt=analysis_prompt,
                task_type="jd_analysis",
                max_tokens=1200,
                temperature=0.1  # Low temperature for consistent analysis
            )
            
            # Parse LLM response
            analysis_result = self._parse_llm_analysis(analysis_response, jd_text, country)
            
            # Determine if we should proceed based on credibility score
            credibility_score = analysis_result.get('credibility_score', 0)
            should_proceed = credibility_score >= 6
            
            if not should_proceed:
                self.logger.info(f"Credibility score {credibility_score}/10 below threshold. Stopping application generation.")
            
            return analysis_result, should_proceed
            
        except Exception as e:
            self.logger.error(f"Error in profile-aware analysis: {e}")
            # Return fallback analysis with low credibility
            return self._get_fallback_analysis(jd_text, country), False
    
    def _build_analysis_prompt(self, jd_text: str, country: str) -> str:
        """Build comprehensive analysis prompt for LLM."""
        
        # Extract key user profile info for matching
        user_skills = self.user_profile.get('skills', {})
        user_experience = self.user_profile.get('experience', [])
        user_projects = self.user_profile.get('projects', [])
        
        return f"""
You are an expert job market analyst specializing in {country} recruitment. Analyze this job description against the user's profile and provide a comprehensive assessment.

JOB DESCRIPTION:
{jd_text}

USER PROFILE SUMMARY:
Technical Skills: {json.dumps(user_skills.get('technical', []))[:500]}
Business Skills: {json.dumps(user_skills.get('business', []))[:500]}
Experience: {len(user_experience)} roles in companies like {', '.join([exp.get('company', 'Unknown') for exp in user_experience[:3]])}
Key Projects: {', '.join([proj.get('name', 'Project') for proj in user_projects[:3]])}

ANALYSIS REQUIREMENTS:

1. ROLE CLASSIFICATION:
   - Primary role focus (e.g., "frontend_development", "product_management", "ai_ml", "communication_platforms")
   - Industry sector
   - Company stage (startup/scale-up/enterprise)

2. REQUIREMENTS ANALYSIS:
   - Must-have technical skills
   - Must-have business skills  
   - Nice-to-have skills
   - Experience level required
   - Domain expertise needed

3. PROFILE MATCHING & CREDIBILITY:
   - Skills alignment percentage
   - Experience relevance
   - Missing critical requirements
   - Credibility score (1-10): How believable would this application be?
   - Credibility reasoning

4. POSITIONING STRATEGY:
   - Key strengths to emphasize from user profile
   - How to frame user's experience for this role
   - Potential concerns to address
   - Cultural adaptation for {country} market

5. COMPANY CONTEXT:
   - Company culture indicators
   - Values and work environment
   - Growth stage and priorities

Return your analysis as JSON in this exact format:
{{
    "role_classification": {{
        "primary_focus": "specific_domain_here",
        "secondary_focus": "if_applicable", 
        "industry": "industry_sector",
        "company_stage": "startup/scaleup/enterprise",
        "seniority_level": "junior/mid/senior"
    }},
    "requirements": {{
        "must_have_technical": ["skill1", "skill2"],
        "must_have_business": ["skill1", "skill2"], 
        "nice_to_have": ["skill1", "skill2"],
        "experience_years": "1-3/3-5/5+",
        "domain_expertise": ["domain1", "domain2"]
    }},
    "profile_match": {{
        "technical_skills_match": 0.8,
        "business_skills_match": 0.7,
        "experience_relevance": 0.9,
        "missing_critical": ["critical_skill"],
        "matching_strengths": ["strength1", "strength2"],
        "credibility_score": 8,
        "credibility_reasoning": "Strong React experience aligns well with frontend role requirements"
    }},
    "positioning_strategy": {{
        "key_strengths_to_emphasize": ["strength1", "strength2"],
        "experience_framing": "How to position user's background",
        "address_gaps": ["How to address missing skills"],
        "cultural_adaptation": "How to adapt for {country} market"
    }},
    "company_context": {{
        "culture_indicators": ["collaborative", "fast-paced"],
        "values": ["innovation", "user-focus"],
        "work_environment": "remote-first/hybrid/office",
        "priorities": ["growth", "technical excellence"]
    }},
    "extracted_info": {{
        "company_name": "Company Name",
        "role_title": "Exact Role Title",
        "location": "Location",
        "employment_type": "full-time/contract/part-time"
    }}
}}

CRITICAL: Ensure credibility_score accurately reflects how believable this application would be. Score 1-4 = weak fit, 5-6 = borderline, 7-8 = good fit, 9-10 = excellent fit.
"""

    def _parse_llm_analysis(self, llm_response: str, jd_text: str, country: str) -> Dict:
        """Parse LLM analysis response into structured format."""
        try:
            # Extract JSON from LLM response
            if "```json" in llm_response:
                json_start = llm_response.find("```json") + 7
                json_end = llm_response.find("```", json_start)
                json_str = llm_response[json_start:json_end].strip()
            else:
                # Try to find JSON object
                json_start = llm_response.find("{")
                json_end = llm_response.rfind("}") + 1
                json_str = llm_response[json_start:json_end]
            
            analysis = json.loads(json_str)
            
            # Add metadata
            analysis['raw_jd_text'] = jd_text
            analysis['analysis_country'] = country
            analysis['analysis_method'] = 'llm_enhanced'
            analysis['analysis_timestamp'] = self._get_timestamp()
            
            return analysis
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM analysis JSON: {e}")
            self.logger.error(f"LLM Response: {llm_response[:500]}...")
            return self._get_fallback_analysis(jd_text, country)
        except Exception as e:
            self.logger.error(f"Error parsing LLM analysis: {e}")
            return self._get_fallback_analysis(jd_text, country)
    
    def _get_fallback_analysis(self, jd_text: str, country: str) -> Dict:
        """Generate fallback analysis if LLM call fails."""
        return {
            "role_classification": {
                "primary_focus": "unknown",
                "secondary_focus": None,
                "industry": "unknown", 
                "company_stage": "unknown",
                "seniority_level": "mid"
            },
            "requirements": {
                "must_have_technical": [],
                "must_have_business": [],
                "nice_to_have": [],
                "experience_years": "3-5",
                "domain_expertise": []
            },
            "profile_match": {
                "technical_skills_match": 0.5,
                "business_skills_match": 0.5,
                "experience_relevance": 0.5,
                "missing_critical": ["Unable to analyze"],
                "matching_strengths": [],
                "credibility_score": 3,  # Low score due to analysis failure
                "credibility_reasoning": "Unable to perform analysis - LLM service unavailable"
            },
            "positioning_strategy": {
                "key_strengths_to_emphasize": [],
                "experience_framing": "Generic professional background",
                "address_gaps": ["Analysis unavailable"],
                "cultural_adaptation": f"Standard professional approach for {country}"
            },
            "company_context": {
                "culture_indicators": [],
                "values": [],
                "work_environment": "unknown",
                "priorities": []
            },
            "extracted_info": {
                "company_name": self._extract_company_regex(jd_text),
                "role_title": self._extract_role_regex(jd_text),
                "location": country,
                "employment_type": "full-time"
            },
            "raw_jd_text": jd_text,
            "analysis_country": country,
            "analysis_method": "fallback",
            "analysis_timestamp": self._get_timestamp()
        }
    
    def _extract_company_regex(self, jd_text: str) -> str:
        """Fallback company extraction using regex."""
        patterns = [
            r'(?i)(?:company|organization|at)\s+([A-Z][a-zA-Z\s&.]{2,30})',
            r'(?i)join\s+([A-Z][a-zA-Z\s&.]{2,30})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, jd_text)
            if match:
                company = match.group(1).strip()
                if len(company) > 3:
                    return company
        
        return "Unknown Company"
    
    def _extract_role_regex(self, jd_text: str) -> str:
        """Fallback role extraction using regex."""
        patterns = [
            r'(?i)(?:role|position|job title):\s*([^\n\r]{5,50})',
            r'(?i)we\'re looking for a\s+([^\n\r]{5,50})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, jd_text)
            if match:
                title = match.group(1).strip()
                if 5 <= len(title) <= 50:
                    return title
        
        return "Unknown Role"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis metadata."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def compare_with_legacy_parser(self, jd_text: str) -> Dict:
        """
        Compare new LLM analysis with legacy parser results for validation.
        Useful for testing and transition period.
        """
        try:
            # Import legacy parser
            from jd_parser import JobDescriptionParser
            legacy_parser = JobDescriptionParser()
            
            # Get legacy analysis
            legacy_result = legacy_parser.parse(jd_text)
            
            # Get new analysis (without profile awareness for fair comparison)
            analysis_prompt = f"""
            Analyze this job description and extract key information:
            
            {jd_text}
            
            Return JSON with:
            {{
                "ai_ml_focus_score": 0.0-1.0,
                "business_model": "b2b/b2c/mixed",
                "seniority_level": "junior/mid/senior",
                "primary_skills": ["skill1", "skill2"],
                "company_name": "extracted name",
                "role_title": "extracted title"
            }}
            """
            
            llm_response = self.llm_service.call_llm(
                prompt=analysis_prompt,
                task_type="comparison_analysis",
                max_tokens=500
            )
            
            # Parse comparison
            new_result = json.loads(llm_response)
            
            return {
                "legacy_analysis": legacy_result,
                "llm_analysis": new_result,
                "comparison": {
                    "ai_ml_focus_diff": abs(legacy_result.get('ai_ml_focus', 0) - new_result.get('ai_ml_focus_score', 0)),
                    "business_model_match": legacy_result.get('b2b_vs_b2c') == new_result.get('business_model'),
                    "seniority_match": legacy_result.get('seniority_level') == new_result.get('seniority_level')
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in comparison analysis: {e}")
            return {"error": str(e)}
    
    def batch_analyze_applications(self, applications: List[Dict]) -> List[Dict]:
        """
        Analyze multiple job applications efficiently.
        
        Args:
            applications: List of dicts with 'jd_text' and 'country' keys
            
        Returns:
            List of analysis results
        """
        results = []
        
        for i, app in enumerate(applications):
            self.logger.info(f"Analyzing application {i+1}/{len(applications)}")
            
            analysis, should_proceed = self.analyze_with_profile_awareness(
                app['jd_text'], 
                app['country']
            )
            
            results.append({
                'analysis': analysis,
                'should_proceed': should_proceed,
                'original_application': app
            })
        
        return results
    
    def get_analysis_summary(self, analysis: Dict) -> str:
        """Generate human-readable summary of analysis."""
        try:
            role_focus = analysis['role_classification']['primary_focus']
            credibility = analysis['profile_match']['credibility_score']
            company = analysis['extracted_info']['company_name']
            
            match_summary = f"Technical: {analysis['profile_match']['technical_skills_match']*100:.0f}%, "
            match_summary += f"Business: {analysis['profile_match']['business_skills_match']*100:.0f}%"
            
            summary = f"""
🎯 **Role Analysis: {company}**
• Focus: {role_focus.replace('_', ' ').title()}
• Credibility: {credibility}/10 
• Skills Match: {match_summary}
• Key Strengths: {', '.join(analysis['positioning_strategy']['key_strengths_to_emphasize'][:3])}
"""
            
            if credibility < 6:
                summary += f"\n⚠️ **Low credibility score - consider skipping this application**"
            
            return summary.strip()
            
        except Exception as e:
            return f"Error generating summary: {e}"

    def save_analysis_to_database(self, 
                                company: str, 
                                role_title: str, 
                                country: str, 
                                jd_text: str, 
                                analysis: Dict) -> int:
        """
        Save analysis results to database for tracking and analytics.
        
        Returns:
            Application ID
        """
        try:
            # Extract components for database storage
            credibility_score = analysis['profile_match']['credibility_score']
            
            # Prepare data for database
            jd_analysis = {
                'role_classification': analysis['role_classification'],
                'requirements': analysis['requirements'],
                'company_context': analysis['company_context']
            }
            
            profile_match_analysis = analysis['profile_match']
            positioning_strategy = analysis['positioning_strategy']
            
            # Save to database
            application_id = self.db_manager.create_application(
                company=company,
                role_title=role_title,
                country=country,
                jd_text=jd_text,
                jd_analysis=jd_analysis,
                credibility_score=credibility_score,
                profile_match_analysis=profile_match_analysis,
                positioning_strategy=positioning_strategy
            )
            
            self.logger.info(f"Analysis saved to database with ID: {application_id}")
            return application_id
            
        except Exception as e:
            self.logger.error(f"Error saving analysis to database: {e}")
            raise
    
    def get_credibility_gate_stats(self, days: int = 30) -> Dict:
        """Get statistics on credibility gate decisions."""
        try:
            applications = self.db_manager.get_applications()
            
            if not applications:
                return {"total": 0, "passed_gate": 0, "gate_pass_rate": 0.0}
            
            total_apps = len(applications)
            passed_gate = len([app for app in applications if app['credibility_score'] >= 6])
            
            return {
                "total_analyzed": total_apps,
                "passed_credibility_gate": passed_gate,
                "gate_pass_rate": passed_gate / total_apps,
                "avg_credibility_score": sum(app['credibility_score'] for app in applications) / total_apps,
                "credibility_distribution": self._get_credibility_distribution(applications)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting credibility stats: {e}")
            return {"error": str(e)}
    
    def _get_credibility_distribution(self, applications: List[Dict]) -> Dict:
        """Get distribution of credibility scores."""
        distribution = {
            "1-3_poor": 0,
            "4-5_weak": 0, 
            "6-7_good": 0,
            "8-10_excellent": 0
        }
        
        for app in applications:
            score = app['credibility_score']
            if score <= 3:
                distribution["1-3_poor"] += 1
            elif score <= 5:
                distribution["4-5_weak"] += 1
            elif score <= 7:
                distribution["6-7_good"] += 1
            else:
                distribution["8-10_excellent"] += 1
        
        return distribution