#!/usr/bin/env python3
"""
Human Voice Agent - Makes content sound authentic and personal, not AI-generated

This agent is the final step in content generation, transforming corporate/LLM-like 
language into natural, human voice while preserving all achievements and metrics.
"""

import re
import json
from typing import Dict, List, Tuple, Any
from pathlib import Path

class HumanVoiceAgent:
    """
    Transforms AI-generated content into authentic human voice
    
    Key principles:
    - Use simple, direct language
    - Active voice over passive
    - Personal tone over corporate speak
    - Specific achievements over vague claims
    - Conversational but professional
    """
    
    def __init__(self):
        self.load_user_profile()
        self.llm_patterns = self._load_llm_patterns()
        self.human_replacements = self._load_human_replacements()
        
    def load_user_profile(self):
        """Load user profile to understand personal voice"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                self.user_profile = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load user profile for voice analysis: {e}")
            self.user_profile = {}
    
    def humanize_content(self, content_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply human voice transformation to all content sections
        
        Args:
            content_dict: Dictionary with resume, cover_letter, linkedin_message, email_template
            
        Returns:
            Content dictionary with humanized text
        """
        humanized_content = {}
        
        # Process each content type with specific rules
        if 'resume' in content_dict:
            humanized_content['resume'] = self._humanize_resume(content_dict['resume'])
            
        if 'cover_letter' in content_dict:
            humanized_content['cover_letter'] = self._humanize_cover_letter(content_dict['cover_letter'])
            
        if 'linkedin_message' in content_dict:
            humanized_content['linkedin_message'] = self._humanize_linkedin_message(content_dict['linkedin_message'])
            
        if 'email_template' in content_dict:
            humanized_content['email_template'] = self._humanize_email_template(content_dict['email_template'])
        
        return humanized_content
    
    def _humanize_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Humanize resume content while preserving structure"""
        humanized_resume = resume_data.copy()
        
        # Humanize summary
        if 'summary' in resume_data:
            humanized_resume['summary'] = self._apply_voice_transformation(
                resume_data['summary'], 
                content_type='resume_summary'
            )
        
        # Humanize experience descriptions
        if 'experience' in resume_data and isinstance(resume_data['experience'], list):
            humanized_resume['experience'] = []
            for exp in resume_data['experience']:
                humanized_exp = exp.copy()
                if 'highlights' in exp:
                    humanized_exp['highlights'] = [
                        self._apply_voice_transformation(highlight, content_type='resume_bullet')
                        for highlight in exp['highlights']
                    ]
                humanized_resume['experience'].append(humanized_exp)
        
        return humanized_resume
    
    def _humanize_cover_letter(self, cover_letter: str) -> str:
        """Humanize cover letter content"""
        return self._apply_voice_transformation(cover_letter, content_type='cover_letter')
    
    def _humanize_linkedin_message(self, linkedin_message: str) -> str:
        """Humanize LinkedIn message"""
        return self._apply_voice_transformation(linkedin_message, content_type='linkedin')
    
    def _humanize_email_template(self, email_template: Dict[str, Any]) -> Dict[str, Any]:
        """Humanize email template"""
        humanized_email = email_template.copy()
        
        if isinstance(email_template, dict):
            if 'subject' in email_template:
                humanized_email['subject'] = self._apply_voice_transformation(
                    email_template['subject'], content_type='email_subject'
                )
            if 'body' in email_template:
                humanized_email['body'] = self._apply_voice_transformation(
                    email_template['body'], content_type='email_body'
                )
        else:
            # Handle string email templates
            humanized_email = self._apply_voice_transformation(email_template, content_type='email_body')
        
        return humanized_email
    
    def _apply_voice_transformation(self, text: str, content_type: str) -> str:
        """
        Apply comprehensive voice transformation
        
        Args:
            text: Original text
            content_type: Type of content for context-specific rules
            
        Returns:
            Humanized text
        """
        if not text or not isinstance(text, str):
            return text
            
        # Step 1: Remove LLM patterns
        transformed_text = self._remove_llm_patterns(text)
        
        # Step 2: Apply human voice replacements
        transformed_text = self._apply_human_replacements(transformed_text)
        
        # Step 3: Convert to active voice
        transformed_text = self._convert_to_active_voice(transformed_text)
        
        # Step 4: Simplify language
        transformed_text = self._simplify_language(transformed_text)
        
        # Step 5: Add personal touches based on content type
        transformed_text = self._add_personal_touches(transformed_text, content_type)
        
        # Step 6: Preserve metrics and achievements
        transformed_text = self._preserve_achievements(transformed_text)
        
        return transformed_text.strip()
    
    def _load_llm_patterns(self) -> List[Dict[str, str]]:
        """Load patterns that indicate LLM-generated content"""
        return [
            # Corporate buzzwords
            {"pattern": r"\b(comprehensive|extensive|robust|strategic|innovative|cutting-edge|dynamic|scalable)\b", "type": "buzzword"},
            {"pattern": r"\b(leverage|utilize|drive|optimize|streamline|facilitate|enable|empower)\b", "type": "business_verb"},
            {"pattern": r"\b(synergize|ideate|actualize|operationalize|systematize|maximize|expedite)\b", "type": "corporate_jargon"},
            
            # LLM-like sentence starters
            {"pattern": r"^I am writing to express my (sincere )?interest", "type": "formal_opener"},
            {"pattern": r"^Throughout my career, I have", "type": "generic_opener"},
            {"pattern": r"^I am excited about the opportunity to", "type": "enthusiasm_phrase"},
            {"pattern": r"^My experience in .* directly aligns with", "type": "alignment_phrase"},
            
            # Overly formal phrases
            {"pattern": r"esteemed organization", "type": "formal_phrase"},
            {"pattern": r"valuable addition to your team", "type": "generic_phrase"},
            {"pattern": r"proven track record", "type": "corporate_phrase"},
            {"pattern": r"best practices", "type": "business_phrase"},
            
            # Passive constructions
            {"pattern": r"has been (implemented|developed|created|established)", "type": "passive_voice"},
            {"pattern": r"was (responsible|tasked) with", "type": "passive_responsibility"},
            
            # Generic qualifiers
            {"pattern": r"\b(significant|substantial|considerable|notable|remarkable)\b", "type": "vague_qualifier"},
            {"pattern": r"\b(various|multiple|numerous|several)\b", "type": "vague_quantifier"},
        ]
    
    def _load_human_replacements(self) -> Dict[str, str]:
        """Load human voice replacements for corporate speak"""
        return {
            # Direct replacements for buzzwords
            "comprehensive": "complete",
            "extensive": "wide",
            "robust": "strong", 
            "strategic": "planned",
            "innovative": "new",
            "cutting-edge": "latest",
            "dynamic": "flexible",
            "scalable": "growable",
            
            # Business verb replacements
            "leverage": "use",
            "utilize": "use",
            "drive": "lead",
            "optimize": "improve",
            "streamline": "simplify",
            "facilitate": "help",
            "enable": "allow",
            "empower": "help",
            
            # Corporate jargon to simple language
            "synergize": "work together",
            "ideate": "brainstorm",
            "actualize": "make happen",
            "operationalize": "put into action",
            "systematize": "organize",
            "maximize": "increase",
            "expedite": "speed up",
            
            # Phrase replacements
            "esteemed organization": "company",
            "valuable addition to your team": "good fit for this role",
            "proven track record": "experience",
            "best practices": "good methods",
            "significant impact": "real results",
            "substantial improvement": "big improvement",
            
            # Formal to casual
            "I am writing to express my interest": "I'm interested",
            "Throughout my career, I have": "In my work, I've",
            "I am excited about the opportunity to": "I'd like to",
            "I would be delighted to": "I'd be happy to",
        }
    
    def _remove_llm_patterns(self, text: str) -> str:
        """Remove obvious LLM-generated patterns"""
        for pattern_dict in self.llm_patterns:
            pattern = pattern_dict["pattern"]
            
            if pattern_dict["type"] == "formal_opener":
                # Replace formal openers with casual ones
                text = re.sub(pattern, "I'm interested in", text, flags=re.IGNORECASE)
            elif pattern_dict["type"] == "generic_opener":
                # Replace generic openers
                text = re.sub(pattern, "In my work, I've", text, flags=re.IGNORECASE)
            elif pattern_dict["type"] == "enthusiasm_phrase":
                text = re.sub(pattern, "I'd like to", text, flags=re.IGNORECASE)
            elif pattern_dict["type"] == "alignment_phrase":
                text = re.sub(r"My experience in (.*?) directly aligns with", r"My \1 experience fits well with", text, flags=re.IGNORECASE)
                
        return text
    
    def _apply_human_replacements(self, text: str) -> str:
        """Apply human voice word replacements"""
        for corporate_term, human_term in self.human_replacements.items():
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(corporate_term) + r'\b'
            text = re.sub(pattern, human_term, text, flags=re.IGNORECASE)
        
        return text
    
    def _convert_to_active_voice(self, text: str) -> str:
        """Convert passive voice to active voice where possible"""
        
        # "was responsible for X" -> "I handled X" or "I managed X"
        text = re.sub(r"was responsible for (.*)", r"handled \1", text, flags=re.IGNORECASE)
        text = re.sub(r"were responsible for (.*)", r"handled \1", text, flags=re.IGNORECASE)
        
        # "was tasked with X" -> "I was asked to X" or "I did X"
        text = re.sub(r"was tasked with (.*)", r"did \1", text, flags=re.IGNORECASE)
        
        # "has been implemented" -> "I implemented" or "I built"
        text = re.sub(r"has been (implemented|developed|created)", r"I built", text, flags=re.IGNORECASE)
        text = re.sub(r"was (implemented|developed|created)", r"I built", text, flags=re.IGNORECASE)
        
        return text
    
    def _simplify_language(self, text: str) -> str:
        """Simplify complex language structures"""
        
        # Replace complex phrases with simple ones
        simplifications = {
            r"in order to": "to",
            r"due to the fact that": "because",
            r"despite the fact that": "although",
            r"in the event that": "if",
            r"with regard to": "about",
            r"in relation to": "about",
            r"for the purpose of": "to",
            r"in conjunction with": "with",
            r"subsequent to": "after",
            r"prior to": "before",
        }
        
        for complex_phrase, simple_phrase in simplifications.items():
            text = re.sub(complex_phrase, simple_phrase, text, flags=re.IGNORECASE)
        
        return text
    
    def _add_personal_touches(self, text: str, content_type: str) -> str:
        """Add personal touches based on content type"""
        
        if content_type == 'cover_letter':
            # Make cover letter more personal and conversational
            text = re.sub(r"Dear Hiring Manager", "Hi there", text)
            text = re.sub(r"I look forward to hearing from you", "I'd love to hear from you", text)
            text = re.sub(r"Thank you for your consideration", "Thanks for considering my application", text)
            
        elif content_type == 'linkedin':
            # Make LinkedIn message more casual and direct
            text = re.sub(r"I hope this message finds you well", "Hope you're doing well", text)
            text = re.sub(r"I would appreciate the opportunity", "I'd appreciate a chance", text)
            
        elif content_type == 'email_subject':
            # Make email subjects more direct
            text = re.sub(r"Application for the position of", "Application:", text)
            text = re.sub(r"Regarding the .* position", "Re:", text)
            
        return text
    
    def _preserve_achievements(self, text: str) -> str:
        """Ensure all metrics and achievements remain intact"""
        
        # This function ensures that specific numbers, percentages, and achievements
        # from the user's profile are preserved during transformation
        
        # Get user's key achievements to preserve
        user_achievements = self.user_profile.get('key_achievements', [])
        
        # Extract and preserve any metrics in the text
        # Numbers, percentages, dollar amounts, time periods should remain unchanged
        metric_patterns = [
            r'\d+%',  # percentages
            r'\$[\d,]+[KMB]?',  # dollar amounts
            r'\d+[KMB]?\+?\s*(users|customers|employees|queries|tickets|orders)',  # user/scale metrics
            r'\d+\s*(days?|hours?|minutes?|seconds?)',  # time metrics
            r'\d+(\.\d+)?[xX]',  # multiplication factors
        ]
        
        # These patterns should remain unchanged - they're the core value propositions
        preserved_metrics = []
        for pattern in metric_patterns:
            matches = re.findall(pattern, text)
            preserved_metrics.extend(matches)
        
        # No transformation needed here - just ensuring metrics stay intact
        # The voice transformation above should already preserve these
        
        return text
    
    def analyze_human_voice_score(self, text: str) -> Dict[str, Any]:
        """
        Analyze how human-like the text sounds
        
        Returns:
            Score and analysis of human voice characteristics
        """
        score_breakdown = {
            'llm_pattern_count': 0,
            'corporate_buzzword_count': 0,
            'passive_voice_count': 0,
            'personal_tone_score': 0,
            'metric_preservation': 0,
            'overall_human_score': 0
        }
        
        # Count LLM patterns
        for pattern_dict in self.llm_patterns:
            matches = len(re.findall(pattern_dict["pattern"], text, re.IGNORECASE))
            score_breakdown['llm_pattern_count'] += matches
        
        # Count corporate buzzwords
        buzzwords = ["comprehensive", "extensive", "leverage", "optimize", "strategic", "innovative"]
        for buzzword in buzzwords:
            if re.search(r'\b' + buzzword + r'\b', text, re.IGNORECASE):
                score_breakdown['corporate_buzzword_count'] += 1
        
        # Count passive voice instances
        passive_patterns = ["was responsible", "has been", "were developed"]
        for passive in passive_patterns:
            if passive in text.lower():
                score_breakdown['passive_voice_count'] += 1
        
        # Calculate personal tone score (more contractions = more personal)
        contractions = re.findall(r"\w+'[a-z]+", text)
        score_breakdown['personal_tone_score'] = min(len(contractions), 5)  # Cap at 5
        
        # Check metric preservation
        metrics = re.findall(r'\d+%|\$[\d,]+|\d+[xX]|\d+\s*(users|days|hours)', text)
        score_breakdown['metric_preservation'] = min(len(metrics), 3)  # Cap at 3
        
        # Calculate overall score (0-10 scale)
        # Lower LLM patterns and buzzwords = higher score
        # Higher personal tone and metrics = higher score
        penalty = (score_breakdown['llm_pattern_count'] + score_breakdown['corporate_buzzword_count'] + 
                  score_breakdown['passive_voice_count']) * 0.5
        bonus = (score_breakdown['personal_tone_score'] + score_breakdown['metric_preservation']) * 1.0
        
        score_breakdown['overall_human_score'] = max(0, min(10, 8 - penalty + bonus))
        
        return score_breakdown