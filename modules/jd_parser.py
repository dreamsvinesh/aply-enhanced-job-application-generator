"""
Job Description Parser Module
Extracts key information from job descriptions including skills, requirements, and company details.
"""

import re
import json
from typing import Dict, List, Set, Optional
from pathlib import Path

class JobDescriptionParser:
    def __init__(self):
        self.load_keywords_database()
        
    def load_keywords_database(self):
        """Load keywords database for skill matching"""
        # Core PM skills
        self.pm_keywords = {
            'product_management': [
                'product manager', 'product management', 'product strategy', 'product vision',
                'product roadmap', 'roadmapping', 'product discovery', 'product ownership',
                'product owner', 'agile', 'scrum', 'safe', 'stakeholder management',
                'cross-functional', 'go-to-market', 'gtm', 'user research', 'user experience',
                'ux', 'ui', 'design thinking', 'customer journey', 'market research',
                'competitive analysis', 'pricing strategy', 'monetization'
            ],
            'ai_ml': [
                'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
                'neural networks', 'rag', 'retrieval augmented generation', 'llm',
                'large language models', 'nlp', 'natural language processing',
                'computer vision', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas',
                'numpy', 'jupyter', 'python', 'r', 'prompt engineering', 'fine-tuning',
                'model training', 'data science', 'predictive modeling', 'algorithms',
                'vector database', 'embedding', 'transformer', 'gpt', 'bert',
                'automation', 'intelligent automation', 'ml ops', 'model deployment'
            ],
            'technical': [
                'salesforce', 'sap', 'mulesoft', 'api', 'rest api', 'graphql',
                'sql', 'database', 'postgresql', 'mysql', 'mongodb', 'redis',
                'aws', 'azure', 'gcp', 'cloud', 'microservices', 'docker',
                'kubernetes', 'ci/cd', 'devops', 'git', 'jira', 'confluence',
                'tableau', 'power bi', 'analytics', 'google analytics',
                'javascript', 'react', 'angular', 'node.js', 'html', 'css',
                'json', 'xml', 'integration', 'workflow automation'
            ],
            'business': [
                'revenue growth', 'kpi', 'metrics', 'analytics', 'roi', 'conversion',
                'retention', 'churn', 'ltv', 'customer acquisition', 'cac',
                'b2b', 'b2c', 'saas', 'enterprise', 'startup', 'scale-up',
                'growth hacking', 'lean startup', 'mvp', 'a/b testing',
                'funnel optimization', 'cohort analysis', 'data-driven'
            ]
        }
        
        # Experience level indicators
        self.seniority_keywords = {
            'senior': ['senior', 'sr', 'lead', 'principal', 'staff', 'head of'],
            'mid': ['product manager', 'pm', '3-5 years', '4-6 years', '5+ years'],
            'junior': ['junior', 'jr', 'associate', 'entry level', '1-3 years', '0-2 years']
        }
        
    def parse(self, job_description: str) -> Dict:
        """
        Parse job description and extract key information
        
        Args:
            job_description: Full job description text
            
        Returns:
            Dictionary containing parsed information
        """
        jd_lower = job_description.lower()
        
        return {
            'company': self._extract_company(job_description),
            'role_title': self._extract_role_title(job_description),
            'location': self._extract_location(job_description),
            'seniority_level': self._extract_seniority(jd_lower),
            'required_skills': self._extract_skills(jd_lower, 'required'),
            'preferred_skills': self._extract_skills(jd_lower, 'preferred'),
            'ai_ml_focus': self._assess_ai_ml_focus(jd_lower),
            'b2b_vs_b2c': self._assess_business_model(jd_lower),
            'matched_skills': [],  # Will be populated by resume generator
            'missing_skills': [],  # Will be populated by resume generator
            'mapped_skills': [],   # Will be populated by resume generator
            'ats_match_score': 0,  # Will be calculated by resume generator
            'raw_text': job_description
        }
    
    def _extract_company(self, jd: str) -> str:
        """Extract company name from job description"""
        # Look for common patterns
        patterns = [
            r'(?i)(?:company|organization|at)\s+([A-Z][a-zA-Z\s&.]{2,30})',
            r'(?i)join\s+([A-Z][a-zA-Z\s&.]{2,30})',
            r'(?i)([A-Z][a-zA-Z\s&.]{2,30})\s+is\s+(?:looking|seeking|hiring)',
            r'(?i)about\s+([A-Z][a-zA-Z\s&.]{2,30})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, jd)
            if match:
                company = match.group(1).strip()
                # Clean up common false positives
                if len(company) > 3 and company.lower() not in ['the company', 'our company', 'this role']:
                    return company
        
        return "Company"  # Default fallback
    
    def _extract_role_title(self, jd: str) -> str:
        """Extract role title from job description"""
        # Look for common role title patterns
        patterns = [
            r'(?i)(?:role|position|job title):\s*([^\n\r]{5,50})',
            r'(?i)^([^\n\r]*product manager[^\n\r]*)',
            r'(?i)we\'re looking for a\s+([^\n\r]{5,50})',
            r'(?i)seeking a\s+([^\n\r]{5,50})',
            r'(?i)hiring a\s+([^\n\r]{5,50})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, jd, re.MULTILINE)
            if match:
                title = match.group(1).strip()
                if 5 <= len(title) <= 50:
                    return title
        
        return "Product Manager"  # Default fallback
    
    def _extract_location(self, jd: str) -> str:
        """Extract location from job description"""
        # Look for location patterns
        patterns = [
            r'(?i)location:?\s*([A-Za-z\s,.-]{3,40})',
            r'(?i)based in\s+([A-Za-z\s,.-]{3,40})',
            r'(?i)office in\s+([A-Za-z\s,.-]{3,40})',
            r'(?i)(Amsterdam|Rotterdam|Netherlands|Finland|Helsinki|Ireland|Dublin|Sweden|Stockholm|Denmark|Copenhagen|Portugal|Lisbon)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, jd)
            if match:
                location = match.group(1).strip()
                if len(location) > 2:
                    return location
        
        return "Remote"  # Default fallback
    
    def _extract_seniority(self, jd_lower: str) -> str:
        """Determine seniority level from job description"""
        for level, keywords in self.seniority_keywords.items():
            for keyword in keywords:
                if keyword in jd_lower:
                    return level
        return "mid"  # Default to mid-level
    
    def _extract_skills(self, jd_lower: str, skill_type: str = 'all') -> List[str]:
        """Extract required or preferred skills from job description"""
        all_skills = []
        
        # Find skills from all categories
        for category, keywords in self.pm_keywords.items():
            for keyword in keywords:
                if keyword in jd_lower:
                    all_skills.append(keyword)
        
        # Look for skills in specific sections
        if 'requirements:' in jd_lower or 'required:' in jd_lower:
            req_section = self._extract_section(jd_lower, ['requirements:', 'required:'])
            if skill_type == 'required' or skill_type == 'all':
                all_skills.extend(self._extract_skills_from_section(req_section))
        
        if 'preferred:' in jd_lower or 'nice to have:' in jd_lower:
            pref_section = self._extract_section(jd_lower, ['preferred:', 'nice to have:', 'bonus:'])
            if skill_type == 'preferred' or skill_type == 'all':
                all_skills.extend(self._extract_skills_from_section(pref_section))
        
        # Remove duplicates and return
        return list(set(all_skills))
    
    def _extract_section(self, text: str, headers: List[str]) -> str:
        """Extract text section starting with given headers"""
        for header in headers:
            pattern = rf'{re.escape(header)}(.*?)(?=\n\s*[A-Z][a-z]+:|$)'
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_skills_from_section(self, section: str) -> List[str]:
        """Extract skills from a specific section of text"""
        skills = []
        
        # Look for bullet points or numbered lists
        lines = section.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*', '·')) or re.match(r'^\d+\.', line):
                # This is likely a skill/requirement line
                line_lower = line.lower()
                for category, keywords in self.pm_keywords.items():
                    for keyword in keywords:
                        if keyword in line_lower:
                            skills.append(keyword)
        
        return skills
    
    def _assess_ai_ml_focus(self, jd_lower: str) -> float:
        """Assess how AI/ML focused the role is (0.0 to 1.0)"""
        ai_ml_mentions = 0
        total_mentions = 0
        
        for keyword in self.pm_keywords['ai_ml']:
            count = jd_lower.count(keyword)
            ai_ml_mentions += count
            
        for category, keywords in self.pm_keywords.items():
            for keyword in keywords:
                total_mentions += jd_lower.count(keyword)
        
        return ai_ml_mentions / max(total_mentions, 1)
    
    def _assess_business_model(self, jd_lower: str) -> str:
        """Determine if role is more B2B or B2C focused"""
        b2b_indicators = ['b2b', 'enterprise', 'business customers', 'corporate', 'saas', 'salesforce', 'sap']
        b2c_indicators = ['b2c', 'consumer', 'mobile app', 'user engagement', 'end user', 'customer facing']
        
        b2b_score = sum(1 for indicator in b2b_indicators if indicator in jd_lower)
        b2c_score = sum(1 for indicator in b2c_indicators if indicator in jd_lower)
        
        if b2b_score > b2c_score:
            return 'b2b'
        elif b2c_score > b2b_score:
            return 'b2c'
        else:
            return 'mixed'