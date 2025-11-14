#!/usr/bin/env python3
"""
LLM-Based Job Description Analyzer
Dynamic analysis and resume tailoring based on LLM understanding
"""

import json
import openai
from typing import Dict, List, Optional
from pathlib import Path

class LLMJobDescriptionAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        if api_key:
            openai.api_key = api_key
        self.load_user_profile()
    
    def load_user_profile(self):
        """Load user profile for context"""
        try:
            profile_path = Path(__file__).parent / "data" / "user_profile.json"
            with open(profile_path, 'r', encoding='utf-8') as f:
                self.user_profile = json.load(f)
        except FileNotFoundError:
            self.user_profile = {"name": "User", "experience": []}
    
    def analyze_job_description(self, jd_text: str) -> Dict:
        """
        Use LLM to analyze job description and determine resume strategy
        
        Returns comprehensive analysis for dynamic resume generation
        """
        
        analysis_prompt = f"""
You are an expert Product Manager resume strategist. Analyze this job description and provide a comprehensive analysis for resume tailoring.

JOB DESCRIPTION:
{jd_text}

USER BACKGROUND CONTEXT:
- 7+ years Product Management experience
- Experience with: Enterprise automation, Salesforce/SAP integration, AI/ML systems, mobile platforms (600K+ users), contract automation, RAG systems, API integrations, B2B/B2C products

ANALYSIS REQUIRED:

1. ROLE CATEGORIZATION:
Identify the PRIMARY domain/focus area (not limited to predefined categories):
Examples: Communication Platforms, Fintech, Healthcare Tech, AI/ML, Enterprise Automation, Developer Tools, Consumer Apps, Security, etc.

2. KEY REQUIREMENTS EXTRACTION:
List the 5 most critical requirements/skills mentioned in the JD.

3. EXPERIENCE MAPPING:
Which of the user's experiences should be HIGHLIGHTED to match this role?

4. RESUME STRATEGY:
What should be the PRIMARY narrative/positioning for this specific role?

5. SKILLS EMPHASIS:
What technical and business skills should be emphasized?

6. BUSINESS IMPACT FOCUS:
What type of metrics/achievements should be highlighted?

7. TONE & MESSAGING:
What messaging approach would resonate best?

Please respond in this exact JSON format:
{{
    "role_domain": "specific domain name",
    "role_focus": "detailed description of role focus",
    "critical_requirements": ["req1", "req2", "req3", "req4", "req5"],
    "experience_to_highlight": ["which experiences to emphasize"],
    "primary_narrative": "the main story/positioning for this role",
    "technical_skills_focus": ["key technical skills to emphasize"],
    "business_skills_focus": ["key business skills to emphasize"],
    "metrics_to_highlight": ["types of achievements to emphasize"],
    "messaging_tone": "recommended tone and approach",
    "resume_strategy": "comprehensive strategy for this specific role"
}}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert Product Manager resume strategist with deep understanding of various tech domains."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content.strip()
            # Parse JSON response
            analysis = json.loads(analysis_text)
            
            return analysis
            
        except Exception as e:
            print(f"LLM Analysis failed: {e}")
            # Fallback to basic analysis
            return self._fallback_analysis(jd_text)
    
    def generate_dynamic_resume_content(self, jd_analysis: Dict, country: str = "global") -> Dict:
        """
        Generate dynamic resume content based on LLM analysis
        """
        
        content_prompt = f"""
Based on this job analysis, create a tailored resume summary and experience bullets for the user.

JOB ANALYSIS:
{json.dumps(jd_analysis, indent=2)}

USER PROFILE CONTEXT:
- Name: {self.user_profile.get('name', 'Vinesh Kumar')}
- 7+ years Product Management experience
- Key achievements: $2M revenue acceleration, 600K+ users, 94% accuracy AI systems, contract automation

GENERATE:

1. PROFESSIONAL SUMMARY (50-80 words)
- Emphasize {jd_analysis.get('role_domain', 'product management')} experience
- Highlight {jd_analysis.get('primary_narrative', 'relevant experience')}
- Include relevant metrics/achievements

2. KEY EXPERIENCE BULLETS (5-6 bullets)
- Reframe existing experience to match {jd_analysis.get('role_focus', 'the role requirements')}
- Emphasize: {', '.join(jd_analysis.get('experience_to_highlight', []))}
- Highlight: {', '.join(jd_analysis.get('metrics_to_highlight', []))}

3. SKILLS SECTION
Technical: {', '.join(jd_analysis.get('technical_skills_focus', []))}
Business: {', '.join(jd_analysis.get('business_skills_focus', []))}

Respond in JSON format:
{{
    "professional_summary": "tailored summary text",
    "experience_bullets": ["bullet1", "bullet2", "bullet3", "bullet4", "bullet5"],
    "technical_skills": ["skill1", "skill2", "skill3"],
    "business_skills": ["skill1", "skill2", "skill3"],
    "positioning": "overall positioning strategy"
}}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer specializing in Product Manager roles across various tech domains."},
                    {"role": "user", "content": content_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            content_text = response.choices[0].message.content.strip()
            content = json.loads(content_text)
            
            return content
            
        except Exception as e:
            print(f"Content generation failed: {e}")
            return self._fallback_content()
    
    def _fallback_analysis(self, jd_text: str) -> Dict:
        """Fallback analysis if LLM fails"""
        return {
            "role_domain": "Product Management",
            "role_focus": "General product management role",
            "critical_requirements": ["Product Management", "Cross-functional leadership", "Data-driven decisions"],
            "experience_to_highlight": ["Enterprise automation", "Platform management"],
            "primary_narrative": "Experienced product manager with proven track record",
            "technical_skills_focus": ["API Integration", "Platform Management"],
            "business_skills_focus": ["Product Strategy", "Stakeholder Management"],
            "metrics_to_highlight": ["Revenue impact", "User growth", "Efficiency improvements"],
            "messaging_tone": "Professional and results-focused",
            "resume_strategy": "Emphasize general product management experience"
        }
    
    def _fallback_content(self) -> Dict:
        """Fallback content if LLM fails"""
        return {
            "professional_summary": "Experienced Product Manager with 7+ years in technology, specializing in enterprise automation and platform development.",
            "experience_bullets": [
                "Led product strategy and development initiatives",
                "Managed cross-functional teams to deliver business outcomes", 
                "Implemented automation solutions driving revenue growth",
                "Built scalable platforms serving enterprise customers",
                "Delivered data-driven product improvements"
            ],
            "technical_skills": ["API Integration", "Platform Management", "Automation"],
            "business_skills": ["Product Strategy", "Stakeholder Management", "Data Analysis"],
            "positioning": "Results-driven product leader"
        }

# Test implementation
if __name__ == "__main__":
    # Example usage (requires OpenAI API key)
    squarespace_jd = """At Squarespace, we empower product teams to solve meaningful customer and business problems. We're looking for a Product Manager to lead Acuity Communications, the team responsible for the tools and infrastructure that help businesses communicate with their clients throughout the scheduling journey."""
    
    analyzer = LLMJobDescriptionAnalyzer()
    
    # For demo without API key, show the structure
    print("=== LLM-BASED JD ANALYZER ===")
    print("This would call LLM with sophisticated prompts to:")
    print("1. Analyze role domain (Communication Platforms)")
    print("2. Extract key requirements (messaging infrastructure, API integration)")
    print("3. Map user experience to role needs")
    print("4. Generate dynamic resume content")
    print("5. Create tailored positioning strategy")
    print("\nResult: Unlimited resume variations based on LLM understanding!")