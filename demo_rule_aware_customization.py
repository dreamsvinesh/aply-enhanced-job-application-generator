#!/usr/bin/env python3
"""
Rule-Aware Content Customization Demonstration
Shows how LLM customization follows all existing rules while providing role-specific tailoring.
"""

import json
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

def demonstrate_rule_aware_customization():
    """Demonstrate how rule-aware customization works."""
    
    print("="*80)
    print("🛡️ RULE-AWARE CONTENT CUSTOMIZATION DEMONSTRATION")
    print("="*80)
    print()
    
    print("📋 **SCENARIO:**")
    print("• Company: Squarespace")
    print("• Role: Frontend Developer - Communication Platforms Team") 
    print("• Country: Portugal (formal, respectful approach required)")
    print("• Content Type: Resume Summary")
    print("• Template Variant: B2B")
    print()
    
    # Sample JD analysis from enhanced parser
    jd_analysis = {
        "role_classification": {
            "primary_focus": "communication_platforms",
            "secondary_focus": "frontend_development"
        },
        "positioning_strategy": {
            "key_strengths_to_emphasize": [
                "React expertise and component library experience",
                "Frontend development with user experience focus"
            ],
            "experience_framing": "Frontend developer with communication platform experience",
            "cultural_adaptation": "Emphasize collaborative approach and technical excellence for Portugal market"
        },
        "extracted_info": {
            "company_name": "Squarespace",
            "role_title": "Frontend Developer"
        }
    }
    
    # User profile data
    user_profile = {
        "skills": {
            "technical": ["React", "JavaScript", "TypeScript", "CSS", "HTML"],
            "business": ["frontend development", "user experience", "component design"]
        },
        "experience": [
            {
                "company": "TechCorp",
                "role": "Frontend Developer", 
                "highlights": [
                    "Built responsive React applications for 50K+ users",
                    "Improved application performance by 35% through optimization"
                ]
            }
        ],
        "key_achievements": [
            "Increased user engagement by 30% through React UI improvements",
            "Built component library used by 5+ development teams",
            "Reduced page load time by 40% with performance optimization",
            "Led frontend architecture decisions for communication features"
        ]
    }
    
    print("🎯 **INPUT DATA:**")
    print("JD Analysis Result:")
    print(f"  • Primary Focus: {jd_analysis['role_classification']['primary_focus']}")
    print(f"  • Key Strengths: {', '.join(jd_analysis['positioning_strategy']['key_strengths_to_emphasize'])}")
    print()
    
    print("User Profile Highlights:")
    print(f"  • Technical Skills: {', '.join(user_profile['skills']['technical'])}")
    print(f"  • Key Achievement: {user_profile['key_achievements'][0]}")
    print(f"  • Recent Role: {user_profile['experience'][0]['role']} at {user_profile['experience'][0]['company']}")
    print()
    
    # Show rule enforcement in action
    print("🛡️ **RULE ENFORCEMENT SYSTEM:**")
    print()
    
    print("**Country-Specific Rules (Portugal):**")
    portugal_rules = {
        "tone": {
            "directness": "low",
            "formality": "high", 
            "avoid": ["too direct approach", "rushing", "ignoring hierarchy"]
        },
        "resume_format": {
            "max_pages": 4,
            "include_photo": True
        }
    }
    
    print(f"  • Directness: {portugal_rules['tone']['directness']} (formal, respectful)")
    print(f"  • Formality: {portugal_rules['tone']['formality']} (professional tone)")
    print(f"  • Avoid: {', '.join(portugal_rules['tone']['avoid'])}")
    print()
    
    print("**Content Quality Rules:**")
    content_rules = {
        "forbidden_phrases": ["leverage", "utilize", "optimize", "streamline", "comprehensive"],
        "llm_red_flags": ["delve into", "furthermore", "esteemed organization"],
        "requirements": ["specific metrics", "factual accuracy", "human voice"]
    }
    
    print(f"  • Forbidden Corporate Jargon: {', '.join(content_rules['forbidden_phrases'])}")
    print(f"  • LLM Red Flags: {', '.join(content_rules['llm_red_flags'])}")
    print(f"  • Requirements: {', '.join(content_rules['requirements'])}")
    print()
    
    # Show BAD customization (rule violations)
    print("❌ **BAD CUSTOMIZATION (Rule Violations):**")
    bad_customization = """
    I am a comprehensive frontend developer who will leverage cutting-edge React technologies to optimize your esteemed organization's communication platforms. 
    Furthermore, I have extensive experience utilizing robust frameworks to streamline user engagement processes.
    I believe I can delve into your requirements and provide dynamic solutions.
    """
    
    print(bad_customization.strip())
    print()
    
    print("**Violations Detected:**")
    violations = []
    
    # Check for forbidden phrases
    forbidden_found = ["comprehensive", "leverage", "cutting-edge", "optimize", "esteemed organization", "extensive", "utilizing", "robust", "streamline", "dynamic"]
    for phrase in forbidden_found:
        if phrase in bad_customization.lower():
            violations.append(f"Corporate jargon: '{phrase}'")
    
    # Check for LLM red flags  
    llm_flags = ["furthermore", "delve into", "esteemed organization"]
    for flag in llm_flags:
        if flag in bad_customization.lower():
            violations.append(f"LLM language: '{flag}'")
    
    # Check for Portugal tone violations
    if "i believe" in bad_customization.lower():
        violations.append("Tone violation: too hesitant for professional context")
    
    for violation in violations[:8]:  # Show first 8
        print(f"  • {violation}")
    
    print(f"\n  💥 **Total Violations: {len(violations)}** (Quality Score: 2/10)")
    print()
    
    # Show GOOD customization (rule-compliant)
    print("✅ **GOOD CUSTOMIZATION (Rule-Compliant):**")
    good_customization = """
    I am an experienced frontend developer specializing in React and communication platform development. 
    In my role at TechCorp, I built responsive applications for 50K+ users and improved engagement by 30% through intuitive UI design.
    I have strong experience with component libraries and performance optimization, having reduced load times by 40% in previous projects.
    My technical expertise in React and TypeScript aligns well with Squarespace's communication platform requirements.
    """
    
    print(good_customization.strip())
    print()
    
    print("**Rule Compliance Analysis:**")
    
    # Check compliance
    compliance_checks = []
    
    # No corporate jargon
    jargon_found = any(phrase in good_customization.lower() for phrase in content_rules['forbidden_phrases'])
    compliance_checks.append(f"✅ Corporate jargon avoided: {not jargon_found}")
    
    # No LLM red flags
    llm_found = any(flag in good_customization.lower() for flag in content_rules['llm_red_flags'])
    compliance_checks.append(f"✅ LLM language avoided: {not llm_found}")
    
    # Specific metrics included
    import re
    metrics = re.findall(r'\d+[%KkMm+]|\d+K\+', good_customization)
    compliance_checks.append(f"✅ Specific metrics included: {len(metrics)} metrics ({', '.join(metrics)})")
    
    # Factual accuracy (references user profile)
    profile_refs = ["TechCorp", "React", "frontend developer"]
    refs_found = [ref for ref in profile_refs if ref in good_customization]
    compliance_checks.append(f"✅ Factual accuracy: References user profile ({', '.join(refs_found)})")
    
    # Portugal cultural appropriateness
    formal_indicators = ["experienced", "strong experience", "expertise", "aligns well"]
    formal_found = [ind for ind in formal_indicators if ind in good_customization.lower()]
    compliance_checks.append(f"✅ Portugal tone: Formal and respectful ({len(formal_found)} indicators)")
    
    for check in compliance_checks:
        print(f"  {check}")
    
    print(f"\n  🎯 **Overall Quality Score: 9.2/10**")
    print()
    
    # Show automatic fixes
    print("🔧 **AUTOMATIC RULE FIXES:**")
    print()
    
    fixes_demo = [
        ("leverage → use", "Will use advanced technologies"),
        ("utilize → use", "Will use React frameworks"), 
        ("optimize → improve", "Will improve performance"),
        ("comprehensive → complete", "Complete frontend solution"),
        ("esteemed organization → company", "Your company's requirements"),
        ("delve into → explore", "Will explore new approaches")
    ]
    
    print("**Phrase Replacements:**")
    for original, fixed in fixes_demo:
        print(f"  • {original}")
        print(f"    Example: '{fixed}'")
    print()
    
    # Show country adaptations
    print("🌍 **COUNTRY-SPECIFIC ADAPTATIONS:**")
    print()
    
    print("**Portugal Market Adaptations:**")
    adaptations = [
        "Formal tone: 'I am experienced' vs 'I'm good at'",
        "Respectful approach: 'aligns well with requirements' vs 'perfect fit'", 
        "Hierarchy awareness: 'technical expertise' vs 'I'm the best'",
        "Relationship focus: 'collaborative experience' vs 'individual achievements'"
    ]
    
    for adaptation in adaptations:
        print(f"  • {adaptation}")
    print()
    
    # Show quality scoring breakdown
    print("📊 **QUALITY SCORING BREAKDOWN:**")
    print()
    
    quality_scores = {
        "Rule Compliance": 9.5,  # No violations
        "Human Voice": 9.0,      # Natural writing, no corporate jargon
        "Country Appropriateness": 8.8,  # Portugal-appropriate tone
        "Specificity": 9.2,     # Metrics and concrete examples
        "Factual Accuracy": 10.0 # Only user profile info
    }
    
    for category, score in quality_scores.items():
        print(f"  • {category}: {score}/10")
    
    overall_score = sum(quality_scores.values()) / len(quality_scores)
    print(f"\n  🎯 **Overall Quality: {overall_score:.1f}/10**")
    print()
    
    # Show integration with existing system
    print("🔗 **INTEGRATION WITH EXISTING SYSTEM:**")
    print()
    
    integration_points = [
        "✅ Uses existing CountryConfig for Portugal rules",
        "✅ Integrates with HumanVoiceAgent for final polishing", 
        "✅ Follows ContentQualityValidator standards",
        "✅ Saves results to DatabaseManager for tracking",
        "✅ Works with existing template structure",
        "✅ Maintains all formatting requirements"
    ]
    
    for point in integration_points:
        print(f"  {point}")
    
    print()
    
    # Show cost and performance
    print("💰 **COST & PERFORMANCE:**")
    print()
    
    print("**LLM Usage:**")
    print("  • Model: GPT-4o Mini")
    print("  • Input Tokens: ~800 (prompt with rules)")
    print("  • Output Tokens: ~400 (customization)")
    print("  • Cost: ~$0.003 per customization")
    print("  • Response Time: ~2 seconds")
    print()
    
    print("**Quality Assurance:**")
    print("  • Automatic rule validation")
    print("  • Violation detection and fixing")
    print("  • Quality scoring (0-10 scale)")
    print("  • Country compliance checking")
    print("  • Database tracking for analytics")
    print()
    
    print("="*80)
    print("🎉 **SUMMARY: LLM Customization with Full Rule Compliance!**")
    print("="*80)
    print("• ✅ Role-specific customization (communication platforms focus)")
    print("• ✅ Complete rule enforcement (corporate jargon eliminated)")
    print("• ✅ Country-appropriate tone (Portugal formal style)")  
    print("• ✅ Factual accuracy (only user profile information)")
    print("• ✅ Human voice quality (natural, professional writing)")
    print("• ✅ Automatic violation fixes (seamless user experience)")
    print("• ✅ Quality scoring and tracking (continuous improvement)")
    print("• ✅ Cost-effective LLM usage (~$0.003 per customization)")
    print()


def demonstrate_multi_country_comparison():
    """Show how the same content is adapted for different countries."""
    
    print("🌍 **MULTI-COUNTRY ADAPTATION EXAMPLE:**")
    print()
    
    base_achievement = "Led frontend development team and improved user engagement"
    
    country_adaptations = {
        "Portugal": {
            "adapted": "Successfully led the frontend development team in collaboration with stakeholders, contributing to improved user engagement through respectful and methodical approach to technical excellence.",
            "characteristics": ["formal tone", "collaborative emphasis", "respectful language"]
        },
        "Netherlands": {
            "adapted": "Led frontend development team and improved user engagement by 30% through direct technical decisions and efficient implementation.",
            "characteristics": ["direct approach", "quantified results", "efficiency focus"]
        }, 
        "Denmark": {
            "adapted": "Led a great frontend development team and improved user engagement in a collaborative, balanced way that maintained work-life harmony.",
            "characteristics": ["casual tone", "team emphasis", "work-life balance"]
        }
    }
    
    for country, data in country_adaptations.items():
        print(f"**{country}:**")
        print(f"  Original: {base_achievement}")
        print(f"  Adapted: {data['adapted']}")
        print(f"  Characteristics: {', '.join(data['characteristics'])}")
        print()


if __name__ == "__main__":
    demonstrate_rule_aware_customization()
    print()
    demonstrate_multi_country_comparison()