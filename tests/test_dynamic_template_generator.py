#!/usr/bin/env python3
"""
Test Dynamic Template Generator
Tests the corrected approach for dynamic template generation with LLM integration.
"""

import unittest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / "modules"))

from dynamic_template_generator import DynamicTemplateGenerator

class TestDynamicTemplateGenerator(unittest.TestCase):
    """Test cases for DynamicTemplateGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = DynamicTemplateGenerator()
        
        # Mock JD analysis for Squarespace Frontend Developer (Communication Platforms)
        self.squarespace_jd_analysis = {
            'extracted_info': {
                'company': 'Squarespace',
                'company_name': 'Squarespace',
                'role_title': 'Frontend Developer - Communication Platforms'
            },
            'role_classification': {
                'primary_focus': 'communication_platforms',
                'secondary_focus': 'frontend_development',
                'industry': 'communication',
                'seniority_level': 'mid'
            },
            'requirements': {
                'must_have_technical': ['React', 'JavaScript', 'CSS', 'Email Systems', 'Communication APIs'],
                'must_have_business': ['User Experience', 'Platform Integration', 'Performance'],
                'experience_years': '3-5 years',
                'domain_expertise': ['Communication Tools', 'Email Platforms', 'User Interfaces']
            },
            'company_context': {
                'stage': 'scale-up',
                'size': 'mid-large',
                'culture': 'creative-technical'
            },
            'positioning_strategy': {
                'key_strengths_to_emphasize': ['React Development', 'Communication UIs', 'User Engagement'],
                'experience_framing': 'Frontend specialist with communication platform expertise'
            }
        }
        
        # Mock user profile
        self.user_profile = {
            'skills': {
                'technical': ['React', 'JavaScript', 'TypeScript', 'CSS', 'HTML'],
                'business': ['User Experience', 'Project Management', 'Communication']
            },
            'experience': [
                {
                    'role': 'Frontend Developer',
                    'company': 'TechCorp',
                    'duration': '2 years',
                    'achievements': ['Built messaging interfaces', 'Improved user engagement by 30%']
                }
            ],
            'key_achievements': [
                'Developed communication features for 50K+ users',
                'Optimized frontend performance by 40%'
            ]
        }
        
        # Mock LLM response for dynamic template generation
        self.mock_llm_response = """
{
    "template_structure": {
        "section_order": ["summary", "experience", "skills", "projects", "education"],
        "section_priorities": {
            "primary_sections": ["summary", "experience", "skills"],
            "secondary_sections": ["projects"],
            "optional_sections": ["education"]
        },
        "content_emphasis": {
            "top_priority": "communication platform development expertise",
            "key_metrics_to_highlight": ["user engagement rates", "message delivery performance", "UI responsiveness"],
            "skills_to_feature": ["React", "JavaScript", "Communication APIs", "Component Design"],
            "experience_angle": "frontend developer specializing in communication interfaces"
        },
        "role_specific_focus": {
            "technical_emphasis": "React component development for communication tools",
            "business_emphasis": "user engagement and communication effectiveness",
            "unique_requirements": ["email campaign interfaces", "messaging system UIs", "notification systems"],
            "success_metrics": ["user engagement improvement", "interface responsiveness", "communication feature adoption"]
        }
    },
    "cultural_adaptations": {
        "country_specific_adjustments": "Portugal professional format with direct communication style",
        "tone_requirements": "professional yet approachable, avoiding corporate jargon",
        "format_requirements": "concise 1-page format with quantified achievements"
    },
    "user_profile_integration": {
        "matching_strengths": ["React expertise", "frontend development experience", "user interface skills"],
        "experience_positioning": "emphasize communication feature development at TechCorp",
        "skills_highlighting": ["React", "JavaScript", "UI Development", "User Engagement"],
        "achievement_selection": "focus on user engagement improvements and interface development"
    }
}
"""
    
    @patch('dynamic_template_generator.LLMService')
    def test_generate_dynamic_template_success(self, mock_llm_service):
        """Test successful dynamic template generation."""
        # Mock LLM service response
        mock_llm_instance = Mock()
        mock_llm_instance.call_llm.return_value = self.mock_llm_response
        mock_llm_service.return_value = mock_llm_instance
        
        # Create generator with mocked LLM service
        generator = DynamicTemplateGenerator()
        generator.llm_service = mock_llm_instance
        
        # Generate dynamic template
        result = generator.generate_dynamic_template(
            jd_analysis=self.squarespace_jd_analysis,
            user_profile=self.user_profile,
            country='portugal'
        )
        
        # Verify template structure
        self.assertIn('template_structure', result)
        self.assertIn('cultural_adaptations', result)
        self.assertIn('user_profile_integration', result)
        self.assertIn('generation_metadata', result)
        
        # Verify template structure content
        template_struct = result['template_structure']
        self.assertIn('section_order', template_struct)
        self.assertIn('content_emphasis', template_struct)
        self.assertIn('role_specific_focus', template_struct)
        
        # Verify summary and experience are included
        section_order = template_struct['section_order']
        self.assertIn('summary', section_order)
        self.assertIn('experience', section_order)
        
        # Verify country adaptations
        cultural_adapt = result['cultural_adaptations']
        self.assertEqual(cultural_adapt['validated_for_country'], 'portugal')
        self.assertIn('max_pages', cultural_adapt)
        
        # Verify generation metadata
        metadata = result['generation_metadata']
        self.assertIn('Squarespace', metadata['generated_for_jd'])
        self.assertEqual(metadata['country_adapted'], 'portugal')
        self.assertEqual(metadata['generation_method'], 'dynamic_llm')
        self.assertTrue(metadata['user_profile_considered'])
    
    @patch('dynamic_template_generator.LLMService')
    def test_generate_template_with_invalid_llm_response(self, mock_llm_service):
        """Test template generation with invalid LLM response falls back gracefully."""
        # Mock LLM service with invalid JSON response
        mock_llm_instance = Mock()
        mock_llm_instance.call_llm.return_value = "Invalid JSON response"
        mock_llm_service.return_value = mock_llm_instance
        
        generator = DynamicTemplateGenerator()
        generator.llm_service = mock_llm_instance
        
        # Generate template (should fallback)
        result = generator.generate_dynamic_template(
            jd_analysis=self.squarespace_jd_analysis,
            user_profile=self.user_profile,
            country='portugal'
        )
        
        # Verify fallback template structure is returned
        self.assertIn('template_structure', result)
        self.assertIn('generation_metadata', result)
        
        # Verify fallback metadata
        metadata = result['generation_metadata']
        self.assertEqual(metadata['generation_method'], 'fallback')
        self.assertIn('fallback_reason', metadata)
    
    def test_template_structure_validation(self):
        """Test template structure validation ensures required sections."""
        # Test structure missing summary
        incomplete_structure = {
            'template_structure': {
                'section_order': ['experience', 'skills'],
                'content_emphasis': {'top_priority': 'test'}
            },
            'cultural_adaptations': {},
            'user_profile_integration': {}
        }
        
        validated = self.generator._validate_template_structure(
            incomplete_structure, 'portugal', 'resume'
        )
        
        # Verify summary was added
        section_order = validated['template_structure']['section_order']
        self.assertIn('summary', section_order)
        self.assertIn('experience', section_order)
        
        # Verify country validation was added
        self.assertEqual(validated['cultural_adaptations']['validated_for_country'], 'portugal')
        self.assertIn('quality_validation', validated)
    
    def test_parse_template_structure_with_code_blocks(self):
        """Test parsing LLM response that includes JSON in code blocks."""
        llm_response_with_blocks = f"""
Here is the dynamic template structure:

```json
{self.mock_llm_response}
```

This template is specifically designed for the role.
"""
        
        result = self.generator._parse_template_structure(llm_response_with_blocks)
        
        # Verify successful parsing
        self.assertIn('template_structure', result)
        self.assertIn('cultural_adaptations', result)
        self.assertIn('user_profile_integration', result)
        
        # Verify content is correct
        template_struct = result['template_structure']
        self.assertIn('communication platform development expertise', 
                     template_struct['content_emphasis']['top_priority'])
    
    def test_basic_template_structure_fallback(self):
        """Test that fallback template structure has required components."""
        fallback = self.generator._get_basic_template_structure()
        
        # Verify all required components
        self.assertIn('template_structure', fallback)
        self.assertIn('cultural_adaptations', fallback)
        self.assertIn('user_profile_integration', fallback)
        
        # Verify template structure has required fields
        template_struct = fallback['template_structure']
        self.assertIn('section_order', template_struct)
        self.assertIn('content_emphasis', template_struct)
        
        # Verify essential sections are included
        section_order = template_struct['section_order']
        self.assertIn('summary', section_order)
        self.assertIn('experience', section_order)
    
    def test_structure_completeness_check(self):
        """Test structure completeness validation."""
        # Complete structure
        complete_structure = {
            'template_structure': {
                'section_order': ['summary', 'experience'],
                'content_emphasis': {'top_priority': 'test'}
            },
            'cultural_adaptations': {},
            'user_profile_integration': {}
        }
        
        self.assertTrue(self.generator._check_structure_completeness(complete_structure))
        
        # Incomplete structure (missing cultural_adaptations)
        incomplete_structure = {
            'template_structure': {
                'section_order': ['summary'],
                'content_emphasis': {'top_priority': 'test'}
            },
            'user_profile_integration': {}
        }
        
        self.assertFalse(self.generator._check_structure_completeness(incomplete_structure))
    
    @patch('dynamic_template_generator.LLMService')
    def test_batch_template_generation(self, mock_llm_service):
        """Test batch generation of multiple dynamic templates."""
        # Mock LLM service
        mock_llm_instance = Mock()
        mock_llm_instance.call_llm.return_value = self.mock_llm_response
        mock_llm_service.return_value = mock_llm_instance
        
        generator = DynamicTemplateGenerator()
        generator.llm_service = mock_llm_instance
        
        # Prepare multiple applications data
        applications_data = [
            {
                'jd_analysis': self.squarespace_jd_analysis,
                'user_profile': self.user_profile,
                'country': 'portugal',
                'content_type': 'resume'
            },
            {
                'jd_analysis': self.squarespace_jd_analysis,  # Reusing for test
                'country': 'spain',
                'content_type': 'cover_letter'
            }
        ]
        
        # Generate batch
        results = generator.batch_generate_templates(applications_data)
        
        # Verify results
        self.assertEqual(len(results), 2)
        
        for result in results:
            self.assertIn('success', result)
            self.assertTrue(result['success'])
            self.assertIn('template_structure', result)
            self.assertIn('application_data', result)
    
    @patch('dynamic_template_generator.DatabaseManager')
    def test_template_generation_tracking(self, mock_db_manager):
        """Test that template generation is properly tracked."""
        # Mock database manager
        mock_db_instance = Mock()
        mock_db_manager.return_value = mock_db_instance
        
        generator = DynamicTemplateGenerator()
        generator.db_manager = mock_db_instance
        
        # Track template generation
        generator._track_template_generation(
            self.squarespace_jd_analysis,
            {'template_structure': {}}
        )
        
        # Verify tracking was called
        mock_db_instance.track_llm_usage.assert_called_once()
        
        # Verify tracking parameters
        call_args = mock_db_instance.track_llm_usage.call_args
        self.assertEqual(call_args[1]['task_type'], 'dynamic_template_generation')
        self.assertEqual(call_args[1]['model_used'], 'gpt-4o-mini')
        self.assertTrue(call_args[1]['success'])
    
    def test_template_prompt_building(self):
        """Test that template generation prompt is built correctly."""
        prompt = self.generator._build_template_generation_prompt(
            self.squarespace_jd_analysis,
            self.user_profile,
            'portugal',
            'resume'
        )
        
        # Verify key information is included in prompt
        self.assertIn('Squarespace', prompt)
        self.assertIn('Frontend Developer - Communication Platforms', prompt)
        self.assertIn('communication_platforms', prompt)
        self.assertIn('React', prompt)
        self.assertIn('portugal', prompt.lower())
        self.assertIn('TechCorp', prompt)
        
        # Verify prompt structure includes required sections
        self.assertIn('JOB DETAILS:', prompt)
        self.assertIn('KEY REQUIREMENTS FROM JD:', prompt)
        self.assertIn('USER PROFILE HIGHLIGHTS:', prompt)
        self.assertIn('POSITIONING STRATEGY:', prompt)
        self.assertIn('COUNTRY REQUIREMENTS', prompt)
        self.assertIn('template_structure', prompt)


class TestDynamicTemplateIntegration(unittest.TestCase):
    """Integration tests for dynamic template generator with other components."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.generator = DynamicTemplateGenerator()
    
    @patch('dynamic_template_generator.LLMService')
    @patch('dynamic_template_generator.CountryConfig')
    @patch('dynamic_template_generator.DatabaseManager')
    def test_full_integration_workflow(self, mock_db, mock_country, mock_llm):
        """Test full integration workflow from JD analysis to final template."""
        # Mock country config
        mock_country_instance = Mock()
        mock_country_instance.get_config.return_value = {
            'resume_format': {'max_pages': 1},
            'tone': {
                'directness': 'direct',
                'formality': 'professional',
                'key_values': ['precision', 'achievement', 'respect']
            }
        }
        mock_country.return_value = mock_country_instance
        
        # Mock LLM service
        mock_llm_instance = Mock()
        mock_llm_instance.call_llm.return_value = """
{
    "template_structure": {
        "section_order": ["summary", "experience", "skills"],
        "content_emphasis": {
            "top_priority": "communication platform expertise",
            "key_metrics_to_highlight": ["user engagement", "platform performance"],
            "skills_to_feature": ["React", "JavaScript"]
        }
    },
    "cultural_adaptations": {
        "country_specific_adjustments": "Portugal professional style"
    },
    "user_profile_integration": {
        "matching_strengths": ["React development", "frontend expertise"]
    }
}
"""
        mock_llm.return_value = mock_llm_instance
        
        # Mock database manager
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance
        
        # Create generator with mocked dependencies
        generator = DynamicTemplateGenerator()
        generator.llm_service = mock_llm_instance
        generator.country_config = mock_country_instance
        generator.db_manager = mock_db_instance
        
        # Test JD analysis from previous component
        jd_analysis = {
            'extracted_info': {
                'company': 'Squarespace',
                'company_name': 'Squarespace',
                'role_title': 'Frontend Developer'
            },
            'role_classification': {
                'primary_focus': 'communication_platforms',
                'seniority_level': 'mid'
            },
            'requirements': {
                'must_have_technical': ['React'],
                'must_have_business': ['User Experience'],
                'experience_years': '3-5 years',
                'domain_expertise': ['Communication Tools']
            },
            'positioning_strategy': {
                'key_strengths_to_emphasize': ['React Development'],
                'experience_framing': 'Frontend specialist'
            },
            'company_context': {}
        }
        
        user_profile = {
            'skills': {'technical': ['React', 'JavaScript']},
            'experience': [{'role': 'Frontend Developer', 'company': 'TechCorp'}],
            'key_achievements': ['Built communication features']
        }
        
        # Generate dynamic template
        result = generator.generate_dynamic_template(
            jd_analysis=jd_analysis,
            user_profile=user_profile,
            country='portugal'
        )
        
        # Verify successful integration
        self.assertIn('template_structure', result)
        self.assertIn('generation_metadata', result)
        
        # Verify country config was used
        mock_country_instance.get_config.assert_called_with('portugal')
        
        # Verify LLM was called with correct parameters
        mock_llm_instance.call_llm.assert_called_once()
        call_args = mock_llm_instance.call_llm.call_args
        self.assertEqual(call_args[1]['task_type'], 'dynamic_template_generation')
        self.assertEqual(call_args[1]['temperature'], 0.2)
        
        # Verify database tracking
        mock_db_instance.track_llm_usage.assert_called_once()
        
        # Verify country validation was applied
        self.assertEqual(result['cultural_adaptations']['validated_for_country'], 'portugal')
        self.assertEqual(result['cultural_adaptations']['max_pages'], 1)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)