#!/usr/bin/env python3
"""
Content Quality Validator
Validates generated content for quality, word count, and natural writing style.
"""

import re
from typing import Dict, List, Any

class ContentQualityValidator:
    """Validates content quality, length, and natural writing style"""
    
    def __init__(self):
        # Word count targets per content type and experience level
        self.word_count_targets = {
            'resume': {
                'summary': {'min': 80, 'max': 120},
                'experience_per_role': {
                    'senior_pm': {'min': 100, 'max': 150, 'bullets': {'min': 5, 'max': 5}},  # Senior PM: exactly 5 bullets
                    'pm': {'min': 60, 'max': 100, 'bullets': {'min': 3, 'max': 5}},          # PM: 3-5 bullets  
                    'engineer': {'min': 30, 'max': 50, 'bullets': {'min': 1, 'max': 2}}     # Engineer: 1-2 bullets
                },
                'total_experience': {'min': 190, 'max': 300}  # 150+100+50 = 300 max total
            },
            'cover_letter': {'min': 250, 'max': 400},
            'email': {'min': 150, 'max': 250},
            'linkedin_connection': {'min': 50, 'max': 150},
            'linkedin_message': {'min': 100, 'max': 200}
        }
        
        # LLM detection patterns
        self.llm_red_flags = [
            r'\b(delve|delving)\b',
            r'\bmultifaceted\b', 
            r'\bfurthermore\b',
            r'\bmoreover\b',
            r'\bin conclusion\b',
            r'\besteemed organization\b',
            r'\bvaluable addition\b',
            r'\bproven track record\b',
            r'\bseamlessly\b',
            r'\brobust\b',
            r'\bcomprehensive\b',
            r'\bleverag(e|ing)\b',
            r'\butiliz(e|ing)\b'
        ]
    
    def validate_content_quality(self, content: str, content_type: str) -> Dict[str, Any]:
        """Comprehensive content quality validation"""
        
        issues = []
        suggestions = []
        word_count = len(content.split())
        
        # 1. Word count validation
        word_issues = self._validate_word_count(content, content_type, word_count)
        issues.extend(word_issues)
        
        # 2. LLM language detection
        llm_issues = self._detect_llm_language(content)
        issues.extend(llm_issues)
        
        # 3. Quality indicators
        quality_suggestions = self._assess_content_quality(content)
        suggestions.extend(quality_suggestions)
        
        return {
            'is_valid': len(issues) == 0,
            'score': self._calculate_score(content, len(issues)),
            'issues': issues,
            'suggestions': suggestions,
            'word_count': word_count,
            'target_range': self.word_count_targets.get(content_type, {})
        }
    
    def validate_experience_section(self, experience_text: str, role_title: str, role_level: str = 'pm') -> Dict[str, Any]:
        """Validate specific experience section for appropriate length and content based on role level"""
        
        lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
        bullet_points = [line for line in lines if line.startswith('•') or line.startswith('-')]
        
        word_count = len(experience_text.split())
        issues = []
        suggestions = []
        
        # Get role-specific targets
        role_targets = self.word_count_targets['resume']['experience_per_role'].get(role_level, 
                       self.word_count_targets['resume']['experience_per_role']['pm'])
        
        # Word count validation
        if word_count < role_targets['min']:
            issues.append(f"{role_level.upper()} experience too short: {word_count} words (min: {role_targets['min']})")
            suggestions.append("Add more specific achievements and metrics")
        elif word_count > role_targets['max']:
            issues.append(f"{role_level.upper()} experience too long: {word_count} words (max: {role_targets['max']})")
            suggestions.append("Condense to most impactful achievements")
        
        # Bullet point validation based on role level
        bullet_targets = role_targets['bullets']
        if len(bullet_points) < bullet_targets['min']:
            issues.append(f"Too few achievements: {len(bullet_points)} bullets (required: {bullet_targets['min']}-{bullet_targets['max']} for {role_level.upper()})")
        elif len(bullet_points) > bullet_targets['max']:
            issues.append(f"Too many achievements: {len(bullet_points)} bullets (max: {bullet_targets['max']} for {role_level.upper()})")
        
        return {
            'role_level': role_level,
            'word_count': word_count,
            'word_target': f"{role_targets['min']}-{role_targets['max']}",
            'bullet_count': len(bullet_points),
            'bullet_target': f"{bullet_targets['min']}-{bullet_targets['max']}",
            'issues': issues,
            'suggestions': suggestions,
            'is_valid': len(issues) == 0
        }
        
    def validate_complete_resume_experience(self, senior_pm_text: str, pm_text: str, engineer_text: str) -> Dict[str, Any]:
        """Validate all experience sections together"""
        
        validations = {
            'senior_pm': self.validate_experience_section(senior_pm_text, 'Senior Product Manager', 'senior_pm'),
            'pm': self.validate_experience_section(pm_text, 'Product Manager', 'pm'), 
            'engineer': self.validate_experience_section(engineer_text, 'Frontend Engineer', 'engineer')
        }
        
        total_words = sum(v['word_count'] for v in validations.values())
        total_target = self.word_count_targets['resume']['total_experience']
        
        all_issues = []
        all_suggestions = []
        
        # Collect all issues
        for role, validation in validations.items():
            all_issues.extend([f"{role}: {issue}" for issue in validation['issues']])
            all_suggestions.extend([f"{role}: {suggestion}" for suggestion in validation['suggestions']])
        
        # Total word count validation
        if total_words < total_target['min']:
            all_issues.append(f"Total experience too short: {total_words} words (min: {total_target['min']})")
        elif total_words > total_target['max']:
            all_issues.append(f"Total experience too long: {total_words} words (max: {total_target['max']})")
        
        return {
            'total_word_count': total_words,
            'total_target': f"{total_target['min']}-{total_target['max']}",
            'role_validations': validations,
            'all_issues': all_issues,
            'all_suggestions': all_suggestions,
            'is_valid': len(all_issues) == 0,
            'summary': {
                'senior_pm': f"{validations['senior_pm']['word_count']} words, {validations['senior_pm']['bullet_count']} bullets",
                'pm': f"{validations['pm']['word_count']} words, {validations['pm']['bullet_count']} bullets", 
                'engineer': f"{validations['engineer']['word_count']} words, {validations['engineer']['bullet_count']} bullets"
            }
        }
    
    def _validate_word_count(self, content: str, content_type: str, word_count: int) -> List[str]:
        """Validate word count against targets"""
        
        if content_type not in self.word_count_targets:
            return []
        
        targets = self.word_count_targets[content_type]
        
        # Handle nested targets (like resume)
        if isinstance(targets, dict) and 'min' not in targets:
            return []
        
        issues = []
        
        if word_count < targets['min']:
            issues.append(f"Content too short: {word_count} words (minimum: {targets['min']})")
        elif word_count > targets['max']:
            issues.append(f"Content too long: {word_count} words (maximum: {targets['max']})")
        
        return issues
    
    def _detect_llm_language(self, content: str) -> List[str]:
        """Detect LLM-generated language patterns"""
        
        detected_patterns = []
        issues = []
        
        for pattern in self.llm_red_flags:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                detected_patterns.extend(matches)
        
        if detected_patterns:
            issues.append(f"LLM language detected: {', '.join(set(detected_patterns))}")
        
        return issues
    
    def _assess_content_quality(self, content: str) -> List[str]:
        """Assess content quality indicators"""
        
        suggestions = []
        
        # Check for specific metrics
        if not re.search(r'\d+%|\d+[xX]|\$\d+[kKmMbB]?|\d+\+', content):
            suggestions.append("Add specific metrics (percentages, dollar amounts, user counts)")
        
        # Check for action verbs
        action_verbs = len(re.findall(r'\b(led|built|created|developed|launched|delivered|achieved|improved|reduced|increased)\b', content, re.IGNORECASE))
        if action_verbs < 2:
            suggestions.append("Use more action verbs to show leadership and initiative")
        
        # Check for business impact
        if not re.search(r'\b(revenue|conversion|efficiency|growth|savings|adoption|retention)\b', content, re.IGNORECASE):
            suggestions.append("Emphasize business impact (revenue, efficiency, growth)")
        
        return suggestions
    
    def _calculate_score(self, content: str, issue_count: int) -> float:
        """Calculate overall quality score (0-10)"""
        
        base_score = 10.0 - (issue_count * 1.5)
        
        # Bonus for quality indicators
        metrics_count = len(re.findall(r'\d+%|\d+[xX]|\$\d+[kKmMbB]?|\d+\+', content))
        action_count = len(re.findall(r'\b(led|built|created|developed|launched|delivered|achieved)\b', content, re.IGNORECASE))
        
        bonus = min(metrics_count * 0.5 + action_count * 0.3, 3.0)
        
        return max(0.0, min(10.0, base_score + bonus))

def main():
    """Demo the content quality validator"""
    
    print("🔍 CONTENT QUALITY VALIDATOR DEMO")
    print("=" * 60)
    
    validator = ContentQualityValidator()
    
    # Test weak content
    weak_content = """Built comprehensive product operations framework from 0→1 for the organization. 
    Implemented OKR system and structured planning cadences to improve delivery. 
    Automated reporting and analytics using various tools."""
    
    print("\n❌ **TESTING WEAK CONTENT:**")
    weak_result = validator.validate_content_quality(weak_content, 'resume')
    print(f"Score: {weak_result['score']:.1f}/10")
    print(f"Word Count: {weak_result['word_count']}")
    print(f"Issues: {len(weak_result['issues'])}")
    for issue in weak_result['issues']:
        print(f"  • {issue}")
    
    # Test strong content  
    strong_content = """Created AI RAG system achieving 94% accuracy, serving 200+ employees in 1,500+ weekly queries. 
    Automated contract activation reducing timeline 99.6% from 42 days to 10 minutes, accelerating $2M revenue recognition. 
    Led automation rollout achieving 100% adoption across 5 departments in 2 weeks."""
    
    print("\n✅ **TESTING STRONG CONTENT:**")
    strong_result = validator.validate_content_quality(strong_content, 'resume')
    print(f"Score: {strong_result['score']:.1f}/10")
    print(f"Word Count: {strong_result['word_count']}")
    print(f"Issues: {len(strong_result['issues'])}")
    
    # Test role-specific experience validation
    print("\n📝 **ROLE-SPECIFIC EXPERIENCE VALIDATION:**")
    
    senior_pm_text = """• Created AI RAG system with pgvector achieving 94% accuracy, serving 200+ employees
• Automated contract activation reducing timeline 99.6% from 42 days to 10 minutes, accelerating $2M revenue
• Led automation rollout achieving 100% adoption across 5 departments in 2 weeks
• Secured CEO approval and $2M investment through ROI presentations and competitive analysis  
• Cut support tickets 75% (500→125 monthly) through intelligent automation and hybrid search"""
    
    pm_text = """• Developed mobile app features increasing engagement 45% across 80+ locations
• Generated €220K monthly revenue through monetizing underutilized inventory  
• Reduced lead conversion time 32% and accelerated onboarding from 110 to 14 days"""
    
    engineer_text = """• Built web applications for 50+ enterprise clients across banking and e-commerce sectors"""
    
    # Test individual validations
    senior_validation = validator.validate_experience_section(senior_pm_text, "Senior Product Manager", "senior_pm")
    pm_validation = validator.validate_experience_section(pm_text, "Product Manager", "pm")
    engineer_validation = validator.validate_experience_section(engineer_text, "Frontend Engineer", "engineer")
    
    print("**SENIOR PM VALIDATION:**")
    print(f"Word Count: {senior_validation['word_count']} (target: {senior_validation['word_target']})")
    print(f"Bullets: {senior_validation['bullet_count']} (target: {senior_validation['bullet_target']})")
    print(f"Valid: {senior_validation['is_valid']}")
    
    print("\n**PM VALIDATION:**")  
    print(f"Word Count: {pm_validation['word_count']} (target: {pm_validation['word_target']})")
    print(f"Bullets: {pm_validation['bullet_count']} (target: {pm_validation['bullet_target']})")
    print(f"Valid: {pm_validation['is_valid']}")
    
    print("\n**ENGINEER VALIDATION:**")
    print(f"Word Count: {engineer_validation['word_count']} (target: {engineer_validation['word_target']})")
    print(f"Bullets: {engineer_validation['bullet_count']} (target: {engineer_validation['bullet_target']})")
    print(f"Valid: {engineer_validation['is_valid']}")
    
    # Test complete resume validation
    print("\n📊 **COMPLETE RESUME VALIDATION:**")
    complete_validation = validator.validate_complete_resume_experience(senior_pm_text, pm_text, engineer_text)
    print(f"Total Words: {complete_validation['total_word_count']} (target: {complete_validation['total_target']})")
    print(f"Overall Valid: {complete_validation['is_valid']}")
    print("Summary:")
    for role, summary in complete_validation['summary'].items():
        print(f"  • {role.replace('_', ' ').title()}: {summary}")

if __name__ == "__main__":
    main()