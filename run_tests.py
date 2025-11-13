#!/usr/bin/env python3
"""
Test runner for Aply Job Application Generator
"""

import unittest
import sys
import os
from pathlib import Path

def run_all_tests():
    """Run all tests and provide detailed results"""
    
    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Discover and run tests
    test_dir = project_root / 'tests'
    loader = unittest.TestLoader()
    
    # Load all test modules
    test_modules = [
        'tests.test_jd_parser',
        'tests.test_resume_generator', 
        'tests.test_country_config',
        'tests.test_integration'
    ]
    
    suite = unittest.TestSuite()
    
    print("🧪 Running Aply Test Suite")
    print("=" * 50)
    
    # Add tests from each module
    for module in test_modules:
        try:
            module_suite = loader.loadTestsFromName(module)
            suite.addTest(module_suite)
            print(f"✅ Loaded tests from {module}")
        except Exception as e:
            print(f"❌ Failed to load {module}: {str(e)}")
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    print(f"\n🚀 Starting test execution...")
    print("-" * 50)
    
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    passed = total_tests - failures - errors - skipped
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failures}")
    print(f"🚫 Errors: {errors}")
    print(f"⏭️  Skipped: {skipped}")
    
    success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    # Show failures and errors
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, failure in result.failures:
            print(f"  - {test}: {failure.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n🚫 ERRORS ({len(result.errors)}):")
        for test, error in result.errors:
            print(f"  - {test}: {error.split('Exception:')[-1].strip()}")
    
    print("\n" + "=" * 50)
    
    if success_rate >= 90:
        print("🎉 Excellent! Tests are passing well.")
    elif success_rate >= 70:
        print("⚠️  Good, but some tests need attention.")
    else:
        print("🚨 Multiple test failures detected. Review needed.")
    
    return result.wasSuccessful()

def run_quick_smoke_test():
    """Run a quick smoke test to verify basic functionality"""
    
    print("🔥 Quick Smoke Test")
    print("-" * 30)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from main import JobApplicationGenerator
        
        # Quick test
        generator = JobApplicationGenerator()
        
        test_jd = "Senior Product Manager with AI experience at TomTom in Amsterdam"
        output_path = generator.generate_application_package(test_jd, "netherlands", "TomTom")
        
        if Path(output_path).exists():
            print("✅ Basic functionality working")
            return True
        else:
            print("❌ Output file not generated")
            return False
            
    except Exception as e:
        print(f"❌ Smoke test failed: {str(e)}")
        return False

if __name__ == "__main__":
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--smoke":
        # Run quick smoke test
        success = run_quick_smoke_test()
        sys.exit(0 if success else 1)
    else:
        # Run full test suite
        success = run_all_tests()
        sys.exit(0 if success else 1)