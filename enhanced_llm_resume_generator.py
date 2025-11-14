#!/usr/bin/env python3
"""
Enhanced LLM-Based Resume Generator
Replaces rule-based system with intelligent LLM analysis
"""

import json
import openai
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class EnhancedLLMResumeGenerator:
    def __init__(self, api_key: Optional[str] = None):
        if api_key:
            openai.api_key = api_key
        self.load_user_profile()
    
    def load_user_profile(self):
        """Load user profile"""
        try:
            profile_path = Path(__file__).parent / "data" / "user_profile.json"
            with open(profile_path, 'r', encoding='utf-8') as f:
                self.user_profile = json.load(f)
        except FileNotFoundError:
            # Fallback profile
            self.user_profile = {
                "name": "Vinesh Kumar",
                "experience": [
                    {
                        "role": "Senior Product Manager",
                        "company": "COWRKS",
                        "duration": "01/2023 - Present",
                        "achievements": [
                            "Built AI-powered RAG knowledge system achieving 94% accuracy serving 200+ users",
                            "Automated contract activation workflow reducing timeline from 42 days to 10 minutes, accelerating $2M revenue",
                            "Orchestrated cross-functional automation initiatives across 15+ processes, saving 50+ resource hours daily"
                        ]
                    },
                    {
                        "role": "Product Manager", 
                        "company": "COWRKS",
                        "duration": "08/2016 - 01/2020",
                        "achievements": [
                            "Led Converge F&B platform serving 600,000+ users with 30,000+ daily orders achieving ₹168-180 crores GMV",
                            "Scaled platform from MVP to production in 6 months achieving 91% NPS",
                            "Generated €220K monthly revenue through data-driven space optimization"
                        ]
                    }
                ]
            }
    
    def analyze_and_generate_resume(self, jd_text: str, country: str = "global") -> Tuple[str, List[str]]:
        """
        Complete LLM-based resume generation pipeline
        
        Returns:
            Tuple of (resume_content, changes_made)
        """
        changes_made = []
        
        # Step 1: LLM analyzes the job description
        print("🤖 Analyzing job description with LLM...")
        jd_analysis = self._analyze_job_with_llm(jd_text)
        changes_made.append(f"LLM identified role as: {jd_analysis.get('role_domain', 'General PM')}")
        
        # Step 2: Generate dynamic resume content
        print("✏️ Generating tailored resume content...")
        resume_content = self._generate_dynamic_resume(jd_analysis, country)
        changes_made.append(f"Tailored resume for {jd_analysis.get('role_focus', 'role requirements')}")
        
        # Step 3: Apply country-specific formatting
        print("🌍 Applying country-specific formatting...")
        formatted_resume = self._apply_country_formatting(resume_content, country)
        changes_made.append(f"Applied {country} formatting and cultural adaptations")
        
        return formatted_resume, changes_made
    
    def _analyze_job_with_llm(self, jd_text: str) -> Dict:
        """Use LLM to analyze job description comprehensively"""
        
        analysis_prompt = f"""
Analyze this job description for resume tailoring. Provide comprehensive analysis for strategic positioning.

JOB DESCRIPTION:
{jd_text}

CANDIDATE BACKGROUND:
- 7+ years Product Management experience
- Enterprise automation expertise (contract workflows: 42 days → 10 minutes, $2M revenue impact)  
- Large-scale platform experience (600K+ users, 30K+ daily orders, ₹180 crores GMV)
- AI/ML systems (94% accuracy RAG system, 200+ users)
- Cross-functional leadership (15+ process automation initiatives)
- API integration & workflow automation expertise

ANALYSIS REQUIRED:

1. **ROLE DOMAIN IDENTIFICATION**: What specific technology domain/industry is this role in? 
   (e.g., "Communication Platforms & Messaging Infrastructure", "Fintech Payment Systems", "Healthcare Technology", "Developer Tools", "Security Platforms", etc.)

2. **KEY SUCCESS FACTORS**: What are the top 5 things this company/role needs someone to excel at?

3. **EXPERIENCE MAPPING**: Which of the candidate's specific experiences best match this role's needs?

4. **COMPETITIVE POSITIONING**: How should the candidate be positioned to stand out for THIS specific role?

5. **TECHNICAL EMPHASIS**: What technical skills/concepts should be prominently featured?

6. **BUSINESS IMPACT FOCUS**: What types of metrics/achievements would impress this hiring manager most?

Respond in JSON format:
{{
    "role_domain": "specific domain (e.g., Communication Platforms & Messaging Infrastructure)",
    "company_mission": "what this company/team is trying to achieve",
    "key_success_factors": ["factor1", "factor2", "factor3", "factor4", "factor5"],
    "best_experience_matches": ["specific experiences that align with needs"],
    "competitive_positioning": "how to position candidate uniquely for this role",
    "technical_emphasis": ["key technical areas to highlight"],
    "business_impact_focus": ["types of metrics that would resonate"],
    "role_challenges": ["main challenges this role will face"],
    "ideal_candidate_profile": "what they're looking for"
}}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Use latest model
                messages=[
                    {"role": "system", "content": "You are an expert Product Manager recruiter and resume strategist with deep knowledge of technology domains."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content.strip()
            # Clean JSON if needed
            if "```json" in analysis_text:
                analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
            
            analysis = json.loads(analysis_text)
            return analysis
            
        except Exception as e:
            print(f"⚠️ LLM Analysis failed: {e}")
            return self._create_fallback_analysis(jd_text)
    
    def _generate_dynamic_resume(self, jd_analysis: Dict, country: str) -> str:
        """Generate completely dynamic resume based on LLM analysis"""
        
        generation_prompt = f"""
Create a tailored resume for this specific role analysis. Use the candidate's real achievements but reframe them strategically.

ROLE ANALYSIS:
{json.dumps(jd_analysis, indent=2)}

CANDIDATE PROFILE:
{json.dumps(self.user_profile, indent=2)}

REQUIREMENTS:
1. **Professional Summary**: 60-80 words positioning candidate for this specific role domain
2. **Experience Section**: Reframe existing achievements to match role needs
3. **Skills Section**: Prioritize skills most relevant to this role
4. **Strategic Positioning**: Position as ideal fit for this specific opportunity

Focus areas based on analysis:
- Role Domain: {jd_analysis.get('role_domain', 'Product Management')}
- Key Success Factors: {', '.join(jd_analysis.get('key_success_factors', []))}
- Technical Emphasis: {', '.join(jd_analysis.get('technical_emphasis', []))}

Generate a complete resume emphasizing the most relevant aspects for THIS specific role.

Format as:
# CANDIDATE NAME
**Title aligned with role domain**

Contact info placeholder

---

## SUMMARY
[Professional summary tailored to role]

---

## EXPERIENCE
[Reframed experience bullets emphasizing relevant aspects]

---

## EDUCATION & SKILLS
[Relevant sections]
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer specializing in Product Manager roles across technology domains."},
                    {"role": "user", "content": generation_prompt}
                ],
                temperature=0.3,
                max_tokens=2500
            )
            
            resume_content = response.choices[0].message.content.strip()
            return resume_content
            
        except Exception as e:
            print(f"⚠️ Resume generation failed: {e}")
            return self._create_fallback_resume()
    
    def _apply_country_formatting(self, resume_content: str, country: str) -> str:
        """Apply country-specific formatting and cultural adaptations"""
        
        if country.lower() in ['portugal', 'spain', 'italy']:
            # European formatting preferences
            resume_content = resume_content.replace('phone', 'telefone')
            # Add country-specific adaptations
        elif country.lower() in ['germany', 'netherlands', 'sweden']:
            # Northern European preferences  
            # More formal, detailed approach
            pass
        
        return resume_content
    
    def _create_fallback_analysis(self, jd_text: str) -> Dict:
        """Fallback if LLM fails"""
        # Basic keyword analysis as fallback
        if 'communication' in jd_text.lower() or 'messaging' in jd_text.lower():
            domain = "Communication Platforms"
        elif 'ai' in jd_text.lower() or 'machine learning' in jd_text.lower():
            domain = "AI/ML Products"  
        else:
            domain = "Product Management"
        
        return {
            "role_domain": domain,
            "company_mission": "Technology innovation",
            "key_success_factors": ["Product Strategy", "Cross-functional Leadership", "Data-driven Decisions"],
            "best_experience_matches": ["Platform experience", "Automation expertise"],
            "competitive_positioning": "Experienced product leader with proven results",
            "technical_emphasis": ["Platform Development", "Process Automation"],
            "business_impact_focus": ["Revenue Growth", "User Growth", "Efficiency Gains"]
        }
    
    def _create_fallback_resume(self) -> str:
        """Fallback resume if LLM fails"""
        return """# VINESH KUMAR
**Senior Product Manager**

Contact Information

---

## SUMMARY

Senior Product Manager with 7+ years of experience in technology product development, specializing in enterprise automation and platform management. Proven track record of driving revenue growth and operational efficiency through data-driven product strategy.

---

## EXPERIENCE

### Senior Product Manager | COWRKS | 01/2023 - Present
• Led product initiatives driving $2M revenue acceleration through automated workflows
• Built AI-powered systems achieving 94% accuracy serving 200+ users  
• Orchestrated cross-functional automation across 15+ processes, saving 50+ hours daily

### Product Manager | COWRKS | 08/2016 - 01/2020  
• Managed platform serving 600,000+ users with 30,000+ daily orders
• Scaled platform achieving ₹180 crores GMV and 91% NPS
• Generated €220K monthly revenue through optimization initiatives

---

## SKILLS

**Product Management:** Strategy, Roadmapping, Stakeholder Management
**Technical:** API Integration, Platform Development, Automation
**Business:** Revenue Growth, Data Analysis, Cross-functional Leadership"""

# Demo the system
if __name__ == "__main__":
    print("=== ENHANCED LLM-BASED RESUME GENERATOR ===")
    print("✅ Replaces rule-based keyword matching with intelligent LLM analysis")
    print("✅ Unlimited resume variations based on role understanding")  
    print("✅ Dynamic content generation for each specific opportunity")
    print("✅ Strategic positioning based on company needs")
    print("\n🚀 This system can handle ANY role domain:")
    print("   • Communication Platforms (like Squarespace)")
    print("   • Fintech & Payment Systems")
    print("   • Healthcare Technology") 
    print("   • Developer Tools & APIs")
    print("   • Security & Compliance")
    print("   • And many more...")
    
    generator = EnhancedLLMResumeGenerator()
    
    # Example for Squarespace  
    squarespace_jd = "Product Manager to lead Acuity Communications, responsible for tools and infrastructure that help businesses communicate with clients through scheduling journey..."
    
    print(f"\n📋 Example: Analyzing Squarespace role...")
    print("🤖 LLM would identify: Communication Platforms & Messaging Infrastructure")
    print("✏️ Generate resume emphasizing: messaging workflows, API integrations, communication platforms")
    print("🎯 Result: Perfect fit for the actual role requirements!")