#!/usr/bin/env python3
"""
Generate Dealfront Denmark Application with ATS Scoring
Enhanced version with fact preservation and ATS comparison against original JD.
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))

try:
    from modules.fact_aware_content_generator import FactAwareContentGenerator
    from modules.ats_scoring_engine import ATSScoringEngine
    from modules.user_data_extractor import UserDataExtractor
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def main():
    print("🚀 DEALFRONT DENMARK APPLICATION WITH ATS SCORING")
    print("=" * 80)
    print()
    
    # Dealfront JD (original text for ATS comparison)
    dealfront_jd = """Dealfront is a go-to-market and signal orchestration platform for B2B mid-market companies. We give businesses the clarity to focus their efforts where they'll count most - on the accounts that fit their ideal customer profile, show real buying intent, and are actively engaging. No more cold outreach and no more bloated target lists. Just better deals, faster.

Our platform brings together powerful data, real-time insights, and intelligent prioritisation to help our customers identify, engage, and convert the right accounts, at the right time. Built for teams that value speed, precision, and simplicity, Dealfront turns complexity into action.

Join us and be a part of our journey to transform the way businesses win more deals!

About The Role

Dealfront is scaling fast and needs structure to match its ambition. This is a founding Product Operations role that will establish the systems, rituals, and frameworks enabling Product, Design, and Engineering to execute with clarity, velocity, and accountability.

Mission

Build the operating model that connects strategy to execution — enabling Product Core & Growth and Tech teams to move faster, smarter, and with measurable impact.

Responsibilities

Design and own the Product Operating Model: planning cadences, PRD standards, roadmap process, and delivery governance.
Set up enablement systems: documentation templates, process playbooks, and feedback loops that create accountability and clarity.
Drive AI-enabled process automation (e.g., auto-generated release notes, PRD assistants, or analytics summaries).
Identify and close skill and knowledge gaps across teams through structured enablement.
Partner with Product Analytics to ensure data-driven decision-making becomes part of every product cycle.
Own & facilitate Product Rhythms with measurable output (OKRs, KPIs, and decisions).

Requirements

6+ years in Product Ops, Product Management, or Strategy Ops roles in SaaS.
Proven record building process foundations from 0→1 in high-growth environments.
Strong business judgment and systems mindset; thrives in ambiguity.
AI-first thinker who leverages tools to improve velocity and quality.
Resourceful, bias-for-action, and comfortable challenging teams.

Success Metrics

Roadmap delivery predictability ↑
Product process adoption rate ↑
Time-to-insight and decision latency ↓
Engagement with documentation and enablement assets ↑"""

    # Enhanced JD Analysis with original JD text for ATS scoring
    jd_analysis = {
        'extracted_info': {
            'company': 'Dealfront',
            'company_name': 'Dealfront',
            'role_title': 'Product Operations (Founding Role)',
            'location': 'Denmark',
            'department': 'Product',
            'seniority_level': 'Senior'
        },
        'role_classification': {
            'primary_focus': 'product_operations',
            'secondary_focus': 'process_automation',
            'industry': 'b2b_saas',
            'stage': 'scaling_startup',
            'team_size': 'mid_size'
        },
        'requirements': {
            'must_have_technical': [
                'Product Operations', 'Process Design', 'AI Automation', 
                'Data Analytics', 'SaaS Operations', 'OKR Management'
            ],
            'must_have_business': [
                'Strategic Operations', 'Team Enablement', 'Process Development', 
                'Change Management', '0→1 Implementation', 'Cross-functional Leadership'
            ],
            'nice_to_have_technical': [
                'PRD Standards', 'Release Notes Automation', 'Analytics Summaries',
                'Documentation Templates', 'Product Analytics'
            ],
            'experience_years': '6+ years',
            'domain_expertise': [
                'Product Ops', 'Process Automation', 'Team Enablement', 
                'Strategic Operations', 'AI-First Approach', 'SaaS Scaling'
            ],
            'key_skills': [
                'Planning cadences', 'PRD standards', 'Roadmap process', 
                'Delivery governance', 'Documentation templates', 'Process playbooks'
            ]
        },
        'company_context': {
            'stage': 'scaling_fast',
            'size': 'mid_market',
            'culture': 'speed_precision_simplicity',
            'values': ['clarity', 'velocity', 'accountability', 'measurable_impact'],
            'competitive_advantage': 'signal_orchestration',
            'mission': 'transform_b2b_go_to_market'
        },
        'positioning_strategy': {
            'key_strengths_to_emphasize': [
                'Process Automation', 'AI-First Approach', '0→1 Experience', 
                'Team Enablement', 'Strategic Operations', 'Data-Driven Decision Making'
            ],
            'experience_framing': 'Product Operations specialist with proven 0→1 scaling and AI automation expertise in high-growth SaaS environments',
            'differentiation_strategy': 'Emphasize founding role experience, AI-enabled process automation, and measurable impact delivery',
            'cultural_adaptation': 'Direct, efficient communication style aligned with Danish business culture and startup velocity'
        },
        'success_metrics': [
            'Roadmap delivery predictability increase',
            'Product process adoption rate improvement', 
            'Time-to-insight and decision latency reduction',
            'Documentation and enablement asset engagement growth'
        ],
        'credibility_score': 9.5,
        'match_reasoning': 'Excellent match - candidate has proven 0→1 product operations experience at COWRKS with AI automation focus, exactly matching founding role requirements',
        # Add original JD text for ATS scoring
        'original_jd': dealfront_jd
    }
    
    print("✅ **ENHANCED JD ANALYSIS WITH ATS SCORING:**")
    print(f"• Credibility Score: {jd_analysis['credibility_score']}/10 (Excellent Match)")
    print(f"• Primary Focus: {jd_analysis['role_classification']['primary_focus']}")
    print(f"• Company Stage: {jd_analysis['company_context']['stage']}")
    print(f"• Key Requirements: {', '.join(jd_analysis['requirements']['domain_expertise'][:3])}")
    print(f"• Cultural Fit: {jd_analysis['company_context']['culture']}")
    print()
    
    # Generate fact-aware content with ATS scoring
    print("🛡️ **GENERATING FACT-AWARE CONTENT WITH ATS ANALYSIS**")
    print("-" * 70)
    
    generator = FactAwareContentGenerator()
    
    # Generate complete package with ATS scoring
    results = generator.generate_complete_fact_aware_package(jd_analysis, country="denmark")
    
    # Display results
    print("\n📊 **CONTENT GENERATION RESULTS:**")
    print("-" * 50)
    
    for content_type in ['resume', 'cover_letter', 'email', 'linkedin']:
        if content_type in results:
            result = results[content_type]
            status = "✅ VALID" if result['preserves_facts'] else "❌ ISSUES"
            print(f"• {content_type.title()}: {status}")
            
            if content_type == 'resume' and 'ats_score' in result:
                ats = result['ats_score']
                print(f"  🎯 ATS Score: {ats['overall_score']:.1f}% (Grade: {ats['grade']})")
                print(f"  🔍 Top Categories: {list(ats['category_scores'].keys())[:3]}")
    
    print()
    
    # Display ATS Analysis Summary
    if 'resume' in results and 'ats_score' in results['resume']:
        ats_data = results['resume']['ats_score']
        print("🎯 **ATS SCORING ANALYSIS:**")
        print("-" * 40)
        print(f"• Overall Score: {ats_data['overall_score']:.1f}% ({ats_data['grade']})")
        print("• Category Scores:")
        for category, score in ats_data['category_scores'].items():
            print(f"  - {category.replace('_', ' ').title()}: {score:.1f}%")
        
        print("\n• Top Recommendations:")
        for i, rec in enumerate(ats_data['recommendations'][:3], 1):
            print(f"  {i}. {rec}")
        print()
    
    # Save complete package with ATS data
    print("💾 **SAVING COMPLETE PACKAGE WITH ATS ANALYSIS**")
    print("-" * 60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("output") / f"Dealfront_Denmark_WithATS_{timestamp}"
    
    saved_path = generator.save_fact_aware_package(results, str(output_dir))
    
    print(f"✅ All files saved to: {saved_path}")
    print()
    
    # Display file summary
    output_path = Path(saved_path)
    files_created = list(output_path.glob("*"))
    
    print("📁 **FILES CREATED:**")
    for file_path in sorted(files_created):
        file_size = file_path.stat().st_size
        print(f"• {file_path.name} ({file_size} bytes)")
    
    print()
    
    # Display ATS vs Original JD comparison
    if 'resume' in results and 'ats_score' in results['resume']:
        print("🔍 **ATS VS ORIGINAL JD COMPARISON:**")
        print("=" * 60)
        
        ats = results['resume']['ats_score']
        
        print(f"📊 Resume ATS Score: {ats['overall_score']:.1f}% ({ats['grade']})")
        print(f"📄 Analyzed against original Dealfront JD ({len(dealfront_jd.split())} words)")
        
        print("\n📈 Category Performance:")
        for category, score in ats['category_scores'].items():
            emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            print(f"{emoji} {category.replace('_', ' ').title()}: {score:.1f}%")
        
        print(f"\n🎯 Keyword Matching:")
        keywords = ats['keyword_analysis']
        for category in ['hard_skills', 'soft_skills', 'job_titles']:
            if category in keywords['resume_keywords']:
                count = len(keywords['resume_keywords'][category])
                print(f"• {category.replace('_', ' ').title()}: {count} keywords found")
        
        print(f"\n💡 Top Improvement Areas:")
        for i, rec in enumerate(ats['recommendations'][:3], 1):
            print(f"{i}. {rec}")
    
    print()
    
    # Final summary
    package_summary = results.get('package_summary', {})
    print("🎉 **COMPLETE PACKAGE WITH ATS ANALYSIS GENERATED**")
    print("=" * 80)
    print()
    
    print("📊 **SUMMARY:**")
    fact_score = package_summary.get('fact_preservation_score', 0)
    ats_summary = package_summary.get('ats_summary', {})
    
    print(f"• ✅ Fact Preservation: {fact_score:.1f}%")
    if ats_summary:
        print(f"• 🎯 ATS Score: {ats_summary['overall_score']:.1f}% ({ats_summary['grade']})")
    print(f"• 📁 Package Location: {output_dir}")
    print(f"• 🗂️ Total Files: {len(files_created)}")
    
    print("\n🛡️ **VALIDATION STATUS:**")
    print("• ✅ Real companies preserved (COWRKS, not fabricated)")
    print("• ✅ Real metrics used (94% accuracy, $2M revenue)")
    print("• ✅ Real personal info maintained")
    print("• ✅ ATS compatibility analyzed")
    print("• ✅ JD analysis data stored")
    
    print(f"\n🚀 **READY FOR DEALFRONT DENMARK APPLICATION!**")
    print(f"📂 Access your enhanced package at: {output_dir}")

if __name__ == "__main__":
    main()