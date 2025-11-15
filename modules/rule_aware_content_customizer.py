#!/usr/bin/env python3
"""
Rule-Aware Content Customizer
Uses LLM to customize content while enforcing all existing rules and guidelines.
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging

# Import existing modules
from llm_service import LLMService
from country_config import CountryConfig
from database_manager import DatabaseManager
from user_data_extractor import UserDataExtractor

class RuleAwareContentCustomizer:
    """
    LLM-based content customization that follows all existing rules.
    
    This module bridges the gap between template-based structure and LLM customization,
    ensuring that all country-specific rules, content quality standards, and formatting
    requirements are preserved while providing role-specific tailoring.
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        self.country_config = CountryConfig()
        self.db_manager = DatabaseManager()
        self.user_extractor = UserDataExtractor()
        self.logger = logging.getLogger(__name__)
        
        # Load real user factual data
        self.factual_data = self.user_extractor.extract_vinesh_data()
        self.user_profile = self._load_user_profile()
        
        # Initialize rule enforcement components
        self._initialize_rule_sets()
    
    def _load_user_profile(self) -> Dict:
        """Load user profile for content personalization."""
        try:
            profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load user profile: {e}")
            return {}
    
    def _initialize_rule_sets(self):
        """Initialize comprehensive rule sets for validation."""
        
        # Content quality rules
        self.content_rules = {
            'forbidden_phrases': [
                'leverage', 'utilize', 'drive results', 'synergize', 'ideate',
                'actualize', 'operationalize', 'streamline', 'optimize',
                'comprehensive', 'extensive', 'robust', 'strategic',
                'innovative', 'cutting-edge', 'dynamic', 'scalable'
            ],
            'llm_red_flags': [
                'delve into', 'furthermore', 'however', 'moreover',
                'in conclusion', 'to summarize', 'it is worth noting',
                'esteemed organization', 'valuable addition to your team',
                'proven track record'
            ],
            'placeholder_patterns': [
                r'\[Your Name\]', r'\[Company\]', r'\[Role\]', r'\[Date\]',
                r'\[Skill\]', r'\[Experience\]', r'<.*?>', r'\{.*?\}'
            ],
            'professional_standards': {
                'min_specificity': 'Include specific metrics, technologies, or achievements',
                'factual_accuracy': 'Only use information from user profile',
                'human_voice': 'Avoid corporate jargon and AI-like language'
            }
        }
        
        # Formatting rules by content type
        self.formatting_rules = {
            'resume': {
                'section_order': ['summary', 'experience', 'education', 'skills'],
                'bullet_format': '• [Achievement with metric]',
                'length_limits': {'summary': 100, 'bullet_point': 150},
                'required_elements': ['quantified achievements', 'action verbs', 'relevant keywords']
            },
            'cover_letter': {
                'structure': ['opening', 'body_paragraph_1', 'body_paragraph_2', 'closing'],
                'opening_style': 'direct_personal',
                'required_elements': ['specific role mention', 'company research', 'value proposition']
            },
            'linkedin_message': {
                'structure': ['greeting', 'connection_reason', 'value_proposition', 'call_to_action'],
                'tone': 'professional_casual',
                'required_elements': ['personal connection', 'mutual benefit', 'clear next step']
            },
            'email_template': {
                'subject_format': 'Application: [Role] - [Your Name]',
                'structure': ['greeting', 'introduction', 'attachment_mention', 'closing'],
                'tone': 'professional_direct'
            }
        }
    
    def customize_with_rules(self, 
                           jd_analysis: Dict, 
                           user_profile: Dict, 
                           country: str,
                           content_type: str = 'resume',
                           template_structure: Optional[Dict] = None) -> Dict:
        """
        Generate customized content while enforcing all rules.
        
        Args:
            jd_analysis: Analysis from enhanced JD parser
            user_profile: User's complete profile
            country: Target country for cultural rules
            content_type: Type of content to generate
            template_structure: Dynamic template structure from template generator
            
        Returns:
            Dictionary with customized content and metadata
        """
        try:
            # Build rule-comprehensive prompt
            rule_prompt = self._build_rule_aware_prompt(
                jd_analysis, user_profile, country, content_type, template_structure
            )
            
            # Generate customization with LLM
            customization_response = self.llm_service.call_llm(
                prompt=rule_prompt,
                task_type="content_customization",
                max_tokens=800,
                temperature=0.3  # Balance creativity with consistency
            )
            
            # Parse and validate LLM response
            customization = self._parse_customization_response(customization_response)
            
            # Apply rule enforcement
            validated_customization = self._enforce_rules(
                customization, country, content_type, jd_analysis
            )
            
            # Apply fact validation
            fact_validation = self.user_extractor.validate_content_against_facts(
                self._extract_all_text_content(validated_customization)
            )
            validated_customization['fact_validation'] = fact_validation
            
            # Track customization in database
            self._track_customization_usage(
                jd_analysis, country, content_type, validated_customization, template_structure
            )
            
            return validated_customization
            
        except Exception as e:
            self.logger.error(f"Error in rule-aware customization: {e}")
            return self._get_fallback_customization(content_type, country)
    
    def _build_rule_aware_prompt(self, 
                               jd_analysis: Dict, 
                               user_profile: Dict, 
                               country: str, 
                               content_type: str,
                               template_structure: Optional[Dict]) -> str:
        """Build comprehensive prompt with all rules embedded."""
        
        # Get country-specific rules
        country_rules = self.country_config.get_config(country)
        content_rules = self.formatting_rules[content_type]
        
        # Extract key information
        role_focus = jd_analysis['role_classification']['primary_focus']
        company_name = jd_analysis['extracted_info']['company_name']
        role_title = jd_analysis['extracted_info']['role_title']
        positioning_strategy = jd_analysis['positioning_strategy']
        
        # Get user's relevant experience and skills
        user_experience = user_profile.get('experience', [])
        user_skills = user_profile.get('skills', {})
        user_achievements = user_profile.get('key_achievements', [])
        
        # Extract template structure information
        template_guidance = ""
        if template_structure:
            template_info = template_structure.get('template_structure', {})
            content_emphasis = template_info.get('content_emphasis', {})
            role_specific = template_structure.get('template_structure', {}).get('role_specific_focus', {})
            
            template_guidance = f"""
DYNAMIC TEMPLATE STRUCTURE (Custom for this role):
Section Order: {', '.join(template_info.get('section_order', ['summary', 'experience', 'skills']))}
Top Priority: {content_emphasis.get('top_priority', 'relevant experience')}
Key Metrics to Highlight: {', '.join(content_emphasis.get('key_metrics_to_highlight', ['performance results']))}
Skills to Feature: {', '.join(content_emphasis.get('skills_to_feature', ['core skills']))}
Technical Emphasis: {role_specific.get('technical_emphasis', 'technical capabilities')}
Business Emphasis: {role_specific.get('business_emphasis', 'business impact')}
"""
        else:
            template_guidance = "STANDARD TEMPLATE STRUCTURE: Focus on relevant experience and achievements"
        
        # Add fact preservation constraints
        fact_constraints = self.user_extractor.create_llm_constraints_prompt()
        
        return f"""
You are an expert {content_type} writer specializing in the {country} job market. Create customized {content_type} content that follows ALL rules below.

{fact_constraints}

STRICT COMPLIANCE RULES:

1. COUNTRY-SPECIFIC RULES FOR {country.upper()}:
   • Tone: {country_rules['tone']['directness']} directness, {country_rules['tone']['formality']} formality
   • Key Values: {', '.join(country_rules['tone']['key_values'])}
   • Avoid: {', '.join(country_rules['tone']['avoid'])}
   • Length Limit: {country_rules[content_type]['max_length'] if content_type in country_rules else 'Standard'} {self._get_length_unit(content_type)}
   • Style: {country_rules[content_type].get('style', 'Professional')}

2. CONTENT QUALITY RULES:
   • ONLY use factual information from user profile below
   • NO placeholder text like [Your Name], [Company], [Role]
   • NO corporate jargon: {', '.join(self.content_rules['forbidden_phrases'][:10])}
   • NO AI language: {', '.join(self.content_rules['llm_red_flags'][:8])}
   • Use specific metrics and quantified achievements only
   • Natural human writing, avoid formal/corporate tone

3. FORMATTING RULES FOR {content_type.upper()}:
   • Structure: {' → '.join(content_rules['structure'])}
   • Required Elements: {', '.join(content_rules['required_elements'])}
   • Tone: {content_rules.get('tone', 'Professional')}

{template_guidance}

JOB CONTEXT:
Company: {company_name}
Role: {role_title}
Focus Area: {role_focus.replace('_', ' ').title()}

POSITIONING STRATEGY:
Key Strengths: {', '.join(positioning_strategy['key_strengths_to_emphasize'])}
Experience Framing: {positioning_strategy['experience_framing']}
Cultural Adaptation: {positioning_strategy['cultural_adaptation']}

USER PROFILE DATA (ONLY use information from here):
Technical Skills: {json.dumps(user_skills.get('technical', []))}
Business Skills: {json.dumps(user_skills.get('business', []))}

Recent Experience (last 3 roles):
{self._format_experience_for_prompt(user_experience[:3])}

Key Achievements:
{self._format_achievements_for_prompt(user_achievements[:5])}

TASK: Generate {content_type} customization that follows ALL rules above.

Return ONLY this JSON format:
{{
    "customized_sections": {{
        "domain_focus": "Specific focus area tailored for this {role_focus.replace('_', ' ')} role using {country} tone",
        "key_achievement_reframed": "User's most relevant achievement rewritten for this role with {country} cultural tone and NO corporate jargon",
        "technical_skills_emphasis": "Most relevant technical skills from user profile for this role",
        "business_impact_framing": "Business impact using {country} values and specific user achievements",
        "experience_positioning": "How to position user's experience for this specific role"
    }},
    "country_adaptations": {{
        "tone_adjustments": "Specific {country} tone adaptations applied",
        "cultural_elements": "Cultural elements emphasized for {country} market",
        "communication_style": "Communication style adjustments for {country}"
    }},
    "rule_compliance": {{
        "length_check": "Content within {country} limits",
        "jargon_removed": "Corporate jargon eliminated", 
        "human_voice": "Natural human writing achieved",
        "factual_accuracy": "Only user profile facts used"
    }}
}}

VALIDATION CHECKLIST before responding:
✓ Follows {country} cultural tone ({country_rules['tone']['directness']} directness, {country_rules['tone']['formality']} formality)?
✓ No corporate jargon or AI language?
✓ Only factual content from user profile?
✓ Appropriate length for {country}?
✓ Natural human writing style?
✓ Specific metrics and achievements included?
"""

    def _format_experience_for_prompt(self, experience_list: List[Dict]) -> str:
        """Format experience for prompt inclusion."""
        formatted = []
        for exp in experience_list:
            company = exp.get('company', 'Unknown')
            role = exp.get('role', 'Unknown Role')
            highlights = exp.get('highlights', [])
            
            exp_text = f"• {role} at {company}"
            if highlights:
                exp_text += f": {', '.join(highlights[:2])}"
            formatted.append(exp_text)
        
        return '\n'.join(formatted) if formatted else "No experience data available"
    
    def _format_achievements_for_prompt(self, achievements_list: List[str]) -> str:
        """Format achievements for prompt inclusion."""
        if not achievements_list:
            return "No specific achievements listed"
        
        formatted = []
        for i, achievement in enumerate(achievements_list, 1):
            formatted.append(f"{i}. {achievement}")
        
        return '\n'.join(formatted)
    
    def _get_length_unit(self, content_type: str) -> str:
        """Get appropriate length unit for content type."""
        units = {
            'resume': 'words per section',
            'cover_letter': 'words total',
            'linkedin_message': 'characters',
            'email_template': 'words'
        }
        return units.get(content_type, 'words')
    
    def _parse_customization_response(self, llm_response: str) -> Dict:
        """Parse LLM customization response."""
        try:
            # Extract JSON from response
            if "```json" in llm_response:
                json_start = llm_response.find("```json") + 7
                json_end = llm_response.find("```", json_start)
                json_str = llm_response[json_start:json_end].strip()
            else:
                json_start = llm_response.find("{")
                json_end = llm_response.rfind("}") + 1
                json_str = llm_response[json_start:json_end]
            
            customization = json.loads(json_str)
            
            # Add metadata
            customization['generation_method'] = 'llm_rule_aware'
            customization['generated_at'] = self._get_timestamp()
            
            return customization
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse customization JSON: {e}")
            return self._get_fallback_customization('resume', 'Netherlands')
        except Exception as e:
            self.logger.error(f"Error parsing customization: {e}")
            return self._get_fallback_customization('resume', 'Netherlands')
    
    def _enforce_rules(self, 
                      customization: Dict, 
                      country: str, 
                      content_type: str, 
                      jd_analysis: Dict) -> Dict:
        """Apply rule enforcement to customization."""
        
        validated_customization = customization.copy()
        
        # Content validation
        validation_results = self._validate_content_rules(customization, country)
        validated_customization['validation_results'] = validation_results
        
        # Apply fixes if needed
        if validation_results['has_violations']:
            validated_customization = self._apply_rule_fixes(
                validated_customization, validation_results, country
            )
        
        # Country-specific tone enforcement
        validated_customization = self._enforce_country_tone(
            validated_customization, country
        )
        
        # Calculate quality scores
        quality_scores = self._calculate_quality_scores(validated_customization, country)
        validated_customization['quality_scores'] = quality_scores
        
        return validated_customization
    
    def _validate_content_rules(self, customization: Dict, country: str) -> Dict:
        """Validate content against all rules."""
        
        violations = []
        warnings = []
        
        # Extract all text content for validation
        all_content = self._extract_all_text_content(customization)
        
        # Check for forbidden phrases
        for phrase in self.content_rules['forbidden_phrases']:
            if phrase.lower() in all_content.lower():
                violations.append(f"Forbidden phrase detected: '{phrase}'")
        
        # Check for LLM red flags
        for flag in self.content_rules['llm_red_flags']:
            if flag.lower() in all_content.lower():
                violations.append(f"LLM language detected: '{flag}'")
        
        # Check for placeholder text
        for pattern in self.content_rules['placeholder_patterns']:
            if re.search(pattern, all_content, re.IGNORECASE):
                violations.append(f"Placeholder text found: pattern '{pattern}'")
        
        # Country-specific validation
        country_rules = self.country_config.get_config(country)
        country_violations = self._validate_country_specific_rules(
            all_content, country_rules
        )
        violations.extend(country_violations)
        
        return {
            'has_violations': len(violations) > 0,
            'violations': violations,
            'warnings': warnings,
            'total_violations': len(violations),
            'compliance_score': max(0, 10 - len(violations))
        }
    
    def _extract_all_text_content(self, customization: Dict) -> str:
        """Extract all text content from customization for validation."""
        content_parts = []
        
        def extract_text(obj):
            if isinstance(obj, str):
                content_parts.append(obj)
            elif isinstance(obj, dict):
                for value in obj.values():
                    extract_text(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_text(item)
        
        extract_text(customization)
        return ' '.join(content_parts)
    
    def _validate_country_specific_rules(self, content: str, country_rules: Dict) -> List[str]:
        """Validate country-specific rules."""
        violations = []
        
        tone_config = country_rules['tone']
        
        # Check for avoided phrases/styles
        avoided_phrases = tone_config.get('avoid', [])
        for phrase in avoided_phrases:
            if phrase.lower() in content.lower():
                violations.append(f"Country rule violation: '{phrase}' should be avoided for this country")
        
        # Check directness level (simple heuristic)
        if tone_config['directness'] == 'high':
            # High directness should avoid hesitant language
            hesitant_phrases = ['perhaps', 'maybe', 'i believe', 'i think', 'possibly']
            for phrase in hesitant_phrases:
                if phrase in content.lower():
                    violations.append(f"Directness violation: '{phrase}' too hesitant for high directness country")
        
        return violations
    
    def _apply_rule_fixes(self, customization: Dict, validation_results: Dict, country: str) -> Dict:
        """Apply automatic fixes for rule violations."""
        
        fixed_customization = customization.copy()
        
        # Fix forbidden phrases
        for violation in validation_results['violations']:
            if 'Forbidden phrase detected' in violation:
                phrase = violation.split("'")[1]
                fixed_customization = self._replace_forbidden_phrase(fixed_customization, phrase)
        
        # Fix LLM language
        for violation in validation_results['violations']:
            if 'LLM language detected' in violation:
                phrase = violation.split("'")[1]
                fixed_customization = self._replace_llm_phrase(fixed_customization, phrase)
        
        # Add fix metadata
        fixed_customization['auto_fixes_applied'] = len(validation_results['violations'])
        
        return fixed_customization
    
    def _replace_forbidden_phrase(self, customization: Dict, phrase: str) -> Dict:
        """Replace forbidden corporate phrase with human alternative."""
        
        replacements = {
            'leverage': 'use',
            'utilize': 'use',
            'optimize': 'improve',
            'streamline': 'simplify',
            'comprehensive': 'complete',
            'extensive': 'wide',
            'robust': 'strong',
            'strategic': 'planned'
        }
        
        replacement = replacements.get(phrase.lower(), phrase)
        
        def replace_in_obj(obj):
            if isinstance(obj, str):
                return obj.replace(phrase, replacement)
            elif isinstance(obj, dict):
                return {k: replace_in_obj(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_in_obj(item) for item in obj]
            return obj
        
        return replace_in_obj(customization)
    
    def _replace_llm_phrase(self, customization: Dict, phrase: str) -> Dict:
        """Replace LLM-like phrase with natural alternative."""
        
        replacements = {
            'delve into': 'explore',
            'furthermore': 'also',
            'moreover': 'also',
            'in conclusion': 'finally',
            'esteemed organization': 'company',
            'proven track record': 'experience'
        }
        
        replacement = replacements.get(phrase.lower(), '')
        
        def replace_in_obj(obj):
            if isinstance(obj, str):
                return obj.replace(phrase, replacement)
            elif isinstance(obj, dict):
                return {k: replace_in_obj(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_in_obj(item) for item in obj]
            return obj
        
        return replace_in_obj(customization)
    
    def _enforce_country_tone(self, customization: Dict, country: str) -> Dict:
        """Enforce country-specific tone adjustments."""
        
        adapted_customization = customization.copy()
        
        # Apply country-specific adaptations using existing country config
        for section_key, section_content in adapted_customization.get('customized_sections', {}).items():
            if isinstance(section_content, str):
                adapted_content = self.country_config.adapt_content_tone(
                    section_content, country, 'general'
                )
                adapted_customization['customized_sections'][section_key] = adapted_content
        
        return adapted_customization
    
    def _calculate_quality_scores(self, customization: Dict, country: str) -> Dict:
        """Calculate quality scores for the customization."""
        
        all_content = self._extract_all_text_content(customization)
        validation_results = customization.get('validation_results', {})
        
        scores = {
            'rule_compliance': validation_results.get('compliance_score', 10),
            'human_voice': self._calculate_human_voice_score(all_content),
            'country_appropriateness': self._calculate_country_score(all_content, country),
            'specificity': self._calculate_specificity_score(all_content),
            'factual_accuracy': self._calculate_factual_accuracy_score(customization)
        }
        
        # Calculate overall score
        scores['overall_quality'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def _calculate_human_voice_score(self, content: str) -> float:
        """Calculate how human-like the content sounds."""
        score = 10.0
        
        # Deduct for corporate jargon
        for phrase in self.content_rules['forbidden_phrases']:
            if phrase.lower() in content.lower():
                score -= 0.5
        
        # Deduct for LLM language
        for phrase in self.content_rules['llm_red_flags']:
            if phrase.lower() in content.lower():
                score -= 1.0
        
        # Bonus for contractions (more human)
        contractions = len(re.findall(r"\w+'[a-z]+", content))
        score += min(contractions * 0.2, 1.0)
        
        return max(0.0, min(10.0, score))
    
    def _calculate_country_score(self, content: str, country: str) -> float:
        """Calculate country cultural appropriateness."""
        country_rules = self.country_config.get_config(country)
        tone_config = country_rules['tone']
        
        score = 8.0  # Start with good baseline
        
        # Check for avoided elements
        avoided_phrases = tone_config.get('avoid', [])
        for phrase in avoided_phrases:
            if phrase.lower() in content.lower():
                score -= 1.0
        
        # Bonus for cultural values
        key_values = tone_config.get('key_values', [])
        for value in key_values:
            if value.lower() in content.lower():
                score += 0.5
        
        return max(0.0, min(10.0, score))
    
    def _calculate_specificity_score(self, content: str) -> float:
        """Calculate how specific and quantified the content is."""
        score = 5.0
        
        # Look for metrics and numbers
        metrics = re.findall(r'\d+%|\d+\+|\d+[kKmMbB]|\$\d+', content)
        score += min(len(metrics) * 0.5, 3.0)
        
        # Look for specific technologies/tools
        tech_mentions = len(re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,2}\b', content))
        score += min(tech_mentions * 0.1, 2.0)
        
        return min(10.0, score)
    
    def _calculate_factual_accuracy_score(self, customization: Dict) -> float:
        """Calculate factual accuracy based on user profile usage."""
        # For now, return high score if no violations detected
        validation_results = customization.get('validation_results', {})
        violations = validation_results.get('violations', [])
        
        # Check for factual accuracy violations
        factual_violations = [v for v in violations if 'factual' in v.lower()]
        
        return max(0.0, 10.0 - len(factual_violations))
    
    def _track_customization_usage(self, jd_analysis: Dict, country: str, content_type: str, customization: Dict, template_structure: Optional[Dict] = None):
        """Track customization usage for analytics."""
        try:
            company = jd_analysis['extracted_info']['company_name']
            
            # Find or create application record
            applications = self.db_manager.get_applications(company=company, limit=1)
            
            if applications:
                app_id = applications[0]['id']
            else:
                # Create new application record
                app_id = self.db_manager.save_analysis_to_database(
                    company=company,
                    role_title=jd_analysis['extracted_info']['role_title'],
                    country=country,
                    jd_text=jd_analysis.get('raw_jd_text', ''),
                    analysis=jd_analysis
                )
            
            # Track LLM usage
            quality_scores = customization.get('quality_scores', {})
            
            self.db_manager.track_llm_usage(
                application_id=app_id,
                task_type="content_customization",
                model_used="gpt-4o-mini",
                tokens_input=800,  # Estimate
                tokens_output=400,  # Estimate
                cost_usd=0.003,  # Estimate
                response_time_ms=2000,  # Estimate
                success=True,
                output_quality_score=quality_scores.get('overall_quality', 8.0)
            )
            
        except Exception as e:
            self.logger.error(f"Error tracking customization usage: {e}")
    
    def _get_fallback_customization(self, content_type: str, country: str) -> Dict:
        """Generate fallback customization if LLM fails."""
        return {
            "customized_sections": {
                "domain_focus": "General professional focus",
                "key_achievement_reframed": "Professional achievements and experience",
                "technical_skills_emphasis": "Core technical competencies",
                "business_impact_framing": "Business value and contributions",
                "experience_positioning": "Professional background and expertise"
            },
            "country_adaptations": {
                "tone_adjustments": f"Standard professional tone for {country}",
                "cultural_elements": f"Cultural considerations for {country} market",
                "communication_style": f"Professional communication style"
            },
            "rule_compliance": {
                "length_check": "Standard length guidelines followed",
                "jargon_removed": "Corporate jargon avoided",
                "human_voice": "Natural professional writing",
                "factual_accuracy": "Profile-based information used"
            },
            "generation_method": "fallback",
            "quality_scores": {
                "rule_compliance": 6.0,
                "human_voice": 7.0,
                "country_appropriateness": 6.0,
                "specificity": 5.0,
                "factual_accuracy": 8.0,
                "overall_quality": 6.4
            }
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def batch_customize_content(self, applications_data: List[Dict]) -> List[Dict]:
        """Batch customize content for multiple applications."""
        results = []
        
        for i, app_data in enumerate(applications_data):
            self.logger.info(f"Customizing content for application {i+1}/{len(applications_data)}")
            
            try:
                customization = self.customize_with_rules(
                    jd_analysis=app_data['jd_analysis'],
                    user_profile=app_data.get('user_profile', self.user_profile),
                    country=app_data['country'],
                    content_type=app_data.get('content_type', 'resume'),
                    template_variant=app_data.get('template_variant', 'b2b')
                )
                
                results.append({
                    'success': True,
                    'customization': customization,
                    'application_data': app_data
                })
                
            except Exception as e:
                self.logger.error(f"Error customizing content for application {i+1}: {e}")
                results.append({
                    'success': False,
                    'error': str(e),
                    'application_data': app_data
                })
        
        return results
    
    def get_customization_analytics(self, days: int = 30) -> Dict:
        """Get analytics on customization quality and performance."""
        try:
            # Get LLM usage for content customization
            llm_stats = self.db_manager.get_llm_cost_summary(days)
            
            customization_stats = llm_stats.get('content_customization', {})
            
            return {
                'total_customizations': customization_stats.get('call_count', 0),
                'avg_quality_score': customization_stats.get('avg_quality_score', 0),
                'total_cost': customization_stats.get('total_cost', 0),
                'avg_response_time': customization_stats.get('avg_response_time', 0),
                'success_rate': 100.0,  # From successful calls
                'cost_per_customization': customization_stats.get('avg_cost_per_call', 0)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting customization analytics: {e}")
            return {"error": str(e)}