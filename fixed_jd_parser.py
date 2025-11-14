#!/usr/bin/env python3
"""
FIXED JD Parser - Word-boundary matching instead of substring matching
"""

import re
from typing import Dict, List

class FixedJobDescriptionParser:
    def __init__(self):
        self.load_keywords_database()
        
    def load_keywords_database(self):
        """Load keywords database with improved categorization"""
        self.pm_keywords = {
            'communication_platform': [
                'communication', 'messaging', 'notifications', 'email', 'sms', 
                'lifecycle messaging', 'reminders', 'alerts', 'messaging platform',
                'communication platform', 'notification system', 'email platform',
                'messaging infrastructure', 'communication tools', 'messaging api',
                'notification api', 'email automation', 'sms automation'
            ],
            'api_integration': [
                'api integration', 'external partners', 'platform integration',
                'third-party integration', 'partner integration', 'webhook',
                'rest api', 'api-driven', 'service-oriented', 'microservices',
                'integration platform', 'external apis', 'partner apis'
            ],
            'ai_ml': [
                'artificial intelligence', 'machine learning', 'deep learning',
                'neural networks', 'rag', 'llm', 'large language models',
                'natural language processing', 'nlp', 'computer vision',
                'tensorflow', 'pytorch', 'scikit-learn', 'model training',
                'predictive modeling', 'data science', 'ml ops'
                # Removed problematic single-letter 'r' and generic 'automation'
            ],
            'product_management': [
                'product manager', 'product management', 'product strategy',
                'product roadmap', 'stakeholder management', 'cross-functional',
                'agile', 'scrum', 'user research', 'market research'
            ],
            'technical': [
                'salesforce', 'sap', 'mulesoft', 'database', 'sql',
                'aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes',
                'javascript', 'python', 'react', 'angular'
            ]
        }
    
    def _count_word_matches(self, text: str, keyword: str) -> int:
        """
        Count word-boundary matches instead of substring matches
        This prevents false positives like 'r' matching inside 'platforms'
        """
        # For single letters, require word boundaries
        if len(keyword) <= 2:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text, re.IGNORECASE)
            return len(matches)
        else:
            # For longer phrases, use case-insensitive substring matching
            return text.lower().count(keyword.lower())
    
    def _assess_ai_ml_focus(self, jd_text: str) -> float:
        """FIXED: Assess AI/ML focus using word-boundary matching"""
        ai_ml_mentions = 0
        total_mentions = 0
        
        # Count AI/ML keywords with proper word boundaries
        for keyword in self.pm_keywords['ai_ml']:
            count = self._count_word_matches(jd_text, keyword)
            ai_ml_mentions += count
            
        # Count all keywords across all categories
        for category, keywords in self.pm_keywords.items():
            for keyword in keywords:
                total_mentions += self._count_word_matches(jd_text, keyword)
        
        return ai_ml_mentions / max(total_mentions, 1)
    
    def _assess_communication_focus(self, jd_text: str) -> float:
        """NEW: Assess communication platform focus"""
        comm_mentions = 0
        total_mentions = 0
        
        # Count communication keywords
        for keyword in self.pm_keywords['communication_platform']:
            count = self._count_word_matches(jd_text, keyword)
            comm_mentions += count
            
        # Count API integration keywords (also relevant for communication roles)
        for keyword in self.pm_keywords['api_integration']:
            count = self._count_word_matches(jd_text, keyword)
            comm_mentions += count
            
        # Count all keywords
        for category, keywords in self.pm_keywords.items():
            for keyword in keywords:
                total_mentions += self._count_word_matches(jd_text, keyword)
        
        return comm_mentions / max(total_mentions, 1)
    
    def parse_and_classify(self, job_description: str) -> Dict:
        """Parse JD and classify the role focus"""
        
        ai_ml_focus = self._assess_ai_ml_focus(job_description)
        comm_focus = self._assess_communication_focus(job_description)
        
        # Determine the primary focus
        if comm_focus > 0.4:
            role_type = 'communication_platform'
        elif ai_ml_focus > 0.3:
            role_type = 'ai_ml'
        else:
            role_type = 'general_product'
            
        return {
            'ai_ml_focus': ai_ml_focus,
            'communication_focus': comm_focus,
            'role_type': role_type,
            'recommendation': self._get_resume_recommendation(role_type)
        }
    
    def _get_resume_recommendation(self, role_type: str) -> str:
        """Get resume tailoring recommendation"""
        recommendations = {
            'communication_platform': 'Emphasize messaging infrastructure, API integrations, communication platforms, email/SMS systems',
            'ai_ml': 'Emphasize AI/ML projects, data science, machine learning capabilities',
            'general_product': 'Emphasize general product management, business impact, cross-functional leadership'
        }
        return recommendations.get(role_type, 'General product management focus')

# Test the fix
if __name__ == "__main__":
    squarespace_jd = """At Squarespace, we empower product teams to solve meaningful customer and business problems. We're looking for a Product Manager to lead Acuity Communications, the team responsible for the tools and infrastructure that help businesses communicate with their clients throughout the scheduling journey.

For appointment-based businesses, client relationships are at the core of long-term success. Communications like confirmations, reminders, reschedules, and follow-ups, help businesses stay connected with clients and reduce no-shows. By overseeing the systems that deliver these messages at scale, you'll help customers operate more efficiently and build the strong client relationships that fuel growth.

You'll own our communication products: emails, reminders, notifications, and lifecycle messaging, while also managing the platform that ensures messages are delivered reliably and securely. You will blend platform ownership with B2B2C product design: empowering businesses with simple, intuitive tools, and ensuring their clients receive clear, timely communication that strengthens the relationship.

Execute the roadmap for Acuity's client communication products across email and SMS
Partner with engineering to deliver a scalable, compliant, and resilient messaging platform
Work with external communication partners to optimize current integrations and evaluate new functionality
Build intuitive tools that let businesses easily create, customize, and automate communications
Collaborate across Acuity product teams to support new triggers and lifecycle messaging use cases
Monitor system health, reliability, abuse risks, and cost efficiency

5–6+ years of Product Management experience, ideally in communications, messaging platforms, or lifecycle automation
Proven ability to tackle complex technical challenges across API-driven and service-oriented systems.
Expertise in owning relationships with external platform partners and driving roadmap alignment, integration improvements, or adoption of new capabilities"""

    parser = FixedJobDescriptionParser()
    result = parser.parse_and_classify(squarespace_jd)
    
    print("=== FIXED JD PARSER RESULTS ===")
    print(f"AI/ML Focus: {result['ai_ml_focus']:.3f}")
    print(f"Communication Focus: {result['communication_focus']:.3f}")
    print(f"Role Type: {result['role_type']}")
    print(f"Recommendation: {result['recommendation']}")