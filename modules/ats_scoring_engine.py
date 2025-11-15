#!/usr/bin/env python3
"""
ATS Scoring Engine
Analyzes and scores resume content against job descriptions for ATS compatibility.
"""

import re
import json
from typing import Dict, List, Set, Tuple, Any
from collections import Counter
import logging

class ATSScoringEngine:
    """Analyzes resume content against JD for ATS compatibility scoring"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # ATS keyword categories with weights
        self.keyword_weights = {
            'hard_skills': 3.0,        # Technical skills, tools, technologies
            'soft_skills': 1.5,        # Leadership, communication, etc.
            'job_titles': 2.5,         # Role titles and job functions
            'industry_terms': 2.0,     # Domain-specific terminology
            'certifications': 3.5,     # Certifications and qualifications
            'metrics': 4.0,            # Numbers, percentages, achievements
            'action_verbs': 1.0        # Action verbs and accomplishments
        }
        
        # Common ATS-friendly patterns
        self.ats_patterns = {
            'metrics': r'\d+%|\d+[xX]|\$\d+[kKmMbB]?|\d+\+|\d+[-]\d+',
            'years_experience': r'\d+\+?\s*years?',
            'technologies': r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,2}\b',
            'certifications': r'\b(?:certified|certificate|certification)\b',
            'achievements': r'\b(?:achieved|delivered|improved|increased|reduced|saved|generated)\b'
        }
    
    def analyze_jd_keywords(self, jd_text: str) -> Dict[str, Any]:
        """Extract and categorize keywords from job description"""
        
        # Clean and normalize text
        clean_jd = self._clean_text(jd_text)
        
        # Extract different keyword categories
        analysis = {
            'hard_skills': self._extract_hard_skills(clean_jd),
            'soft_skills': self._extract_soft_skills(clean_jd),
            'job_titles': self._extract_job_titles(clean_jd),
            'industry_terms': self._extract_industry_terms(clean_jd),
            'certifications': self._extract_certifications(clean_jd),
            'metrics_patterns': self._extract_metrics_patterns(clean_jd),
            'action_verbs': self._extract_action_verbs(clean_jd),
            'requirements': self._extract_requirements(clean_jd),
            'total_keywords': 0
        }
        
        # Calculate total unique keywords
        all_keywords = set()
        for category in ['hard_skills', 'soft_skills', 'job_titles', 'industry_terms', 'certifications']:
            all_keywords.update(analysis[category])
        analysis['total_keywords'] = len(all_keywords)
        
        return analysis
    
    def score_resume_against_jd(self, resume_text: str, jd_analysis: Dict, jd_text: str) -> Dict[str, Any]:
        """Score resume content against job description for ATS compatibility"""
        
        # Analyze resume content
        resume_analysis = self.analyze_resume_content(resume_text)
        
        # Get JD keywords if not provided
        if 'ats_keywords' not in jd_analysis:
            jd_keywords = self.analyze_jd_keywords(jd_text)
        else:
            jd_keywords = jd_analysis['ats_keywords']
        
        # Calculate category scores
        category_scores = {}
        total_weighted_score = 0
        total_weight = 0
        
        for category in self.keyword_weights:
            jd_keywords_cat = set(jd_keywords.get(category, []))
            resume_keywords_cat = set(resume_analysis.get(category, []))
            
            if jd_keywords_cat:
                # Calculate intersection and score
                matches = jd_keywords_cat.intersection(resume_keywords_cat)
                score = (len(matches) / len(jd_keywords_cat)) * 100
                
                category_scores[category] = {
                    'score': score,
                    'matches': list(matches),
                    'missing': list(jd_keywords_cat - resume_keywords_cat),
                    'jd_keywords': list(jd_keywords_cat),
                    'resume_keywords': list(resume_keywords_cat),
                    'match_count': len(matches),
                    'total_jd_keywords': len(jd_keywords_cat)
                }
                
                # Weight the score
                weight = self.keyword_weights[category]
                total_weighted_score += score * weight
                total_weight += weight
            else:
                category_scores[category] = {
                    'score': 100,  # No keywords required in this category
                    'matches': [],
                    'missing': [],
                    'jd_keywords': [],
                    'resume_keywords': list(resume_analysis.get(category, [])),
                    'match_count': 0,
                    'total_jd_keywords': 0
                }
        
        # Calculate overall ATS score
        overall_ats_score = total_weighted_score / total_weight if total_weight > 0 else 0
        
        # Additional ATS factors
        ats_factors = self._analyze_ats_factors(resume_text, jd_text)
        
        # Generate recommendations
        recommendations = self._generate_ats_recommendations(category_scores, ats_factors)
        
        return {
            'overall_ats_score': round(overall_ats_score, 1),
            'grade': self._get_ats_grade(overall_ats_score),
            'category_scores': category_scores,
            'ats_factors': ats_factors,
            'recommendations': recommendations,
            'summary': {
                'total_matches': sum(cat['match_count'] for cat in category_scores.values()),
                'total_jd_keywords': sum(cat['total_jd_keywords'] for cat in category_scores.values()),
                'keyword_density': self._calculate_keyword_density(resume_text, jd_keywords),
                'readability_score': ats_factors['readability_score']
            }
        }
    
    def analyze_resume_content(self, resume_text: str) -> Dict[str, List[str]]:
        """Analyze resume content and extract categorized keywords"""
        
        clean_resume = self._clean_text(resume_text)
        
        return {
            'hard_skills': self._extract_hard_skills(clean_resume),
            'soft_skills': self._extract_soft_skills(clean_resume),
            'job_titles': self._extract_job_titles(clean_resume),
            'industry_terms': self._extract_industry_terms(clean_resume),
            'certifications': self._extract_certifications(clean_resume),
            'metrics_patterns': self._extract_metrics_patterns(clean_resume),
            'action_verbs': self._extract_action_verbs(clean_resume)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        # Remove special characters but keep spaces and alphanumeric
        cleaned = re.sub(r'[^\w\s\-\+\$%]', ' ', text)
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.lower().strip()
    
    def _extract_hard_skills(self, text: str) -> List[str]:
        """Extract technical skills and tools"""
        hard_skills_patterns = [
            # Programming languages
            r'\b(?:python|javascript|java|typescript|react|angular|vue|node|sql|mongodb|postgresql)\b',
            # Cloud platforms
            r'\b(?:aws|azure|gcp|docker|kubernetes|terraform)\b',
            # Product management tools
            r'\b(?:jira|confluence|figma|sketch|miro|notion|slack|salesforce|hubspot)\b',
            # Analytics tools
            r'\b(?:google analytics|mixpanel|amplitude|tableau|power bi|looker)\b',
            # AI/ML tools
            r'\b(?:machine learning|ai|llm|gpt|openai|tensorflow|pytorch|scikit-learn)\b',
            # Methodologies
            r'\b(?:agile|scrum|kanban|okr|kpi|a/b testing|user research)\b'
        ]
        
        skills = []
        for pattern in hard_skills_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend(matches)
        
        return list(set(skills))
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills and leadership terms"""
        soft_skills_patterns = [
            r'\b(?:leadership|management|communication|collaboration|teamwork)\b',
            r'\b(?:strategic|analytical|problem.solving|decision.making)\b',
            r'\b(?:stakeholder|cross.functional|project.management)\b'
        ]
        
        skills = []
        for pattern in soft_skills_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend(matches)
        
        return list(set(skills))
    
    def _extract_job_titles(self, text: str) -> List[str]:
        """Extract job titles and role functions"""
        job_title_patterns = [
            r'\b(?:product manager|senior product manager|product operations|product ops)\b',
            r'\b(?:program manager|project manager|technical lead|engineering manager)\b',
            r'\b(?:director|vp|head of|chief|founder|co-founder)\b'
        ]
        
        titles = []
        for pattern in job_title_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            titles.extend(matches)
        
        return list(set(titles))
    
    def _extract_industry_terms(self, text: str) -> List[str]:
        """Extract industry-specific terminology"""
        industry_patterns = [
            r'\b(?:saas|b2b|b2c|marketplace|platform|api|automation)\b',
            r'\b(?:go.to.market|customer acquisition|user experience|product.market fit)\b',
            r'\b(?:scalability|optimization|integration|workflow|process)\b'
        ]
        
        terms = []
        for pattern in industry_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms.extend(matches)
        
        return list(set(terms))
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications and qualifications"""
        cert_patterns = [
            r'\b(?:pmp|csm|psm|safe|aws certified|google certified)\b',
            r'\b(?:master|bachelor|mba|phd|degree|certification)\b'
        ]
        
        certs = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certs.extend(matches)
        
        return list(set(certs))
    
    def _extract_metrics_patterns(self, text: str) -> List[str]:
        """Extract metrics and quantifiable achievements"""
        metrics = re.findall(self.ats_patterns['metrics'], text)
        return list(set(metrics))
    
    def _extract_action_verbs(self, text: str) -> List[str]:
        """Extract action verbs and accomplishment terms"""
        action_patterns = [
            r'\b(?:led|managed|developed|created|built|launched|delivered|improved)\b',
            r'\b(?:increased|reduced|achieved|generated|optimized|implemented)\b',
            r'\b(?:drove|established|designed|executed|facilitated|coordinated)\b'
        ]
        
        verbs = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            verbs.extend(matches)
        
        return list(set(verbs))
    
    def _extract_requirements(self, text: str) -> Dict[str, List[str]]:
        """Extract must-have vs nice-to-have requirements"""
        requirements = {
            'must_have': [],
            'nice_to_have': [],
            'years_experience': []
        }
        
        # Find years of experience requirements
        years_matches = re.findall(r'(\d+)\+?\s*years?', text, re.IGNORECASE)
        requirements['years_experience'] = years_matches
        
        # Look for must-have indicators
        must_have_indicators = r'(?:required|must have|essential|mandatory|minimum|needed)'
        nice_have_indicators = r'(?:preferred|nice to have|bonus|plus|desirable|ideal)'
        
        # Extract requirements based on indicators
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            if re.search(must_have_indicators, sentence, re.IGNORECASE):
                requirements['must_have'].append(sentence.strip())
            elif re.search(nice_have_indicators, sentence, re.IGNORECASE):
                requirements['nice_to_have'].append(sentence.strip())
        
        return requirements
    
    def _analyze_ats_factors(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Analyze additional ATS compatibility factors"""
        
        return {
            'readability_score': self._calculate_readability_score(resume_text),
            'formatting_score': self._analyze_formatting(resume_text),
            'length_score': self._analyze_length(resume_text),
            'keyword_stuffing': self._detect_keyword_stuffing(resume_text),
            'section_structure': self._analyze_section_structure(resume_text)
        }
    
    def _calculate_readability_score(self, text: str) -> float:
        """Calculate text readability score"""
        words = len(text.split())
        sentences = len(re.split(r'[.!?]', text))
        avg_words_per_sentence = words / max(sentences, 1)
        
        # Simple readability score (lower is better for ATS)
        if avg_words_per_sentence <= 15:
            return 100
        elif avg_words_per_sentence <= 20:
            return 80
        elif avg_words_per_sentence <= 25:
            return 60
        else:
            return 40
    
    def _analyze_formatting(self, text: str) -> float:
        """Analyze text formatting for ATS compatibility"""
        score = 100
        
        # Check for proper bullet points
        if '•' not in text and '-' not in text:
            score -= 20
        
        # Check for excessive special characters
        special_chars = len(re.findall(r'[^\w\s\-•]', text))
        if special_chars > len(text) * 0.05:  # More than 5% special chars
            score -= 15
        
        return max(0, score)
    
    def _analyze_length(self, text: str) -> float:
        """Analyze resume length appropriateness"""
        word_count = len(text.split())
        
        if 400 <= word_count <= 800:  # Optimal range
            return 100
        elif 300 <= word_count < 400 or 800 < word_count <= 1000:
            return 80
        elif 200 <= word_count < 300 or 1000 < word_count <= 1200:
            return 60
        else:
            return 40
    
    def _detect_keyword_stuffing(self, text: str) -> Dict[str, Any]:
        """Detect potential keyword stuffing"""
        words = text.lower().split()
        word_freq = Counter(words)
        
        total_words = len(words)
        stuffed_words = []
        
        for word, count in word_freq.items():
            if len(word) > 3 and count / total_words > 0.03:  # Word appears more than 3% of the time
                stuffed_words.append({'word': word, 'frequency': count, 'percentage': (count/total_words)*100})
        
        return {
            'is_stuffed': len(stuffed_words) > 0,
            'stuffed_words': stuffed_words,
            'risk_level': 'high' if len(stuffed_words) > 3 else 'medium' if len(stuffed_words) > 1 else 'low'
        }
    
    def _analyze_section_structure(self, text: str) -> Dict[str, Any]:
        """Analyze resume section structure"""
        required_sections = ['experience', 'education', 'skills']
        found_sections = []
        
        for section in required_sections:
            if re.search(section, text, re.IGNORECASE):
                found_sections.append(section)
        
        return {
            'found_sections': found_sections,
            'missing_sections': list(set(required_sections) - set(found_sections)),
            'structure_score': (len(found_sections) / len(required_sections)) * 100
        }
    
    def _calculate_keyword_density(self, resume_text: str, jd_keywords: Dict) -> float:
        """Calculate overall keyword density"""
        resume_words = set(resume_text.lower().split())
        
        all_jd_keywords = set()
        for category_keywords in jd_keywords.values():
            if isinstance(category_keywords, list):
                all_jd_keywords.update([kw.lower() for kw in category_keywords])
        
        if not all_jd_keywords:
            return 0
        
        matches = resume_words.intersection(all_jd_keywords)
        return (len(matches) / len(all_jd_keywords)) * 100
    
    def _get_ats_grade(self, score: float) -> str:
        """Convert ATS score to letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _generate_ats_recommendations(self, category_scores: Dict, ats_factors: Dict) -> List[str]:
        """Generate ATS improvement recommendations"""
        recommendations = []
        
        # Check category scores
        for category, data in category_scores.items():
            if data['score'] < 70 and data['total_jd_keywords'] > 0:
                missing = data['missing'][:3]  # Top 3 missing keywords
                recommendations.append(f"Add {category.replace('_', ' ')} keywords: {', '.join(missing)}")
        
        # Check formatting
        if ats_factors['formatting_score'] < 80:
            recommendations.append("Improve formatting: Use bullet points and avoid excessive special characters")
        
        # Check length
        if ats_factors['length_score'] < 80:
            recommendations.append("Adjust resume length to 400-800 words for optimal ATS scanning")
        
        # Check keyword stuffing
        if ats_factors['keyword_stuffing']['is_stuffed']:
            recommendations.append("Reduce keyword repetition to avoid appearing as keyword stuffing")
        
        # Check structure
        if ats_factors['section_structure']['structure_score'] < 100:
            missing = ats_factors['section_structure']['missing_sections']
            recommendations.append(f"Add missing sections: {', '.join(missing)}")
        
        return recommendations[:5]  # Top 5 recommendations

def main():
    """Demo the ATS scoring engine"""
    
    print("🔍 ATS SCORING ENGINE DEMO")
    print("=" * 60)
    
    engine = ATSScoringEngine()
    
    # Sample JD
    sample_jd = """We are looking for a Senior Product Manager with 5+ years experience in B2B SaaS. 
    Must have experience with agile methodologies, stakeholder management, and data analytics.
    Experience with AI/ML products preferred. Strong leadership and communication skills required."""
    
    # Sample resume  
    sample_resume = """Senior Product Manager with 7 years experience leading B2B SaaS products.
    Expert in agile methodologies and stakeholder management. Led cross-functional teams and delivered
    AI-powered solutions. Strong analytical and communication skills."""
    
    # Analyze JD
    print("📋 **JD KEYWORD ANALYSIS:**")
    jd_analysis = engine.analyze_jd_keywords(sample_jd)
    print(f"Hard Skills: {jd_analysis['hard_skills']}")
    print(f"Soft Skills: {jd_analysis['soft_skills']}")
    print(f"Job Titles: {jd_analysis['job_titles']}")
    print()
    
    # Score resume
    print("📊 **ATS SCORING RESULTS:**")
    ats_score = engine.score_resume_against_jd(sample_resume, {'ats_keywords': jd_analysis}, sample_jd)
    
    print(f"Overall ATS Score: {ats_score['overall_ats_score']}/100 (Grade: {ats_score['grade']})")
    print(f"Total Keyword Matches: {ats_score['summary']['total_matches']}/{ats_score['summary']['total_jd_keywords']}")
    print(f"Keyword Density: {ats_score['summary']['keyword_density']:.1f}%")
    
    print("\n📝 **RECOMMENDATIONS:**")
    for i, rec in enumerate(ats_score['recommendations'], 1):
        print(f"{i}. {rec}")

if __name__ == "__main__":
    main()