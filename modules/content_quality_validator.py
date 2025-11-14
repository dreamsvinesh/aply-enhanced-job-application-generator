"""
Content Quality Validator Agent
Validates generated content for accuracy, completeness, and professional standards
"""

import re
import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ContentIssue:
    """Represents a content quality issue"""
    severity: str  # 'critical', 'major', 'minor'
    category: str
    location: str
    description: str
    fix_suggestion: str
    detected_value: Optional[str] = None

@dataclass
class ContentValidationResult:
    """Content validation result"""
    should_regenerate: bool
    decision: str  # 'APPROVE', 'APPROVE_WITH_WARNINGS', 'REGENERATE'
    issues: List[ContentIssue]
    scores: Dict[str, float]
    summary: str

class ContentQualityValidator:
    """
    Validates generated content for accuracy and professional standards
    
    Activation: AFTER content generation, BEFORE final packaging
    Purpose: Ensure factual accuracy and professional quality
    """
    
    def __init__(self):
        self.factual_checks = {
            'placeholder_text': self._check_placeholder_text,
            'factual_accuracy': self._check_factual_accuracy,
            'domain_consistency': self._check_domain_consistency,
            'content_completeness': self._check_content_completeness,
            'professional_standards': self._check_professional_standards,
            'human_writing_quality': self._check_human_writing_quality
        }
        
        # LLM-generated language patterns to avoid
        self.llm_red_flags = {
            'overused_phrases': [
                'leverage', 'utilize', 'spearhead', 'orchestrate', 'champion',
                'drive results', 'synergize', 'optimize', 'streamline', 'facilitate',
                'enhance operational efficiency', 'deliver exceptional results',
                'passionate about', 'excited to contribute', 'thrilled to',
                'dynamic environment', 'fast-paced environment', 'cutting-edge',
                'innovative solutions', 'best practices', 'thought leadership',
                'paradigm shift', 'game-changing', 'revolutionary', 'transformative',
                'end-to-end solutions', 'holistic approach', 'strategic initiatives',
                'cross-functional collaboration', 'stakeholder alignment'
            ],
            'ai_sentence_starters': [
                'As a seasoned', 'With extensive experience in', 'Throughout my career',
                'I am passionate about', 'I am excited to bring', 'I would love to',
                'I am confident that', 'Given my background in', 'Having worked in'
            ],
            'robotic_transitions': [
                'Furthermore,', 'Moreover,', 'Additionally,', 'Subsequently,',
                'Consequently,', 'In addition to this,', 'Building upon'
            ],
            'perfect_grammar_flags': [
                'whom', 'shall', 'whilst', 'endeavor', 'endeavour',
                'commence', 'terminate', 'subsequent to', 'prior to',
                'in order to', 'with regard to', 'in relation to'
            ]
        }
    
    def validate_generated_content(self, content_dict: Dict, user_profile: Dict, jd_data: Dict) -> ContentValidationResult:
        """
        Comprehensive content validation
        
        Args:
            content_dict: Generated content (resume, cover_letter, etc.)
            user_profile: Original user profile data
            jd_data: Job description data
            
        Returns:
            ContentValidationResult with decision and issues
        """
        all_issues = []
        
        # Run all validation checks
        for check_name, check_function in self.factual_checks.items():
            issues = check_function(content_dict, user_profile, jd_data)
            all_issues.extend(issues)
        
        # Calculate scores
        scores = self._calculate_quality_scores(all_issues)
        
        # Determine decision
        critical_issues = [i for i in all_issues if i.severity == 'critical']
        major_issues = [i for i in all_issues if i.severity == 'major']
        
        if len(critical_issues) >= 3:
            decision = 'REGENERATE'
            should_regenerate = True
            summary = f"Critical issues require regeneration: {len(critical_issues)} critical issues found"
        elif len(critical_issues) >= 1 or len(major_issues) >= 5:
            decision = 'APPROVE_WITH_WARNINGS'
            should_regenerate = False
            summary = f"Content approved with warnings: {len(critical_issues)} critical, {len(major_issues)} major issues"
        else:
            decision = 'APPROVE'
            should_regenerate = False
            summary = f"Content approved: {len(all_issues)} minor issues found"
        
        return ContentValidationResult(
            should_regenerate=should_regenerate,
            decision=decision,
            issues=all_issues,
            scores=scores,
            summary=summary
        )
    
    def _check_placeholder_text(self, content_dict: Dict, user_profile: Dict, jd_data: Dict) -> List[ContentIssue]:
        """Check for placeholder text that wasn't replaced"""
        issues = []
        
        # Common placeholder patterns
        placeholder_patterns = [
            r'\[.*?\]',  # [Your Name], [Company]
            r'\{.*?\}',  # {name}, {company}
            r'YOUR_.*',  # YOUR_NAME
            r'COMPANY_NAME',
            r'ROLE_TITLE',
            r'\.\.\.',  # Ellipsis placeholders
            r'TODO',
            r'PLACEHOLDER',
            r'INSERT_.*'
        ]
        
        for content_type, content in content_dict.items():
            if content_type == 'resume':
                # Handle resume dict structure
                resume_text = self._extract_resume_text(content)
                content_to_check = resume_text
            else:
                content_to_check = str(content)
            
            for pattern in placeholder_patterns:
                matches = re.findall(pattern, content_to_check, re.IGNORECASE)
                if matches:
                    for match in matches:
                        issues.append(ContentIssue(
                            severity='critical',
                            category='placeholder_text',
                            location=content_type,
                            description=f'Placeholder text found: {match}',
                            fix_suggestion='Replace placeholder with actual content',
                            detected_value=match
                        ))
        
        return issues
    
    def _check_factual_accuracy(self, content_dict: Dict, user_profile: Dict, jd_data: Dict) -> List[ContentIssue]:
        """Check if facts match the user profile exactly"""
        issues = []
        
        # Extract profile facts
        profile_name = user_profile.get('personal_info', {}).get('name', '')
        profile_title = user_profile.get('personal_info', {}).get('title', '')
        profile_achievements = user_profile.get('key_achievements', [])
        profile_projects = user_profile.get('projects', {})
        
        # Check name consistency
        for content_type, content in content_dict.items():
            if content_type == 'resume':
                resume_text = self._extract_resume_text(content)
                content_text = resume_text
            else:
                content_text = str(content)
            
            # Check if name appears correctly (if it appears at all)
            if profile_name and profile_name.upper() in content_text.upper():
                # Name found - check if it's formatted correctly
                name_variants = [
                    profile_name,
                    profile_name.upper(),
                    profile_name.lower(),
                    profile_name.title()
                ]
                
                correct_format_found = any(variant in content_text for variant in name_variants)
                if not correct_format_found:
                    issues.append(ContentIssue(
                        severity='major',
                        category='factual_accuracy',
                        location=content_type,
                        description=f'Name format inconsistency detected',
                        fix_suggestion=f'Ensure name appears as: {profile_name}'
                    ))
        
        # Check for invented metrics not in profile
        profile_metrics = self._extract_profile_metrics(user_profile)
        
        for content_type, content in content_dict.items():
            if content_type == 'resume':
                content_text = self._extract_resume_text(content)
            else:
                content_text = str(content)
            
            # Find all metrics in generated content
            metric_patterns = [
                r'(\d+(?:\.\d+)?%)',  # Percentages
                r'(\$\d+(?:[KMB]|\d+)?)',  # Dollar amounts
                r'(\d+[KMB](?:\+)?)',  # Numbers with K/M/B
                r'(\d+\+)',  # Numbers with +
                r'(\d+(?:\.\d+)?\s*(?:days?|hours?|minutes?))',  # Time periods
            ]
            
            found_metrics = []
            for pattern in metric_patterns:
                found_metrics.extend(re.findall(pattern, content_text, re.IGNORECASE))
            
            # Check if metrics exist in profile
            for metric in found_metrics:
                metric_clean = re.sub(r'[^\d.]', '', metric)
                if metric_clean and not any(metric_clean in str(pm) for pm in profile_metrics):
                    # Check if it's a reasonable variation (within 10% of profile metric)
                    if not self._is_reasonable_variation(metric, profile_metrics):
                        issues.append(ContentIssue(
                            severity='major',
                            category='factual_accuracy',
                            location=content_type,
                            description=f'Potentially invented metric: {metric}',
                            fix_suggestion='Verify metric exists in profile or remove if uncertain',
                            detected_value=metric
                        ))
        
        return issues
    
    def _check_domain_consistency(self, content_dict: Dict, user_profile: Dict, jd_data: Dict) -> List[ContentIssue]:
        """Check if content focuses on the right domain for the job"""
        issues = []
        
        job_domain = jd_data.get('domain', '').lower()
        job_skills = [skill.lower() for skill in jd_data.get('required_skills', [])]
        
        # Define domain-specific keywords that should be prominent
        domain_keywords = {
            'ai': ['ai', 'ml', 'machine learning', 'rag', 'llm', 'artificial intelligence', 'vector'],
            'fintech': ['fintech', 'financial', 'payment', 'banking', 'compliance', 'regulatory'],
            'saas': ['saas', 'platform', 'api', 'cloud', 'software'],
            'enterprise': ['enterprise', 'b2b', 'salesforce', 'sap', 'integration', 'automation']
        }
        
        relevant_keywords = []
        for domain, keywords in domain_keywords.items():
            if domain in job_domain or any(kw in job_skills for kw in keywords):
                relevant_keywords.extend(keywords)
        
        if relevant_keywords:
            # Check if resume emphasizes relevant domain
            resume_content = content_dict.get('resume', {})
            resume_text = self._extract_resume_text(resume_content).lower()
            
            keyword_count = sum(1 for kw in relevant_keywords if kw in resume_text)
            if keyword_count < 3:
                issues.append(ContentIssue(
                    severity='major',
                    category='domain_consistency',
                    location='resume',
                    description=f'Insufficient domain focus for {job_domain} role',
                    fix_suggestion=f'Emphasize {job_domain} experience and relevant keywords'
                ))
        
        return issues
    
    def _check_content_completeness(self, content_dict: Dict, user_profile: Dict, jd_data: Dict) -> List[ContentIssue]:
        """Check if all required content sections are present and populated"""
        issues = []
        
        # Check resume completeness
        resume = content_dict.get('resume', {})
        required_resume_sections = ['summary', 'experience', 'skills']
        
        for section in required_resume_sections:
            if section not in resume or not resume[section]:
                issues.append(ContentIssue(
                    severity='critical',
                    category='content_completeness',
                    location='resume',
                    description=f'Missing or empty resume section: {section}',
                    fix_suggestion=f'Ensure {section} section is properly populated'
                ))
        
        # Check cover letter completeness
        cover_letter = content_dict.get('cover_letter', '')
        if not cover_letter or len(cover_letter.strip()) < 100:
            issues.append(ContentIssue(
                severity='critical',
                category='content_completeness',
                location='cover_letter',
                description='Cover letter too short or missing',
                fix_suggestion='Generate adequate cover letter content (150+ words)'
            ))
        
        # Check if company name appears in cover letter when provided
        company_name = jd_data.get('company', '')
        if company_name and company_name.lower() not in cover_letter.lower():
            issues.append(ContentIssue(
                severity='major',
                category='content_completeness',
                location='cover_letter',
                description=f'Company name "{company_name}" not mentioned in cover letter',
                fix_suggestion='Personalize cover letter with specific company name'
            ))
        
        return issues
    
    def _check_professional_standards(self, content_dict: Dict, user_profile: Dict, jd_data: Dict) -> List[ContentIssue]:
        """Check for professional writing standards (objective criteria only)"""
        issues = []
        
        # Check for quantified achievements
        resume = content_dict.get('resume', {})
        resume_text = self._extract_resume_text(resume)
        
        # Count quantified achievements
        metrics_pattern = r'\d+(?:\.\d+)?(?:%|\$|[KMB]|\+|(?:\s*(?:days?|hours?|minutes?|years?)))'
        metrics_count = len(re.findall(metrics_pattern, resume_text))
        
        if metrics_count < 5:
            issues.append(ContentIssue(
                severity='minor',
                category='professional_standards',
                location='resume',
                description=f'Low quantified achievements: {metrics_count} found',
                fix_suggestion='Include more specific metrics and numbers'
            ))
        
        # Check for action verbs in experience
        experience = resume.get('experience', [])
        if experience:
            first_role_highlights = experience[0].get('highlights', [])
            action_verbs = ['built', 'led', 'managed', 'developed', 'implemented', 'achieved', 
                          'delivered', 'increased', 'reduced', 'optimized', 'created']
            
            action_verb_count = 0
            for highlight in first_role_highlights:
                if any(verb in highlight.lower() for verb in action_verbs):
                    action_verb_count += 1
            
            if action_verb_count < len(first_role_highlights) * 0.7:
                issues.append(ContentIssue(
                    severity='minor',
                    category='professional_standards',
                    location='resume',
                    description='Limited use of strong action verbs',
                    fix_suggestion='Start bullet points with strong action verbs'
                ))
        
        return issues
    
    def _check_human_writing_quality(self, content_dict: Dict, user_profile: Dict, jd_data: Dict) -> List[ContentIssue]:
        """Check for human-like writing and flag LLM-generated patterns"""
        issues = []
        
        for content_type, content in content_dict.items():
            if content_type == 'resume':
                content_text = self._extract_resume_text(content)
            else:
                content_text = str(content)
            
            content_lower = content_text.lower()
            
            # Check for overused corporate jargon
            jargon_count = 0
            found_jargon = []
            for phrase in self.llm_red_flags['overused_phrases']:
                if phrase.lower() in content_lower:
                    jargon_count += 1
                    found_jargon.append(phrase)
            
            if jargon_count >= 3:
                issues.append(ContentIssue(
                    severity='major',
                    category='human_writing_quality',
                    location=content_type,
                    description=f'Overused corporate jargon: {jargon_count} instances found',
                    fix_suggestion='Replace corporate buzzwords with direct, specific language',
                    detected_value=', '.join(found_jargon[:3])
                ))
            
            # Check for AI sentence starters
            ai_starters_found = []
            for starter in self.llm_red_flags['ai_sentence_starters']:
                if starter.lower() in content_lower:
                    ai_starters_found.append(starter)
            
            if len(ai_starters_found) >= 2:
                issues.append(ContentIssue(
                    severity='major',
                    category='human_writing_quality',
                    location=content_type,
                    description=f'AI-generated sentence patterns detected: {len(ai_starters_found)} instances',
                    fix_suggestion='Use more natural, conversational sentence openings',
                    detected_value=', '.join(ai_starters_found[:2])
                ))
            
            # Check for robotic transitions
            robotic_transitions_found = []
            for transition in self.llm_red_flags['robotic_transitions']:
                if transition.lower() in content_lower:
                    robotic_transitions_found.append(transition)
            
            if len(robotic_transitions_found) >= 2:
                issues.append(ContentIssue(
                    severity='minor',
                    category='human_writing_quality',
                    location=content_type,
                    description=f'Overly formal transitions: {len(robotic_transitions_found)} instances',
                    fix_suggestion='Use simpler, more natural connecting words',
                    detected_value=', '.join(robotic_transitions_found)
                ))
            
            # Check for perfect grammar that sounds unnatural
            perfect_grammar_found = []
            for word in self.llm_red_flags['perfect_grammar_flags']:
                if word.lower() in content_lower:
                    perfect_grammar_found.append(word)
            
            if len(perfect_grammar_found) >= 2:
                issues.append(ContentIssue(
                    severity='minor',
                    category='human_writing_quality',
                    location=content_type,
                    description=f'Overly formal/perfect grammar: {len(perfect_grammar_found)} instances',
                    fix_suggestion='Use more casual, conversational language',
                    detected_value=', '.join(perfect_grammar_found)
                ))
            
            # Check for repetitive sentence structure (all sentences same length)
            sentences = [s.strip() for s in content_text.replace('.', '.|').split('|') if s.strip()]
            if len(sentences) >= 4:
                sentence_lengths = [len(s.split()) for s in sentences]
                avg_length = sum(sentence_lengths) / len(sentence_lengths)
                
                # Check if all sentences are very similar length (indicates AI generation)
                length_variance = sum((length - avg_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
                if length_variance < 5:  # Very low variance = robotic
                    issues.append(ContentIssue(
                        severity='minor',
                        category='human_writing_quality',
                        location=content_type,
                        description='Repetitive sentence structure detected',
                        fix_suggestion='Vary sentence lengths for more natural flow',
                        detected_value=f'Avg length: {avg_length:.1f} words'
                    ))
            
            # Check for human-friendly patterns (positive indicators)
            human_indicators = [
                'I built', 'I led', 'I worked', 'I created', 'I helped',
                'my team', 'we developed', 'we launched', 'our goal',
                'actually', 'really', 'pretty', 'quite', 'very'
            ]
            
            human_score = sum(1 for indicator in human_indicators if indicator.lower() in content_lower)
            total_words = len(content_text.split())
            human_ratio = human_score / max(total_words / 50, 1)  # Per 50 words
            
            if human_ratio < 0.5 and total_words > 100:
                issues.append(ContentIssue(
                    severity='minor',
                    category='human_writing_quality',
                    location=content_type,
                    description='Content sounds too formal/robotic',
                    fix_suggestion='Add more personal pronouns and conversational language',
                    detected_value=f'Human-friendly ratio: {human_ratio:.1f}'
                ))
        
        return issues
    
    def _extract_resume_text(self, resume_content: Any) -> str:
        """Extract all text from resume content"""
        if isinstance(resume_content, str):
            return resume_content
        
        if isinstance(resume_content, dict):
            text_parts = []
            
            # Extract from common resume fields
            if 'summary' in resume_content:
                text_parts.append(str(resume_content['summary']))
            
            if 'experience' in resume_content:
                for exp in resume_content['experience']:
                    if isinstance(exp, dict):
                        text_parts.append(exp.get('title', ''))
                        text_parts.append(exp.get('company', ''))
                        if 'highlights' in exp:
                            text_parts.extend(exp['highlights'])
            
            if 'skills' in resume_content:
                if isinstance(resume_content['skills'], dict):
                    for skill_cat in resume_content['skills'].values():
                        if isinstance(skill_cat, list):
                            text_parts.extend(skill_cat)
                else:
                    text_parts.append(str(resume_content['skills']))
            
            return ' '.join(str(part) for part in text_parts)
        
        return str(resume_content)
    
    def _extract_profile_metrics(self, user_profile: Dict) -> List[str]:
        """Extract all metrics from user profile for comparison"""
        metrics = []
        
        # From achievements
        achievements = user_profile.get('key_achievements', [])
        for achievement in achievements:
            metric_matches = re.findall(r'\d+(?:\.\d+)?(?:%|\$|[KMB]|\+)', str(achievement))
            metrics.extend(metric_matches)
        
        # From projects
        projects = user_profile.get('projects', {})
        for project in projects.values():
            if isinstance(project, dict) and 'metrics' in project:
                metrics.append(str(project['metrics']))
        
        return metrics
    
    def _is_reasonable_variation(self, metric: str, profile_metrics: List[str]) -> bool:
        """Check if a metric is a reasonable variation of a profile metric"""
        try:
            metric_num = float(re.sub(r'[^\d.]', '', metric))
            for profile_metric in profile_metrics:
                profile_num = float(re.sub(r'[^\d.]', '', str(profile_metric)))
                if abs(metric_num - profile_num) / max(profile_num, 1) < 0.1:  # Within 10%
                    return True
        except (ValueError, ZeroDivisionError):
            pass
        return False
    
    def _calculate_quality_scores(self, issues: List[ContentIssue]) -> Dict[str, float]:
        """Calculate quality scores based on issues found"""
        critical_count = sum(1 for issue in issues if issue.severity == 'critical')
        major_count = sum(1 for issue in issues if issue.severity == 'major')
        minor_count = sum(1 for issue in issues if issue.severity == 'minor')
        
        # Count human writing issues specifically
        human_writing_issues = [issue for issue in issues if issue.category == 'human_writing_quality']
        human_critical = sum(1 for issue in human_writing_issues if issue.severity == 'critical')
        human_major = sum(1 for issue in human_writing_issues if issue.severity == 'major')
        human_minor = sum(1 for issue in human_writing_issues if issue.severity == 'minor')
        
        # Calculate scores (100 = perfect)
        factual_score = max(0, 100 - (critical_count * 30) - (major_count * 15) - (minor_count * 5))
        completeness_score = max(0, 100 - (critical_count * 25) - (major_count * 10) - (minor_count * 3))
        professional_score = max(0, 100 - (critical_count * 20) - (major_count * 8) - (minor_count * 4))
        
        # Human writing quality score (new)
        human_writing_score = max(0, 100 - (human_critical * 25) - (human_major * 12) - (human_minor * 6))
        
        overall_score = (factual_score + completeness_score + professional_score + human_writing_score) / 4
        
        return {
            'factual_accuracy_score': factual_score,
            'content_completeness_score': completeness_score,
            'professional_standards_score': professional_score,
            'human_writing_score': human_writing_score,
            'overall_content_score': overall_score
        }
    
    def print_validation_report(self, result: ContentValidationResult) -> None:
        """Print formatted validation report"""
        print(f"\n🔍 CONTENT QUALITY VALIDATION")
        print("=" * 50)
        
        # Decision
        decision_icons = {
            'APPROVE': '✅',
            'APPROVE_WITH_WARNINGS': '⚠️',
            'REGENERATE': '🔄'
        }
        
        icon = decision_icons.get(result.decision, '❓')
        print(f"{icon} Decision: {result.decision}")
        print(f"📊 Overall Score: {result.scores['overall_content_score']:.1f}/100")
        print(f"📋 {result.summary}")
        
        # Score breakdown
        print(f"\n📊 Quality Scores:")
        print(f"   🎯 Factual Accuracy: {result.scores['factual_accuracy_score']:.1f}/100")
        print(f"   📝 Completeness: {result.scores['content_completeness_score']:.1f}/100")
        print(f"   👔 Professional Standards: {result.scores['professional_standards_score']:.1f}/100")
        print(f"   🤖 Human Writing Quality: {result.scores['human_writing_score']:.1f}/100")
        
        # Issues
        if result.issues:
            print(f"\n📋 Issues found: {len(result.issues)}")
            
            critical = [i for i in result.issues if i.severity == 'critical']
            major = [i for i in result.issues if i.severity == 'major']
            minor = [i for i in result.issues if i.severity == 'minor']
            
            if critical:
                print(f"   🚨 Critical: {len(critical)}")
                for issue in critical[:3]:  # Show top 3
                    print(f"      • {issue.description} ({issue.location})")
            
            if major:
                print(f"   ⚠️ Major: {len(major)}")
                for issue in major[:3]:  # Show top 3
                    print(f"      • {issue.description} ({issue.location})")
            
            if minor:
                print(f"   ℹ️ Minor: {len(minor)}")
        else:
            print("✅ No issues detected")
        
        print("=" * 50)

# Export the validator
__all__ = ['ContentQualityValidator', 'ContentValidationResult', 'ContentIssue']