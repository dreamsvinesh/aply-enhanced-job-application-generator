#!/usr/bin/env python3
"""
Unified Application Generator with Complete Validation
This is the MAIN script that should be used for all resume generation.
Integrates all validation steps: pre-generation, brutal workflow, content quality.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple
from datetime import datetime

# Add modules to path
sys.path.append(str(Path(__file__).parent / 'modules'))

try:
    from modules.enhanced_jd_parser import EnhancedJobDescriptionParser
    from modules.pre_generation_validator import PreGenerationValidator
    from modules.enhanced_fact_aware_generator import EnhancedFactAwareGenerator
    from modules.real_user_data_extractor import RealUserDataExtractor
    from modules.content_quality_validator import ContentQualityValidator
    from modules.workflow_validation_agent import BrutalWorkflowValidator
    from generate_universal_application import (
        generate_universal_resume, 
        generate_universal_cover_letter, 
        generate_universal_email,
        generate_universal_linkedin_messages,
        save_universal_package
    )
except ImportError:
    # Fallback to direct imports for testing
    sys.path.append(str(Path(__file__).parent / 'modules'))
    from enhanced_jd_parser import EnhancedJobDescriptionParser
    from pre_generation_validator import PreGenerationValidator
    from enhanced_fact_aware_generator import EnhancedFactAwareGenerator
    from real_user_data_extractor import RealUserDataExtractor
    from content_quality_validator import ContentQualityValidator
    from workflow_validation_agent import BrutalWorkflowValidator

class UnifiedApplicationGenerator:
    """
    Single entry point for all job application generation with complete validation
    
    Workflow:
    1. Parse JD 
    2. Pre-generation validation (blocks critical domain mismatches)
    3. User confirmation for warnings
    4. Enhanced generation with brutal validation
    5. Content quality validation
    6. Final output with comprehensive reports
    """
    
    def __init__(self):
        self.jd_parser = EnhancedJobDescriptionParser()
        self.pre_validator = PreGenerationValidator()
        self.generator = EnhancedFactAwareGenerator(
            ats_optimization_enabled=True,
            target_ats_score=85.0,
            enable_brutal_validation=True
        )
        self.content_validator = ContentQualityValidator()
        self.user_extractor = RealUserDataExtractor()
        
        # Load user profile
        self.user_profile = self.user_extractor.extract_vinesh_data()
        
        print("🚀 UNIFIED APPLICATION GENERATOR WITH COMPLETE VALIDATION")
        print("=" * 80)
        print("✅ All validation systems enabled")
        print("🛡️  Critical domain mismatch detection active")
        print("🔥 Brutal workflow validation enabled")
        print("🎯 Content quality validation active")
        print("=" * 80)
    
    def generate_application(self, jd_text: str, country: str, company_name: str = "") -> Dict[str, Any]:
        """
        Complete application generation with full validation workflow
        
        Returns:
            Dict with generation results, validation reports, and file paths
        """
        
        print(f"\n📋 STEP 1: JOB DESCRIPTION ANALYSIS")
        print("-" * 50)
        
        try:
            # Parse JD
            jd_analysis = self.jd_parser.enhanced_parse(jd_text)
            jd_analysis['country'] = country
            if company_name:
                jd_analysis['extracted_info']['company'] = company_name
            
            print(f"✅ JD parsed successfully")
            print(f"🏢 Company: {jd_analysis['extracted_info'].get('company', 'Unknown')}")
            print(f"💼 Role: {jd_analysis['extracted_info'].get('role_title', 'Unknown')}")
            
        except Exception as e:
            return {
                'success': False,
                'error': f'JD parsing failed: {str(e)}',
                'stage': 'jd_parsing'
            }
        
        print(f"\n🛡️  STEP 2: PRE-GENERATION VALIDATION")
        print("-" * 50)
        
        # Pre-generation validation
        pre_validation_result = self.pre_validator.validate_pre_generation(
            self.user_profile, jd_analysis
        )
        
        self.pre_validator.print_validation_report(pre_validation_result)
        
        # Handle validation decision
        if not pre_validation_result.should_proceed:
            print(f"\n❌ GENERATION BLOCKED: {pre_validation_result.decision}")
            return {
                'success': False,
                'blocked_reason': 'Pre-generation validation failed',
                'validation_result': pre_validation_result,
                'stage': 'pre_validation'
            }
        
        # Ask for user confirmation if warnings exist
        if pre_validation_result.decision == 'PROCEED_WITH_WARNINGS':
            warnings = [issue for issue in pre_validation_result.issues if issue.severity in ['warning', 'critical']]
            if warnings:
                confirmation = self._get_user_confirmation(warnings)
                if not confirmation:
                    print("\n🚫 GENERATION CANCELLED BY USER")
                    return {
                        'success': False,
                        'cancelled_reason': 'User declined to proceed with warnings',
                        'validation_result': pre_validation_result,
                        'stage': 'user_confirmation'
                    }
        
        print(f"\n🤖 STEP 3: ENHANCED GENERATION WITH BRUTAL VALIDATION")
        print("-" * 50)
        
        try:
            # Generate complete application package using universal generator
            print("📄 Generating Resume...")
            resume_results = generate_universal_resume(jd_analysis, country)
            
            print("📝 Generating Cover Letter...")
            cover_letter = generate_universal_cover_letter(jd_analysis, country)
            
            print("📧 Generating Email...")
            email = generate_universal_email(jd_analysis)
            
            print("💼 Generating LinkedIn Messages...")
            linkedin_messages = generate_universal_linkedin_messages(jd_analysis, country)
            
            if not resume_results or 'resume_generation' not in resume_results:
                return {
                    'success': False,
                    'error': 'Resume generation failed - no resume content produced',
                    'stage': 'generation'
                }
            
            # Package all generation results
            generation_results = {
                'resume_generation': resume_results.get('resume_generation', {}),
                'cover_letter': cover_letter,
                'email': email,
                'linkedin_messages': linkedin_messages
            }
            
            print("✅ Complete application package generated")
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Generation failed: {str(e)}',
                'stage': 'generation'
            }
        
        print(f"\n🔍 STEP 4: CONTENT QUALITY VALIDATION")
        print("-" * 50)
        
        try:
            # Prepare content for validation using actual generated content
            content_dict = {
                'resume': generation_results.get('resume_generation', {}),
                'cover_letter': generation_results.get('cover_letter', 'No cover letter generated'),
                'email': generation_results.get('email', 'No email generated'),
                'linkedin_messages': generation_results.get('linkedin_messages', 'No LinkedIn messages generated'),
            }
            
            # Content quality validation
            content_validation = self.content_validator.validate_generated_content(
                content_dict, self.user_profile, jd_analysis
            )
            
            self.content_validator.print_validation_report(content_validation)
            
        except Exception as e:
            print(f"⚠️ Content validation failed: {str(e)}")
            content_validation = None
        
        print(f"\n💾 STEP 5: SAVING RESULTS")
        print("-" * 50)
        
        # Save complete application package using universal saver
        extracted_info = jd_analysis.get('extracted_info', {})
        company = extracted_info.get('company', 'Unknown')
        role = extracted_info.get('role_title', 'Unknown Role')
        
        output_path = save_universal_package(
            company, role, 
            resume_results, 
            generation_results.get('cover_letter'), 
            generation_results.get('email'),
            generation_results.get('linkedin_messages'),
            jd_analysis
        )
        
        # Save additional validation reports
        self._save_validation_reports(output_path, pre_validation_result, content_validation)
        
        print(f"\n🎉 APPLICATION GENERATION COMPLETE!")
        print(f"📁 Output saved to: {output_path}")
        
        return {
            'success': True,
            'output_path': output_path,
            'jd_analysis': jd_analysis,
            'pre_validation': pre_validation_result,
            'generation_results': generation_results,
            'content_validation': content_validation,
            'stage': 'completed'
        }
    
    def _get_user_confirmation(self, warnings) -> bool:
        """Get user confirmation to proceed with warnings"""
        
        print(f"\n⚠️  WARNING: Validation issues detected!")
        print("The following concerns were identified:")
        print("-" * 50)
        
        for i, warning in enumerate(warnings, 1):
            print(f"{i}. [{warning.severity.upper()}] {warning.message}")
            print(f"   💡 Suggestion: {warning.suggestion}")
            print()
        
        print("These warnings indicate potential misrepresentation of your experience.")
        print("Proceeding may result in interview questions you cannot answer authentically.")
        
        while True:
            response = input("\nDo you want to proceed anyway? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                print("✅ User confirmed - proceeding with warnings")
                return True
            elif response in ['n', 'no']:
                print("🚫 User cancelled - stopping generation")
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no")
    
    def _save_validation_reports(self, output_path: str, pre_validation, content_validation):
        """Save additional validation reports to the output directory"""
        
        output_dir = Path(output_path)
        
        # Save validation reports
        validation_report = {
            'generation_timestamp': datetime.now().isoformat(),
            'pre_validation': {
                'decision': pre_validation.decision,
                'confidence': pre_validation.confidence_score,
                'issues': [
                    {
                        'severity': issue.severity,
                        'category': issue.category,
                        'message': issue.message,
                        'suggestion': issue.suggestion
                    }
                    for issue in pre_validation.issues
                ]
            },
            'content_validation': content_validation.__dict__ if content_validation else None
        }
        
        # Save validation report
        validation_file = output_dir / f"comprehensive_validation_report.json"
        with open(validation_file, 'w', encoding='utf-8') as f:
            json.dump(validation_report, f, indent=2, default=str, ensure_ascii=False)
        print(f"✅ Validation report saved: {validation_file}")

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Generate job application with complete validation')
    parser.add_argument('--jd-file', help='Path to job description file')
    parser.add_argument('--jd-text', help='Job description text directly')
    parser.add_argument('--country', default='netherlands', help='Target country')
    parser.add_argument('--company', help='Company name (optional)')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    generator = UnifiedApplicationGenerator()
    
    if args.interactive or not (args.jd_file or args.jd_text):
        # Interactive mode
        print("\n📋 Please provide the job description:")
        if args.jd_file:
            with open(args.jd_file, 'r', encoding='utf-8') as f:
                jd_text = f.read()
        else:
            print("Enter job description (press Ctrl+D when done):")
            jd_text = sys.stdin.read()
        
        country = args.country or input("Target country (default: netherlands): ") or "netherlands"
        company = args.company or input("Company name (optional): ") or ""
        
    else:
        if args.jd_file:
            with open(args.jd_file, 'r', encoding='utf-8') as f:
                jd_text = f.read()
        else:
            jd_text = args.jd_text
        
        country = args.country
        company = args.company or ""
    
    # Generate application
    result = generator.generate_application(jd_text, country, company)
    
    if result['success']:
        print(f"\n🎯 SUCCESS: Application generated successfully!")
        print(f"📂 Check output at: {result['output_path']}")
    else:
        print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
        print(f"🔍 Failed at stage: {result.get('stage', 'unknown')}")
        if 'validation_result' in result:
            print("See validation details above for more information.")

# Function for programmatic use (Claude Code integration)
def generate_validated_application(jd_text: str, country: str, company_name: str = "") -> Dict[str, Any]:
    """
    Main function for Claude Code to call
    Returns complete results including validation status
    """
    generator = UnifiedApplicationGenerator()
    return generator.generate_application(jd_text, country, company_name)

if __name__ == "__main__":
    main()