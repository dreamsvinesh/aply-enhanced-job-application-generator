#!/usr/bin/env python3
"""
System Validation Script
Comprehensive validation of all interconnected components after project mixing fixes
"""

import sys
import traceback
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def print_header(title: str):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def print_test(name: str, status: str, details: str = ""):
    """Print test result"""
    symbol = "✅" if status == "PASS" else "❌"
    print(f"{symbol} {name}: {status}")
    if details:
        print(f"   {details}")

def validate_module_imports():
    """Test 1: Validate all module imports"""
    print_header("MODULE IMPORTS VALIDATION")
    
    modules_to_test = [
        ('enhanced_fact_aware_generator', 'EnhancedFactAwareGenerator'),
        ('real_user_data_extractor', 'RealUserDataExtractor'),
        ('adlina_style_guide', 'AdlinaStyleGuide'),
        ('content_depth_validator', 'ContentDepthValidator'),
        ('human_writing_validator', 'HumanWritingValidator'),
        ('llm_service', 'LLMService'),
        ('workflow_validation_agent', None)  # Module only, no specific class
    ]
    
    results = []
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(f'modules.{module_name}', fromlist=[class_name] if class_name else [''])
            if class_name:
                getattr(module, class_name)
            print_test(f"modules.{module_name}", "PASS")
            results.append(True)
        except Exception as e:
            print_test(f"modules.{module_name}", "FAIL", str(e))
            results.append(False)
    
    return all(results)

def validate_project_separation():
    """Test 2: Validate project separation is working"""
    print_header("PROJECT SEPARATION VALIDATION")
    
    try:
        from modules.adlina_style_guide import AdlinaStyleGuide
        
        # Test cases
        test_cases = [
            {
                'name': 'Bad mixing (AI + F&B in one sentence)',
                'content': 'Built AI-powered RAG system achieving 94% accuracy while generating €20-22M annual GMV through F&B platform optimization.',
                'should_fail': True
            },
            {
                'name': 'Good separation (separate sentences)',
                'content': 'Built AI-powered RAG system achieving 94% accuracy with sub-second response times. Led F&B platform scaling generating €20-22M annual GMV.',
                'should_fail': False
            },
            {
                'name': 'Current professional summary',
                'content': 'Senior Product Manager with 6+ years scaling digital platforms serving 600,000+ users. Built AI-powered RAG system achieving 94% accuracy with sub-second response times. Led F&B platform scaling across 24 business parks, generating €20-22M annual GMV from 1,330 to 30,000+ daily orders. Specialized in automation and enterprise integration—reducing contract activation from 42 days to 10 minutes and accelerating invoicing from 21 days to real-time through Salesforce-SAP integration.',
                'should_fail': False
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            result = AdlinaStyleGuide.check_project_mixing(test_case['content'])
            has_mixing = result['has_mixing']
            
            if test_case['should_fail']:
                # Should detect mixing
                if has_mixing:
                    print_test(test_case['name'], "PASS", "Correctly detected project mixing")
                else:
                    print_test(test_case['name'], "FAIL", "Failed to detect project mixing")
                    all_passed = False
            else:
                # Should NOT detect mixing
                if not has_mixing:
                    print_test(test_case['name'], "PASS", "No project mixing detected (correct)")
                else:
                    print_test(test_case['name'], "FAIL", f"False positive: {result['violations']}")
                    all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("Project separation validation", "FAIL", f"Error: {e}")
        traceback.print_exc()
        return False

def validate_user_data_extraction():
    """Test 3: Validate user data extraction"""
    print_header("USER DATA EXTRACTION VALIDATION")
    
    try:
        from modules.real_user_data_extractor import RealUserDataExtractor
        
        extractor = RealUserDataExtractor()
        data = extractor.extract_vinesh_data()
        
        # Critical validation checks
        checks = [
            ('personal_info' in data, "Personal info present"),
            ('work_experience' in data, "Work experience present"),
            (len(data['work_experience']) == 3, f"3 work experiences (found {len(data['work_experience'])})"),
            ('project_documentation' in data, "Project documentation present"),
            ('professional_summary' in data, "Professional summary present")
        ]
        
        all_passed = True
        for condition, description in checks:
            if condition:
                print_test(description, "PASS")
            else:
                print_test(description, "FAIL")
                all_passed = False
        
        # Check summary content
        summary = data['professional_summary']['description']
        
        # Critical content checks
        content_checks = [
            ('94% accuracy with sub-second' in summary, "AI RAG project properly referenced"),
            ('F&B platform scaling' in summary, "F&B project properly referenced"),
            ('Salesforce-SAP integration' in summary, "Salesforce project properly referenced"),
            ('94% accuracy while generating' not in summary, "No project mixing in summary"),
            ('innovative' not in summary.lower(), "No forbidden generic words"),
            ('transformative' not in summary.lower(), "No forbidden generic words")
        ]
        
        for condition, description in content_checks:
            if condition:
                print_test(description, "PASS")
            else:
                print_test(description, "FAIL")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("User data extraction", "FAIL", f"Error: {e}")
        traceback.print_exc()
        return False

def validate_currency_conversion():
    """Test 4: Validate currency conversion"""
    print_header("CURRENCY CONVERSION VALIDATION")
    
    try:
        from modules.real_user_data_extractor import RealUserDataExtractor
        
        extractor = RealUserDataExtractor()
        
        # Test different currencies
        test_text = 'Generated ₹168-180 crores annual GMV and added ₹1.5/sq ft revenue'
        
        currency_tests = [
            ('denmark', '€', 'EUR'),
            ('usa', '$', 'USD'),
            ('uk', '£', 'GBP'),
            ('singapore', 'SGD', 'SGD')
        ]
        
        all_passed = True
        for country, symbol, currency_name in currency_tests:
            result = extractor.convert_currency_for_country(test_text, country)
            
            if symbol in result and '₹' not in result:
                print_test(f"{country.title()} ({currency_name})", "PASS", f"Converted to {symbol}")
            else:
                print_test(f"{country.title()} ({currency_name})", "FAIL", f"Conversion failed: {result}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("Currency conversion", "FAIL", f"Error: {e}")
        traceback.print_exc()
        return False

def validate_adlina_style_compliance():
    """Test 5: Validate Adlina style compliance"""
    print_header("ADLINA STYLE COMPLIANCE VALIDATION")
    
    try:
        from modules.adlina_style_guide import AdlinaStyleGuide
        
        # Test summary validation using actual current summary
        from modules.real_user_data_extractor import RealUserDataExtractor
        extractor = RealUserDataExtractor()
        data = extractor.extract_vinesh_data()
        good_summary = data['professional_summary']['description']
        
        bad_summary = "Innovative product leader with extensive experience in leveraging cutting-edge technologies to drive transformative business outcomes and optimize organizational performance."
        
        # Test good summary
        good_result = AdlinaStyleGuide.validate_summary(good_summary)
        if good_result['is_valid']:
            print_test("Good summary validation", "PASS", "Valid Adlina-style summary")
        else:
            print_test("Good summary validation", "FAIL", f"Issues: {good_result['issues']}")
        
        # Test bad summary
        bad_result = AdlinaStyleGuide.validate_summary(bad_summary)
        if not bad_result['is_valid']:
            print_test("Bad summary detection", "PASS", "Correctly identified generic language")
        else:
            print_test("Bad summary detection", "FAIL", "Failed to catch generic language")
        
        # Test forbidden words detection
        forbidden_count = len(AdlinaStyleGuide.FORBIDDEN_GENERIC_WORDS)
        action_verbs_count = len(AdlinaStyleGuide.PREFERRED_ACTION_VERBS)
        
        print_test("Forbidden words list", "PASS" if forbidden_count > 20 else "FAIL", 
                  f"{forbidden_count} forbidden words defined")
        print_test("Action verbs list", "PASS" if action_verbs_count > 15 else "FAIL", 
                  f"{action_verbs_count} action verbs defined")
        
        return good_result['is_valid'] and not bad_result['is_valid']
        
    except Exception as e:
        print_test("Adlina style validation", "FAIL", f"Error: {e}")
        traceback.print_exc()
        return False

def validate_enhanced_generator_integration():
    """Test 6: Validate enhanced generator integration"""
    print_header("ENHANCED GENERATOR INTEGRATION VALIDATION")
    
    try:
        from modules.enhanced_fact_aware_generator import EnhancedFactAwareGenerator
        
        # Test initialization
        generator = EnhancedFactAwareGenerator(enable_brutal_validation=False)
        
        # Check critical components
        checks = [
            (hasattr(generator, 'user_extractor'), "User extractor connected"),
            (hasattr(generator, 'depth_validator'), "Depth validator connected"),
            (hasattr(generator, 'llm_service'), "LLM service connected"),
            (hasattr(generator, 'ats_optimizer'), "ATS optimizer connected")
        ]
        
        all_passed = True
        for condition, description in checks:
            if condition:
                print_test(description, "PASS")
            else:
                print_test(description, "FAIL")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("Enhanced generator integration", "FAIL", f"Error: {e}")
        traceback.print_exc()
        return False

def validate_file_generation():
    """Test 7: Validate file generation capabilities"""
    print_header("FILE GENERATION VALIDATION")
    
    try:
        # Check if key application generators exist
        generators = [
            'generate_hellofresh_copenhagen_application.py',
            'generate_universal_application.py'
        ]
        
        all_passed = True
        for generator in generators:
            file_path = Path(generator)
            if file_path.exists():
                print_test(f"{generator}", "PASS", "Generator file exists")
            else:
                print_test(f"{generator}", "FAIL", "Generator file missing")
                all_passed = False
        
        # Check output directory structure
        output_dir = Path('output')
        if output_dir.exists():
            print_test("Output directory", "PASS", f"Exists with {len(list(output_dir.iterdir()))} subdirectories")
        else:
            print_test("Output directory", "FAIL", "Missing output directory")
            all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("File generation validation", "FAIL", f"Error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run comprehensive system validation"""
    print("🚀 COMPREHENSIVE SYSTEM VALIDATION")
    print("=" * 60)
    print(f"📅 Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Purpose: Validate all changes after project mixing fixes")
    
    # Run all validation tests
    test_results = []
    
    test_results.append(("Module Imports", validate_module_imports()))
    test_results.append(("Project Separation", validate_project_separation()))
    test_results.append(("User Data Extraction", validate_user_data_extraction()))
    test_results.append(("Currency Conversion", validate_currency_conversion()))
    test_results.append(("Adlina Style Compliance", validate_adlina_style_compliance()))
    test_results.append(("Enhanced Generator Integration", validate_enhanced_generator_integration()))
    test_results.append(("File Generation", validate_file_generation()))
    
    # Print summary
    print_header("VALIDATION SUMMARY")
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! System is ready for git commit.")
        return True
    else:
        print("⚠️  Some tests failed. Please review and fix before committing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)