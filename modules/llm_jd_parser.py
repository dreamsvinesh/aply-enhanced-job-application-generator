#!/usr/bin/env python3
"""
LLM-Powered Job Description Parser
Replaces keyword-based analysis with intelligent LLM understanding
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from .llm_service import call_llm

@dataclass
class JDAnalysis:
    """Structured job description analysis result"""
    success: bool
    company: str
    role_title: str
    industry: str
    role_type: str
    experience_years: int
    seniority_level: str
    required_skills: List[str]
    preferred_skills: List[str]
    tech_stack: List[str]
    company_stage: str
    company_size: str
    remote_friendly: bool
    location: str
    culture_keywords: List[str]
    key_responsibilities: List[str]
    success_metrics: List[str]
    domain_focus: str
    regulatory_requirements: List[str]
    team_structure: str
    growth_opportunities: List[str]
    confidence_score: float
    analysis_cost: float
    raw_jd: str
    llm_reasoning: str
    error_message: Optional[str] = None

class LLMJobDescriptionParser:
    """Intelligent job description parser using LLM analysis"""
    
    def __init__(self):
        self.cache_dir = Path(__file__).parent.parent / "cache" / "jd_analysis"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def get_cache_key(self, job_description: str) -> str:
        """Generate cache key for job description"""
        # Use hash of cleaned JD text for consistent caching
        cleaned_jd = ' '.join(job_description.split())  # Normalize whitespace
        return hashlib.md5(cleaned_jd.encode()).hexdigest()
    
    def load_cached_analysis(self, job_description: str) -> Optional[JDAnalysis]:
        """Load cached analysis if available"""
        cache_key = self.get_cache_key(job_description)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                return JDAnalysis(**data)
            except Exception as e:
                print(f"Warning: Failed to load cached analysis: {e}")
        
        return None
    
    def save_analysis_to_cache(self, analysis: JDAnalysis):
        """Save analysis to cache"""
        try:
            cache_key = self.get_cache_key(analysis.raw_jd)
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            # Convert to dict for JSON serialization
            data = {
                'success': analysis.success,
                'company': analysis.company,
                'role_title': analysis.role_title,
                'industry': analysis.industry,
                'role_type': analysis.role_type,
                'experience_years': analysis.experience_years,
                'seniority_level': analysis.seniority_level,
                'required_skills': analysis.required_skills,
                'preferred_skills': analysis.preferred_skills,
                'tech_stack': analysis.tech_stack,
                'company_stage': analysis.company_stage,
                'company_size': analysis.company_size,
                'remote_friendly': analysis.remote_friendly,
                'location': analysis.location,
                'culture_keywords': analysis.culture_keywords,
                'key_responsibilities': analysis.key_responsibilities,
                'success_metrics': analysis.success_metrics,
                'domain_focus': analysis.domain_focus,
                'regulatory_requirements': analysis.regulatory_requirements,
                'team_structure': analysis.team_structure,
                'growth_opportunities': analysis.growth_opportunities,
                'confidence_score': analysis.confidence_score,
                'analysis_cost': analysis.analysis_cost,
                'raw_jd': analysis.raw_jd,
                'llm_reasoning': analysis.llm_reasoning,
                'error_message': analysis.error_message
            }
            
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Failed to cache analysis: {e}")
    
    def build_analysis_prompt(self, job_description: str) -> str:
        """Build comprehensive analysis prompt for LLM"""
        
        return f"""
You are an expert job market analyst. Analyze this job description and extract structured information.

JOB DESCRIPTION:
{job_description}

Extract the following information and return as valid JSON:

{{
    "company": "Company name (extract from text, not 'Unknown')",
    "role_title": "Clean job title (e.g., 'Senior Product Manager', 'Software Engineer')",
    "industry": "Primary industry (e.g., 'fintech', 'healthcare', 'saas', 'ecommerce', 'enterprise_software')",
    "role_type": "Role category (e.g., 'product_manager', 'software_engineer', 'data_scientist', 'designer')",
    "experience_years": "Minimum years required (number, 0 if not specified)",
    "seniority_level": "Level (entry/mid/senior/staff/principal/director)",
    "required_skills": [
        "List of explicitly required skills and technologies",
        "Include specific technologies, methodologies, tools mentioned as required"
    ],
    "preferred_skills": [
        "List of preferred/nice-to-have skills",
        "Include bonus qualifications"
    ],
    "tech_stack": [
        "Specific technologies mentioned (programming languages, platforms, tools)",
        "e.g., React, Python, Salesforce, AWS, etc."
    ],
    "company_stage": "startup/scaleup/growth/enterprise/public (based on description)",
    "company_size": "estimate based on context (startup/small/medium/large/enterprise)",
    "remote_friendly": true/false,
    "location": "Primary location or 'Remote'",
    "culture_keywords": [
        "Words describing company culture",
        "e.g., innovative, collaborative, fast-paced, etc."
    ],
    "key_responsibilities": [
        "Top 5 main responsibilities from job description",
        "Focus on specific activities and deliverables"
    ],
    "success_metrics": [
        "How success is measured in this role",
        "KPIs, goals, expected outcomes mentioned"
    ],
    "domain_focus": "Primary domain (payments/healthcare/fintech/ai_ml/enterprise/consumer/b2b_saas/etc)",
    "regulatory_requirements": [
        "Any compliance, regulatory, or certification requirements",
        "e.g., PSD2, GDPR, SOX, HIPAA, etc."
    ],
    "team_structure": "Description of team (size, cross-functional, leadership, etc.)",
    "growth_opportunities": [
        "Career growth and learning opportunities mentioned"
    ],
    "confidence_score": 0.85,
    "llm_reasoning": "Brief explanation of your analysis and any ambiguities"
}}

ANALYSIS GUIDELINES:
1. **Company Name**: Extract actual company name from text, don't use generic terms
2. **Industry Classification**: 
   - fintech: banking, payments, financial services
   - healthcare: medical, pharma, healthtech
   - saas: software-as-a-service, enterprise software
   - ecommerce: retail, marketplace, shopping
   - ai_ml: artificial intelligence, machine learning focus
3. **Domain Focus**: Be specific about the business area
   - payments: card processing, payment flows, fintech infrastructure
   - healthcare: medical devices, patient care, health data
   - enterprise: B2B tools, internal operations, business software
   - consumer: B2C products, user-facing applications
4. **Skills Extraction**: 
   - Required: Must-have skills explicitly stated
   - Preferred: Nice-to-have, bonus qualifications
   - Avoid inferring skills not explicitly mentioned
5. **Experience Level**: 
   - Look for "X+ years", "senior", "lead", etc.
   - entry: 0-2 years, mid: 3-5 years, senior: 5+ years
6. **Regulatory**: Extract specific compliance requirements mentioned
7. **Be Conservative**: If something is unclear, mark as "not_specified" rather than guessing

CRITICAL: Return ONLY valid JSON. No additional text or explanations outside the JSON structure.
"""
    
    def analyze_job_description(self, job_description: str, use_cache: bool = True) -> JDAnalysis:
        """
        Analyze job description using LLM
        
        Args:
            job_description: Full job description text
            use_cache: Whether to use cached results
        
        Returns:
            JDAnalysis with structured data
        """
        
        # Check cache first
        if use_cache:
            cached = self.load_cached_analysis(job_description)
            if cached:
                print("📋 Using cached JD analysis")
                return cached
        
        # Build analysis prompt
        prompt = self.build_analysis_prompt(job_description)
        
        # Call LLM for analysis
        response = call_llm(
            prompt=prompt,
            task_type="analysis",
            use_cache=False,  # Don't cache at LLM level for JD analysis
            max_tokens=2000
        )
        
        if not response.success:
            return JDAnalysis(
                success=False,
                company="Unknown",
                role_title="Unknown",
                industry="unknown",
                role_type="unknown", 
                experience_years=0,
                seniority_level="unknown",
                required_skills=[],
                preferred_skills=[],
                tech_stack=[],
                company_stage="unknown",
                company_size="unknown",
                remote_friendly=False,
                location="unknown",
                culture_keywords=[],
                key_responsibilities=[],
                success_metrics=[],
                domain_focus="unknown",
                regulatory_requirements=[],
                team_structure="unknown",
                growth_opportunities=[],
                confidence_score=0.0,
                analysis_cost=response.cost_usd,
                raw_jd=job_description,
                llm_reasoning="",
                error_message=f"LLM analysis failed: {response.error_message}"
            )
        
        # Parse LLM response
        try:
            analysis_data = json.loads(response.content.strip())
            
            analysis = JDAnalysis(
                success=True,
                company=analysis_data.get('company', 'Unknown'),
                role_title=analysis_data.get('role_title', 'Unknown'),
                industry=analysis_data.get('industry', 'unknown'),
                role_type=analysis_data.get('role_type', 'unknown'),
                experience_years=analysis_data.get('experience_years', 0),
                seniority_level=analysis_data.get('seniority_level', 'unknown'),
                required_skills=analysis_data.get('required_skills', []),
                preferred_skills=analysis_data.get('preferred_skills', []),
                tech_stack=analysis_data.get('tech_stack', []),
                company_stage=analysis_data.get('company_stage', 'unknown'),
                company_size=analysis_data.get('company_size', 'unknown'),
                remote_friendly=analysis_data.get('remote_friendly', False),
                location=analysis_data.get('location', 'unknown'),
                culture_keywords=analysis_data.get('culture_keywords', []),
                key_responsibilities=analysis_data.get('key_responsibilities', []),
                success_metrics=analysis_data.get('success_metrics', []),
                domain_focus=analysis_data.get('domain_focus', 'unknown'),
                regulatory_requirements=analysis_data.get('regulatory_requirements', []),
                team_structure=analysis_data.get('team_structure', 'unknown'),
                growth_opportunities=analysis_data.get('growth_opportunities', []),
                confidence_score=analysis_data.get('confidence_score', 0.8),
                analysis_cost=response.cost_usd,
                raw_jd=job_description,
                llm_reasoning=analysis_data.get('llm_reasoning', ''),
                error_message=None
            )
            
            # Cache successful analysis
            if use_cache:
                self.save_analysis_to_cache(analysis)
            
            print(f"✅ JD analyzed: {analysis.company} - {analysis.role_title}")
            print(f"🎯 Domain: {analysis.domain_focus} | Industry: {analysis.industry}")
            print(f"💰 Cost: ${analysis.analysis_cost:.4f}")
            
            return analysis
            
        except json.JSONDecodeError as e:
            return JDAnalysis(
                success=False,
                company="Unknown",
                role_title="Unknown", 
                industry="unknown",
                role_type="unknown",
                experience_years=0,
                seniority_level="unknown",
                required_skills=[],
                preferred_skills=[],
                tech_stack=[],
                company_stage="unknown",
                company_size="unknown",
                remote_friendly=False,
                location="unknown",
                culture_keywords=[],
                key_responsibilities=[],
                success_metrics=[],
                domain_focus="unknown",
                regulatory_requirements=[],
                team_structure="unknown",
                growth_opportunities=[],
                confidence_score=0.0,
                analysis_cost=response.cost_usd,
                raw_jd=job_description,
                llm_reasoning="",
                error_message=f"Failed to parse LLM response as JSON: {e}"
            )
    
    def convert_to_legacy_format(self, analysis: JDAnalysis) -> Dict:
        """
        Convert new analysis format to legacy format for compatibility
        """
        return {
            'company': analysis.company,
            'role_title': analysis.role_title,
            'location': analysis.location,
            'seniority_level': analysis.seniority_level,
            'required_skills': analysis.required_skills,
            'preferred_skills': analysis.preferred_skills,
            'experience_years': analysis.experience_years,
            'industry': analysis.industry,
            'domain': analysis.domain_focus,
            'company_stage': analysis.company_stage,
            'company_size': analysis.company_size,
            'tech_stack': analysis.tech_stack,
            'remote_friendly': analysis.remote_friendly,
            'culture_keywords': analysis.culture_keywords,
            'key_responsibilities': analysis.key_responsibilities,
            'regulatory_requirements': analysis.regulatory_requirements,
            'confidence_score': analysis.confidence_score,
            'analysis_cost_usd': analysis.analysis_cost,
            'llm_reasoning': analysis.llm_reasoning,
            'raw_text': analysis.raw_jd,
            # Legacy fields for compatibility
            'ai_ml_focus': 0.9 if 'ai' in analysis.domain_focus.lower() or 'ml' in analysis.domain_focus.lower() else 0.1,
            'b2b_vs_b2c': 'b2b' if any(term in analysis.domain_focus.lower() for term in ['enterprise', 'b2b', 'business']) else 'b2c',
            'matched_skills': [],  # Will be populated by other components
            'missing_skills': [],   # Will be populated by other components  
            'mapped_skills': [],    # Will be populated by other components
            'ats_match_score': 0    # Will be calculated by other components
        }
    
    def get_analysis_summary(self, analysis: JDAnalysis) -> str:
        """Get human-readable summary of analysis"""
        if not analysis.success:
            return f"❌ Analysis failed: {analysis.error_message}"
        
        summary = []
        summary.append(f"🏢 {analysis.company} - {analysis.role_title}")
        summary.append(f"🎯 {analysis.domain_focus.title()} | {analysis.industry.title()}")
        summary.append(f"📍 {analysis.location} | {analysis.seniority_level.title()} level")
        summary.append(f"⏰ {analysis.experience_years}+ years required")
        summary.append(f"🔧 Tech: {', '.join(analysis.tech_stack[:3])}{'...' if len(analysis.tech_stack) > 3 else ''}")
        summary.append(f"🎯 Confidence: {analysis.confidence_score:.1%}")
        
        if analysis.regulatory_requirements:
            summary.append(f"⚖️  Compliance: {', '.join(analysis.regulatory_requirements[:2])}")
        
        return '\n'.join(summary)

# Global instance for easy access
llm_jd_parser = LLMJobDescriptionParser()

# Convenience function
def analyze_job_description(job_description: str, use_cache: bool = True) -> JDAnalysis:
    """Convenience function for JD analysis"""
    return llm_jd_parser.analyze_job_description(job_description, use_cache)