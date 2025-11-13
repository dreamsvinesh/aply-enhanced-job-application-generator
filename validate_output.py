#!/usr/bin/env python3
"""
Output validation script for generated application packages
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

def validate_application_package(file_path: str) -> Dict[str, any]:
    """
    Validate a generated application package for quality and completeness
    
    Args:
        file_path: Path to the generated markdown file
        
    Returns:
        Dictionary with validation results
    """
    
    results = {
        'file_exists': False,
        'has_all_sections': False,
        'resume_quality': {},
        'cover_letter_quality': {},
        'linkedin_quality': {},
        'email_quality': {},
        'overall_score': 0,
        'issues': [],
        'recommendations': []
    }
    
    # Check if file exists
    if not Path(file_path).exists():
        results['issues'].append("Generated file does not exist")
        return results
    
    results['file_exists'] = True
    
    # Read content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required sections
    required_sections = ['## Resume', '## Cover Letter', '## LinkedIn Message', '## Email Template', '## Changes Made']
    missing_sections = []
    
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        results['issues'].append(f"Missing sections: {', '.join(missing_sections)}")
    else:
        results['has_all_sections'] = True
    
    # Validate individual sections
    results['resume_quality'] = validate_resume_section(content)
    results['cover_letter_quality'] = validate_cover_letter_section(content) 
    results['linkedin_quality'] = validate_linkedin_section(content)
    results['email_quality'] = validate_email_section(content)
    
    # Calculate overall score
    section_scores = [
        results['resume_quality'].get('score', 0),
        results['cover_letter_quality'].get('score', 0),
        results['linkedin_quality'].get('score', 0),
        results['email_quality'].get('score', 0)
    ]
    
    results['overall_score'] = sum(section_scores) / len(section_scores)
    
    # Generate recommendations
    if results['overall_score'] < 70:
        results['recommendations'].append("Consider reviewing JD parsing and content generation")
    if results['linkedin_quality'].get('char_count', 0) > 400:
        results['recommendations'].append("LinkedIn message is too long - aim for under 400 characters")
    
    return results

def validate_resume_section(content: str) -> Dict[str, any]:
    """Validate resume section quality"""
    
    try:
        resume_section = content.split('## Resume')[1].split('## Cover Letter')[0]
    except IndexError:
        return {'score': 0, 'issues': ['Resume section not found']}
    
    quality = {
        'score': 0,
        'issues': [],
        'metrics_count': 0,
        'has_contact_info': False,
        'has_ai_ml_content': False
    }
    
    # Check for contact information
    contact_patterns = [r'\+\d+', r'@\w+\.\w+', r'linkedin\.com']
    if any(re.search(pattern, resume_section) for pattern in contact_patterns):
        quality['has_contact_info'] = True
        quality['score'] += 20
    
    # Check for AI/ML content
    ai_ml_terms = ['AI', 'ML', 'RAG', 'machine learning', 'artificial intelligence']
    if any(term.lower() in resume_section.lower() for term in ai_ml_terms):
        quality['has_ai_ml_content'] = True
        quality['score'] += 25
    
    # Check for quantified metrics
    metric_patterns = [r'\d+%', r'\$\d+', r'\d+[KMB]\+?', r'\d+ days?', r'\d+ hours?']
    metrics_found = []
    
    for pattern in metric_patterns:
        matches = re.findall(pattern, resume_section)
        metrics_found.extend(matches)
    
    quality['metrics_count'] = len(metrics_found)
    if quality['metrics_count'] >= 5:
        quality['score'] += 30
    elif quality['metrics_count'] >= 3:
        quality['score'] += 20
    elif quality['metrics_count'] >= 1:
        quality['score'] += 10
    
    # Check for proper structure
    if 'EXPERIENCE' in resume_section and 'SKILLS' in resume_section:
        quality['score'] += 25
    
    return quality

def validate_cover_letter_section(content: str) -> Dict[str, any]:
    """Validate cover letter section quality"""
    
    try:
        cover_letter = content.split('## Cover Letter')[1].split('## LinkedIn Message')[0]
    except IndexError:
        return {'score': 0, 'issues': ['Cover letter section not found']}
    
    quality = {
        'score': 0,
        'issues': [],
        'word_count': 0,
        'has_opening': False,
        'has_closing': False,
        'has_specific_examples': False
    }
    
    # Count words
    words = len(cover_letter.split())
    quality['word_count'] = words
    
    # Check word count (should be reasonable length)
    if 150 <= words <= 400:
        quality['score'] += 25
    elif words < 100:
        quality['issues'].append("Cover letter too short")
    elif words > 500:
        quality['issues'].append("Cover letter too long")
    
    # Check for proper opening
    if any(greeting in cover_letter for greeting in ['Dear', 'Hi', 'Hello']):
        quality['has_opening'] = True
        quality['score'] += 25
    
    # Check for proper closing
    if any(closing in cover_letter for closing in ['regards', 'sincerely', 'yours', 'Vinesh Kumar']):
        quality['has_closing'] = True
        quality['score'] += 25
    
    # Check for specific examples/metrics
    if re.search(r'\d+%|revenue|\$\d+', cover_letter):
        quality['has_specific_examples'] = True
        quality['score'] += 25
    
    return quality

def validate_linkedin_section(content: str) -> Dict[str, any]:
    """Validate LinkedIn message section"""
    
    try:
        linkedin_section = content.split('## LinkedIn Message')[1].split('## Email Template')[0]
        
        # Extract actual message (skip the length indicator line)
        lines = [line.strip() for line in linkedin_section.split('\n') if line.strip()]
        message_lines = [line for line in lines if not line.startswith('**')]
        
        if message_lines:
            message = message_lines[0]
        else:
            message = ""
            
    except (IndexError, ValueError):
        return {'score': 0, 'issues': ['LinkedIn section not found']}
    
    quality = {
        'score': 0,
        'issues': [],
        'char_count': len(message),
        'has_cta': False,
        'has_personalization': False
    }
    
    # Check character count (should be under 400)
    if len(message) <= 350:
        quality['score'] += 40
    elif len(message) <= 400:
        quality['score'] += 30
    else:
        quality['issues'].append(f"Message too long: {len(message)} characters")
    
    # Check for call-to-action
    cta_phrases = ['call', 'chat', 'discuss', 'available', 'connect', 'meet']
    if any(phrase in message.lower() for phrase in cta_phrases):
        quality['has_cta'] = True
        quality['score'] += 30
    
    # Check for personalization (company name, specific role)
    if len(message) > 20:  # Avoid false positives
        quality['has_personalization'] = True
        quality['score'] += 30
    
    return quality

def validate_email_section(content: str) -> Dict[str, any]:
    """Validate email template section"""
    
    try:
        email_section = content.split('## Email Template')[1].split('## Changes Made')[0]
    except IndexError:
        return {'score': 0, 'issues': ['Email section not found']}
    
    quality = {
        'score': 0,
        'issues': [],
        'has_subject': False,
        'has_greeting': False,
        'has_signature': False
    }
    
    # Check for subject line
    if 'Subject:' in email_section:
        quality['has_subject'] = True
        quality['score'] += 35
    
    # Check for proper greeting
    if any(greeting in email_section for greeting in ['Dear', 'Hi', 'Hello']):
        quality['has_greeting'] = True
        quality['score'] += 30
    
    # Check for signature with contact info
    if 'Vinesh Kumar' in email_section and '@gmail.com' in email_section:
        quality['has_signature'] = True
        quality['score'] += 35
    
    return quality

def main():
    """Main validation function"""
    
    if len(sys.argv) < 2:
        print("Usage: python validate_output.py <path_to_generated_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print("🔍 Validating Application Package")
    print("=" * 40)
    print(f"File: {file_path}")
    print()
    
    # Run validation
    results = validate_application_package(file_path)
    
    # Display results
    print(f"📊 Overall Score: {results['overall_score']:.1f}/100")
    print()
    
    # Section scores
    sections = [
        ('Resume', 'resume_quality'),
        ('Cover Letter', 'cover_letter_quality'), 
        ('LinkedIn Message', 'linkedin_quality'),
        ('Email Template', 'email_quality')
    ]
    
    for section_name, key in sections:
        score = results[key].get('score', 0)
        print(f"  {section_name}: {score}/100")
    
    print()
    
    # Issues
    if results['issues']:
        print("⚠️  Issues Found:")
        for issue in results['issues']:
            print(f"  • {issue}")
        print()
    
    # Recommendations
    if results['recommendations']:
        print("💡 Recommendations:")
        for rec in results['recommendations']:
            print(f"  • {rec}")
        print()
    
    # Summary
    if results['overall_score'] >= 85:
        print("✅ Excellent quality! Package ready to send.")
    elif results['overall_score'] >= 70:
        print("👍 Good quality with minor improvements needed.")
    elif results['overall_score'] >= 50:
        print("⚠️  Acceptable quality but several improvements needed.")
    else:
        print("❌ Quality below standards. Major improvements required.")

if __name__ == "__main__":
    main()