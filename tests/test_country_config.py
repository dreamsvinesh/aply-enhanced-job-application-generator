#!/usr/bin/env python3
"""
Unit tests for Country Configuration module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from modules.country_config import CountryConfig

class TestCountryConfig(unittest.TestCase):
    def setUp(self):
        self.config = CountryConfig()
    
    def test_supported_countries(self):
        """Test that all required countries are supported"""
        countries = self.config.get_supported_countries()
        
        required_countries = ['netherlands', 'finland', 'ireland', 'sweden', 'denmark', 'portugal']
        
        for country in required_countries:
            self.assertIn(country, countries)
    
    def test_country_config_structure(self):
        """Test that country configs have required structure"""
        for country in ['netherlands', 'finland', 'ireland']:
            config = self.config.get_config(country)
            
            # Check required sections exist
            self.assertIn('resume_format', config)
            self.assertIn('tone', config)
            self.assertIn('cover_letter', config)
            self.assertIn('linkedin_message', config)
            self.assertIn('cultural_notes', config)
    
    def test_tone_adaptation(self):
        """Test tone adaptation for different countries"""
        original_text = "I believe that I can contribute to your team"
        
        # Netherlands should be more direct
        nl_adapted = self.config.adapt_content_tone(original_text, 'netherlands')
        self.assertNotEqual(original_text, nl_adapted)
        self.assertIn('I can', nl_adapted)
        
    def test_resume_format_differences(self):
        """Test that countries have different resume format requirements"""
        nl_format = self.config.get_resume_format('netherlands')
        pt_format = self.config.get_resume_format('portugal')
        
        # Netherlands: no photo, Portugal: photo optional
        self.assertEqual(nl_format['include_photo'], False)
        self.assertEqual(pt_format['include_photo'], True)
        
        # Different page limits
        self.assertNotEqual(nl_format['max_pages'], pt_format['max_pages'])
    
    def test_linkedin_char_limits(self):
        """Test LinkedIn character limits by country"""
        nl_rules = self.config.get_linkedin_rules('netherlands')
        dk_rules = self.config.get_linkedin_rules('denmark')
        
        # Denmark should have shorter limit (more direct)
        self.assertLessEqual(dk_rules['max_chars'], nl_rules['max_chars'])

if __name__ == '__main__':
    unittest.main()