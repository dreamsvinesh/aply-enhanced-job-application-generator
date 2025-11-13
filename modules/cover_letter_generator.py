"""
Cover Letter Generator Module
Creates country-specific cover letters that sound human and avoid AI-generated feel.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from .country_config import CountryConfig

class CoverLetterGenerator:
    def __init__(self):
        self.country_config = CountryConfig()
        self.load_user_profile()
        
    def load_user_profile(self):
        """Load user profile from JSON file"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.user_profile = json.load(f)
    
    def generate(self, jd_data: Dict, country: str, company_name: str) -> str:
        """
        Generate country-specific cover letter
        
        Args:
            jd_data: Parsed job description data
            country: Target country
            company_name: Company name
            
        Returns:
            Generated cover letter content
        """
        
        # Get country-specific rules
        country_config = self.country_config.get_config(country)
        cover_letter_rules = country_config['cover_letter']
        tone_guidelines = country_config['tone']
        
        # Determine the best approach based on JD analysis
        ai_ml_focus = jd_data.get('ai_ml_focus', 0.0)
        business_model = jd_data.get('b2b_vs_b2c', 'mixed')
        role_title = jd_data.get('role_title', 'Product Manager')
        
        # Select the most relevant achievement to highlight
        key_achievement = self._select_key_achievement(ai_ml_focus, business_model, jd_data)
        
        # Generate cover letter sections
        opening = self._generate_opening(company_name, role_title, country, cover_letter_rules)
        body = self._generate_body(jd_data, key_achievement, country, tone_guidelines)
        closing = self._generate_closing(country, cover_letter_rules)
        
        # Assemble the letter
        cover_letter = f"{opening}\n\n{body}\n\n{closing}"
        
        # Apply country-specific tone adjustments
        cover_letter = self.country_config.adapt_content_tone(cover_letter, country, 'cover_letter')
        
        return cover_letter
    
    def _select_key_achievement(self, ai_ml_focus: float, business_model: str, jd_data: Dict) -> Dict:
        """Select the most relevant achievement to highlight based on JD"""
        
        achievements = self.user_profile['key_achievements']
        projects = self.user_profile['projects']
        
        # Determine which project to feature based on JD focus
        if ai_ml_focus > 0.3:
            # AI/ML focused role - highlight RAG system
            featured_project = projects['rag_knowledge_system']
            return {
                'project': 'AI Knowledge System',
                'impact': 'built AI-powered RAG system achieving 94% accuracy',
                'result': 'serving 200+ users with 1,500+ weekly queries',
                'relevance': 'AI/ML automation'
            }
            
        elif business_model == 'b2b':
            # B2B focused role - highlight contract automation
            featured_project = projects['contract_automation']
            return {
                'project': 'Enterprise Automation',
                'impact': 'automated contract workflows reducing timelines 99.6%',
                'result': 'from 42 days to 10 minutes, accelerating $2M revenue',
                'relevance': 'enterprise efficiency'
            }
            
        elif business_model == 'b2c':
            # B2C focused role - highlight Converge platform
            featured_project = projects['converge_fnb_platform']
            return {
                'project': 'User Engagement Platform',
                'impact': 'scaled F&B platform to 600K+ users',
                'result': 'achieving 91% NPS with 30K+ daily orders',
                'relevance': 'user experience optimization'
            }
        else:
            # Default to most impressive metric
            return {
                'project': 'Process Automation',
                'impact': 'automated workflows reducing timelines from 42 days to 10 minutes',
                'result': 'accelerating $2M revenue and saving 50+ resource hours daily',
                'relevance': 'operational excellence'
            }
    
    def _generate_opening(self, company_name: str, role_title: str, country: str, rules: Dict) -> str:
        """Generate country-specific opening paragraph"""
        
        opening_style = rules.get('opening_style', 'professional')
        personal_info = self.user_profile['personal_info']
        
        if country.lower() == 'netherlands':
            # Direct, efficient opening
            return f"Dear Hiring Manager,\n\nI am writing to express my strong interest in the {role_title} position at {company_name}. With 11 years of technology experience and a proven track record in AI/ML automation and enterprise product management, I am confident I can contribute immediately to your team's success."
            
        elif country.lower() in ['finland', 'sweden']:
            # Modest, competence-focused opening
            return f"Dear Hiring Manager,\n\nI would like to apply for the {role_title} position at {company_name}. My background in product management, particularly in AI/ML systems and enterprise automation, aligns well with the requirements outlined in your posting."
            
        elif country.lower() == 'denmark':
            # Direct but friendly opening
            return f"Hi there,\n\nI'm excited to apply for the {role_title} role at {company_name}. Your company's approach to innovation resonates with my experience in building AI-powered products that deliver real business value."
            
        elif country.lower() == 'portugal':
            # Formal, respectful opening with cultural appreciation
            return f"Dear Hiring Manager,\n\nI am writing to express my sincere interest in the {role_title} position at {company_name}. Having researched your company's innovative work in the European market, I am particularly drawn to the opportunity to contribute my expertise in AI/ML product management to your esteemed organization."
            
        elif country.lower() == 'ireland':
            # Formal but warm opening
            return f"Dear Hiring Manager,\n\nI am delighted to apply for the {role_title} position at {company_name}. Your company's reputation for innovation and excellence in the industry has long impressed me, and I am eager to contribute my product management expertise to your continued success."
            
        else:
            # Default professional opening
            return f"Dear Hiring Manager,\n\nI am writing to express my interest in the {role_title} position at {company_name}. With my extensive background in product management and proven success in AI/ML automation, I believe I would be a valuable addition to your team."
    
    def _generate_body(self, jd_data: Dict, key_achievement: Dict, country: str, tone_guidelines: Dict) -> str:
        """Generate the main body of the cover letter"""
        
        # Get relevant skills from JD
        required_skills = jd_data.get('required_skills', [])
        role_title = jd_data.get('role_title', 'Product Manager')
        
        # Build connection between experience and role requirements
        relevance_statement = self._build_relevance_statement(key_achievement, required_skills, country)
        
        # Add specific example
        example_paragraph = self._build_example_paragraph(key_achievement, country)
        
        # Add forward-looking statement
        future_contribution = self._build_future_contribution(jd_data, country, tone_guidelines)
        
        return f"{relevance_statement}\n\n{example_paragraph}\n\n{future_contribution}"
    
    def _build_relevance_statement(self, achievement: Dict, required_skills: List[str], country: str) -> str:
        """Build statement connecting experience to role requirements"""
        
        if country.lower() == 'netherlands':
            return f"My experience in {achievement['relevance']} directly aligns with your requirements. I have successfully {achievement['impact']}, demonstrating my ability to deliver measurable business outcomes through strategic product management."
            
        elif country.lower() in ['finland', 'sweden']:
            return f"In my current role, I have focused on {achievement['relevance']}, where I {achievement['impact']}. This experience has given me strong technical foundations and the ability to work effectively with cross-functional teams."
            
        elif country.lower() == 'denmark':
            return f"What excites me about this opportunity is how my hands-on experience with {achievement['relevance']} matches what you're looking for. I've {achievement['impact']}, which taught me the importance of building products that truly solve user problems."
            
        elif country.lower() == 'portugal':
            return f"Throughout my career, I have developed extensive expertise in {achievement['relevance']}, particularly in how I {achievement['impact']}. This experience has provided me with a comprehensive understanding of both technical implementation and business strategy."
            
        elif country.lower() == 'ireland':
            return f"My professional journey has been centered around {achievement['relevance']}, where I {achievement['impact']}. This experience has not only strengthened my technical capabilities but also enhanced my ability to collaborate effectively with diverse stakeholders."
            
        else:
            return f"My expertise in {achievement['relevance']} is particularly relevant to this role. I have {achievement['impact']}, which demonstrates my capability to drive significant business results through strategic product management."
    
    def _build_example_paragraph(self, achievement: Dict, country: str) -> str:
        """Build specific example paragraph"""
        
        if country.lower() == 'netherlands':
            return f"For example, when I {achievement['impact']}, the result was {achievement['result']}. This project required careful stakeholder management, technical execution, and measurement of business impact - skills that would transfer directly to your {achievement['project'].lower()} initiatives."
            
        elif country.lower() in ['finland', 'sweden']:
            return f"In one project, I {achievement['impact']}, resulting in {achievement['result']}. This required collaboration with engineering, design, and business teams to ensure we delivered a solution that met both technical and user requirements."
            
        elif country.lower() == 'denmark':
            return f"One project I'm particularly proud of is when I {achievement['impact']}, which led to {achievement['result']}. It was a great example of how focusing on user needs while maintaining technical excellence can create real business value."
            
        elif country.lower() == 'portugal':
            return f"A particularly significant accomplishment in my career occurred when I {achievement['impact']}, ultimately achieving {achievement['result']}. This project required comprehensive planning, meticulous execution, and strong leadership to coordinate multiple departments toward a common goal."
            
        elif country.lower() == 'ireland':
            return f"One achievement I am especially proud of is when I {achievement['impact']}, which resulted in {achievement['result']}. This project highlighted the importance of building strong relationships across teams and maintaining clear communication throughout the development process."
            
        else:
            return f"A key example of my impact is when I {achievement['impact']}, resulting in {achievement['result']}. This demonstrates my ability to translate technical complexity into business value while leading cross-functional teams."
    
    def _build_future_contribution(self, jd_data: Dict, country: str, tone_guidelines: Dict) -> str:
        """Build forward-looking contribution statement"""
        
        role_title = jd_data.get('role_title', 'Product Manager')
        company_focus = self._infer_company_focus(jd_data)
        
        if country.lower() == 'netherlands':
            return f"I am excited about the opportunity to bring my experience in AI/ML automation and enterprise product management to your team. I believe I can contribute immediately to your {company_focus} objectives while helping streamline processes and improve efficiency."
            
        elif country.lower() in ['finland', 'sweden']:
            return f"I would welcome the opportunity to contribute to your team's success and learn from your experienced colleagues. My technical background and collaborative approach would enable me to make meaningful contributions to your {company_focus} initiatives."
            
        elif country.lower() == 'denmark':
            return f"I'm genuinely excited about the possibility of joining your team and contributing to your {company_focus} goals. I believe my experience building user-focused products combined with my passion for innovation would be a great fit for your company culture."
            
        elif country.lower() == 'portugal':
            return f"I would be honored to have the opportunity to contribute my expertise to your distinguished organization. My commitment to excellence and comprehensive understanding of {company_focus} would enable me to make valuable contributions to your team's continued success."
            
        elif country.lower() == 'ireland':
            return f"I am very enthusiastic about the prospect of joining your team and contributing to your {company_focus} initiatives. My experience combined with my passion for building meaningful products would enable me to make a positive impact from day one."
            
        else:
            return f"I am excited about the opportunity to leverage my product management expertise to contribute to your {company_focus} goals. I believe my track record of delivering measurable results would be valuable to your team."
    
    def _infer_company_focus(self, jd_data: Dict) -> str:
        """Infer company focus from JD to personalize future contribution"""
        
        raw_text = jd_data.get('raw_text', '').lower()
        
        if any(term in raw_text for term in ['ai', 'machine learning', 'automation', 'intelligent']):
            return 'AI/ML innovation'
        elif any(term in raw_text for term in ['enterprise', 'b2b', 'business', 'saas']):
            return 'enterprise growth'
        elif any(term in raw_text for term in ['user', 'customer', 'mobile', 'app']):
            return 'user experience'
        elif any(term in raw_text for term in ['platform', 'scale', 'infrastructure']):
            return 'platform development'
        else:
            return 'product innovation'
    
    def _generate_closing(self, country: str, rules: Dict) -> str:
        """Generate country-specific closing"""
        
        closing_style = rules.get('closing', 'professional')
        
        if country.lower() == 'netherlands':
            return f"Thank you for considering my application. I look forward to discussing how I can contribute to your team's success.\n\nBest regards,\nVinesh Kumar"
            
        elif country.lower() in ['finland', 'sweden']:
            return f"Thank you for your time and consideration. I would be happy to discuss my qualifications further at your convenience.\n\nKind regards,\nVinesh Kumar"
            
        elif country.lower() == 'denmark':
            return f"Thanks for taking the time to read my application. I'd love to chat more about how I can help your team achieve its goals.\n\nBest regards,\nVinesh Kumar"
            
        elif country.lower() == 'portugal':
            return f"Thank you very much for your time and consideration. I would be delighted to discuss my qualifications and enthusiasm for this position in greater detail.\n\nRespectfully yours,\nVinesh Kumar"
            
        elif country.lower() == 'ireland':
            return f"Thank you for your time and consideration. I would welcome the opportunity to discuss how my experience and passion for product management can contribute to your team's continued success.\n\nWarm regards,\nVinesh Kumar"
            
        else:
            return f"Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your organization.\n\nSincerely,\nVinesh Kumar"