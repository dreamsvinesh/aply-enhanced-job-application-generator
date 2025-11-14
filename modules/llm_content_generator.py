#!/usr/bin/env python3
"""
LLM Content Generator
Dynamic generation of resumes, cover letters, and messages using LLM analysis
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

from .llm_service import call_llm
from .llm_jd_parser import JDAnalysis
from .profile_extractor import ProfileExtractor
from .country_config import CountryConfig

class LLMContentGenerator:
    """Generate tailored application content using LLM and comprehensive profile data"""
    
    def __init__(self):
        self.profile_extractor = ProfileExtractor()
        self.country_config = CountryConfig()
        self.profile_data = self.load_profile()
        
    def load_profile(self) -> Dict:
        """Load comprehensive profile data"""
        profile = self.profile_extractor.load_profile()
        if not profile:
            print("⚠️  No comprehensive profile found. Please run extract_profile.py first.")
            return {}
        return profile
    
    def generate_tailored_resume(self, 
                               jd_analysis: JDAnalysis, 
                               country: str,
                               max_tokens: int = 3000) -> Tuple[str, List[str], float]:
        """
        Generate tailored resume using LLM based on job requirements
        
        Returns:
            Tuple of (resume_content, changes_made, generation_cost)
        """
        
        if not self.profile_data:
            return "Error: No profile data available", ["Profile extraction required"], 0.0
        
        # Build comprehensive resume generation prompt
        prompt = self._build_resume_prompt(jd_analysis, country)
        
        # Generate resume using LLM
        response = call_llm(
            prompt=prompt,
            task_type="generation",
            use_cache=False,  # Don't cache personal content
            max_tokens=max_tokens
        )
        
        if not response.success:
            return f"Error: Resume generation failed - {response.error_message}", [], response.cost_usd
        
        # Parse response to extract resume and changes
        try:
            result = json.loads(response.content.strip())
            resume_content = result.get('resume_content', '')
            changes_made = result.get('changes_made', [])
            
            print(f"✅ Resume generated for {jd_analysis.domain_focus} role")
            print(f"💰 Generation cost: ${response.cost_usd:.4f}")
            
            return resume_content, changes_made, response.cost_usd
            
        except json.JSONDecodeError:
            # Fallback: treat entire response as resume content
            changes = [f"Generated tailored resume for {jd_analysis.domain_focus} role at {jd_analysis.company}"]
            return response.content.strip(), changes, response.cost_usd
    
    def _build_resume_prompt(self, jd_analysis: JDAnalysis, country: str) -> str:
        """Build comprehensive resume generation prompt"""
        
        # Extract relevant profile projects based on domain
        relevant_projects = self._select_relevant_projects(jd_analysis)
        
        # Get country-specific preferences
        country_prefs = self.country_config.get_country_preferences(country)
        
        return f"""
You are an expert resume writer specializing in {jd_analysis.domain_focus} product management roles. Create a tailored resume that PRIORITIZES {jd_analysis.domain_focus.upper()} experience and skills.

JOB ANALYSIS:
Company: {jd_analysis.company}
Role: {jd_analysis.role_title} 
Domain Focus: {jd_analysis.domain_focus} ⭐ PRIMARY FOCUS
Industry: {jd_analysis.industry}
Required Skills: {', '.join(jd_analysis.required_skills)}
Key Responsibilities: {', '.join(jd_analysis.key_responsibilities[:3])}
Regulatory Requirements: {', '.join(jd_analysis.regulatory_requirements)}
Experience Required: {jd_analysis.experience_years}+ years

CANDIDATE PROFILE:
{json.dumps(self.profile_data, indent=2)}

RELEVANT PROJECTS TO EMPHASIZE:
{json.dumps(relevant_projects, indent=2)}

COUNTRY: {country.title()}
Cultural Preferences: {country_prefs.get('resume_style', 'Professional and concise')}

RESUME GENERATION INSTRUCTIONS:

1. **Professional Summary (2-3 lines)** - CRITICAL DOMAIN FOCUS:
   - Lead with "{jd_analysis.domain_focus.title()} Product Manager" title
   - Highlight {jd_analysis.experience_years}+ years PM experience IN {jd_analysis.domain_focus.upper()} domain
   - Emphasize ONLY {jd_analysis.domain_focus} relevant achievements from candidate profile
   - Mention specific {jd_analysis.domain_focus} technologies/skills from job requirements
   - Use {country} business communication style

2. **Experience Section** - PRIORITIZE {jd_analysis.domain_focus.upper()} PROJECTS:
   - SELECT ONLY projects relevant to {jd_analysis.domain_focus} domain from profile
   - REFRAME other projects to highlight {jd_analysis.domain_focus} aspects if applicable
   - EMPHASIZE {jd_analysis.domain_focus} technologies and outcomes
   - Use domain-specific action verbs for {jd_analysis.domain_focus}
   - Highlight regulatory/compliance experience if {jd_analysis.domain_focus} is fintech

3. **Skills Section**:
   - Prioritize skills mentioned in job requirements
   - Group by relevance: Product Management, Domain-Specific, Technical, Business
   - Include regulatory/compliance skills if relevant to role

4. **Cultural Adaptation for {country}**:
   - {country_prefs.get('resume_tone', 'Use professional tone')}
   - {country_prefs.get('achievement_style', 'Include quantified achievements')}

CRITICAL REQUIREMENTS:
- Only include information that exists in the candidate profile
- Maintain truthfulness - do not invent experience or skills
- Emphasize transferable skills when direct experience is limited
- Use specific metrics and achievements from profile projects
- Adapt language to match job description terminology
- Focus on {jd_analysis.domain_focus} relevant experience

OUTPUT FORMAT:
Return a JSON object with:
{{
    "resume_content": "Complete resume text in markdown format",
    "changes_made": [
        "List of specific customizations made for this role",
        "e.g., Emphasized fintech compliance experience",
        "e.g., Highlighted payment processing skills"
    ]
}}

Generate a compelling, accurate resume that positions the candidate for this specific {jd_analysis.domain_focus} role at {jd_analysis.company}.
"""
    
    def _select_relevant_projects(self, jd_analysis: JDAnalysis) -> List[Dict]:
        """Select most relevant projects based on job requirements"""
        
        all_projects = self.profile_data.get('detailed_projects', [])
        
        if not all_projects:
            return []
        
        # Score projects based on relevance to JD
        scored_projects = []
        
        for project in all_projects:
            score = self._calculate_project_relevance(project, jd_analysis)
            scored_projects.append((project, score))
        
        # Sort by relevance and return top 3
        scored_projects.sort(key=lambda x: x[1], reverse=True)
        
        return [project for project, score in scored_projects[:3]]
    
    def _calculate_project_relevance(self, project: Dict, jd_analysis: JDAnalysis) -> float:
        """Calculate how relevant a project is to the job requirements"""
        
        score = 0.0
        
        # Domain relevance - PRIORITIZE EXACT DOMAIN MATCHES
        relevant_for_roles = project.get('relevant_for_roles', [])
        domain_mapping = {
            'payments': ['fintech_pm', 'payments_pm', 'banking_pm', 'automation_pm'],
            'fintech': ['fintech_pm', 'payments_pm', 'banking_pm', 'automation_pm'],
            'banking': ['fintech_pm', 'payments_pm', 'banking_pm', 'enterprise_pm'],
            'enterprise': ['enterprise_pm', 'b2b_pm', 'automation_pm'],
            'saas': ['saas_pm', 'b2b_pm', 'enterprise_pm'],
            'ai_ml': ['ai_pm', 'technical_pm']
        }
        
        domain_keywords = domain_mapping.get(jd_analysis.domain_focus.lower(), [])
        if any(keyword in relevant_for_roles for keyword in domain_keywords):
            # BOOST fintech/payments match significantly 
            if jd_analysis.domain_focus.lower() in ['payments', 'fintech', 'banking']:
                if any(fk in relevant_for_roles for fk in ['fintech_pm', 'payments_pm', 'banking_pm']):
                    score += 0.8  # Much higher weight for direct fintech match
                else:
                    score += 0.4
            else:
                score += 0.4
        
        # Technology overlap
        project_tech = [tech.lower() for tech in project.get('technologies', [])]
        jd_tech = [skill.lower() for skill in jd_analysis.tech_stack]
        
        tech_overlap = sum(1 for tech in jd_tech if any(pt in tech for pt in project_tech))
        if jd_tech:
            score += (tech_overlap / len(jd_tech)) * 0.3
        
        # Skills demonstrated
        project_skills = [skill.lower() for skill in project.get('skills_demonstrated', [])]
        jd_skills = [skill.lower() for skill in jd_analysis.required_skills]
        
        skill_overlap = sum(1 for skill in jd_skills if any(ps in skill for ps in project_skills))
        if jd_skills:
            score += (skill_overlap / len(jd_skills)) * 0.3
        
        return min(score, 1.0)
    
    def generate_cover_letter(self, 
                             jd_analysis: JDAnalysis,
                             country: str,
                             max_tokens: int = 2000) -> Tuple[str, float]:
        """
        Generate personalized cover letter using LLM
        
        Returns:
            Tuple of (cover_letter_content, generation_cost)
        """
        
        prompt = self._build_cover_letter_prompt(jd_analysis, country)
        
        response = call_llm(
            prompt=prompt,
            task_type="generation",
            use_cache=False,
            max_tokens=max_tokens
        )
        
        if not response.success:
            return f"Error: Cover letter generation failed - {response.error_message}", response.cost_usd
        
        print(f"✅ Cover letter generated for {jd_analysis.company}")
        print(f"💰 Generation cost: ${response.cost_usd:.4f}")
        
        return response.content.strip(), response.cost_usd
    
    def _build_cover_letter_prompt(self, jd_analysis: JDAnalysis, country: str) -> str:
        """Build cover letter generation prompt"""
        
        personal_info = self.profile_data.get('personal_info', {})
        core_identity = self.profile_data.get('core_identity', {})
        relevant_projects = self._select_relevant_projects(jd_analysis)
        
        return f"""
You are an expert cover letter writer. Create a compelling, personalized cover letter for this specific role.

JOB DETAILS:
Company: {jd_analysis.company}
Role: {jd_analysis.role_title}
Domain: {jd_analysis.domain_focus}
Key Responsibilities: {', '.join(jd_analysis.key_responsibilities[:3])}
Company Culture Keywords: {', '.join(jd_analysis.culture_keywords)}

CANDIDATE BACKGROUND:
Name: {personal_info.get('name', 'Candidate')}
Primary Expertise: {core_identity.get('primary_expertise', 'Product Management')}
Value Proposition: {core_identity.get('value_proposition', 'Experienced product manager')}

TOP RELEVANT PROJECTS:
{json.dumps(relevant_projects, indent=2)}

COUNTRY CULTURE: {country.title()}

COVER LETTER REQUIREMENTS:

1. **Opening Hook** (1-2 sentences):
   - Express genuine interest in {jd_analysis.company} and the {jd_analysis.domain_focus} space
   - Mention specific aspects of the role that align with candidate's background

2. **Relevant Experience** (2-3 paragraphs):
   - Highlight most relevant project that demonstrates {jd_analysis.domain_focus} capabilities
   - Use specific metrics and achievements from candidate's profile
   - Connect experience to job requirements and company needs
   - Show understanding of {jd_analysis.domain_focus} challenges

3. **Value Proposition** (1 paragraph):
   - Explain how candidate's unique background solves company's specific needs
   - Reference company culture keywords if relevant
   - Mention any regulatory/compliance experience if required

4. **Cultural Fit** (if applicable):
   - Adapt tone for {country} business culture
   - Reference company's mission or values if mentioned in job description

5. **Strong Closing**:
   - Reiterate interest and value
   - Professional sign-off

TONE & STYLE:
- Confident but not arrogant
- Specific and metric-driven
- Genuine enthusiasm for {jd_analysis.domain_focus}
- Adapted for {country} business communication style
- Professional and engaging

CRITICAL REQUIREMENTS:
- Only use real information from candidate profile
- Do not invent experience or skills
- Keep to 3-4 paragraphs maximum
- Make it personal and specific to this role
- Show clear understanding of {jd_analysis.domain_focus} domain

Generate a compelling cover letter that positions this candidate as the ideal fit for {jd_analysis.company}'s {jd_analysis.role_title} role.
"""
    
    def generate_messages(self, 
                         jd_analysis: JDAnalysis,
                         country: str,
                         max_tokens: int = 1000) -> Tuple[Dict[str, str], float]:
        """
        Generate LinkedIn and email messages using LLM
        
        Returns:
            Tuple of (messages_dict, generation_cost)
        """
        
        prompt = self._build_messages_prompt(jd_analysis, country)
        
        response = call_llm(
            prompt=prompt,
            task_type="generation",
            use_cache=False,
            max_tokens=max_tokens
        )
        
        if not response.success:
            error_msg = f"Error: Message generation failed - {response.error_message}"
            return {"linkedin": error_msg, "email": {"subject": "Error", "body": error_msg}}, response.cost_usd
        
        try:
            messages = json.loads(response.content.strip())
            print(f"✅ Messages generated for {jd_analysis.company}")
            print(f"💰 Generation cost: ${response.cost_usd:.4f}")
            return messages, response.cost_usd
            
        except json.JSONDecodeError:
            fallback_messages = {
                "linkedin": f"Hi! I'm interested in the {jd_analysis.role_title} role at {jd_analysis.company}. My background in {jd_analysis.domain_focus} aligns well with your needs. Would love to connect!",
                "email": {
                    "subject": f"Interest in {jd_analysis.role_title} Position",
                    "body": f"Hi,\n\nI'm very interested in the {jd_analysis.role_title} position at {jd_analysis.company}. My experience with {jd_analysis.domain_focus} makes me a strong fit for this role.\n\nBest regards"
                }
            }
            return fallback_messages, response.cost_usd
    
    def _build_messages_prompt(self, jd_analysis: JDAnalysis, country: str) -> str:
        """Build messages generation prompt"""
        
        core_identity = self.profile_data.get('core_identity', {})
        top_achievements = self.profile_data.get('achievements_quantified', [])[:2]
        
        return f"""
Generate LinkedIn and email outreach messages for this job application.

JOB DETAILS:
Company: {jd_analysis.company}
Role: {jd_analysis.role_title}  
Domain: {jd_analysis.domain_focus}

CANDIDATE PROFILE:
Expertise: {core_identity.get('primary_expertise', 'Product Management')}
Key Achievements: {json.dumps(top_achievements, indent=2)}

COUNTRY: {country}

Generate messages in JSON format:

{{
    "linkedin": "LinkedIn connection message (max 300 characters, engaging, specific to {jd_analysis.domain_focus})",
    "email": {{
        "subject": "Professional subject line",
        "body": "Concise email body (2-3 sentences, specific value proposition)"
    }}
}}

Requirements:
- LinkedIn message must be under 300 characters
- Reference specific {jd_analysis.domain_focus} experience
- Use {country} business communication style
- Include 1-2 specific metrics from achievements
- Professional and engaging tone
- Mention genuine interest in {jd_analysis.company}
"""
    
    def generate_complete_package(self, 
                                 jd_analysis: JDAnalysis,
                                 country: str) -> Dict[str, Any]:
        """
        Generate complete application package using LLM
        
        Returns:
            Dictionary with all generated content and metadata
        """
        
        if not self.profile_data:
            return {
                "success": False,
                "error": "No comprehensive profile available. Please run extract_profile.py first.",
                "total_cost": 0.0
            }
        
        print(f"🚀 Generating complete application package for {jd_analysis.company}")
        
        total_cost = 0.0
        
        # Generate resume
        resume_content, resume_changes, resume_cost = self.generate_tailored_resume(jd_analysis, country)
        total_cost += resume_cost
        
        # Generate cover letter  
        cover_letter, cover_cost = self.generate_cover_letter(jd_analysis, country)
        total_cost += cover_cost
        
        # Generate messages
        messages, messages_cost = self.generate_messages(jd_analysis, country)
        total_cost += messages_cost
        
        package = {
            "success": True,
            "job_analysis": {
                "company": jd_analysis.company,
                "role_title": jd_analysis.role_title,
                "domain_focus": jd_analysis.domain_focus,
                "industry": jd_analysis.industry,
                "confidence_score": jd_analysis.confidence_score
            },
            "generated_content": {
                "resume": resume_content,
                "cover_letter": cover_letter,
                "linkedin_message": messages.get("linkedin", ""),
                "email": messages.get("email", {}),
                "resume_changes": resume_changes
            },
            "generation_metadata": {
                "total_cost_usd": total_cost,
                "country": country,
                "profile_used": bool(self.profile_data),
                "llm_generated": True
            }
        }
        
        print(f"✅ Complete package generated!")
        print(f"💰 Total cost: ${total_cost:.4f}")
        
        return package

# Global instance
llm_content_generator = LLMContentGenerator()

# Convenience functions
def generate_application_package(jd_analysis: JDAnalysis, country: str) -> Dict[str, Any]:
    """Generate complete application package"""
    return llm_content_generator.generate_complete_package(jd_analysis, country)