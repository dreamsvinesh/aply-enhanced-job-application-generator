#!/usr/bin/env python3
"""
Integration tests for the complete Aply system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import shutil
from pathlib import Path
from main import JobApplicationGenerator

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.generator = JobApplicationGenerator()
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample job descriptions for different scenarios
        self.ai_jd = """
        Senior AI Product Manager
        OpenAI
        Amsterdam, Netherlands
        
        We need a PM with AI/ML expertise, RAG systems, LLMs, TensorFlow experience.
        Requirements: Product management, machine learning, vector databases, prompt engineering.
        """
        
        self.b2b_jd = """
        Enterprise Product Manager
        Salesforce
        Dublin, Ireland
        
        Looking for PM with B2B SaaS experience, Salesforce, SAP integration.
        Requirements: Enterprise software, stakeholder management, B2B customers.
        """
        
        self.b2c_jd = """
        Consumer Product Manager
        Spotify
        Stockholm, Sweden
        
        Mobile app PM for consumer music platform with millions of users.
        Requirements: Mobile apps, user engagement, A/B testing, consumer products.
        """
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_ai_role_end_to_end(self):
        """Test complete workflow for AI/ML role"""
        output_path = self.generator.generate_application_package(
            self.ai_jd, 
            "netherlands", 
            "OpenAI"
        )
        
        # Verify file was created
        self.assertTrue(Path(output_path).exists())
        
        # Read and verify content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check all sections exist
        self.assertIn('## Resume', content)
        self.assertIn('## Cover Letter', content)
        self.assertIn('## LinkedIn Message', content)
        self.assertIn('## Email Template', content)
        self.assertIn('## Changes Made', content)
        
        # Check AI/ML emphasis
        self.assertIn('RAG', content)
        self.assertIn('94% accuracy', content)
        self.assertIn('AI', content.upper())
        
        # Check Netherlands tone (direct)
        self.assertNotIn('I believe that', content)
    
    def test_b2b_role_end_to_end(self):
        """Test complete workflow for B2B role"""
        output_path = self.generator.generate_application_package(
            self.b2b_jd, 
            "ireland", 
            "Salesforce"
        )
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check B2B emphasis
        self.assertIn('Salesforce', content)
        self.assertIn('enterprise', content.lower())
        self.assertIn('$2M revenue', content)
        
        # Check Ireland tone (formal but warm)
        self.assertIn('delighted', content.lower())
    
    def test_b2c_role_end_to_end(self):
        """Test complete workflow for B2C role"""
        output_path = self.generator.generate_application_package(
            self.b2c_jd, 
            "sweden", 
            "Spotify"
        )
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check B2C emphasis
        self.assertIn('600K+ users', content)
        self.assertIn('91% NPS', content)
        self.assertIn('mobile', content.lower())
        
        # Check Sweden tone (modest, collaborative)
        self.assertNotIn('excellent', content)
        self.assertNotIn('outstanding', content)
    
    def test_ats_scoring_accuracy(self):
        """Test ATS scoring gives reasonable results"""
        # High-match scenario
        high_match_jd = "Looking for PM with AI, machine learning, RAG systems, product management, Salesforce"
        output_path = self.generator.generate_application_package(high_match_jd, "netherlands")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract ATS score
        import re
        score_match = re.search(r'ATS Match Score:\s*(\d+)%', content)
        self.assertIsNotNone(score_match)
        
        score = int(score_match.group(1))
        self.assertGreaterEqual(score, 70)  # Should have good match
    
    def test_linkedin_character_limits(self):
        """Test LinkedIn messages stay under character limits"""
        for country in ['netherlands', 'finland', 'ireland', 'sweden', 'denmark', 'portugal']:
            output_path = self.generator.generate_application_package(
                self.ai_jd, 
                country
            )
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract LinkedIn message
            linkedin_section = content.split('## LinkedIn Message')[1].split('## Email Template')[0]
            message_lines = [line for line in linkedin_section.split('\n') if line.strip() and not line.startswith('**')]
            
            if message_lines:
                message = message_lines[0]
                self.assertLessEqual(len(message), 400, f"LinkedIn message too long for {country}: {len(message)} chars")
    
    def test_all_countries_generate_successfully(self):
        """Test that all supported countries generate without errors"""
        countries = ['netherlands', 'finland', 'ireland', 'sweden', 'denmark', 'portugal']
        
        for country in countries:
            with self.subTest(country=country):
                try:
                    output_path = self.generator.generate_application_package(
                        self.ai_jd, 
                        country, 
                        "TestCompany"
                    )
                    
                    self.assertTrue(Path(output_path).exists())
                    
                    # Verify content is not empty
                    with open(output_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    self.assertGreater(len(content), 1000)  # Reasonable minimum length
                    
                except Exception as e:
                    self.fail(f"Failed to generate for {country}: {str(e)}")

if __name__ == '__main__':
    unittest.main()