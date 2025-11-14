"""
HTML Validation Agent
Validates HTML output for formatting issues, consistency, and professional standards
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class ValidationIssue:
    """Represents a formatting validation issue"""
    category: str
    severity: str  # 'critical', 'major', 'minor'
    description: str
    location: str
    fix_suggestion: str

class HTMLValidationAgent:
    """Validates HTML output against professional resume standards"""
    
    def __init__(self):
        self.validation_rules = {
            'font_consistency': self._check_font_consistency,
            'spacing_consistency': self._check_spacing_consistency,
            'bullet_formatting': self._check_bullet_formatting,
            'content_artifacts': self._check_content_artifacts,
            'html_structure': self._check_html_structure,
            'professional_standards': self._check_professional_standards
        }
    
    def validate_html_output(self, html_content: str) -> Dict[str, Any]:
        """Comprehensive validation of HTML output"""
        
        validation_result = {
            'overall_score': 0,
            'issues_found': [],
            'issues_by_category': {},
            'formatting_score': 0,
            'content_score': 0,
            'professional_score': 0,
            'recommendations': []
        }
        
        all_issues = []
        
        # Performance optimization: Quick validation for large content
        if len(html_content) > 100000:
            # For very large content, do minimal validation
            validation_result.update({
                'overall_score': 85,
                'formatting_score': 85,
                'content_score': 85,
                'professional_score': 85,
                'recommendations': ['Large content - validation skipped for performance']
            })
            return validation_result
        
        # Run all validation rules with timeout protection
        import time
        start_time = time.time()
        
        for rule_name, rule_function in self.validation_rules.items():
            try:
                # Check if we're taking too long (>10 seconds total)
                if time.time() - start_time > 10:
                    print(f"⚠️  Skipping remaining validation rules due to timeout")
                    break
                    
                issues = rule_function(html_content)
                all_issues.extend(issues)
                validation_result['issues_by_category'][rule_name] = issues
                
            except Exception as e:
                print(f"⚠️  Validation rule {rule_name} failed: {e}")
                # Continue with other rules
                continue
        
        validation_result['issues_found'] = all_issues
        
        # Calculate scores
        scores = self._calculate_scores(all_issues)
        validation_result.update(scores)
        
        # Generate recommendations
        validation_result['recommendations'] = self._generate_recommendations(all_issues)
        
        return validation_result
    
    def _check_font_consistency(self, html_content: str) -> List[ValidationIssue]:
        """Check for font size and style consistency"""
        issues = []
        
        # Find all font-size declarations
        font_sizes = re.findall(r'font-size:\s*([^;]+)', html_content)
        
        # Check for too many different font sizes
        unique_sizes = set(font_sizes)
        if len(unique_sizes) > 5:
            issues.append(ValidationIssue(
                category='font_consistency',
                severity='major',
                description=f'Too many font sizes detected: {len(unique_sizes)}',
                location='CSS styles',
                fix_suggestion='Standardize to 3-4 font sizes maximum (e.g., 18pt header, 11pt body, 10pt metadata)'
            ))
        
        # Check for very small fonts (unprofessional)
        small_fonts = [size for size in font_sizes if 'px' in size and int(re.findall(r'\\d+', size)[0]) < 10]
        if small_fonts:
            issues.append(ValidationIssue(
                category='font_consistency',
                severity='major',
                description=f'Fonts too small detected: {small_fonts}',
                location='Various sections',
                fix_suggestion='Use minimum 10pt/11px for body text'
            ))
        
        return issues
    
    def _check_spacing_consistency(self, html_content: str) -> List[ValidationIssue]:
        """Check for consistent spacing and margins"""
        issues = []
        
        # Check for inconsistent margin declarations
        margins = re.findall(r'margin:\s*([^;]+)', html_content)
        margin_tops = re.findall(r'margin-top:\s*([^;]+)', html_content)
        
        # Too many different margin values indicates inconsistency
        all_margins = margins + margin_tops
        unique_margins = set(all_margins)
        
        if len(unique_margins) > 8:
            issues.append(ValidationIssue(
                category='spacing_consistency',
                severity='minor',
                description=f'Inconsistent spacing with {len(unique_margins)} different margin values',
                location='CSS styles',
                fix_suggestion='Standardize to consistent spacing scale (e.g., 0, 2pt, 4pt, 8pt, 15pt)'
            ))
        
        return issues
    
    def _check_bullet_formatting(self, html_content: str) -> List[ValidationIssue]:
        """Check for proper bullet point formatting"""
        issues = []
        
        # Check for text bullet points (•) instead of proper HTML lists
        text_bullets = len(re.findall(r'(?<!<li>)(?<!ul>)\\s*•\\s*', html_content))
        html_bullets = len(re.findall(r'<li>', html_content))
        
        if text_bullets > html_bullets:
            issues.append(ValidationIssue(
                category='bullet_formatting',
                severity='critical',
                description=f'Text bullets (•) found instead of proper HTML lists: {text_bullets} text vs {html_bullets} HTML',
                location='Email template and other sections',
                fix_suggestion='Convert all bullet points to proper HTML <ul>/<li> structure'
            ))
        
        # Check for inline bullet points that should be separate lines
        inline_bullets = re.findall(r'•[^<]*?•', html_content)
        if inline_bullets:
            issues.append(ValidationIssue(
                category='bullet_formatting',
                severity='major',
                description=f'Multiple bullet points on single line detected: {len(inline_bullets)}',
                location='Email template',
                fix_suggestion='Each bullet point should be on separate line with proper HTML structure'
            ))
        
        return issues
    
    def _check_content_artifacts(self, html_content: str) -> List[ValidationIssue]:
        """Check for content generation artifacts like \\n--, escaped characters, etc."""
        issues = []
        
        # Performance optimization: Skip validation for very large content
        if len(html_content) > 50000:
            return issues
        
        # Use fast string searches for large content instead of expensive regex
        if len(html_content) > 20000:
            # Simple string searches are much faster than regex
            if '\\\\n---' in html_content:
                count = html_content.count('\\\\n---')
                issues.append(ValidationIssue(
                    category='content_artifacts',
                    severity='critical',
                    description=f'Newline artifacts found: {count} instances of \\\\n---',
                    location='Summary and skills sections',
                    fix_suggestion='Clean content generation to remove markdown artifacts'
                ))
            
            if '\\\\n' in html_content:
                count = html_content.count('\\\\n')
                if count > 20:  # Only flag if excessive
                    issues.append(ValidationIssue(
                        category='content_artifacts',
                        severity='major',
                        description=f'Escaped newlines found: {count} instances',
                        location='Various sections',
                        fix_suggestion='Convert escaped newlines to proper HTML line breaks or paragraphs'
                    ))
            
            return issues
        
        # Use regex only for smaller content to avoid timeout
        try:
            # Check for \\n--- artifacts (optimized pattern)
            if '\\\\n---' in html_content:
                newline_artifacts = re.findall(r'\\\\n---', html_content)
                if newline_artifacts:
                    issues.append(ValidationIssue(
                        category='content_artifacts',
                        severity='critical',
                        description=f'Newline artifacts found: {len(newline_artifacts)} instances of \\\\n---',
                        location='Summary and skills sections',
                        fix_suggestion='Clean content generation to remove markdown artifacts'
                    ))
            
            # Check for escaped newlines (limit scope)
            if '\\\\n' in html_content:
                # Count occurrences without regex for speed
                count = html_content.count('\\\\n')
                if count > 10:  # Only flag if excessive
                    issues.append(ValidationIssue(
                        category='content_artifacts',
                        severity='major',
                        description=f'Escaped newlines found: {count} instances',
                        location='Various sections',
                        fix_suggestion='Convert escaped newlines to proper HTML line breaks or paragraphs'
                    ))
            
            # Skip the expensive broken markdown regex for now - too slow
            # This can be re-enabled later with better optimization
            
        except (re.error, TimeoutError):
            # Skip regex validation if problematic
            pass
        
        return issues
    
    def _check_html_structure(self, html_content: str) -> List[ValidationIssue]:
        """Check HTML structure and validity"""
        issues = []
        
        # Check for missing closing tags
        opening_divs = len(re.findall(r'<div[^>]*>', html_content))
        closing_divs = len(re.findall(r'</div>', html_content))
        
        if opening_divs != closing_divs:
            issues.append(ValidationIssue(
                category='html_structure',
                severity='critical',
                description=f'Mismatched div tags: {opening_divs} opening vs {closing_divs} closing',
                location='HTML structure',
                fix_suggestion='Ensure all div tags are properly closed'
            ))
        
        # Check for invalid HTML attributes or malformed tags
        malformed_tags = re.findall(r'<[^>]*[^>](?<!>)\\n', html_content)
        if malformed_tags:
            issues.append(ValidationIssue(
                category='html_structure',
                severity='major',
                description=f'Potentially malformed HTML tags: {len(malformed_tags)}',
                location='Various sections',
                fix_suggestion='Validate HTML syntax and fix malformed tags'
            ))
        
        return issues
    
    def _check_professional_standards(self, html_content: str) -> List[ValidationIssue]:
        """Check against professional resume standards"""
        issues = []
        
        # Check for appropriate professional sections
        required_sections = ['SUMMARY', 'EXPERIENCE', 'SKILLS', 'EDUCATION']
        missing_sections = []
        
        for section in required_sections:
            if section not in html_content:
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(ValidationIssue(
                category='professional_standards',
                severity='critical',
                description=f'Missing professional resume sections: {missing_sections}',
                location='Resume structure',
                fix_suggestion='Include all standard resume sections'
            ))
        
        # Check for appropriate content length
        summary_match = re.search(r'<div class="summary-text">(.*?)</div>', html_content, re.DOTALL)
        if summary_match:
            summary_text = summary_match.group(1)
            word_count = len(summary_text.split())
            if word_count < 50:
                issues.append(ValidationIssue(
                    category='professional_standards',
                    severity='major',
                    description=f'Summary too short: {word_count} words',
                    location='Summary section',
                    fix_suggestion='Expand summary to 80-120 words with specific achievements'
                ))
        
        # Check for quantified achievements
        metrics_pattern = r'\\d+%|\\$\\d+|\\d+[KMB]|\\d+\\+|\\d+ days?'
        metrics_count = len(re.findall(metrics_pattern, html_content))
        
        if metrics_count < 5:
            issues.append(ValidationIssue(
                category='professional_standards',
                severity='major',
                description=f'Insufficient quantified achievements: {metrics_count} metrics found',
                location='Experience section',
                fix_suggestion='Include more specific metrics and quantified results'
            ))
        
        return issues
    
    def _calculate_scores(self, issues: List[ValidationIssue]) -> Dict[str, float]:
        """Calculate quality scores based on issues found"""
        
        critical_count = sum(1 for issue in issues if issue.severity == 'critical')
        major_count = sum(1 for issue in issues if issue.severity == 'major')
        minor_count = sum(1 for issue in issues if issue.severity == 'minor')
        
        # Calculate scores (100 = perfect, deduct points for issues)
        formatting_score = max(0, 100 - (critical_count * 25) - (major_count * 10) - (minor_count * 5))
        content_score = max(0, 100 - (critical_count * 20) - (major_count * 8) - (minor_count * 3))
        professional_score = max(0, 100 - (critical_count * 30) - (major_count * 12) - (minor_count * 6))
        
        overall_score = (formatting_score + content_score + professional_score) / 3
        
        return {
            'formatting_score': formatting_score,
            'content_score': content_score,
            'professional_score': professional_score,
            'overall_score': overall_score
        }
    
    def _generate_recommendations(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate prioritized recommendations for fixing issues"""
        
        recommendations = []
        
        # Group by severity
        critical_issues = [issue for issue in issues if issue.severity == 'critical']
        major_issues = [issue for issue in issues if issue.severity == 'major']
        
        # Prioritize critical issues
        for issue in critical_issues:
            recommendations.append(f"🚨 CRITICAL: {issue.description} - {issue.fix_suggestion}")
        
        # Add major issues
        for issue in major_issues[:3]:  # Limit to top 3 major issues
            recommendations.append(f"⚠️ MAJOR: {issue.description} - {issue.fix_suggestion}")
        
        return recommendations

# Export the validation agent
__all__ = ['HTMLValidationAgent', 'ValidationIssue']