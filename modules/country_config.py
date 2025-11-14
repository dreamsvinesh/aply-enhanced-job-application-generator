"""
Country Configuration Module
Manages country-specific formatting rules, tone guidelines, and cultural adaptations.
"""

from typing import Dict, List, Optional

class CountryConfig:
    def __init__(self):
        self.countries = {
            'netherlands': {
                'name': 'Netherlands',
                'resume_format': {
                    'max_pages': 2,
                    'include_photo': False,
                    'date_format': 'dd/mm/yyyy',
                    'sections_order': ['summary', 'experience', 'education', 'skills', 'certifications']
                },
                'tone': {
                    'directness': 'high',  # Direct, efficient communication
                    'formality': 'moderate',  # Professional but not overly formal
                    'key_values': ['efficiency', 'work-life balance', 'innovation', 'directness'],
                    'avoid': ['excessive politeness', 'lengthy explanations', 'corporate jargon']
                },
                'cover_letter': {
                    'max_length': 300,  # words
                    'opening_style': 'direct',  # Get straight to the point
                    'emphasis': ['relevant experience', 'measurable results', 'cultural fit'],
                    'closing': 'professional_direct'
                },
                'linkedin_message': {
                    'max_chars': 350,
                    'style': 'professional_casual',
                    'opener': ['mutual connection', 'role interest', 'company admiration'],
                    'cta': 'clear_next_step'
                },
                'cultural_notes': [
                    'Value work-life balance highly',
                    'Appreciate direct, honest communication',
                    'Focus on efficiency and results',
                    'Less hierarchy, more collaboration'
                ]
            },
            
            'finland': {
                'name': 'Finland',
                'resume_format': {
                    'max_pages': 2,
                    'include_photo': False,
                    'date_format': 'd.m.yyyy',
                    'sections_order': ['summary', 'skills', 'experience', 'education', 'certifications']
                },
                'tone': {
                    'directness': 'moderate',
                    'formality': 'moderate',
                    'key_values': ['technical excellence', 'modesty', 'reliability', 'innovation'],
                    'avoid': ['boasting', 'excessive self-promotion', 'informal language']
                },
                'cover_letter': {
                    'max_length': 250,
                    'opening_style': 'modest_confident',
                    'emphasis': ['technical skills', 'education', 'team collaboration'],
                    'closing': 'polite_professional'
                },
                'linkedin_message': {
                    'max_chars': 300,
                    'style': 'modest_professional',
                    'opener': ['technical interest', 'industry connection'],
                    'cta': 'polite_inquiry'
                },
                'cultural_notes': [
                    'Value modesty and understatement',
                    'Technical competence highly respected',
                    'Education and qualifications important',
                    'Silence is comfortable, don\'t oversell'
                ]
            },
            
            'ireland': {
                'name': 'Ireland',
                'resume_format': {
                    'max_pages': 3,  # More detailed CVs acceptable
                    'include_photo': False,
                    'date_format': 'dd/mm/yyyy',
                    'sections_order': ['summary', 'experience', 'education', 'skills', 'achievements']
                },
                'tone': {
                    'directness': 'moderate',
                    'formality': 'high',  # More formal approach
                    'key_values': ['relationship building', 'communication skills', 'education', 'experience'],
                    'avoid': ['overly casual tone', 'too much humor', 'aggressive selling']
                },
                'cover_letter': {
                    'max_length': 350,
                    'opening_style': 'formal_warm',
                    'emphasis': ['relationship building', 'communication', 'cultural fit'],
                    'closing': 'formal_enthusiastic'
                },
                'linkedin_message': {
                    'max_chars': 400,
                    'style': 'formal_friendly',
                    'opener': ['company appreciation', 'role excitement'],
                    'cta': 'respectful_request'
                },
                'cultural_notes': [
                    'Relationships and networking very important',
                    'Good communication skills highly valued',
                    'Education credentials matter',
                    'Warm but professional approach works'
                ]
            },
            
            'sweden': {
                'name': 'Sweden', 
                'resume_format': {
                    'max_pages': 2,
                    'include_photo': False,
                    'date_format': 'yyyy-mm-dd',
                    'sections_order': ['summary', 'skills', 'experience', 'education', 'achievements']
                },
                'tone': {
                    'directness': 'moderate',
                    'formality': 'moderate',
                    'key_values': ['equality', 'collaboration', 'sustainability', 'innovation'],
                    'avoid': ['hierarchy emphasis', 'individual glory', 'aggressive language']
                },
                'cover_letter': {
                    'max_length': 250,
                    'opening_style': 'collaborative',
                    'emphasis': ['team contribution', 'shared goals', 'sustainable impact'],
                    'closing': 'team_oriented'
                },
                'linkedin_message': {
                    'max_chars': 300,
                    'style': 'collaborative_professional',
                    'opener': ['shared values', 'team contribution'],
                    'cta': 'mutual_benefit'
                },
                'cultural_notes': [
                    'Lagom - balance and moderation valued',
                    'Team collaboration over individual achievement',
                    'Equality and flat hierarchies',
                    'Sustainability and social responsibility important'
                ]
            },
            
            'denmark': {
                'name': 'Denmark',
                'resume_format': {
                    'max_pages': 2,
                    'include_photo': False,
                    'date_format': 'dd/mm/yyyy',
                    'sections_order': ['summary', 'experience', 'skills', 'education', 'personal']
                },
                'tone': {
                    'directness': 'high',  # Very direct like Netherlands
                    'formality': 'low',   # More casual approach
                    'key_values': ['hygge', 'work-life balance', 'honesty', 'simplicity'],
                    'avoid': ['formality', 'hierarchy', 'complexity', 'boasting']
                },
                'cover_letter': {
                    'max_length': 200,  # Shorter preferred
                    'opening_style': 'direct_honest',
                    'emphasis': ['honest communication', 'work-life balance', 'team fit'],
                    'closing': 'simple_direct'
                },
                'linkedin_message': {
                    'max_chars': 250,  # Shorter than others
                    'style': 'direct_friendly',
                    'opener': ['honest interest', 'direct approach'],
                    'cta': 'simple_question'
                },
                'cultural_notes': [
                    'Hygge - comfort and coziness valued',
                    'Very direct communication style',
                    'Work-life balance extremely important',
                    'Informal, egalitarian culture'
                ]
            },
            
            'portugal': {
                'name': 'Portugal',
                'resume_format': {
                    'max_pages': 4,  # More detailed CVs expected
                    'include_photo': True,  # Photos are common
                    'date_format': 'dd/mm/yyyy',
                    'sections_order': ['personal', 'summary', 'experience', 'education', 'skills', 'languages']
                },
                'tone': {
                    'directness': 'low',   # More indirect approach
                    'formality': 'high',   # Formal and respectful
                    'key_values': ['respect', 'relationships', 'education', 'cultural interest'],
                    'avoid': ['too direct approach', 'rushing', 'ignoring hierarchy']
                },
                'cover_letter': {
                    'max_length': 400,  # Longer, more detailed
                    'opening_style': 'formal_respectful',
                    'emphasis': ['cultural appreciation', 'language skills', 'formal qualifications'],
                    'closing': 'respectful_formal'
                },
                'linkedin_message': {
                    'max_chars': 400,
                    'style': 'formal_warm',
                    'opener': ['cultural appreciation', 'respect for company'],
                    'cta': 'respectful_inquiry'
                },
                'cultural_notes': [
                    'Relationships and personal connections important',
                    'Formal titles and hierarchy respected',
                    'Cultural interest and language learning appreciated',
                    'Patience and relationship building valued'
                ]
            }
        }
        
    def get_config(self, country: str) -> Dict:
        """Get configuration for a specific country"""
        country_lower = country.lower()
        if country_lower not in self.countries:
            # Default to Netherlands config if country not found
            return self.countries['netherlands']
        return self.countries[country_lower]
    
    def get_resume_format(self, country: str) -> Dict:
        """Get resume format guidelines for a country"""
        config = self.get_config(country)
        return config['resume_format']
    
    def get_tone_guidelines(self, country: str) -> Dict:
        """Get tone and communication guidelines for a country"""
        config = self.get_config(country)
        return config['tone']
    
    def get_cover_letter_rules(self, country: str) -> Dict:
        """Get cover letter specific rules for a country"""
        config = self.get_config(country)
        return config['cover_letter']
    
    def get_linkedin_rules(self, country: str) -> Dict:
        """Get LinkedIn message rules for a country"""
        config = self.get_config(country)
        return config['linkedin_message']
    
    def get_cultural_notes(self, country: str) -> List[str]:
        """Get cultural adaptation notes for a country"""
        config = self.get_config(country)
        return config['cultural_notes']
    
    def adapt_content_tone(self, content: str, country: str, content_type: str = 'general') -> str:
        """
        Adapt content tone based on country preferences
        
        Args:
            content: Original content
            country: Target country
            content_type: Type of content (resume, cover_letter, linkedin, email)
        """
        tone_config = self.get_tone_guidelines(country)
        
        # Basic tone adaptations based on country preferences
        if country.lower() == 'netherlands':
            # More direct, less fluff
            content = self._make_more_direct(content)
        elif country.lower() in ['finland', 'sweden']:
            # More modest, less self-promotion
            content = self._make_more_modest(content)
        elif country.lower() == 'denmark':
            # Very direct but friendly
            content = self._make_direct_friendly(content)
        elif country.lower() == 'portugal':
            # More formal and respectful
            content = self._make_more_formal(content)
        elif country.lower() == 'ireland':
            # Formal but warm
            content = self._make_formal_warm(content)
            
        return content
    
    def _make_more_direct(self, content: str) -> str:
        """Make content more direct for Netherlands style"""
        # Remove unnecessary politeness words
        replacements = {
            'I would like to': 'I will',
            'I believe that I can': 'I can',
            'I think I would be': 'I am',
            'perhaps': '',
            'maybe': '',
            'I hope to': 'I will'
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        return content
    
    def _make_more_modest(self, content: str) -> str:
        """Make content more modest for Nordic countries"""
        replacements = {
            'excellent': 'strong',
            'outstanding': 'solid',
            'exceptional': 'good',
            'amazing': 'effective',
            'incredible': 'significant'
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        return content
    
    def _make_direct_friendly(self, content: str) -> str:
        """Make content direct but friendly for Denmark"""
        # Add friendly but direct language
        if content.startswith('Dear'):
            content = content.replace('Dear Sir/Madam', 'Hi there')
        
        return content
    
    def _make_more_formal(self, content: str) -> str:
        """Make content more formal for Portugal"""
        replacements = {
            "Hi": "Dear",
            "Thanks": "Thank you",
            "I'm": "I am",
            "We're": "We are",
            "Can't": "Cannot"
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        return content
    
    def _make_formal_warm(self, content: str) -> str:
        """Make content formal but warm for Ireland"""
        # Add warmth while maintaining formality
        if 'I am writing to' in content:
            content = content.replace('I am writing to', 'I am delighted to write to')
        
        return content
    
    def get_supported_countries(self) -> List[str]:
        """Get list of supported countries"""
        return list(self.countries.keys())
    
    def get_country_preferences(self, country: str) -> Dict:
        """Get country-specific preferences for content generation"""
        country = country.lower()
        if country in self.countries:
            return self.countries[country]
        else:
            # Return default preferences for unknown countries
            return {
                'resume_style': 'Professional and concise',
                'resume_tone': 'Use professional tone',
                'achievement_style': 'Include quantified achievements'
            }