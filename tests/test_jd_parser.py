#!/usr/bin/env python3
"""
Unit tests for JD Parser module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from modules.jd_parser import JobDescriptionParser

class TestJDParser(unittest.TestCase):
    def setUp(self):
        self.parser = JobDescriptionParser()
    
    def test_company_extraction(self):
        """Test company name extraction"""
        jd = "We're looking for a Product Manager to join TomTom's innovative team."
        result = self.parser.parse(jd)
        self.assertIn('TomTom', result['company'])
    
    def test_ai_ml_focus_detection(self):
        """Test AI/ML focus assessment"""
        ai_jd = "Looking for PM with AI, machine learning, and RAG experience"
        non_ai_jd = "Looking for PM with marketing and sales experience"
        
        ai_result = self.parser.parse(ai_jd)
        non_ai_result = self.parser.parse(non_ai_jd)
        
        self.assertGreater(ai_result['ai_ml_focus'], 0.3)
        self.assertLess(non_ai_result['ai_ml_focus'], 0.1)
    
    def test_b2b_vs_b2c_detection(self):
        """Test business model detection"""
        b2b_jd = "Enterprise software, B2B customers, Salesforce integration"
        b2c_jd = "Mobile app, consumer users, user engagement"
        
        b2b_result = self.parser.parse(b2b_jd)
        b2c_result = self.parser.parse(b2c_jd)
        
        self.assertEqual(b2b_result['b2b_vs_b2c'], 'b2b')
        self.assertEqual(b2c_result['b2b_vs_b2c'], 'b2c')
    
    def test_skills_extraction(self):
        """Test skills extraction from JD"""
        jd = "Requirements: Python, SQL, machine learning, agile methodology"
        result = self.parser.parse(jd)
        
        extracted_skills = result['required_skills'] + result['preferred_skills']
        self.assertIn('python', [skill.lower() for skill in extracted_skills])
        self.assertIn('machine learning', [skill.lower() for skill in extracted_skills])

if __name__ == '__main__':
    unittest.main()