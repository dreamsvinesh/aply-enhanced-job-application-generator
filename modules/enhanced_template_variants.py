#!/usr/bin/env python3
"""
Enhanced Template Variants Manager
Dynamically selects and customizes templates based on JD analysis and user profile.
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging

# Import existing modules
from rule_aware_content_customizer import RuleAwareContentCustomizer
from country_config import CountryConfig
from database_manager import DatabaseManager

class EnhancedTemplateVariants:
    """
    Enhanced template management that goes beyond the original 3 fixed variants (aiml, b2b, b2c).
    
    Features:
    - Dynamic template selection based on JD analysis
    - LLM-enhanced template customization
    - Role-specific template adaptations
    - Country-aware template modifications
    - Template quality scoring and optimization
    """
    
    def __init__(self):
        self.customizer = RuleAwareContentCustomizer()
        self.country_config = CountryConfig()
        self.db_manager = DatabaseManager()
        self.logger = logging.getLogger(__name__)
        
        # Load user profile
        self.user_profile = self._load_user_profile()
        
        # Initialize enhanced template system
        self._initialize_template_variants()
        self._initialize_template_selectors()
    
    def _load_user_profile(self) -> Dict:
        """Load user profile for template personalization."""
        try:
            profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load user profile: {e}")
            return {}
    
    def _initialize_template_variants(self):
        """Initialize enhanced template variants beyond the original 3."""
        
        self.template_variants = {
            # Original variants (enhanced)
            'aiml': {
                'name': 'AI/ML Specialist',
                'focus_areas': ['artificial intelligence', 'machine learning', 'data science', 'research'],
                'key_sections': ['technical_expertise', 'research_experience', 'publications', 'model_development'],
                'tone': 'technical_expert',
                'emphasis': ['algorithms', 'statistical analysis', 'model performance', 'research contributions']
            },
            'b2b': {
                'name': 'B2B Professional',
                'focus_areas': ['enterprise', 'business_solutions', 'client_management', 'sales'],
                'key_sections': ['business_impact', 'client_relationships', 'revenue_generation', 'solution_delivery'],
                'tone': 'business_professional',
                'emphasis': ['ROI', 'client satisfaction', 'business growth', 'strategic thinking']
            },
            'b2c': {
                'name': 'B2C Specialist', 
                'focus_areas': ['consumer_products', 'user_experience', 'engagement', 'growth'],
                'key_sections': ['user_impact', 'engagement_metrics', 'product_growth', 'consumer_insights'],
                'tone': 'user_focused',
                'emphasis': ['user engagement', 'conversion rates', 'product adoption', 'consumer behavior']
            },
            
            # New enhanced variants
            'frontend_specialist': {
                'name': 'Frontend Development Specialist',
                'focus_areas': ['frontend_development', 'user_interface', 'react', 'javascript'],
                'key_sections': ['ui_development', 'component_architecture', 'performance_optimization', 'user_experience'],
                'tone': 'technical_creative',
                'emphasis': ['responsive design', 'component libraries', 'performance metrics', 'user accessibility']
            },
            'platform_engineer': {
                'name': 'Platform Engineering Expert',
                'focus_areas': ['platform_engineering', 'infrastructure', 'scalability', 'devops'],
                'key_sections': ['platform_design', 'infrastructure_scaling', 'system_reliability', 'developer_experience'],
                'tone': 'systems_architect',
                'emphasis': ['system scalability', 'platform reliability', 'automation', 'infrastructure optimization']
            },
            'communication_platforms': {
                'name': 'Communication Platform Developer',
                'focus_areas': ['communication_tools', 'messaging_systems', 'email_platforms', 'collaboration'],
                'key_sections': ['communication_features', 'messaging_architecture', 'user_engagement', 'platform_integration'],
                'tone': 'platform_focused',
                'emphasis': ['message delivery', 'user engagement', 'platform integrations', 'communication metrics']
            },
            'product_technical': {
                'name': 'Technical Product Professional',
                'focus_areas': ['product_management', 'technical_leadership', 'cross_functional', 'strategy'],
                'key_sections': ['product_strategy', 'technical_coordination', 'stakeholder_management', 'delivery_excellence'],
                'tone': 'product_leader',
                'emphasis': ['product metrics', 'technical decisions', 'team coordination', 'strategic impact']
            },
            'startup_generalist': {
                'name': 'Startup Generalist',
                'focus_areas': ['startup', 'growth', 'versatility', 'impact'],
                'key_sections': ['cross_functional_impact', 'growth_contributions', 'adaptability', 'initiative_leadership'],
                'tone': 'entrepreneurial',
                'emphasis': ['rapid growth', 'versatile skills', 'impact creation', 'startup agility']
            },
            'enterprise_specialist': {
                'name': 'Enterprise Solution Specialist', 
                'focus_areas': ['enterprise', 'large_scale', 'compliance', 'governance'],
                'key_sections': ['enterprise_solutions', 'compliance_expertise', 'large_scale_impact', 'governance_experience'],
                'tone': 'enterprise_professional',
                'emphasis': ['enterprise scale', 'compliance standards', 'governance processes', 'stakeholder management']
            }
        }
    
    def _initialize_template_selectors(self):
        """Initialize intelligent template selection logic."""
        
        self.selection_criteria = {
            # Primary focus mapping
            'primary_focus_mapping': {
                'ai_ml': 'aiml',
                'artificial_intelligence': 'aiml',
                'machine_learning': 'aiml',
                'data_science': 'aiml',
                'frontend_development': 'frontend_specialist',
                'communication_platforms': 'communication_platforms',
                'platform_engineering': 'platform_engineer',
                'product_management': 'product_technical',
                'enterprise_solutions': 'enterprise_specialist',
                'startup': 'startup_generalist'
            },
            
            # Company stage influence
            'company_stage_influence': {
                'startup': ['startup_generalist', 'frontend_specialist'],
                'scale-up': ['product_technical', 'platform_engineer'], 
                'enterprise': ['enterprise_specialist', 'b2b']
            },
            
            # Business model alignment
            'business_model_alignment': {
                'b2b': ['b2b', 'enterprise_specialist', 'product_technical'],
                'b2c': ['b2c', 'frontend_specialist', 'communication_platforms'],
                'platform': ['platform_engineer', 'communication_platforms']
            },
            
            # Seniority level considerations
            'seniority_adaptations': {
                'junior': ['focused_specialist', 'learning_emphasis'],
                'mid': ['balanced_approach', 'growth_potential'],
                'senior': ['leadership_focus', 'strategic_impact']
            }
        }
    
    def select_optimal_template(self, 
                              jd_analysis: Dict, 
                              user_profile: Dict, 
                              country: str) -> Tuple[str, Dict]:
        """
        Intelligently select the optimal template variant based on comprehensive analysis.
        
        Args:
            jd_analysis: Enhanced JD analysis results
            user_profile: User's complete profile
            country: Target country
            
        Returns:
            Tuple of (template_variant_name, selection_rationale)
        """
        try:
            # Extract key factors for selection
            role_classification = jd_analysis['role_classification']
            primary_focus = role_classification['primary_focus']
            company_stage = role_classification['company_stage']
            seniority_level = role_classification['seniority_level']
            
            # Get user's experience alignment
            profile_match = jd_analysis['profile_match']
            credibility_score = profile_match['credibility_score']
            
            # Calculate template scores
            template_scores = self._calculate_template_scores(
                primary_focus, company_stage, seniority_level, 
                profile_match, user_profile
            )
            
            # Select best template
            best_template = max(template_scores.items(), key=lambda x: x[1])
            selected_template = best_template[0]
            selection_score = best_template[1]
            
            # Generate selection rationale
            rationale = self._generate_selection_rationale(
                selected_template, primary_focus, company_stage, 
                seniority_level, selection_score
            )
            
            self.logger.info(f"Selected template '{selected_template}' with score {selection_score:.2f}")
            
            return selected_template, rationale
            
        except Exception as e:
            self.logger.error(f"Error in template selection: {e}")
            # Fallback to original logic
            return self._fallback_template_selection(jd_analysis)
    
    def _calculate_template_scores(self, 
                                  primary_focus: str, 
                                  company_stage: str, 
                                  seniority_level: str,
                                  profile_match: Dict, 
                                  user_profile: Dict) -> Dict[str, float]:
        """Calculate scores for each template variant."""
        
        scores = {}
        
        for template_name, template_config in self.template_variants.items():
            score = 0.0
            
            # Primary focus alignment (40% weight)
            focus_score = self._calculate_focus_alignment(primary_focus, template_config['focus_areas'])
            score += focus_score * 0.4
            
            # Company stage fit (20% weight)
            stage_score = self._calculate_stage_fit(company_stage, template_name)
            score += stage_score * 0.2
            
            # User profile match (25% weight) 
            profile_score = self._calculate_profile_match(user_profile, template_config)
            score += profile_score * 0.25
            
            # Seniority appropriateness (15% weight)
            seniority_score = self._calculate_seniority_fit(seniority_level, template_config)
            score += seniority_score * 0.15
            
            scores[template_name] = score
        
        return scores
    
    def _calculate_focus_alignment(self, primary_focus: str, template_focus_areas: List[str]) -> float:
        """Calculate how well the template aligns with the job's primary focus."""
        
        # Direct match
        if primary_focus in template_focus_areas:
            return 1.0
        
        # Partial match through keywords
        focus_keywords = primary_focus.replace('_', ' ').split()
        matches = 0
        
        for area in template_focus_areas:
            area_keywords = area.replace('_', ' ').split()
            for keyword in focus_keywords:
                if keyword in area_keywords:
                    matches += 1
        
        # Normalize by number of keywords
        return min(1.0, matches / max(len(focus_keywords), 1))
    
    def _calculate_stage_fit(self, company_stage: str, template_name: str) -> float:
        """Calculate how well the template fits the company stage."""
        
        stage_preferences = self.selection_criteria['company_stage_influence']
        
        if company_stage in stage_preferences:
            if template_name in stage_preferences[company_stage]:
                return 1.0
            # Give partial credit to related templates
            return 0.5
        
        # Default score for unspecified stages
        return 0.6
    
    def _calculate_profile_match(self, user_profile: Dict, template_config: Dict) -> float:
        """Calculate how well the user's profile matches the template."""
        
        user_skills = set()
        
        # Collect all user skills
        skills = user_profile.get('skills', {})
        for skill_category in skills.values():
            if isinstance(skill_category, list):
                user_skills.update(skill.lower() for skill in skill_category)
        
        # Collect template focus areas
        template_areas = set(area.lower().replace('_', ' ') for area in template_config['focus_areas'])
        
        # Calculate overlap
        matches = 0
        for area in template_areas:
            for skill in user_skills:
                if area in skill or skill in area:
                    matches += 1
        
        # Normalize by template areas count
        return min(1.0, matches / max(len(template_areas), 1))
    
    def _calculate_seniority_fit(self, seniority_level: str, template_config: Dict) -> float:
        """Calculate seniority appropriateness for template."""
        
        # All templates are suitable for mid-level (default)
        if seniority_level == 'mid':
            return 0.8
        
        # Senior roles prefer strategic/leadership templates
        senior_preferred = ['product_technical', 'enterprise_specialist', 'platform_engineer']
        if seniority_level == 'senior' and template_config.get('name', '').split()[0] in ['Technical', 'Enterprise', 'Platform']:
            return 1.0
        elif seniority_level == 'senior':
            return 0.7
        
        # Junior roles prefer specialist templates
        specialist_templates = ['frontend_specialist', 'communication_platforms', 'aiml']
        if seniority_level == 'junior':
            template_name = [k for k, v in self.template_variants.items() if v == template_config][0]
            if template_name in specialist_templates:
                return 1.0
            else:
                return 0.6
        
        return 0.7  # Default
    
    def _generate_selection_rationale(self, 
                                    selected_template: str, 
                                    primary_focus: str, 
                                    company_stage: str,
                                    seniority_level: str, 
                                    selection_score: float) -> Dict:
        """Generate explanation for template selection."""
        
        template_config = self.template_variants[selected_template]
        
        return {
            'selected_template': selected_template,
            'template_name': template_config['name'],
            'selection_score': round(selection_score, 2),
            'primary_reasons': [
                f"Aligns with {primary_focus.replace('_', ' ')} focus",
                f"Suitable for {company_stage} company stage", 
                f"Appropriate for {seniority_level} seniority level"
            ],
            'template_strengths': template_config['emphasis'][:3],
            'key_sections_emphasized': template_config['key_sections'][:3],
            'selection_confidence': self._calculate_confidence_level(selection_score)
        }
    
    def _calculate_confidence_level(self, score: float) -> str:
        """Calculate confidence level based on selection score."""
        if score >= 0.8:
            return "High"
        elif score >= 0.6:
            return "Medium"
        else:
            return "Low"
    
    def _fallback_template_selection(self, jd_analysis: Dict) -> Tuple[str, Dict]:
        """Fallback to original template selection logic."""
        
        # Use original logic as fallback
        primary_focus = jd_analysis['role_classification']['primary_focus']
        
        if 'ai' in primary_focus or 'ml' in primary_focus:
            return 'aiml', {'fallback': True, 'reason': 'AI/ML focus detected'}
        elif 'b2b' in str(jd_analysis).lower():
            return 'b2b', {'fallback': True, 'reason': 'B2B indicators found'}
        else:
            return 'b2c', {'fallback': True, 'reason': 'Default B2C selection'}
    
    def generate_enhanced_template(self, 
                                 selected_template: str,
                                 jd_analysis: Dict, 
                                 user_profile: Dict, 
                                 country: str,
                                 content_type: str = 'resume') -> Dict:
        """
        Generate enhanced template content with LLM customization.
        
        Args:
            selected_template: Name of selected template variant
            jd_analysis: JD analysis results
            user_profile: User profile
            country: Target country
            content_type: Type of content to generate
            
        Returns:
            Enhanced template with customized content
        """
        try:
            # Get base template structure
            base_template = self._get_base_template_structure(
                selected_template, content_type, country
            )
            
            # Apply LLM customization using rule-aware customizer
            customization = self.customizer.customize_with_rules(
                jd_analysis=jd_analysis,
                user_profile=user_profile, 
                country=country,
                content_type=content_type,
                template_variant=selected_template
            )
            
            # Merge template structure with customization
            enhanced_template = self._merge_template_with_customization(
                base_template, customization, selected_template
            )
            
            # Apply template-specific enhancements
            enhanced_template = self._apply_template_specific_enhancements(
                enhanced_template, selected_template, jd_analysis
            )
            
            # Add metadata
            enhanced_template['template_metadata'] = {
                'variant': selected_template,
                'variant_name': self.template_variants[selected_template]['name'],
                'country': country,
                'content_type': content_type,
                'generation_method': 'enhanced_llm_template',
                'customization_applied': True
            }
            
            return enhanced_template
            
        except Exception as e:
            self.logger.error(f"Error generating enhanced template: {e}")
            return self._get_fallback_template(selected_template, content_type)
    
    def _get_base_template_structure(self, 
                                   template_variant: str, 
                                   content_type: str, 
                                   country: str) -> Dict:
        """Get base template structure for the selected variant."""
        
        template_config = self.template_variants[template_variant]
        country_rules = self.country_config.get_config(country)
        
        if content_type == 'resume':
            return {
                'structure': {
                    'sections': template_config['key_sections'],
                    'order': country_rules['resume_format']['sections_order'],
                    'emphasis': template_config['emphasis']
                },
                'formatting': {
                    'tone': template_config['tone'],
                    'style': country_rules['resume_format'],
                    'length_limits': self._get_length_limits(country, content_type)
                },
                'content_guidelines': {
                    'focus_areas': template_config['focus_areas'],
                    'key_sections': template_config['key_sections'],
                    'required_elements': ['quantified achievements', 'relevant skills', 'impact metrics']
                }
            }
        
        elif content_type == 'cover_letter':
            return {
                'structure': {
                    'sections': ['opening', 'body', 'closing'],
                    'emphasis': template_config['emphasis'][:3]
                },
                'formatting': {
                    'tone': template_config['tone'],
                    'max_length': country_rules['cover_letter']['max_length'],
                    'style': country_rules['cover_letter']['opening_style']
                },
                'content_guidelines': {
                    'focus_areas': template_config['focus_areas'][:2],
                    'required_elements': ['role interest', 'relevant experience', 'value proposition']
                }
            }
        
        # Add other content types as needed
        return {'basic_structure': True}
    
    def _get_length_limits(self, country: str, content_type: str) -> Dict:
        """Get appropriate length limits for country and content type."""
        
        country_rules = self.country_config.get_config(country)
        
        if content_type == 'resume':
            return {
                'max_pages': country_rules['resume_format']['max_pages'],
                'summary_words': 80 if country == 'denmark' else 100,
                'bullet_points': 2 if country == 'denmark' else 3
            }
        elif content_type == 'cover_letter':
            return {
                'max_words': country_rules['cover_letter']['max_length'],
                'paragraphs': 3 if country == 'denmark' else 4
            }
        
        return {'standard': True}
    
    def _merge_template_with_customization(self, 
                                         base_template: Dict, 
                                         customization: Dict, 
                                         template_variant: str) -> Dict:
        """Merge base template structure with LLM customization."""
        
        enhanced_template = base_template.copy()
        
        # Add customized sections
        if 'customized_sections' in customization:
            enhanced_template['customized_content'] = customization['customized_sections']
        
        # Add country adaptations
        if 'country_adaptations' in customization:
            enhanced_template['cultural_adaptations'] = customization['country_adaptations']
        
        # Add quality metrics
        if 'quality_scores' in customization:
            enhanced_template['quality_assessment'] = customization['quality_scores']
        
        # Template-specific customizations
        template_config = self.template_variants[template_variant]
        enhanced_template['template_focus'] = {
            'primary_areas': template_config['focus_areas'],
            'key_emphasis': template_config['emphasis'],
            'tone_style': template_config['tone']
        }
        
        return enhanced_template
    
    def _apply_template_specific_enhancements(self, 
                                           template: Dict, 
                                           template_variant: str, 
                                           jd_analysis: Dict) -> Dict:
        """Apply template-specific enhancements based on variant type."""
        
        enhanced = template.copy()
        
        if template_variant == 'aiml':
            # AI/ML specific enhancements
            enhanced['specialized_sections'] = {
                'technical_expertise': 'Advanced ML algorithms and frameworks',
                'model_performance': 'Quantified model accuracy and performance metrics',
                'research_contributions': 'Publications and research achievements'
            }
        
        elif template_variant == 'frontend_specialist':
            # Frontend specific enhancements
            enhanced['specialized_sections'] = {
                'ui_development': 'React component architecture and design systems',
                'performance_metrics': 'Load time optimization and user experience metrics', 
                'accessibility': 'WCAG compliance and inclusive design principles'
            }
        
        elif template_variant == 'communication_platforms':
            # Communication platform specific enhancements
            enhanced['specialized_sections'] = {
                'messaging_systems': 'Email delivery and messaging architecture',
                'user_engagement': 'Communication feature adoption and engagement metrics',
                'platform_integrations': 'API integrations and third-party platform connectivity'
            }
        
        elif template_variant == 'product_technical':
            # Product technical enhancements
            enhanced['specialized_sections'] = {
                'product_strategy': 'Technical product roadmap and strategic decisions',
                'cross_functional_leadership': 'Engineering and business team coordination',
                'delivery_excellence': 'Product launch metrics and technical delivery'
            }
        
        # Add role-specific metrics emphasis
        role_focus = jd_analysis['role_classification']['primary_focus']
        enhanced['metrics_emphasis'] = self._get_role_specific_metrics(role_focus)
        
        return enhanced
    
    def _get_role_specific_metrics(self, role_focus: str) -> List[str]:
        """Get role-specific metrics to emphasize."""
        
        metrics_map = {
            'frontend_development': ['Page load time', 'User engagement', 'Component reusability', 'Accessibility score'],
            'communication_platforms': ['Message delivery rate', 'User engagement', 'Platform integrations', 'Feature adoption'],
            'ai_ml': ['Model accuracy', 'Performance improvements', 'Data processing efficiency', 'Research citations'],
            'platform_engineering': ['System uptime', 'Scalability metrics', 'Developer productivity', 'Infrastructure cost'],
            'product_management': ['Feature adoption', 'User satisfaction', 'Revenue impact', 'Time to market']
        }
        
        return metrics_map.get(role_focus, ['Performance improvements', 'User impact', 'Business results', 'Quality metrics'])
    
    def _get_fallback_template(self, template_variant: str, content_type: str) -> Dict:
        """Generate fallback template if enhancement fails."""
        
        return {
            'basic_template': True,
            'variant': template_variant,
            'content_type': content_type,
            'fallback_reason': 'Enhancement failed, using basic template',
            'customized_content': {
                'summary': 'Professional with relevant experience',
                'skills': 'Core technical and business skills',
                'achievements': 'Quantified professional achievements'
            }
        }
    
    def batch_generate_templates(self, applications_data: List[Dict]) -> List[Dict]:
        """Generate enhanced templates for multiple applications."""
        
        results = []
        
        for i, app_data in enumerate(applications_data):
            self.logger.info(f"Generating template for application {i+1}/{len(applications_data)}")
            
            try:
                # Select optimal template
                selected_template, rationale = self.select_optimal_template(
                    jd_analysis=app_data['jd_analysis'],
                    user_profile=app_data.get('user_profile', self.user_profile),
                    country=app_data['country']
                )
                
                # Generate enhanced template
                enhanced_template = self.generate_enhanced_template(
                    selected_template=selected_template,
                    jd_analysis=app_data['jd_analysis'],
                    user_profile=app_data.get('user_profile', self.user_profile),
                    country=app_data['country'],
                    content_type=app_data.get('content_type', 'resume')
                )
                
                results.append({
                    'success': True,
                    'template': enhanced_template,
                    'selection_rationale': rationale,
                    'application_data': app_data
                })
                
            except Exception as e:
                self.logger.error(f"Error generating template for application {i+1}: {e}")
                results.append({
                    'success': False,
                    'error': str(e),
                    'application_data': app_data
                })
        
        return results
    
    def get_template_analytics(self, days: int = 30) -> Dict:
        """Get analytics on template usage and performance."""
        
        try:
            # Get applications from database
            applications = self.db_manager.get_applications()
            
            if not applications:
                return {"no_data": True}
            
            # Analyze template usage
            template_usage = {}
            quality_by_template = {}
            
            for app in applications:
                # Get content versions for this application
                all_content = self.db_manager.get_all_content(app['id'])
                
                for content_type, content_data in all_content.items():
                    template_variant = content_data.get('template_variant', 'unknown')
                    
                    if template_variant not in template_usage:
                        template_usage[template_variant] = 0
                        quality_by_template[template_variant] = []
                    
                    template_usage[template_variant] += 1
                    
                    if 'quality_score' in content_data:
                        quality_by_template[template_variant].append(content_data['quality_score'])
            
            # Calculate statistics
            analytics = {
                'total_applications': len(applications),
                'template_distribution': template_usage,
                'template_quality_scores': {
                    template: {
                        'avg_quality': sum(scores) / len(scores) if scores else 0,
                        'usage_count': len(scores)
                    }
                    for template, scores in quality_by_template.items()
                },
                'most_popular_template': max(template_usage.items(), key=lambda x: x[1])[0] if template_usage else 'none',
                'highest_quality_template': max(
                    [(t, sum(s)/len(s) if s else 0) for t, s in quality_by_template.items()],
                    key=lambda x: x[1]
                )[0] if quality_by_template else 'none'
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting template analytics: {e}")
            return {"error": str(e)}