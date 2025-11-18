"""
Pre-Generation Validator Agent
Validates data completeness and compatibility before content generation
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import json

@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    severity: str  # 'critical', 'warning', 'info'
    category: str
    message: str
    suggestion: str

@dataclass
class ValidationResult:
    """Pre-generation validation result"""
    should_proceed: bool
    decision: str  # 'PROCEED', 'PROCEED_WITH_WARNINGS', 'ABORT'
    issues: List[ValidationIssue]
    confidence_score: float

class PreGenerationValidator:
    """
    Validates profile completeness and domain compatibility before generation
    
    Activation: BEFORE any content generation
    Purpose: Ensure sufficient data and no critical conflicts
    """
    
    def __init__(self):
        self.critical_thresholds = {
            'min_projects': 3,
            'min_achievements': 5,
            'min_experience_years': 1,
            'max_experience_gap_years': 8
        }
    
    def validate_pre_generation(self, user_profile: Dict, jd_data: Dict) -> ValidationResult:
        """
        Comprehensive pre-generation validation
        
        Args:
            user_profile: User's profile data
            jd_data: Parsed job description data
            
        Returns:
            ValidationResult with decision and issues
        """
        issues = []
        
        # Run all validation checks
        issues.extend(self._check_profile_completeness(user_profile))
        issues.extend(self._check_domain_compatibility(user_profile, jd_data))
        issues.extend(self._check_experience_level_match(user_profile, jd_data))
        issues.extend(self._check_explicit_conflicts(user_profile, jd_data))
        
        # Determine decision based on issues
        critical_issues = [i for i in issues if i.severity == 'critical']
        warning_issues = [i for i in issues if i.severity == 'warning']
        
        if critical_issues:
            decision = 'ABORT'
            should_proceed = False
            confidence_score = 0.0
        elif len(warning_issues) >= 3:
            decision = 'PROCEED_WITH_WARNINGS'
            should_proceed = True
            confidence_score = 0.6
        else:
            decision = 'PROCEED'
            should_proceed = True
            confidence_score = 0.9
        
        return ValidationResult(
            should_proceed=should_proceed,
            decision=decision,
            issues=issues,
            confidence_score=confidence_score
        )
    
    def _check_profile_completeness(self, user_profile: Dict) -> List[ValidationIssue]:
        """Check if profile has sufficient data for generation"""
        issues = []
        
        # Check contact information
        personal_info = user_profile.get('personal_info', {})
        if not personal_info.get('name'):
            issues.append(ValidationIssue(
                severity='critical',
                category='profile_completeness',
                message='Missing user name in profile',
                suggestion='Add name to personal_info section'
            ))
        
        if not personal_info.get('email'):
            issues.append(ValidationIssue(
                severity='critical',
                category='profile_completeness',
                message='Missing email address in profile',
                suggestion='Add email to personal_info section'
            ))
        
        # Check project completeness
        projects = user_profile.get('projects', {})
        if len(projects) < self.critical_thresholds['min_projects']:
            issues.append(ValidationIssue(
                severity='critical',
                category='profile_completeness',
                message=f'Insufficient projects: {len(projects)} < {self.critical_thresholds["min_projects"]}',
                suggestion='Add more detailed project descriptions to profile'
            ))
        
        # Check quantified achievements
        achievements = user_profile.get('key_achievements', [])
        metrics_count = sum(1 for ach in achievements if any(char.isdigit() for char in str(ach)))
        
        if metrics_count < self.critical_thresholds['min_achievements']:
            issues.append(ValidationIssue(
                severity='warning',
                category='profile_completeness',
                message=f'Low quantified achievements: {metrics_count} < {self.critical_thresholds["min_achievements"]}',
                suggestion='Add more specific metrics and numbers to achievements'
            ))
        
        # Check experience data
        experience = user_profile.get('experience', [])
        if not experience:
            issues.append(ValidationIssue(
                severity='critical',
                category='profile_completeness',
                message='No experience data found in profile',
                suggestion='Add work experience to profile'
            ))
        
        return issues
    
    def _check_domain_compatibility(self, user_profile: Dict, jd_data: Dict) -> List[ValidationIssue]:
        """Check if user's experience matches job domain - Enhanced with critical domain blocking"""
        issues = []
        
        job_domain = jd_data.get('domain', '').lower()
        job_title = jd_data.get('title', '').lower()
        job_description = jd_data.get('description', '').lower()
        job_requirements = ' '.join(jd_data.get('requirements', [])).lower()
        
        # Combined job text for analysis
        job_text = f"{job_domain} {job_title} {job_description} {job_requirements}"
        
        # CRITICAL DOMAINS - These require explicit domain experience to avoid misrepresentation
        critical_domains = {
            'energy_trading': {
                'keywords': ['energy trading', 'commodity trading', 'power trading', 'gas trading', 
                           'energy markets', 'commodity markets', 'trading desk', 'energy derivatives',
                           'renewable energy trading', 'carbon trading', 'electricity trading'],
                'description': 'Energy/Commodity Trading'
            },
            'financial_trading': {
                'keywords': ['algorithmic trading', 'quantitative trading', 'derivatives trading',
                           'forex trading', 'securities trading', 'investment banking', 'hedge fund',
                           'trading algorithms', 'market making', 'proprietary trading'],
                'description': 'Financial Trading & Investment'
            },
            'healthcare_medical': {
                'keywords': ['medical device', 'healthcare technology', 'clinical', 'pharmaceutical',
                           'biotech', 'medical software', 'health records', 'patient care',
                           'medical data', 'clinical trials', 'fda approval'],
                'description': 'Healthcare/Medical Technology'
            },
            'aerospace_defense': {
                'keywords': ['aerospace', 'defense', 'military', 'aviation', 'satellite',
                           'space technology', 'defense contractor', 'missile systems',
                           'aircraft', 'radar systems'],
                'description': 'Aerospace & Defense'
            },
            'blockchain_crypto': {
                'keywords': ['blockchain', 'cryptocurrency', 'crypto', 'defi', 'smart contracts',
                           'web3', 'bitcoin', 'ethereum', 'nft', 'dao'],
                'description': 'Blockchain/Cryptocurrency'
            },
            'legal_compliance': {
                'keywords': ['legal technology', 'compliance software', 'regulatory technology',
                           'legal operations', 'contract management', 'litigation support',
                           'regulatory compliance', 'legal analytics'],
                'description': 'Legal Technology & Compliance'
            }
        }
        
        # USER'S ACTUAL EXPERIENCE DOMAINS - What Vinesh has actually worked in
        user_experience_domains = {
            'coworking_workspace': ['coworking', 'workspace', 'shared office', 'business centers'],
            'food_beverage_platform': ['food delivery', 'f&b platform', 'restaurant', 'catering', 
                                     'food ordering', 'meal delivery'],
            'enterprise_automation': ['enterprise automation', 'workflow automation', 'process automation',
                                    'salesforce', 'sap integration', 'business process'],
            'saas_product_management': ['saas', 'product management', 'platform development', 
                                      'api integration', 'cloud platform'],
            'ai_ml_systems': ['ai systems', 'machine learning', 'rag systems', 'artificial intelligence'],
            'frontend_development': ['frontend development', 'web development', 'javascript', 'react', 'ui/ux']
        }
        
        # Extract user's actual experience
        user_experience = user_profile.get('experience', [])
        user_text = ' '.join([
            ' '.join([exp.get('title', ''), exp.get('company', ''), 
                     ' '.join(exp.get('highlights', []))])
            for exp in user_experience
        ]).lower()
        
        # Check for CRITICAL domain mismatches
        for domain_key, domain_info in critical_domains.items():
            domain_matches = sum(1 for keyword in domain_info['keywords'] if keyword in job_text)
            
            if domain_matches >= 2:  # Strong indication this is a specialized domain job
                # Check if user has ANY experience in this domain
                user_domain_matches = sum(1 for keyword in domain_info['keywords'] if keyword in user_text)
                
                if user_domain_matches == 0:  # No experience in this critical domain
                    issues.append(ValidationIssue(
                        severity='critical',
                        category='domain_mismatch',
                        message=f'CRITICAL DOMAIN MISMATCH: Job requires {domain_info["description"]} experience, '
                               f'but user profile shows no background in this specialized domain',
                        suggestion=f'This role requires specific {domain_info["description"]} experience. '
                                 f'Applying may result in interview questions you cannot answer authentically. '
                                 f'Consider focusing on roles in your actual experience domains.'
                    ))
        
        # Check for general domain alignment with user's actual domains  
        user_domain_matches = []
        for user_domain, keywords in user_experience_domains.items():
            user_matches = sum(1 for kw in keywords if kw in user_text)
            job_matches = sum(1 for kw in keywords if kw in job_text)
            
            if user_matches >= 2 and job_matches >= 1:
                user_domain_matches.append(user_domain)
        
        # If no alignment with user's actual domains, add warning
        if not user_domain_matches:
            issues.append(ValidationIssue(
                severity='warning',
                category='domain_alignment',
                message=f'Limited alignment with your core experience domains: '
                       f'{", ".join(user_experience_domains.keys())}',
                suggestion='Consider emphasizing transferable skills and relevant project experience'
            ))
        
        # Additional check for experience reframing requirements
        reframing_indicators = ['trading', 'commodity', 'energy', 'medical', 'healthcare', 
                              'financial services', 'investment', 'blockchain', 'crypto']
        
        reframing_needed = any(indicator in job_text for indicator in reframing_indicators)
        if reframing_needed and not any(issue.severity == 'critical' for issue in issues):
            issues.append(ValidationIssue(
                severity='warning',
                category='experience_reframing',
                message='This role may require reframing your experience to match industry terminology',
                suggestion='Ensure any reframing maintains factual accuracy and avoid overstating domain expertise'
            ))
        
        return issues
    
    def _check_experience_level_match(self, user_profile: Dict, jd_data: Dict) -> List[ValidationIssue]:
        """Check if experience level matches job requirements"""
        issues = []
        
        user_years = user_profile.get('personal_info', {}).get('total_experience_years', 0)
        
        # Extract experience requirements from JD
        jd_text = ' '.join([
            jd_data.get('description', ''),
            ' '.join(jd_data.get('requirements', []))
        ]).lower()
        
        # Look for experience patterns
        experience_patterns = [
            ('10+ years', 10), ('8+ years', 8), ('5+ years', 5),
            ('senior level', 7), ('senior', 7), ('lead', 8),
            ('junior', 2), ('entry level', 1), ('graduate', 1)
        ]
        
        required_years = None
        for pattern, years in experience_patterns:
            if pattern in jd_text:
                required_years = years
                break
        
        if required_years:
            experience_gap = abs(user_years - required_years)
            
            if user_years < required_years - 2:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='experience_level',
                    message=f'Experience gap: {user_years} years vs {required_years}+ required',
                    suggestion='Emphasize rapid learning, relevant projects, and transferable skills'
                ))
            elif user_years > required_years + 5:
                issues.append(ValidationIssue(
                    severity='info',
                    category='experience_level',
                    message=f'Potential overqualification: {user_years} years vs {required_years}+ required',
                    suggestion='Focus on relevant achievements and avoid mentioning all experience'
                ))
        
        return issues
    
    def _check_explicit_conflicts(self, user_profile: Dict, jd_data: Dict) -> List[ValidationIssue]:
        """Check for explicit conflicts between user preferences and job"""
        issues = []
        
        preferences = user_profile.get('preferences', {})
        
        # Check industry preferences
        avoid_industries = preferences.get('industries_avoid', [])
        job_domain = jd_data.get('domain', '').lower()
        company = jd_data.get('company', '').lower()
        
        for avoid_industry in avoid_industries:
            if avoid_industry.lower() in job_domain or avoid_industry.lower() in company:
                issues.append(ValidationIssue(
                    severity='critical',
                    category='explicit_conflicts',
                    message=f'Job conflicts with avoided industry: {avoid_industry}',
                    suggestion=f'Consider if this {avoid_industry} role aligns with career goals'
                ))
        
        # Check location constraints
        location_constraints = preferences.get('location_constraints', [])
        job_country = jd_data.get('country', '').lower()
        
        if location_constraints and job_country:
            location_match = any(constraint.lower() in job_country 
                               for constraint in location_constraints)
            if not location_match:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='location_preferences',
                    message=f'Job location ({job_country}) outside preferred regions',
                    suggestion='Verify remote work options or relocation willingness'
                ))
        
        return issues
    
    def print_validation_report(self, result: ValidationResult) -> None:
        """Print formatted validation report"""
        print(f"\n🛡️  PRE-GENERATION VALIDATION")
        print("=" * 50)
        
        # Decision
        decision_icons = {
            'PROCEED': '✅',
            'PROCEED_WITH_WARNINGS': '⚠️',
            'ABORT': '❌'
        }
        
        icon = decision_icons.get(result.decision, '❓')
        print(f"{icon} Decision: {result.decision}")
        print(f"🎯 Confidence: {result.confidence_score:.1%}")
        print(f"📊 Issues found: {len(result.issues)}")
        
        # Issues breakdown
        if result.issues:
            print(f"\n📋 Issues by severity:")
            
            critical = [i for i in result.issues if i.severity == 'critical']
            warnings = [i for i in result.issues if i.severity == 'warning']
            info = [i for i in result.issues if i.severity == 'info']
            
            if critical:
                print(f"   🚨 Critical: {len(critical)}")
                for issue in critical:
                    print(f"      • {issue.message}")
                    print(f"        → {issue.suggestion}")
            
            if warnings:
                print(f"   ⚠️ Warnings: {len(warnings)}")
                for issue in warnings:
                    print(f"      • {issue.message}")
            
            if info:
                print(f"   ℹ️ Info: {len(info)}")
        else:
            print("✅ No issues detected")
        
        print("=" * 50)

# Export the validator
__all__ = ['PreGenerationValidator', 'ValidationResult', 'ValidationIssue']