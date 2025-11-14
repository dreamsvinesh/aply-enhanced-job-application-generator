#!/usr/bin/env python3
"""
Enhanced Role Fit Analyzer
Integrates existing agents with LLM-powered JD analysis and comprehensive profile data
"""

import time
from typing import Dict, List, Optional
from pathlib import Path
import json

from .role_fit_agents import (
    DomainMismatchAgent, 
    SkillsGapAgent, 
    ExperienceMatchingAgent, 
    IndustryAlignmentAgent,
    AgentResult
)
from .llm_jd_parser import analyze_job_description, JDAnalysis
from .profile_extractor import ProfileExtractor

class EnhancedRoleFitAnalyzer:
    """
    Enhanced role fit analyzer that combines:
    1. LLM-powered job analysis
    2. Comprehensive profile data
    3. Existing specialized agents
    4. Intelligent result aggregation
    """
    
    def __init__(self):
        # Initialize existing agents
        self.domain_agent = DomainMismatchAgent()
        self.skills_agent = SkillsGapAgent()
        self.experience_agent = ExperienceMatchingAgent()
        self.industry_agent = IndustryAlignmentAgent()
        
        # Profile and data management
        self.profile_extractor = ProfileExtractor()
        self.profile_data = self.load_comprehensive_profile()
        
    def load_comprehensive_profile(self) -> Dict:
        """Load comprehensive profile data"""
        profile = self.profile_extractor.load_profile()
        
        if profile:
            print("✅ Loaded comprehensive profile")
            return profile
        else:
            print("⚠️  No comprehensive profile found, using basic profile")
            # Fallback to basic profile structure
            return self._load_basic_profile()
    
    def _load_basic_profile(self) -> Dict:
        """Load basic profile as fallback"""
        basic_profile_path = Path(__file__).parent.parent / "config" / "user_profile.json"
        
        if basic_profile_path.exists():
            try:
                with open(basic_profile_path, 'r') as f:
                    basic = json.load(f)
                
                # Convert to comprehensive format structure
                return self._convert_basic_to_comprehensive(basic)
            except Exception as e:
                print(f"⚠️  Failed to load basic profile: {e}")
        
        return self._get_default_comprehensive_profile()
    
    def _convert_basic_to_comprehensive(self, basic_profile: Dict) -> Dict:
        """Convert basic profile to comprehensive structure"""
        return {
            'personal_info': {
                'name': 'User',
                'total_experience_years': basic_profile.get('basic_info', {}).get('experience_years', 7),
                'pm_experience_years': 7
            },
            'experience_domains': {
                'fintech': {'experience_level': 'intermediate', 'years_experience': 3},
                'enterprise_saas': {'experience_level': 'advanced', 'years_experience': 5},
                'ai_automation': {'experience_level': 'intermediate', 'years_experience': 2}
            },
            'skills_detailed': {
                'product_management': {
                    'proficiency': 'expert',
                    'specific_skills': basic_profile.get('skills', {}).get('core_skills', [])
                }
            },
            'preferences': {
                'industries_avoid': basic_profile.get('experience', {}).get('avoid_domains', [])
            }
        }
    
    def _get_default_comprehensive_profile(self) -> Dict:
        """Default comprehensive profile structure"""
        return {
            'personal_info': {
                'name': 'User',
                'total_experience_years': 7,
                'pm_experience_years': 7
            },
            'experience_domains': {
                'fintech': {'experience_level': 'intermediate'},
                'enterprise_saas': {'experience_level': 'advanced'},
                'ai_automation': {'experience_level': 'intermediate'}
            },
            'skills_detailed': {
                'product_management': {
                    'proficiency': 'expert',
                    'specific_skills': ['product strategy', 'stakeholder management', 'data analysis']
                }
            },
            'preferences': {
                'industries_avoid': ['crypto', 'gambling', 'adult_content']
            }
        }
    
    def analyze_comprehensive_fit(self, job_description: str, timeout: float = 20.0) -> Dict:
        """
        Comprehensive role fit analysis using LLM JD analysis + agents
        
        Returns enhanced analysis with detailed reasoning
        """
        start_time = time.time()
        
        analysis = {
            "fit_score": 0,
            "recommendation": "",
            "critical_gaps": [],
            "minor_gaps": [],
            "strengths": [],
            "effort_required": "high",
            "should_apply": False,
            "detailed_analysis": {},
            "agent_results": {},
            "llm_jd_analysis": {},
            "profile_matching": {},
            "execution_time": 0,
            "analysis_cost": 0.0
        }
        
        try:
            # Step 1: LLM-powered JD analysis
            print("🧠 Analyzing job description with LLM...")
            jd_analysis = analyze_job_description(job_description, use_cache=True)
            
            analysis["analysis_cost"] += jd_analysis.analysis_cost
            
            if not jd_analysis.success:
                analysis["recommendation"] = f"ANALYSIS ERROR - {jd_analysis.error_message}"
                analysis["should_apply"] = False
                analysis["critical_gaps"] = [f"JD analysis failed: {jd_analysis.error_message}"]
                return analysis
            
            # Store LLM analysis results
            analysis["llm_jd_analysis"] = {
                "company": jd_analysis.company,
                "role_title": jd_analysis.role_title,
                "domain_focus": jd_analysis.domain_focus,
                "industry": jd_analysis.industry,
                "required_skills": jd_analysis.required_skills,
                "experience_years": jd_analysis.experience_years,
                "regulatory_requirements": jd_analysis.regulatory_requirements,
                "confidence_score": jd_analysis.confidence_score,
                "llm_reasoning": jd_analysis.llm_reasoning
            }
            
            print(f"✅ JD Analysis: {jd_analysis.company} - {jd_analysis.domain_focus}")
            
            # Step 2: Profile-to-JD matching analysis
            profile_match = self._analyze_profile_domain_fit(jd_analysis)
            analysis["profile_matching"] = profile_match
            
            # Step 3: Run existing agents with enhanced data
            if time.time() - start_time < timeout:
                # Convert LLM analysis to format agents expect
                agent_jd_data = self._convert_llm_to_agent_format(jd_analysis)
                agent_profile_data = self._convert_profile_to_agent_format(self.profile_data)
                
                # Domain mismatch analysis
                domain_result = self.domain_agent.analyze(agent_profile_data, job_description)
                analysis["agent_results"]["domain"] = domain_result
                
                # Skills gap analysis with enhanced data
                skills_result = self.skills_agent.analyze(agent_profile_data, agent_jd_data)
                analysis["agent_results"]["skills"] = skills_result
                
                # Experience matching
                experience_result = self.experience_agent.analyze(agent_profile_data, agent_jd_data)
                analysis["agent_results"]["experience"] = experience_result
                
                # Industry alignment
                industry_result = self.industry_agent.analyze(agent_profile_data, agent_jd_data)
                analysis["agent_results"]["industry"] = industry_result
                
            # Step 4: Intelligent result aggregation
            analysis = self._aggregate_enhanced_results(analysis, jd_analysis, profile_match)
            
        except Exception as e:
            analysis["recommendation"] = f"ANALYSIS ERROR - {str(e)}"
            analysis["should_apply"] = False
            analysis["critical_gaps"] = [f"Enhanced analysis failed: {str(e)}"]
        
        analysis["execution_time"] = time.time() - start_time
        return analysis
    
    def _analyze_profile_domain_fit(self, jd_analysis: JDAnalysis) -> Dict:
        """Analyze how well user's profile matches the specific domain/role"""
        
        profile_domains = self.profile_data.get('experience_domains', {})
        
        # Map JD domain to profile domains
        domain_mapping = {
            'payments': 'fintech',
            'fintech': 'fintech', 
            'banking': 'fintech',
            'financial_services': 'fintech',
            'enterprise': 'enterprise_saas',
            'b2b_saas': 'enterprise_saas',
            'saas': 'enterprise_saas',
            'ai_ml': 'ai_automation',
            'artificial_intelligence': 'ai_automation',
            'machine_learning': 'ai_automation'
        }
        
        jd_domain = jd_analysis.domain_focus.lower()
        profile_domain_key = domain_mapping.get(jd_domain, 'enterprise_saas')  # Default fallback
        
        profile_domain = profile_domains.get(profile_domain_key, {})
        experience_level = profile_domain.get('experience_level', 'basic')
        domain_years = profile_domain.get('years_experience', 0)
        
        # Calculate domain fit score
        experience_scores = {
            'none': 0.0,
            'basic': 0.3,
            'intermediate': 0.7,
            'advanced': 0.9,
            'expert': 1.0
        }
        
        domain_score = experience_scores.get(experience_level, 0.3)
        
        # Check for specific domain requirements
        domain_strengths = []
        domain_gaps = []
        
        if jd_domain in ['payments', 'fintech']:
            if profile_domain_key == 'fintech':
                domain_strengths.append(f"Strong fintech background ({experience_level})")
                if domain_years >= jd_analysis.experience_years:
                    domain_strengths.append(f"Sufficient domain experience ({domain_years} years)")
                else:
                    domain_gaps.append(f"Limited fintech experience ({domain_years} vs {jd_analysis.experience_years}+ required)")
            else:
                domain_gaps.append("No direct fintech/payments experience")
        
        # Check regulatory alignment
        if jd_analysis.regulatory_requirements:
            profile_regulatory = profile_domain.get('regulatory_knowledge', [])
            missing_regulatory = [req for req in jd_analysis.regulatory_requirements 
                                if not any(reg.lower() in req.lower() for reg in profile_regulatory)]
            
            if missing_regulatory:
                domain_gaps.append(f"Missing regulatory knowledge: {', '.join(missing_regulatory)}")
            else:
                domain_strengths.append("Regulatory knowledge aligns")
        
        return {
            'domain_score': domain_score,
            'matched_domain': profile_domain_key,
            'experience_level': experience_level,
            'domain_years': domain_years,
            'strengths': domain_strengths,
            'gaps': domain_gaps,
            'regulatory_alignment': len(jd_analysis.regulatory_requirements) == 0 or len(domain_gaps) == 0
        }
    
    def _convert_llm_to_agent_format(self, jd_analysis: JDAnalysis) -> Dict:
        """Convert LLM analysis to format expected by existing agents"""
        return {
            'company': jd_analysis.company,
            'role_title': jd_analysis.role_title,
            'required_skills': jd_analysis.required_skills,
            'preferred_skills': jd_analysis.preferred_skills,
            'experience_years': jd_analysis.experience_years,
            'seniority_level': jd_analysis.seniority_level,
            'industry': jd_analysis.industry,
            'domain': jd_analysis.domain_focus,
            'company_stage': jd_analysis.company_stage,
            'company_size': jd_analysis.company_size
        }
    
    def _convert_profile_to_agent_format(self, profile_data: Dict) -> Dict:
        """Convert comprehensive profile to format expected by agents"""
        
        # Extract skills from detailed structure
        all_skills = []
        skills_detailed = profile_data.get('skills_detailed', {})
        
        for category, skill_info in skills_detailed.items():
            specific_skills = skill_info.get('specific_skills', [])
            all_skills.extend(specific_skills)
        
        # Get experience info
        personal_info = profile_data.get('personal_info', {})
        preferences = profile_data.get('preferences', {})
        
        return {
            'experience': {
                'avoid_domains': preferences.get('industries_avoid', []),
                'industries': preferences.get('industries_interested', ['fintech', 'saas', 'technology'])
            },
            'skills': {
                'core_skills': all_skills
            },
            'basic_info': {
                'experience_years': personal_info.get('total_experience_years', 7),
                'experience_level': 'senior'
            }
        }
    
    def _aggregate_enhanced_results(self, analysis: Dict, jd_analysis: JDAnalysis, profile_match: Dict) -> Dict:
        """Enhanced result aggregation using LLM insights and profile matching"""
        
        agent_results = analysis["agent_results"]
        
        # Base scoring with enhanced weights
        scores = {}
        weights = {
            "domain": 0.35,    # Increased weight for domain fit
            "skills": 0.30,    # Skills alignment
            "experience": 0.20, # Experience level
            "industry": 0.15   # Industry transition
        }
        
        total_weight = 0.0
        weighted_score = 0.0
        
        # Include profile domain matching in scoring
        profile_domain_score = profile_match['domain_score'] * 100
        scores['profile_domain'] = profile_domain_score
        
        # Process agent results
        for agent_type, result in agent_results.items():
            if result.success:
                scores[agent_type] = result.score * 100
                weighted_score += result.score * weights.get(agent_type, 0.25)
                total_weight += weights.get(agent_type, 0.25)
        
        # Blend profile domain score into final calculation
        if total_weight > 0:
            agent_score = (weighted_score / total_weight) * 100
            # Blend agent score with profile domain score (70% agent, 30% profile)
            analysis["fit_score"] = (agent_score * 0.7) + (profile_domain_score * 0.3)
        else:
            analysis["fit_score"] = profile_domain_score
        
        # Enhanced gap and strength identification
        critical_gaps = []
        strengths = []
        
        # Domain-specific analysis
        if profile_match['domain_score'] < 0.4:
            critical_gaps.extend([f"Profile Domain: {gap}" for gap in profile_match['gaps']])
        else:
            strengths.extend([f"Profile Domain: {strength}" for strength in profile_match['strengths']])
        
        # Agent-based gaps and strengths
        for agent_type, result in agent_results.items():
            if result.success:
                if result.score < 0.4:
                    critical_gaps.append(f"{agent_type.title()}: {result.findings[0] if result.findings else 'Low compatibility'}")
                elif result.score > 0.8:
                    strengths.append(f"{agent_type.title()}: {result.findings[0] if result.findings else 'Strong alignment'}")
        
        # Enhanced recommendation logic
        fit_score = analysis["fit_score"]
        has_domain_conflict = any('avoid' in gap.lower() or 'conflict' in gap.lower() 
                                for gap in critical_gaps)
        
        if has_domain_conflict:
            analysis["recommendation"] = "POOR FIT - Domain conflicts with profile preferences"
            analysis["effort_required"] = "very_high"
            analysis["should_apply"] = False
        elif fit_score >= 80:
            analysis["recommendation"] = "STRONG FIT - Apply with confidence"
            analysis["effort_required"] = "low"
            analysis["should_apply"] = True
        elif fit_score >= 65:
            analysis["recommendation"] = "GOOD FIT - Apply with targeted customization"
            analysis["effort_required"] = "medium"
            analysis["should_apply"] = True
        elif fit_score >= 50:
            analysis["recommendation"] = "MODERATE FIT - Consider with significant preparation"
            analysis["effort_required"] = "high"
            analysis["should_apply"] = False
        else:
            analysis["recommendation"] = "POOR FIT - Not recommended"
            analysis["effort_required"] = "very_high"
            analysis["should_apply"] = False
        
        analysis["critical_gaps"] = critical_gaps
        analysis["strengths"] = strengths
        analysis["detailed_analysis"] = scores
        
        return analysis
    
    def generate_enhanced_fit_report(self, job_description: str) -> str:
        """Generate detailed fit analysis report"""
        analysis = self.analyze_comprehensive_fit(job_description)
        
        report_lines = []
        report_lines.append("## ENHANCED ROLE FIT ANALYSIS")
        report_lines.append("")
        
        # LLM Analysis Summary
        llm_data = analysis.get("llm_jd_analysis", {})
        if llm_data:
            report_lines.append(f"**🏢 Job Analysis:** {llm_data.get('company', 'Unknown')} - {llm_data.get('role_title', 'Unknown')}")
            report_lines.append(f"**🎯 Domain Focus:** {llm_data.get('domain_focus', 'Unknown')}")
            report_lines.append(f"**🏭 Industry:** {llm_data.get('industry', 'Unknown')}")
            report_lines.append("")
        
        # Overall Assessment
        report_lines.append(f"**Overall Fit Score:** {analysis['fit_score']:.0f}/100")
        report_lines.append(f"**Recommendation:** {analysis['recommendation']}")
        report_lines.append(f"**Effort Required:** {analysis['effort_required'].title()}")
        report_lines.append(f"**Should Apply:** {'✅ Yes' if analysis['should_apply'] else '❌ No'}")
        report_lines.append("")
        
        # Profile Domain Matching
        profile_match = analysis.get("profile_matching", {})
        if profile_match:
            report_lines.append(f"**Domain Experience:** {profile_match.get('experience_level', 'Unknown').title()} level in {profile_match.get('matched_domain', 'Unknown')}")
            report_lines.append(f"**Domain Years:** {profile_match.get('domain_years', 0)} years")
            report_lines.append("")
        
        # Strengths and Gaps
        if analysis['strengths']:
            report_lines.append("### ✅ Strengths")
            for strength in analysis['strengths']:
                report_lines.append(f"• {strength}")
            report_lines.append("")
        
        if analysis['critical_gaps']:
            report_lines.append("### ❌ Critical Gaps")
            for gap in analysis['critical_gaps']:
                report_lines.append(f"• {gap}")
            report_lines.append("")
        
        # Agent Breakdown
        agent_results = analysis.get("agent_results", {})
        if agent_results:
            report_lines.append("### 🤖 Agent Analysis Breakdown")
            for agent_name, result in agent_results.items():
                if result.success:
                    score_pct = result.score * 100
                    report_lines.append(f"• **{agent_name.title()}:** {score_pct:.0f}% ({result.confidence:.0%} confidence)")
            report_lines.append("")
        
        # Cost and Performance
        report_lines.append(f"**Analysis Cost:** ${analysis.get('analysis_cost', 0):.4f}")
        report_lines.append(f"**Execution Time:** {analysis.get('execution_time', 0):.2f}s")
        
        return "\n".join(report_lines)

# Global instance for easy access
enhanced_analyzer = EnhancedRoleFitAnalyzer()

# Convenience function
def analyze_enhanced_fit(job_description: str) -> Dict:
    """Convenience function for enhanced role fit analysis"""
    return enhanced_analyzer.analyze_comprehensive_fit(job_description)