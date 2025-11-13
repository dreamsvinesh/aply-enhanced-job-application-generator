"""
Message Generator Module
Creates LinkedIn messages and email templates for outreach to recruiters and hiring managers.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from .country_config import CountryConfig

class MessageGenerator:
    def __init__(self):
        self.country_config = CountryConfig()
        self.load_user_profile()
        
    def load_user_profile(self):
        """Load user profile from JSON file"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.user_profile = json.load(f)
    
    def generate_linkedin_message(self, jd_data: Dict, country: str) -> str:
        """
        Generate LinkedIn message optimized for country and role
        Target: Under 400 characters for optimal response rates
        
        Args:
            jd_data: Parsed job description data
            country: Target country
            
        Returns:
            LinkedIn message string
        """
        
        # Get country-specific LinkedIn rules
        linkedin_rules = self.country_config.get_linkedin_rules(country)
        max_chars = linkedin_rules.get('max_chars', 350)
        
        # Extract key info
        company = jd_data.get('company', 'your company')
        role_title = jd_data.get('role_title', 'Product Manager')
        ai_ml_focus = jd_data.get('ai_ml_focus', 0.0)
        
        # Select key achievement to mention
        key_metric = self._select_key_metric_for_linkedin(ai_ml_focus, jd_data)
        
        # Generate message based on country style
        message = self._generate_linkedin_content(company, role_title, key_metric, country, linkedin_rules)
        
        # Ensure under character limit
        if len(message) > max_chars:
            message = self._trim_linkedin_message(message, max_chars)
        
        return message
    
    def generate_email_message(self, jd_data: Dict, country: str, company_name: str) -> Dict[str, str]:
        """
        Generate email template with subject line and body
        
        Args:
            jd_data: Parsed job description data
            country: Target country
            company_name: Company name
            
        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        
        role_title = jd_data.get('role_title', 'Product Manager')
        ai_ml_focus = jd_data.get('ai_ml_focus', 0.0)
        
        # Generate subject line
        subject = self._generate_email_subject(role_title, company_name, country)
        
        # Generate email body
        body = self._generate_email_body(jd_data, company_name, country, ai_ml_focus)
        
        return {
            'subject': subject,
            'body': body
        }
    
    def _select_key_metric_for_linkedin(self, ai_ml_focus: float, jd_data: Dict) -> str:
        """Select the most compelling metric for LinkedIn message"""
        
        if ai_ml_focus > 0.3:
            return "94% accuracy AI system"
        
        business_model = jd_data.get('b2b_vs_b2c', 'mixed')
        if business_model == 'b2b':
            return "$2M revenue acceleration"
        elif business_model == 'b2c':
            return "600K+ users, 91% NPS"
        else:
            return "42 days→10 minutes automation"
    
    def _generate_linkedin_content(self, company: str, role_title: str, key_metric: str, 
                                  country: str, linkedin_rules: Dict) -> str:
        """Generate LinkedIn message content based on country style"""
        
        if country.lower() == 'netherlands':
            # Direct, efficient approach
            return f"Hi! I saw your {role_title} opening at {company}. I've built AI-powered products achieving {key_metric} and have 7 years PM experience in enterprise automation. Would love to discuss how I can contribute to your team. Are you available for a brief call this week?"
            
        elif country.lower() in ['finland', 'sweden']:
            # Modest, competence-focused
            return f"Hello, I noticed the {role_title} position at {company}. My background includes {key_metric} and experience in AI/ML product management. I believe my skills could contribute to your team's goals. Would you be interested in a brief conversation about this opportunity?"
            
        elif country.lower() == 'denmark':
            # Direct but friendly
            return f"Hey! Your {role_title} role at {company} caught my attention. I've worked on products achieving {key_metric} and love building solutions that create real user value. Think there might be a fit? Would be great to chat!"
            
        elif country.lower() == 'portugal':
            # Formal, respectful
            return f"Dear Hiring Manager, I am very interested in the {role_title} position at {company}. My experience includes developing systems achieving {key_metric} and I would be honored to contribute to your organization. May I request a brief conversation to discuss this opportunity?"
            
        elif country.lower() == 'ireland':
            # Formal but warm
            return f"Hello! I hope you're well. I'm reaching out regarding the {role_title} opportunity at {company}. My experience building products with {key_metric} aligns well with your needs. I'd love to learn more about your team and discuss how I could contribute. Might you have time for a quick chat?"
            
        else:
            # Default professional approach
            return f"Hi! I'm interested in the {role_title} role at {company}. I've built products achieving {key_metric} and have strong AI/ML product experience. Would love to discuss how my background could benefit your team. Available for a brief call?"
    
    def _trim_linkedin_message(self, message: str, max_chars: int) -> str:
        """Trim LinkedIn message to stay under character limit"""
        
        if len(message) <= max_chars:
            return message
        
        # Progressive trimming strategies
        
        # 1. Remove extra spaces and line breaks
        trimmed = ' '.join(message.split())
        if len(trimmed) <= max_chars:
            return trimmed
        
        # 2. Shorten specific phrases
        replacements = {
            'Would love to discuss': 'Let\'s discuss',
            'I would be honored to': 'I\'d like to',
            'available for a brief call': 'free for a call',
            'Would you be interested in': 'Interested in',
            'May I request a brief conversation': 'Can we chat',
            'experience building products': 'experience with',
            'I believe my skills could contribute': 'My skills fit'
        }
        
        for long_phrase, short_phrase in replacements.items():
            trimmed = trimmed.replace(long_phrase, short_phrase)
            if len(trimmed) <= max_chars:
                return trimmed
        
        # 3. Final truncation with ellipsis
        return trimmed[:max_chars-3] + "..."
    
    def _generate_email_subject(self, role_title: str, company_name: str, country: str) -> str:
        """Generate email subject line"""
        
        if country.lower() == 'netherlands':
            return f"Product Manager Application - {company_name}"
            
        elif country.lower() in ['finland', 'sweden']:
            return f"Application: {role_title} Position at {company_name}"
            
        elif country.lower() == 'denmark':
            return f"Interested in {role_title} Role - {company_name}"
            
        elif country.lower() == 'portugal':
            return f"Application for {role_title} Position - {company_name}"
            
        elif country.lower() == 'ireland':
            return f"Application: {role_title} Opportunity at {company_name}"
            
        else:
            return f"{role_title} Application - {company_name}"
    
    def _generate_email_body(self, jd_data: Dict, company_name: str, country: str, ai_ml_focus: float) -> str:
        """Generate email body content"""
        
        role_title = jd_data.get('role_title', 'Product Manager')
        
        # Select key achievements based on JD focus
        if ai_ml_focus > 0.3:
            key_achievement = "built AI-powered RAG system achieving 94% accuracy serving 200+ users"
            secondary_achievement = "automated workflows reducing timelines from 42 days to 10 minutes"
        else:
            key_achievement = "automated contract activation reducing timelines 99.6% (42 days→10 minutes)"
            secondary_achievement = "built AI-powered systems achieving 94% accuracy"
        
        # Generate country-specific email body
        if country.lower() == 'netherlands':
            return f"""Dear Hiring Manager,

I am writing to apply for the {role_title} position at {company_name}. 

My experience directly aligns with your requirements:
• {key_achievement}, accelerating $2M revenue
• {secondary_achievement}
• 7+ years PM experience in enterprise automation and AI/ML systems

I can contribute immediately to your team's objectives and would appreciate the opportunity to discuss how my background matches your needs.

Best regards,
Vinesh Kumar
+91-81230-79049
vineshmuthukumar@gmail.com"""

        elif country.lower() in ['finland', 'sweden']:
            return f"""Dear Hiring Manager,

I would like to apply for the {role_title} position at {company_name}.

My background includes:
• {key_achievement}
• {secondary_achievement}
• Strong experience in cross-functional product management

I believe my technical skills and collaborative approach would enable me to contribute effectively to your team's success.

Kind regards,
Vinesh Kumar
+91-81230-79049
vineshmuthukumar@gmail.com"""

        elif country.lower() == 'denmark':
            return f"""Hi there,

I'm excited to apply for the {role_title} role at {company_name}.

What I bring:
• {key_achievement}
• {secondary_achievement} 
• Passion for building products that solve real problems

I'd love to chat about how my experience building user-focused products could help your team achieve its goals.

Best regards,
Vinesh Kumar
+91-81230-79049
vineshmuthukumar@gmail.com"""

        elif country.lower() == 'portugal':
            return f"""Dear Hiring Manager,

I am writing to express my sincere interest in the {role_title} position at {company_name}.

My professional accomplishments include:
• {key_achievement}, demonstrating strong technical leadership
• {secondary_achievement}
• Comprehensive experience in AI/ML product management and enterprise systems

I would be honored to contribute my expertise to your esteemed organization and would welcome the opportunity to discuss my qualifications in detail.

Respectfully yours,
Vinesh Kumar
+91-81230-79049
vineshmuthukumar@gmail.com"""

        elif country.lower() == 'ireland':
            return f"""Dear Hiring Manager,

I hope this message finds you well. I am writing to apply for the {role_title} position at {company_name}.

My experience includes:
• {key_achievement}, showcasing ability to deliver measurable impact
• {secondary_achievement}
• Strong track record in stakeholder management and team collaboration

I am enthusiastic about the opportunity to contribute to your team's continued success and would welcome the chance to discuss how my experience aligns with your needs.

Warm regards,
Vinesh Kumar
+91-81230-79049
vineshmuthukumar@gmail.com"""

        else:
            return f"""Dear Hiring Manager,

I am writing to apply for the {role_title} position at {company_name}.

Key qualifications:
• {key_achievement}
• {secondary_achievement}
• 7+ years experience in AI/ML and enterprise product management

I am excited about the opportunity to leverage my expertise to contribute to your team's success. I look forward to discussing how my background can benefit {company_name}.

Sincerely,
Vinesh Kumar
+91-81230-79049
vineshmuthukumar@gmail.com"""