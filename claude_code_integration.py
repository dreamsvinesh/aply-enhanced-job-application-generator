#!/usr/bin/env python3
"""
Claude Code Integration for Validated Application Generation

This script should be called by Claude Code when the user provides:
- Job description text
- Target country/location

It provides the validation flow that was missing and ensures proper domain checking.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Tuple

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from generate_application_with_validation import generate_validated_application

def claude_generate_application(jd_text: str, country: str, company_name: str = "") -> Dict[str, Any]:
    """
    Main function for Claude Code to call when user provides JD + location
    
    This replaces the manual file creation that was bypassing all validation
    
    Args:
        jd_text: The job description provided by user
        country: Target country (e.g., "netherlands", "denmark", "sweden") 
        company_name: Optional company name override
        
    Returns:
        Dict with validation results and recommendations for Claude
    """
    
    print("🤖 CLAUDE CODE INTEGRATION - VALIDATED APPLICATION GENERATION")
    print("=" * 80)
    print("🛡️  Running complete validation workflow...")
    print("🔍 Checking for domain mismatches...")
    print("⚠️  Will ask for user confirmation if warnings detected...")
    print("=" * 80)
    
    try:
        # Run the complete validation workflow
        result = generate_validated_application(jd_text, country, company_name)
        
        # Process results for Claude Code response
        if result['success']:
            return _handle_successful_generation(result)
        else:
            return _handle_failed_generation(result)
            
    except Exception as e:
        return {
            'claude_action': 'report_error',
            'error_message': f"Application generation system error: {str(e)}",
            'user_message': "❌ There was an error with the application generation system. Please try again or contact support."
        }

def _handle_successful_generation(result: Dict[str, Any]) -> Dict[str, Any]:
    """Handle successful generation with validation results"""
    
    pre_validation = result.get('pre_validation')
    content_validation = result.get('content_validation')
    output_path = result.get('output_path', '')
    
    # Determine Claude's response based on validation results
    claude_response = {
        'claude_action': 'show_success_with_validation',
        'output_path': output_path,
        'files_created': [],
        'validation_summary': {},
        'user_message': ""
    }
    
    # Build validation summary
    validation_summary = {
        'pre_generation': {
            'decision': pre_validation.decision,
            'confidence': f"{pre_validation.confidence_score:.1%}",
            'critical_issues': len([i for i in pre_validation.issues if i.severity == 'critical']),
            'warnings': len([i for i in pre_validation.issues if i.severity == 'warning']),
        }
    }
    
    if content_validation:
        validation_summary['content_quality'] = {
            'decision': content_validation.decision,
            'overall_score': f"{content_validation.scores.get('overall_content_score', 0):.1f}/10",
            'should_regenerate': content_validation.should_regenerate
        }
    
    # Check for critical issues that were somehow missed
    critical_issues = [i for i in pre_validation.issues if i.severity == 'critical']
    warnings = [i for i in pre_validation.issues if i.severity == 'warning']
    
    if critical_issues:
        # This shouldn't happen if validation worked correctly
        claude_response['claude_action'] = 'report_critical_issues'
        claude_response['critical_issues'] = [
            {'message': issue.message, 'suggestion': issue.suggestion} 
            for issue in critical_issues
        ]
        claude_response['user_message'] = (
            "⚠️ **CRITICAL VALIDATION ISSUES DETECTED**\n\n"
            "The application was generated but contains critical domain mismatches. "
            "This could result in interview questions you cannot answer authentically.\n\n"
            "**Issues Found:**\n" + 
            "\n".join([f"• {issue.message}" for issue in critical_issues])
        )
    
    elif warnings:
        claude_response['claude_action'] = 'show_success_with_warnings'
        claude_response['warnings'] = [
            {'category': w.category, 'message': w.message, 'suggestion': w.suggestion}
            for w in warnings
        ]
        claude_response['user_message'] = (
            f"✅ **Application Generated Successfully**\n\n"
            f"📁 **Files Created:** {output_path}\n\n"
            f"⚠️ **{len(warnings)} Warning(s) Detected:**\n" +
            "\n".join([f"• **{w.category}:** {w.message}" for w in warnings]) +
            "\n\n**Recommendation:** Review these warnings before submitting your application."
        )
    
    else:
        claude_response['claude_action'] = 'show_clean_success'
        claude_response['user_message'] = (
            f"✅ **Application Generated Successfully - No Issues Detected!**\n\n"
            f"📁 **Files Created:** {output_path}\n\n"
            f"🎯 **Validation Results:**\n"
            f"• Pre-generation: {pre_validation.decision} ({pre_validation.confidence_score:.1%} confidence)\n"
            f"• Domain compatibility: ✅ Good alignment\n"
            f"• Content quality: ✅ Passed all checks\n\n"
            f"Your application is ready for submission!"
        )
    
    claude_response['validation_summary'] = validation_summary
    return claude_response

def _handle_failed_generation(result: Dict[str, Any]) -> Dict[str, Any]:
    """Handle failed generation - blocked by validation or errors"""
    
    stage = result.get('stage', 'unknown')
    
    if stage == 'pre_validation':
        # Blocked by pre-generation validation
        validation_result = result.get('validation_result')
        critical_issues = [i for i in validation_result.issues if i.severity == 'critical']
        
        return {
            'claude_action': 'report_domain_mismatch',
            'blocked_reason': result.get('blocked_reason', 'Pre-validation failed'),
            'critical_issues': [
                {'message': issue.message, 'suggestion': issue.suggestion}
                for issue in critical_issues
            ],
            'user_message': (
                "🚫 **Application Generation Blocked**\n\n"
                "**Reason:** Critical domain mismatch detected\n\n" +
                "**Issues Found:**\n" +
                "\n".join([f"• {issue.message}" for issue in critical_issues]) +
                "\n\n**Recommendation:** " +
                "\n".join([f"• {issue.suggestion}" for issue in critical_issues]) +
                "\n\nThis validation prevents potential misrepresentation of your experience."
            )
        }
    
    elif stage == 'user_confirmation':
        return {
            'claude_action': 'report_user_cancellation',
            'cancelled_reason': result.get('cancelled_reason', 'User declined'),
            'user_message': (
                "🚫 **Application Generation Cancelled**\n\n"
                "You chose not to proceed with the validation warnings. "
                "This was the right choice to maintain authenticity in your applications."
            )
        }
    
    else:
        # Technical failure
        return {
            'claude_action': 'report_technical_error',
            'error': result.get('error', 'Unknown error'),
            'stage': stage,
            'user_message': (
                f"❌ **Technical Error During Generation**\n\n"
                f"**Error:** {result.get('error', 'Unknown error')}\n"
                f"**Stage:** {stage}\n\n"
                f"Please try again or check the system logs."
            )
        }

def test_claude_integration():
    """Test the Claude integration with sample data"""
    
    print("🧪 TESTING CLAUDE CODE INTEGRATION")
    print("=" * 60)
    
    # Test 1: Energy trading JD (should be blocked)
    print("\n🔬 TEST 1: Energy Trading JD (should be blocked)")
    energy_jd = """
    Senior Product Manager - Energy Trading Platform
    Support Asset Backed Trading from Tech with the proper data and technological solutions 
    for their trading activities, such as algorithmic trading, market models and other trade initiatives.
    Energy & commodity trading are preferred. Experience in energy markets required.
    """
    
    result1 = claude_generate_application(energy_jd, "netherlands", "Eneco")
    print(f"✅ Result: {result1['claude_action']}")
    print(f"📝 Message: {result1['user_message'][:100]}...")
    
    # Test 2: Regular Product Manager JD (should proceed)
    print("\n🔬 TEST 2: Regular Product Manager JD (should proceed)")
    regular_jd = """
    Senior Product Manager - SaaS Platform
    Lead product development for our enterprise SaaS platform.
    Experience with product management, cross-functional collaboration, and data-driven decisions required.
    """
    
    result2 = claude_generate_application(regular_jd, "netherlands", "TestCompany")
    print(f"✅ Result: {result2['claude_action']}")
    print(f"📝 Message: {result2['user_message'][:100]}...")

# Functions for direct Claude Code usage
def validate_jd_and_generate(jd_text: str, country: str) -> str:
    """
    Simple function for Claude Code to call
    Returns user-friendly message with validation results
    """
    result = claude_generate_application(jd_text, country)
    return result['user_message']

def check_domain_compatibility(jd_text: str) -> Dict[str, Any]:
    """
    Quick domain compatibility check without full generation
    Useful for Claude to give quick feedback before generation
    """
    sys.path.append(str(Path(__file__).parent / 'modules'))
    
    from modules.enhanced_jd_parser import EnhancedJobDescriptionParser
    from modules.pre_generation_validator import PreGenerationValidator
    from modules.real_user_data_extractor import RealUserDataExtractor
    
    try:
        parser = EnhancedJobDescriptionParser()
        validator = PreGenerationValidator()
        extractor = RealUserDataExtractor()
        
        jd_analysis = parser.enhanced_parse(jd_text)
        user_profile = extractor.extract_vinesh_data()
        validation_result = validator.validate_pre_generation(user_profile, jd_analysis)
        
        critical_issues = [i for i in validation_result.issues if i.severity == 'critical']
        warnings = [i for i in validation_result.issues if i.severity == 'warning']
        
        return {
            'compatible': validation_result.should_proceed,
            'decision': validation_result.decision,
            'critical_issues': len(critical_issues),
            'warnings': len(warnings),
            'summary': f"{validation_result.decision} ({validation_result.confidence_score:.1%} confidence)",
            'issues': [{'severity': i.severity, 'message': i.message} for i in validation_result.issues]
        }
        
    except Exception as e:
        return {
            'compatible': False,
            'error': str(e),
            'summary': f"Validation check failed: {str(e)}"
        }

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_claude_integration()
    else:
        print("Claude Code Integration for Validated Application Generation")
        print("=" * 60)
        print("Functions available for Claude Code:")
        print("• claude_generate_application(jd_text, country)")
        print("• validate_jd_and_generate(jd_text, country)")  
        print("• check_domain_compatibility(jd_text)")
        print("\nRun with 'test' argument to run integration tests.")