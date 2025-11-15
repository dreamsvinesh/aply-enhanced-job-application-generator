#!/usr/bin/env python3
"""
Content Depth Validator
Ensures proper content depth based on role seniority and JD requirements.
Implements strict rules for bullet points and content richness.
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class RoleDepthRequirements:
    """Content depth requirements for different role levels"""
    min_bullets: int
    max_bullets: int
    min_words_per_bullet: int
    max_words_per_bullet: int
    requires_metrics: bool
    requires_technical_details: bool
    role_keywords: List[str]

class ContentDepthValidator:
    """Validates content depth based on role seniority and target position"""
    
    def __init__(self):
        # Role-specific depth requirements
        self.role_requirements = {
            'senior_pm': RoleDepthRequirements(
                min_bullets=6, max_bullets=8,
                min_words_per_bullet=15, max_words_per_bullet=35,
                requires_metrics=True, requires_technical_details=True,
                role_keywords=['strategic', 'leadership', 'vision', 'roadmap', 'investment', 'CEO', 'cross-functional']
            ),
            'pm': RoleDepthRequirements(
                min_bullets=4, max_bullets=5,
                min_words_per_bullet=12, max_words_per_bullet=30,
                requires_metrics=True, requires_technical_details=False,
                role_keywords=['product', 'features', 'user', 'market', 'strategy', 'growth']
            ),
            'engineer': RoleDepthRequirements(
                min_bullets=2, max_bullets=3,
                min_words_per_bullet=10, max_words_per_bullet=25,
                requires_metrics=False, requires_technical_details=True,
                role_keywords=['built', 'developed', 'implemented', 'maintained', 'technical']
            ),
            'founding_role': RoleDepthRequirements(
                min_bullets=7, max_bullets=9,
                min_words_per_bullet=18, max_words_per_bullet=40,
                requires_metrics=True, requires_technical_details=True,
                role_keywords=['founded', '0→1', 'established', 'built from scratch', 'founding', 'scaled']
            )
        }
        
        # Metrics patterns
        self.metrics_patterns = [
            r'\d+%',  # Percentages
            r'\d+[xX]',  # Multipliers
            r'\$\d+[kKmMbB]?',  # Money amounts
            r'\d+\+',  # Plus numbers
            r'\d+[-–]\d+',  # Ranges
            r'\d+:\d+',  # Ratios
            r'\d+→\d+',  # Before/after
        ]
        
        # Technical keywords for different domains
        self.technical_keywords = {
            'ai_ml': ['AI', 'ML', 'RAG', 'pgvector', 'LLM', 'prompt engineering', 'machine learning', 'neural'],
            'automation': ['automation', 'workflow', 'API', 'integration', 'Salesforce', 'MuleSoft', 'IVR'],
            'platform': ['platform', 'architecture', 'scalable', 'infrastructure', 'cloud', 'microservices'],
            'data': ['analytics', 'data-driven', 'metrics', 'insights', 'dashboard', 'reporting'],
            'frontend': ['HTML5', 'CSS3', 'JavaScript', 'Angular', 'React', 'UI/UX', 'responsive']
        }
    
    def validate_content_depth(self, resume_content: str, jd_analysis: Dict) -> Dict[str, Any]:
        """Validate overall content depth of resume"""
        
        validation_result = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'suggestions': [],
            'depth_score': 0,
            'role_validations': []
        }
        
        # Check for professional title after name (CRITICAL REQUIREMENT)
        lines = resume_content.strip().split('\n')
        if len(lines) < 2:
            validation_result['is_valid'] = False
            validation_result['issues'].append("Missing professional title line after name")
            return validation_result
        
        # Check if second line contains professional title
        name_line = lines[0].strip()
        title_line = lines[1].strip()
        
        if not title_line or 'Product Manager' not in title_line or ('Product Operations' not in title_line and 'AI' not in title_line):
            validation_result['is_valid'] = False
            validation_result['issues'].append(f"Missing or invalid professional title. Expected: 'Senior Product Manager - Product Operations | AI & Process Automation' but found: '{title_line}'")
            return validation_result
        
        # Extract experience sections
        experience_sections = self._extract_experience_sections(resume_content)
        
        if not experience_sections:
            validation_result['is_valid'] = False
            validation_result['issues'].append("No experience sections found")
            return validation_result
        
        total_depth_score = 0
        
        # Validate each role section
        for i, section in enumerate(experience_sections):
            role_validation = self._validate_role_section(section, jd_analysis)
            validation_result['role_validations'].append(role_validation)
            
            if not role_validation['meets_requirements']:
                validation_result['is_valid'] = False
                validation_result['issues'].extend(role_validation['issues'])
            
            validation_result['warnings'].extend(role_validation['warnings'])
            validation_result['suggestions'].extend(role_validation['suggestions'])
            total_depth_score += role_validation['depth_score']
        
        # Calculate overall depth score
        validation_result['depth_score'] = total_depth_score / len(experience_sections) if experience_sections else 0
        
        # Overall content validation
        self._validate_overall_content_quality(resume_content, validation_result)
        
        return validation_result
    
    def _extract_experience_sections(self, resume_content: str) -> List[Dict[str, Any]]:
        """Extract individual role sections from resume"""
        
        sections = []
        lines = resume_content.split('\n')
        
        current_section = None
        in_experience = False
        
        for line in lines:
            line = line.strip()
            
            # Check if we're in experience section
            line_upper = line.upper()
            if (line_upper in ['EXPERIENCE', 'WORK EXPERIENCE', 'PROFESSIONAL EXPERIENCE'] or
                line_upper == '**EXPERIENCE:**' or line_upper.startswith('**EXPERIENCE')):
                in_experience = True
                continue
            
            # Check if we hit another major section
            line_upper = line.upper()
            if (line_upper in ['EDUCATION', 'SKILLS', 'CORE COMPETENCIES', 'CERTIFICATIONS'] or
                line_upper == '**EDUCATION:**' or line_upper.startswith('**EDUCATION') or
                line_upper.startswith('**CERTIFICATIONS') or line_upper.startswith('**CONTACT')) and in_experience:
                if current_section:
                    sections.append(current_section)
                break
            
            if not in_experience:
                continue
            
            # Detect role headers (Company • Role • Duration) or **Role Title - Company (Duration)**
            is_role_header = (
                ('•' in line and any(year in line for year in ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012'])) or
                (line.startswith('**') and any(year in line for year in ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012'])) or
                (line.startswith('**') and any(company in line for company in ['COWRKS', 'Automne', 'Rukshaya']))
            )
            if is_role_header:
                # Save previous section
                if current_section:
                    sections.append(current_section)
                
                # Start new section
                current_section = {
                    'header': line,
                    'role_title': '',
                    'company': '',
                    'duration': '',
                    'bullets': [],
                    'content': line + '\n'
                }
                
                # Parse header
                self._parse_role_header(line, current_section)
            
            # Collect bullet points (both • and - formats)
            elif (line.startswith('•') or line.startswith('-')) and current_section:
                bullet_text = line[1:].strip() if line.startswith('•') else line[1:].strip()
                current_section['bullets'].append(bullet_text)
                current_section['content'] += line + '\n'
            
            # Add other content
            elif current_section and line:
                current_section['content'] += line + '\n'
        
        # Add last section
        if current_section:
            sections.append(current_section)
        
        return sections
    
    def _parse_role_header(self, header: str, section: Dict[str, Any]) -> None:
        """Parse role header to extract title, company, duration"""
        
        # Handle **Role Title - Company (Duration)** format
        if header.startswith('**') and header.endswith('**'):
            clean_header = header.strip('*').strip()
            if ' - ' in clean_header:
                parts = clean_header.split(' - ', 1)  # Split only on first occurrence
                section['role_title'] = parts[0].strip()
                if len(parts) > 1:
                    company_duration = parts[1]
                    if '(' in company_duration and ')' in company_duration:
                        # Extract company before the first parenthesis
                        section['company'] = company_duration.split('(')[0].strip()
                        # Extract duration from within parentheses
                        duration_part = company_duration.split('(')[1].split(')')[0]
                        section['duration'] = duration_part.strip()
                    else:
                        section['company'] = company_duration.strip()
            else:
                section['role_title'] = clean_header
        # Handle Role • Company • Duration format
        elif '•' in header:
            parts = [part.strip() for part in header.split('•')]
            if len(parts) >= 3:
                section['role_title'] = parts[0]
                section['company'] = parts[1]
                section['duration'] = parts[2]
            elif len(parts) == 2:
                section['role_title'] = parts[0]
                section['company'] = parts[1]
        else:
            # Fallback - just use the header as role title
            section['role_title'] = header.strip()
    
    def _validate_role_section(self, section: Dict[str, Any], jd_analysis: Dict) -> Dict[str, Any]:
        """Validate individual role section depth"""
        
        role_validation = {
            'role_title': section.get('role_title', ''),
            'company': section.get('company', ''),
            'bullet_count': len(section['bullets']),
            'meets_requirements': True,
            'issues': [],
            'warnings': [],
            'suggestions': [],
            'depth_score': 0,
            'role_level': '',
            'requirements_used': None
        }
        
        # Determine role level
        role_level = self._determine_role_level(section['role_title'], jd_analysis)
        role_validation['role_level'] = role_level
        
        requirements = self.role_requirements.get(role_level)
        if not requirements:
            role_validation['warnings'].append(f"No requirements defined for role level: {role_level}")
            return role_validation
        
        role_validation['requirements_used'] = requirements
        
        # Validate bullet count
        bullet_count = len(section['bullets'])
        if bullet_count < requirements.min_bullets:
            role_validation['meets_requirements'] = False
            role_validation['issues'].append(f"Insufficient bullets: {bullet_count} < {requirements.min_bullets} required for {role_level}")
        elif bullet_count > requirements.max_bullets:
            role_validation['warnings'].append(f"Too many bullets: {bullet_count} > {requirements.max_bullets} recommended for {role_level}")
        
        # Validate bullet quality
        bullet_issues = self._validate_bullet_quality(section['bullets'], requirements)
        role_validation['issues'].extend(bullet_issues['issues'])
        role_validation['warnings'].extend(bullet_issues['warnings'])
        role_validation['suggestions'].extend(bullet_issues['suggestions'])
        
        if bullet_issues['issues']:
            role_validation['meets_requirements'] = False
        
        # Calculate depth score
        role_validation['depth_score'] = self._calculate_role_depth_score(section, requirements)
        
        return role_validation
    
    def _determine_role_level(self, role_title: str, jd_analysis: Dict) -> str:
        """Determine role level based on title and target JD"""
        
        role_lower = role_title.lower()
        
        # Check for founding roles
        if any(keyword in role_lower for keyword in ['founding', '0→1']):
            return 'founding_role'
        
        # Check for senior roles  
        if 'senior' in role_lower:
            return 'senior_pm'
        
        # Check for product manager roles
        if any(keyword in role_lower for keyword in ['product manager', 'product owner', 'pm']):
            return 'pm'
        
        # Check for engineering roles
        if any(keyword in role_lower for keyword in ['engineer', 'developer', 'frontend', 'backend']):
            return 'engineer'
        
        # Default to PM level
        return 'pm'
    
    def _validate_bullet_quality(self, bullets: List[str], requirements: RoleDepthRequirements) -> Dict[str, List[str]]:
        """Validate quality of individual bullet points"""
        
        result = {'issues': [], 'warnings': [], 'suggestions': []}
        
        for i, bullet in enumerate(bullets, 1):
            # Check word count
            word_count = len(bullet.split())
            if word_count < requirements.min_words_per_bullet:
                result['issues'].append(f"Bullet {i} too short: {word_count} words < {requirements.min_words_per_bullet} required")
            elif word_count > requirements.max_words_per_bullet:
                result['warnings'].append(f"Bullet {i} too long: {word_count} words > {requirements.max_words_per_bullet} recommended")
            
            # Check for metrics if required
            if requirements.requires_metrics:
                has_metrics = any(re.search(pattern, bullet) for pattern in self.metrics_patterns)
                if not has_metrics:
                    result['warnings'].append(f"Bullet {i} missing metrics/numbers")
            
            # Check for technical details if required
            if requirements.requires_technical_details:
                has_technical = any(
                    any(keyword.lower() in bullet.lower() for keyword in keywords)
                    for keywords in self.technical_keywords.values()
                )
                if not has_technical:
                    result['warnings'].append(f"Bullet {i} missing technical details")
            
            # Check for role-appropriate keywords
            has_role_keywords = any(keyword.lower() in bullet.lower() for keyword in requirements.role_keywords)
            if not has_role_keywords:
                result['suggestions'].append(f"Bullet {i} could include role-appropriate keywords: {', '.join(requirements.role_keywords[:3])}")
        
        return result
    
    def _calculate_role_depth_score(self, section: Dict[str, Any], requirements: RoleDepthRequirements) -> float:
        """Calculate depth score for role section (0-100)"""
        
        score = 0
        max_score = 100
        
        # Bullet count score (30 points)
        bullet_count = len(section['bullets'])
        if bullet_count >= requirements.min_bullets:
            bullet_score = min(30, (bullet_count / requirements.max_bullets) * 30)
            score += bullet_score
        
        # Content quality score (40 points)
        content_text = ' '.join(section['bullets'])
        
        # Metrics score (15 points)
        if requirements.requires_metrics:
            metrics_count = sum(1 for pattern in self.metrics_patterns if re.search(pattern, content_text))
            score += min(15, metrics_count * 3)
        else:
            score += 15  # Full points if not required
        
        # Technical details score (15 points)
        if requirements.requires_technical_details:
            tech_count = sum(
                1 for keywords in self.technical_keywords.values()
                for keyword in keywords
                if keyword.lower() in content_text.lower()
            )
            score += min(15, tech_count * 2)
        else:
            score += 15  # Full points if not required
        
        # Role keywords score (10 points)
        role_keyword_count = sum(1 for keyword in requirements.role_keywords if keyword.lower() in content_text.lower())
        score += min(10, role_keyword_count * 2)
        
        return min(score, max_score)
    
    def _validate_overall_content_quality(self, resume_content: str, validation_result: Dict[str, Any]) -> None:
        """Validate overall resume content quality"""
        
        # Check for required sections
        required_sections = ['SUMMARY', 'EXPERIENCE', 'EDUCATION']
        content_upper = resume_content.upper()
        
        missing_sections = [section for section in required_sections if section not in content_upper]
        if missing_sections:
            validation_result['is_valid'] = False
            validation_result['issues'].extend([f"Missing section: {section}" for section in missing_sections])
        
        # Check overall length
        word_count = len(resume_content.split())
        if word_count < 300:
            validation_result['is_valid'] = False
            validation_result['issues'].append(f"Resume too short: {word_count} words (minimum 300)")
        elif word_count > 800:
            validation_result['warnings'].append(f"Resume may be too long: {word_count} words (recommended max 800)")
        
        # Check for company preservation
        if 'COWRKS' not in resume_content:
            validation_result['is_valid'] = False
            validation_result['issues'].append("Real company COWRKS not found - fact preservation failed")
        
        # Check for metrics throughout
        total_metrics = sum(1 for pattern in self.metrics_patterns if re.search(pattern, resume_content))
        if total_metrics < 5:
            validation_result['warnings'].append(f"Few metrics found: {total_metrics} (recommend at least 5 throughout resume)")
    
    def enhance_content_depth(self, resume_content: str, jd_analysis: Dict) -> Dict[str, Any]:
        """Provide specific suggestions to enhance content depth"""
        
        validation = self.validate_content_depth(resume_content, jd_analysis)
        
        enhancement_suggestions = {
            'priority_fixes': [],
            'content_additions': [],
            'restructuring_needed': False,
            'enhanced_content': resume_content
        }
        
        # Analyze role validations for specific fixes
        for role_val in validation['role_validations']:
            if not role_val['meets_requirements']:
                role_title = role_val['role_title']
                
                if role_val['bullet_count'] < role_val['requirements_used'].min_bullets:
                    needed = role_val['requirements_used'].min_bullets - role_val['bullet_count']
                    enhancement_suggestions['priority_fixes'].append(
                        f"Add {needed} more bullet points to {role_title} role"
                    )
                
                # Suggest specific content additions
                if role_val['role_level'] == 'senior_pm':
                    enhancement_suggestions['content_additions'].extend([
                        "Add strategic vision and roadmap achievements",
                        "Include CEO/executive-level interactions",
                        "Emphasize cross-functional leadership",
                        "Highlight investment/budget approvals"
                    ])
        
        return enhancement_suggestions

def main():
    """Demo content depth validation"""
    print("📏 CONTENT DEPTH VALIDATOR DEMO")
    print("=" * 50)
    
    # Sample resume content for testing
    sample_resume = """
SUMMARY
Senior Product Manager with 11 years experience.

EXPERIENCE

Senior Product Manager • COWRKS • 01/2023 - Present • Bangalore, India
• Built AI system achieving 94% accuracy
• Automated workflows reducing timeline 99.6%
• Led team across 5 departments
• Secured $2M investment

Product Manager • COWRKS • 08/2016 - 01/2020 • Bangalore, India
• Developed mobile features increasing engagement 45%
• Generated €220K monthly revenue
• Reduced onboarding from 110 days to 14 days

EDUCATION
Master of Science in Software Engineering • Anna University
"""
    
    # Mock JD analysis
    jd_analysis = {
        'extracted_info': {'role_title': 'Senior Product Manager'},
        'requirements': {'must_have_business': ['strategic operations']}
    }
    
    validator = ContentDepthValidator()
    
    # Validate content depth
    result = validator.validate_content_depth(sample_resume, jd_analysis)
    
    print("📊 Validation Results:")
    print(f"Valid: {'✅' if result['is_valid'] else '❌'}")
    print(f"Depth Score: {result['depth_score']:.1f}/100")
    print(f"Total Issues: {len(result['issues'])}")
    print(f"Total Warnings: {len(result['warnings'])}")
    
    if result['issues']:
        print("\n❌ Issues:")
        for issue in result['issues']:
            print(f"  • {issue}")
    
    if result['warnings']:
        print("\n⚠️ Warnings:")
        for warning in result['warnings']:
            print(f"  • {warning}")
    
    # Role-specific analysis
    print("\n📋 Role Analysis:")
    for role_val in result['role_validations']:
        print(f"• {role_val['role_title']}: {role_val['bullet_count']} bullets, "
              f"Level: {role_val['role_level']}, Score: {role_val['depth_score']:.1f}")
    
    print("\n✅ Content depth validation demo complete!")

if __name__ == "__main__":
    main()