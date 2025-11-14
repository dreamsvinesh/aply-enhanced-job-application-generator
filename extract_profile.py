#!/usr/bin/env python3
"""
Profile Extraction Script
One-time extraction of comprehensive user profile
"""

import sys
sys.path.append('/Users/vinesh.kumar/Downloads/Aply')

from modules.profile_extractor import ProfileExtractor

def main():
    print("🎯 Comprehensive Profile Extraction")
    print("=" * 50)
    
    extractor = ProfileExtractor()
    
    # Check if profile already exists
    existing = extractor.load_profile()
    if existing:
        print("📋 Existing profile found:")
        print(extractor.get_profile_summary())
        
        overwrite = input("\nDo you want to extract a new profile? This will backup the existing one. (y/N): ")
        if overwrite.lower() != 'y':
            print("✅ Keeping existing profile. Use existing data for applications.")
            return
    
    print("\n📝 Profile Extraction Instructions:")
    print("To create your comprehensive profile, please provide information about:")
    print("• Your professional experience and roles")
    print("• Key projects you've worked on with specific results")
    print("• Technologies and skills you've developed")
    print("• Quantified achievements (metrics, revenue impact, etc.)")
    print("• Education and certifications")
    print("\nYou can provide this as:")
    print("1. Copy-paste from your resume or CV")
    print("2. Claude Skills conversation history")
    print("3. Free-form description of your background")
    print("4. LinkedIn profile content")
    
    print("\n" + "="*50)
    print("Please paste your professional information below.")
    print("Press Enter twice when done, or type 'quit' to exit:")
    print("="*50)
    
    # Collect input
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if line.strip().lower() == 'quit':
                print("❌ Extraction cancelled.")
                return
            
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
            
            lines.append(line)
        except KeyboardInterrupt:
            print("\n❌ Extraction cancelled.")
            return
    
    user_input = "\n".join(lines).strip()
    
    if not user_input:
        print("❌ No input provided. Extraction cancelled.")
        return
    
    print(f"\n🔄 Processing {len(user_input)} characters of profile data...")
    
    # Extract profile
    result = extractor.extract_and_save(user_input)
    
    if result.success:
        print(f"\n🎉 SUCCESS! Profile extracted and saved.")
        print(f"💰 Cost: ${result.extraction_cost:.4f}")
        print(f"🎯 Confidence: {result.confidence_score:.1%}")
        print("\n📊 Profile Summary:")
        print(extractor.get_profile_summary())
        
        print(f"\n✅ Your comprehensive profile is now ready!")
        print("🔄 You can now generate tailored applications using the LLM-powered system.")
        
        # Show what was extracted
        profile = extractor.load_profile()
        if profile:
            domains = profile.get('experience_domains', {})
            projects = profile.get('detailed_projects', [])
            
            print(f"\n📋 Extracted Data Summary:")
            print(f"   • Experience domains: {', '.join(domains.keys())}")
            print(f"   • Detailed projects: {len(projects)}")
            print(f"   • Skills categories: {len(profile.get('skills_detailed', {}))}")
            print(f"   • Quantified achievements: {len(profile.get('achievements_quantified', []))}")
        
    else:
        print(f"\n❌ FAILED! Profile extraction unsuccessful.")
        print("Errors encountered:")
        for error in result.errors:
            print(f"   • {error}")
        
        if result.extraction_cost > 0:
            print(f"💰 Cost incurred: ${result.extraction_cost:.4f}")
            
        print("\n🔧 Troubleshooting:")
        print("1. Check that API keys are set correctly")
        print("2. Ensure the input data contains enough detail")
        print("3. Try providing more structured information")

if __name__ == "__main__":
    main()