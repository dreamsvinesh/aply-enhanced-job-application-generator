#!/usr/bin/env python3
"""
Unit tests for Resume Generator module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from modules.resume_generator import ResumeGenerator
from modules.jd_parser import JobDescriptionParser

class TestResumeGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ResumeGenerator()
        self.parser = JobDescriptionParser()
    
    def test_aiml_variant_selection(self):
        """Test AIML resume variant selection"""
        ai_jd = "Looking for PM with AI, machine learning, TensorFlow, and RAG systems"
        jd_data = self.parser.parse(ai_jd)
        
        variant = self.generator._determine_resume_variant(
            jd_data['ai_ml_focus'], 
            jd_data['b2b_vs_b2c'], 
            jd_data['required_skills']
        )
        
        self.assertEqual(variant, 'aiml')
    
    def test_b2b_variant_selection(self):
        """Test B2B resume variant selection"""
        b2b_jd = "Enterprise software, B2B customers, Salesforce, SAP integration"
        jd_data = self.parser.parse(b2b_jd)
        
        variant = self.generator._determine_resume_variant(
            jd_data['ai_ml_focus'], 
            jd_data['b2b_vs_b2c'], 
            jd_data['required_skills']
        )
        
        self.assertEqual(variant, 'b2b')
    
    def test_ats_score_calculation(self):
        """Test ATS score calculation"""
        jd_data = {
            'required_skills': ['python', 'machine learning', 'product management'],
            'preferred_skills': ['salesforce', 'agile']
        }
        
        resume_content = "Python expert with machine learning and product management experience. Salesforce certified."
        
        score = self.generator._calculate_ats_score(jd_data, resume_content)
        
        self.assertGreaterEqual(score, 70)  # Should have good match
        self.assertLessEqual(score, 100)
    
    def test_missing_skills_detection(self):
        """Test missing skills detection and mapping"""
        user_skills = ['Machine Learning', 'Python', 'Product Strategy']
        jd_skills = {'tensorflow', 'pytorch', 'python', 'kubernetes'}
        
        missing = self.generator._find_missing_skills(user_skills, jd_skills, 'ai_ml')
        
        self.assertIn('TensorFlow', missing)
        self.assertIn('PyTorch', missing)
        self.assertNotIn('Python', missing)  # Should not include existing skills

if __name__ == '__main__':
    unittest.main()