#!/usr/bin/env python3
"""
Dynamic Email and LinkedIn Generator
Creates personalized email templates and LinkedIn messages using dynamic template structures and enhanced JD analysis.
Integrated with the corrected dynamic template approach.
"""

import json
import logging
from typing import Dict, List, Optional
from pathlib import Path

# Import existing modules
from llm_service import LLMService
from country_config import CountryConfig
from database_manager import DatabaseManager
from dynamic_template_generator import DynamicTemplateGenerator

class DynamicEmailLinkedInGenerator:
    """
    Generates emails and LinkedIn messages using dynamic template structures created by LLM for each specific JD.
    
    Key Features:
    - Uses enhanced JD analysis instead of old classification system
    - Integrates with dynamic template generation (not predefined templates)
    - Creates role-specific LinkedIn messages and email templates
    - Applies country-specific tone and cultural adaptation
    - Tracks generation in database with quality metrics
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        self.country_config = CountryConfig()
        self.db_manager = DatabaseManager()
        self.template_generator = DynamicTemplateGenerator()
        self.logger = logging.getLogger(__name__)
        
        # Load user profile
        self.user_profile = self._load_user_profile()
        
        # LinkedIn character limits
        self.linkedin_limits = {
            'connection_request': 300,
            'message': 8000,
            'optimal_length': 400  # For best response rates
        }
    
    def _load_user_profile(self) -> Dict:
        """Load user profile for personalization."""
        try:
            profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load user profile: {e}")
            return {}
    
    def generate_linkedin_message(self, 
                                jd_analysis: Dict, 
                                user_profile: Dict, 
                                country: str,
                                message_type: str = 'connection') -> Dict:
        """
        Generate LinkedIn message using dynamic template structure and enhanced JD analysis.
        
        Args:
            jd_analysis: Enhanced JD analysis results
            user_profile: User's complete profile
            country: Target country for cultural adaptation
            message_type: 'connection' for connection request, 'message' for direct message
            
        Returns:
            Complete LinkedIn message generation result
        """
        try:
            # Step 1: Generate dynamic template structure for LinkedIn message
            template_structure = self.template_generator.generate_dynamic_template(
                jd_analysis=jd_analysis,
                user_profile=user_profile,
                country=country,
                content_type='linkedin_message'
            )
            
            # Step 2: Build LinkedIn message generation prompt
            generation_prompt = self._build_linkedin_prompt(
                jd_analysis, user_profile, country, template_structure, message_type
            )
            
            # Step 3: Generate LinkedIn message with LLM
            linkedin_response = self.llm_service.call_llm(
                prompt=generation_prompt,
                task_type="linkedin_message_generation",
                max_tokens=300,
                temperature=0.4
            )
            
            # Step 4: Parse and validate message
            message_content = self._parse_and_validate_linkedin_message(
                linkedin_response, message_type, country
            )
            
            # Step 5: Calculate quality metrics
            quality_metrics = self._calculate_linkedin_quality_metrics(
                message_content, message_type, jd_analysis
            )
            
            return {
                'content': message_content,
                'message_type': message_type,
                'character_count': len(message_content),
                'template_structure_used': template_structure,
                'quality_metrics': quality_metrics,
                'generation_metadata': {
                    'content_type': f'linkedin_{message_type}',
                    'generated_for_jd': f"{jd_analysis.get('extracted_info', {}).get('company', 'Unknown')} - {jd_analysis.get('extracted_info', {}).get('role_title', 'Unknown Role')}",
                    'country_adapted': country,
                    'generation_method': 'dynamic_template_llm'
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating LinkedIn message: {e}")
            return self._get_fallback_linkedin_message(jd_analysis, country, message_type)
    
    def generate_email_template(self, 
                              jd_analysis: Dict, 
                              user_profile: Dict, 
                              country: str,
                              email_type: str = 'application') -> Dict:
        """
        Generate email template using dynamic template structure and enhanced JD analysis.
        
        Args:
            jd_analysis: Enhanced JD analysis results
            user_profile: User's complete profile
            country: Target country for cultural adaptation
            email_type: 'application' for job application, 'followup' for follow-up email
            
        Returns:
            Complete email template generation result with subject and body
        """
        try:
            # Step 1: Generate dynamic template structure for email
            template_structure = self.template_generator.generate_dynamic_template(
                jd_analysis=jd_analysis,
                user_profile=user_profile,
                country=country,
                content_type='email_template'
            )
            
            # Step 2: Build email generation prompt
            generation_prompt = self._build_email_prompt(
                jd_analysis, user_profile, country, template_structure, email_type
            )
            
            # Step 3: Generate email with LLM
            email_response = self.llm_service.call_llm(
                prompt=generation_prompt,
                task_type="email_template_generation",
                max_tokens=500,
                temperature=0.3
            )
            
            # Step 4: Parse and validate email
            email_content = self._parse_email_content(email_response, country)
            
            # Step 5: Calculate quality metrics
            quality_metrics = self._calculate_email_quality_metrics(
                email_content, email_type, jd_analysis
            )
            
            return {
                'subject': email_content.get('subject', ''),
                'body': email_content.get('body', ''),
                'email_type': email_type,
                'template_structure_used': template_structure,
                'quality_metrics': quality_metrics,
                'generation_metadata': {
                    'content_type': f'email_{email_type}',
                    'generated_for_jd': f"{jd_analysis.get('extracted_info', {}).get('company', 'Unknown')} - {jd_analysis.get('extracted_info', {}).get('role_title', 'Unknown Role')}",
                    'country_adapted': country,
                    'generation_method': 'dynamic_template_llm'
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating email template: {e}")
            return self._get_fallback_email_template(jd_analysis, country, email_type)
    
    def _build_linkedin_prompt(self, 
                             jd_analysis: Dict, 
                             user_profile: Dict, 
                             country: str, 
                             template_structure: Dict,
                             message_type: str) -> str:
        """Build comprehensive prompt for LinkedIn message generation."""
        
        # Extract information
        extracted_info = jd_analysis.get('extracted_info', {})
        role_classification = jd_analysis.get('role_classification', {})
        positioning_strategy = jd_analysis.get('positioning_strategy', {})
        
        # Get template guidance
        template_struct = template_structure.get('template_structure', {})
        content_emphasis = template_struct.get('content_emphasis', {})
        
        # Get user info
        user_experience = user_profile.get('experience', [])
        user_achievements = user_profile.get('key_achievements', [])
        
        # Character limit based on message type
        char_limit = self.linkedin_limits['connection_request'] if message_type == 'connection' else self.linkedin_limits['optimal_length']
        
        return f"""
You are an expert LinkedIn messaging strategist. Create a compelling LinkedIn {message_type} message.

JOB DETAILS:
Company: {extracted_info.get('company_name', 'Unknown Company')}
Role: {extracted_info.get('role_title', 'Unknown Role')}
Primary Focus: {role_classification.get('primary_focus', 'general')}
Industry: {role_classification.get('industry', 'technology')}

USER POSITIONING:
Key Strengths: {', '.join(positioning_strategy.get('key_strengths_to_emphasize', [])[:2])}
Experience Framing: {positioning_strategy.get('experience_framing', 'Professional background')}
Most Relevant Achievement: {user_achievements[0] if user_achievements else 'Professional achievements available'}

DYNAMIC TEMPLATE GUIDANCE:
Content Priority: {content_emphasis.get('top_priority', 'relevant experience')}
Skills to Highlight: {', '.join(content_emphasis.get('skills_to_feature', [])[:2])}

COUNTRY: {country.upper()}
MESSAGE TYPE: {message_type}
CHARACTER LIMIT: {char_limit} characters maximum

TASK: Create a {message_type} message that:

1. **Opening**: Personalized connection to the company or role
   - Reference the specific position
   - Show you've researched the company/role
   - Be genuine and specific

2. **Value Proposition**: Brief but compelling
   - Highlight ONE key skill/achievement relevant to {role_classification.get('primary_focus', 'this role')}
   - Include a specific metric if possible
   - Show clear value for the company

3. **Call to Action**: Professional and appropriate
   - Request appropriate next step for {message_type} type
   - Be respectful of their time
   - Express genuine interest

CRITICAL REQUIREMENTS:
- Stay under {char_limit} characters
- Sound human and personable, not AI-generated
- Be specific to {extracted_info.get('company_name', 'this company')} and {role_classification.get('primary_focus', 'this role')}
- Avoid corporate jargon and AI language
- Match {country} cultural communication style
- Include ONE specific achievement/metric relevant to the role

EXAMPLES OF WHAT TO AVOID:
- "I am reaching out to you" (generic)
- "I believe I would be a great fit" (generic)
- "Leveraging my experience" (corporate jargon)
- "I am excited to delve into" (AI language)

Return ONLY the LinkedIn message content, nothing else.
"""
    
    def _build_email_prompt(self, 
                           jd_analysis: Dict, 
                           user_profile: Dict, 
                           country: str, 
                           template_structure: Dict,
                           email_type: str) -> str:
        """Build comprehensive prompt for email generation."""
        
        # Extract information
        extracted_info = jd_analysis.get('extracted_info', {})
        role_classification = jd_analysis.get('role_classification', {})
        positioning_strategy = jd_analysis.get('positioning_strategy', {})
        
        # Get template guidance
        template_struct = template_structure.get('template_structure', {})
        content_emphasis = template_struct.get('content_emphasis', {})
        
        # Get country config
        country_config = self.country_config.get_config(country)
        
        return f"""
You are an expert email strategist. Create a professional {email_type} email with subject line and body.

JOB DETAILS:
Company: {extracted_info.get('company_name', 'Unknown Company')}
Role: {extracted_info.get('role_title', 'Unknown Role')}
Primary Focus: {role_classification.get('primary_focus', 'general')}
Industry: {role_classification.get('industry', 'technology')}

USER POSITIONING:
Key Strengths: {', '.join(positioning_strategy.get('key_strengths_to_emphasize', [])[:3])}
Experience Framing: {positioning_strategy.get('experience_framing', 'Professional background')}

DYNAMIC TEMPLATE GUIDANCE:
Content Priority: {content_emphasis.get('top_priority', 'relevant experience')}
Skills to Feature: {', '.join(content_emphasis.get('skills_to_feature', [])[:3])}

COUNTRY: {country.upper()}
Cultural Tone: {country_config['tone']['formality']} formality, {country_config['tone']['directness']} directness

TASK: Create an {email_type} email with:

1. **Subject Line**: Compelling and specific
   - Include the role title
   - Make it clear this is an {email_type}
   - Be professional and direct
   - 50 characters or less

2. **Email Body**: Professional and concise
   - Proper greeting for {country}
   - Clear purpose statement
   - ONE key achievement relevant to {role_classification.get('primary_focus', 'this role')}
   - Brief explanation of value for the company
   - Professional closing appropriate for {country}

CRITICAL REQUIREMENTS:
- Subject and body should be separate
- Professional tone appropriate for {country}
- Avoid corporate jargon and AI language
- Include specific metrics where relevant
- Be concise but informative
- Sound human and professional

Return in this exact format:
SUBJECT: [subject line]

BODY:
[email body content]
"""
    
    def _parse_and_validate_linkedin_message(self, 
                                           llm_response: str, 
                                           message_type: str, 
                                           country: str) -> str:
        """Parse and validate LinkedIn message content."""
        try:
            message = llm_response.strip()
            
            # Remove any formatting
            message = message.replace("```", "").strip()
            
            # Check character limits
            limit = self.linkedin_limits['connection_request'] if message_type == 'connection' else self.linkedin_limits['optimal_length']
            
            if len(message) > limit:
                # Trim while preserving structure
                sentences = message.split('. ')
                trimmed = ""
                for sentence in sentences:
                    if len(trimmed + sentence + '. ') <= limit:
                        trimmed += sentence + '. '
                    else:
                        break
                message = trimmed.rstrip('. ')
                
                if len(message) > limit:
                    message = message[:limit-3] + "..."
            
            # Apply basic jargon cleanup
            jargon_replacements = {
                'leverage': 'use',
                'utilize': 'use',
                'reaching out to you': 'contacting you',
                'I believe I would be': 'I am',
                'delve into': 'explore'
            }
            
            for jargon, replacement in jargon_replacements.items():
                message = message.replace(jargon, replacement)
            
            return message
            
        except Exception as e:
            self.logger.error(f"Error parsing LinkedIn message: {e}")
            return llm_response[:self.linkedin_limits['connection_request']] if message_type == 'connection' else llm_response[:self.linkedin_limits['optimal_length']]
    
    def _parse_email_content(self, llm_response: str, country: str) -> Dict:
        """Parse email response into subject and body."""
        try:
            content = llm_response.strip()
            
            # Split subject and body
            if "SUBJECT:" in content and "BODY:" in content:
                parts = content.split("BODY:")
                subject_part = parts[0].replace("SUBJECT:", "").strip()
                body_part = parts[1].strip()
            else:
                # Fallback parsing
                lines = content.split('\n')
                subject_part = lines[0] if lines else "Application for Position"
                body_part = '\n'.join(lines[1:]) if len(lines) > 1 else content
            
            # Clean up
            subject = subject_part.strip().replace('"', '').replace("'", "")
            body = body_part.strip()
            
            # Apply jargon cleanup to body
            jargon_replacements = {
                'leverage': 'use',
                'utilize': 'use',
                'comprehensive': 'complete',
                'esteemed organization': 'company'
            }
            
            for jargon, replacement in jargon_replacements.items():
                body = body.replace(jargon, replacement)
            
            return {
                'subject': subject,
                'body': body
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing email content: {e}")
            return {
                'subject': "Application for Position",
                'body': llm_response
            }
    
    def _calculate_linkedin_quality_metrics(self, 
                                          content: str, 
                                          message_type: str, 
                                          jd_analysis: Dict) -> Dict:
        """Calculate quality metrics for LinkedIn message."""
        
        metrics = {
            'length_appropriate': True,
            'personalization_score': 7.0,
            'human_voice_score': 8.0,
            'relevance_score': 7.5,
            'overall_quality': 7.5
        }
        
        # Length check
        limit = self.linkedin_limits['connection_request'] if message_type == 'connection' else self.linkedin_limits['optimal_length']
        char_count = len(content)
        
        if char_count > limit:
            metrics['length_appropriate'] = False
            metrics['overall_quality'] -= 1.0
        
        # Check for personalization
        company = jd_analysis.get('extracted_info', {}).get('company_name', '')
        role = jd_analysis.get('extracted_info', {}).get('role_title', '')
        
        if company.lower() in content.lower():
            metrics['personalization_score'] += 1.0
        if role.lower() in content.lower():
            metrics['personalization_score'] += 1.0
        
        # Check for metrics/achievements
        if any(char.isdigit() for char in content):
            metrics['relevance_score'] += 1.0
        
        # Calculate overall
        metrics['overall_quality'] = (
            metrics['personalization_score'] * 0.3 +
            metrics['human_voice_score'] * 0.3 +
            metrics['relevance_score'] * 0.4
        )
        
        return metrics
    
    def _calculate_email_quality_metrics(self, 
                                       email_content: Dict, 
                                       email_type: str, 
                                       jd_analysis: Dict) -> Dict:
        """Calculate quality metrics for email."""
        
        metrics = {
            'subject_quality': 7.0,
            'body_quality': 7.5,
            'personalization_score': 7.0,
            'professional_tone': 8.0,
            'overall_quality': 7.5
        }
        
        subject = email_content.get('subject', '')
        body = email_content.get('body', '')
        
        # Subject line evaluation
        if len(subject) <= 50 and len(subject) >= 10:
            metrics['subject_quality'] += 1.0
        
        company = jd_analysis.get('extracted_info', {}).get('company_name', '')
        role = jd_analysis.get('extracted_info', {}).get('role_title', '')
        
        if company.lower() in (subject + body).lower():
            metrics['personalization_score'] += 1.0
        if role.lower() in (subject + body).lower():
            metrics['personalization_score'] += 1.0
        
        # Check for metrics in body
        if any(char.isdigit() for char in body):
            metrics['body_quality'] += 1.0
        
        # Calculate overall
        metrics['overall_quality'] = (
            metrics['subject_quality'] * 0.2 +
            metrics['body_quality'] * 0.3 +
            metrics['personalization_score'] * 0.3 +
            metrics['professional_tone'] * 0.2
        )
        
        return metrics
    
    def _get_fallback_linkedin_message(self, jd_analysis: Dict, country: str, message_type: str) -> Dict:
        """Generate fallback LinkedIn message."""
        
        extracted_info = jd_analysis.get('extracted_info', {})
        company = extracted_info.get('company_name', 'your company')
        role = extracted_info.get('role_title', 'the role')
        
        if message_type == 'connection':
            content = f"Hi! I saw the {role} position at {company} and I'm very interested. My background in product management and AI systems aligns well with your needs. Would love to connect!"
        else:
            content = f"Hello! I'm interested in the {role} position at {company}. With my experience in product management and proven track record in delivering results, I believe I could contribute to your team's success. Would you be open to a brief conversation?"
        
        return {
            'content': content,
            'message_type': message_type,
            'character_count': len(content),
            'quality_metrics': {'overall_quality': 6.0, 'fallback_used': True},
            'generation_metadata': {
                'content_type': f'linkedin_{message_type}',
                'generation_method': 'fallback',
                'country_adapted': country
            }
        }
    
    def _get_fallback_email_template(self, jd_analysis: Dict, country: str, email_type: str) -> Dict:
        """Generate fallback email template."""
        
        extracted_info = jd_analysis.get('extracted_info', {})
        company = extracted_info.get('company_name', 'the company')
        role = extracted_info.get('role_title', 'the role')
        
        subject = f"Application for {role} position"
        body = f"""Dear Hiring Manager,

I am writing to express my interest in the {role} position at {company}. With my background in product management and technology, I believe I would be a valuable addition to your team.

In my previous roles, I have successfully delivered projects that drive business results and improve operational efficiency. I am excited about the opportunity to contribute to {company}'s continued success.

Thank you for your consideration.

Best regards,
Vinesh Kumar"""
        
        return {
            'subject': subject,
            'body': body,
            'email_type': email_type,
            'quality_metrics': {'overall_quality': 6.0, 'fallback_used': True},
            'generation_metadata': {
                'content_type': f'email_{email_type}',
                'generation_method': 'fallback',
                'country_adapted': country
            }
        }
    
    def generate_complete_outreach_package(self, 
                                         jd_analysis: Dict, 
                                         user_profile: Dict, 
                                         country: str) -> Dict:
        """Generate complete outreach package: LinkedIn connection, LinkedIn message, and email."""
        
        try:
            # Generate all components
            linkedin_connection = self.generate_linkedin_message(
                jd_analysis, user_profile, country, 'connection'
            )
            
            linkedin_message = self.generate_linkedin_message(
                jd_analysis, user_profile, country, 'message'
            )
            
            email_template = self.generate_email_template(
                jd_analysis, user_profile, country, 'application'
            )
            
            return {
                'linkedin_connection': linkedin_connection,
                'linkedin_message': linkedin_message,
                'email_template': email_template,
                'package_metadata': {
                    'generated_for_jd': f"{jd_analysis.get('extracted_info', {}).get('company', 'Unknown')} - {jd_analysis.get('extracted_info', {}).get('role_title', 'Unknown Role')}",
                    'country_adapted': country,
                    'generation_method': 'dynamic_template_package',
                    'components_count': 3
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating complete outreach package: {e}")
            return {"error": str(e)}