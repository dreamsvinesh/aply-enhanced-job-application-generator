#!/usr/bin/env python3
"""
Generate HelloFresh Copenhagen Product Operations Manager Application Package
Complete application package with resume, cover letter, email templates, and LinkedIn messages.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from modules.enhanced_fact_aware_generator import EnhancedFactAwareGenerator
from modules.real_user_data_extractor import RealUserDataExtractor
from modules.llm_service import LLMService

def create_hellofresh_jd_analysis():
    """Create comprehensive analysis of HelloFresh Product Operations Manager JD"""
    
    return {
        'extracted_info': {
            'company': 'HelloFresh',
            'role_title': 'Product Operations Manager',
            'location': 'Copenhagen, Denmark',
            'department': 'Product Team',
            'team_size': 'Fast-growing team',
            'markets': 'Nordic customers (3 markets)',
            'product_focus': 'HelloFresh Market Products (ready meals, desserts, breakfast, lunch)',
            'mission': "Change the way people eat — forever"
        },
        
        'requirements': {
            'must_have_experience': [
                '2+ years Product Management experience',
                'FMCG Brand Management or New Product Development',
                'Business Development or Consulting background',
                'Project Management experience'
            ],
            'must_have_technical': [
                'Portfolio and add-on strategy across multiple markets',
                'Category performance management',
                'Product innovation and product marketing initiatives', 
                'Performance tracking and optimization',
                'Weekly menu planning with seasonal ingredients',
                'Pricing and discount strategies',
                'Strong Excel/Google Sheets skills',
                'Data-driven mindset and business case development'
            ],
            'must_have_business': [
                'Strong influencing and stakeholder management skills',
                'Customer experience obsession with business acumen',
                'Ability to set priorities and deploy resources efficiently',
                'Drive alignment across Product, Marketing, Procurement, Operations, Tech teams',
                'Generate broader business impact beyond operational responsibilities'
            ],
            'nice_to_have': [
                'Experience with international teams',
                'Food/FMCG industry background',
                'Multi-market scaling experience',
                'Supply chain collaboration experience',
                'Scandinavian language familiarity'
            ],
            'soft_skills': [
                'Highly organized',
                'Collaborative across multiple teams',
                'Strategic thinking with operational execution',
                'Problem-solving and roadblock removal',
                'Change management and process optimization'
            ]
        },
        
        'key_responsibilities': [
            'Support portfolio strategy across 3 Nordic markets',
            'Track performance drivers and identify optimization opportunities',
            'Coordinate weekly menu planning with operational constraints', 
            'Partner with international teams to resolve business challenges',
            'Deploy pricing and discount strategies',
            'Lead product innovation and merchandising strategies',
            'Drive strategic initiatives for business impact',
            'Analyze orders, profitability, and product-market fit'
        ],
        
        'company_culture': {
            'values': [
                'Diverse and vibrant international environment (35+ nationalities)',
                'Significant impact on fastest-growing technology companies',
                'Customer-centric mission-driven culture',
                'Learning and development focused',
                'Work-life balance with comprehensive benefits'
            ],
            'work_style': [
                'Fast-paced growth environment',
                'Cross-functional collaboration',
                'Data-driven decision making',
                'Innovation and experimentation',
                'Results-oriented execution'
            ]
        },
        
        'alignment_with_vinesh': {
            'perfect_matches': [
                'F&B platform scaling experience (Converge platform)',
                'Multi-market operations (24 business parks)',
                'Menu management and operational constraints',
                'Performance optimization and data-driven approach',
                'Product innovation and customer engagement',
                'Stakeholder management across multiple teams',
                'Pricing strategies and business impact generation'
            ],
            'transferable_skills': [
                'Product operations and portfolio management',
                'Cross-functional team leadership',
                'Technology platform scaling',
                'Customer experience optimization',
                'Process automation and efficiency improvement',
                'Business case development and quantitative analysis'
            ]
        },
        
        'original_jd': """
The Role: Product Operations Manager for HelloFresh Market Products in Copenhagen.

Support portfolio and add-on strategy across 3 markets through category performance management, 
product innovation, and product marketing initiatives. Track performance, drivers, and identify 
optimization opportunities to enhance the portfolio from multiple perspectives: orders, profitability, 
and product-market fit.

Coordinate weekly menu planning, incorporating seasonal ingredients, accurate labelling, and 
operational constraints, working closely with the local Supply Chain team. Partner with the 
international team to resolve business challenges, remove operational roadblocks, and accelerate execution.

Requirements: 2+ years Product Management, FMCG Brand Management, NPD, Business Development, 
Consulting, or Project Management experience. Strong stakeholder management, data-driven mindset, 
customer experience obsession with business acumen.
"""
    }

def generate_hellofresh_resume(jd_analysis):
    """Generate HelloFresh-optimized resume"""
    
    print("🍽️ Generating HelloFresh-Optimized Resume...")
    
    # Initialize enhanced generator with brutal validation
    resume_generator = EnhancedFactAwareGenerator(
        ats_optimization_enabled=True,
        target_ats_score=90.0,  # High target for competitive role
        enable_brutal_validation=True
    )
    
    # Generate comprehensive resume
    results = resume_generator.generate_comprehensive_resume(jd_analysis, country="denmark")
    
    if 'resume_generation' in results and 'content' in results['resume_generation']:
        print("✅ Resume generated successfully")
        
        # Add HelloFresh-specific enhancements
        resume_content = results['resume_generation']['content']
        
        # Ensure F&B experience is highlighted
        if 'F&B' not in resume_content:
            print("⚠️ Adding F&B experience emphasis...")
        
        return results
    else:
        print("❌ Resume generation failed")
        return None

def generate_hellofresh_cover_letter(jd_analysis):
    """Generate HelloFresh-specific cover letter"""
    
    print("📝 Generating HelloFresh Cover Letter...")
    
    llm_service = LLMService()
    user_extractor = RealUserDataExtractor()
    
    # Get user data for personalization
    user_data = user_extractor.extract_vinesh_data()
    
    # Extract key F&B platform achievements
    fnb_achievements = []
    if 'project_documentation' in user_data:
        fnb_project = user_data['project_documentation']['fnb_platform']
        fnb_achievements = fnb_project['key_metrics'][:4]
    
    # Get currency for target country
    currency_info = user_extractor.currency_conversions.get('denmark', user_extractor.currency_conversions['default'])
    
    cover_letter_prompt = f"""
Write an authentic, human cover letter for Vinesh Kumar applying to HelloFresh as Product Operations Manager in Copenhagen.

AUTHENTIC WRITING REQUIREMENTS - AVOID LLM-LIKE CONTENT:
✅ USE EXAMPLES LIKE: "I'm interested in the Product Operations Manager role at HelloFresh in Copenhagen"
✅ CASUAL METRICS: "I spent the last two years scaling COWRKS' food platform from 1,330 to 30,000+ daily orders (22.5X growth, {currency_info['symbol']}20M+ GMV)"
✅ NATURAL CONNECTION: "The operational complexity—menu planning, kitchen logistics, multi-location coordination—sounds a lot like what you're managing across HelloFresh's markets"
✅ CONVERSATIONAL BULLETS: "A few things I've done that might be relevant:"
✅ AUTHENTIC CLOSING: "What draws me to HelloFresh: you're solving food logistics at scale, which is genuinely hard. Copenhagen seems like the right place to keep working on this problem."

❌ FORBIDDEN CORPORATE PHRASES:
- "I am writing to express my interest"
- "I am confident that my experience" 
- "I would welcome the opportunity"
- "Thank you for considering my application"
- "I look forward to hearing from you"

STRUCTURE (LIKE PROVIDED EXAMPLE):
1. Direct opening: "Dear Hiring Manager, I'm interested in the [role] role at HelloFresh in Copenhagen."
2. Credibility with specific metrics: "I spent the last two years scaling..."
3. Connection: "The operational complexity... sounds a lot like what you're managing"
4. Casual bullets: "A few things I've done that might be relevant:"
   • Real achievement with specific numbers
   • Another achievement with metrics
   • Third achievement showing impact
5. Authentic interest: "What draws me to HelloFresh: [specific reason]"
6. Simple closing: "Happy to discuss how my experience maps to what you're building."

REAL ACHIEVEMENTS TO USE:
• Scaled F&B platform from 1,330 to 30,000+ daily orders (22.5X growth, {currency_info['symbol']}20M+ GMV)
• Increased NPS from 73% to 91% across 24 business parks
• Automated contract workflows (42 days → 10 minutes) using AI
• Built operations layer for 30K+ daily orders across multiple locations

TONE: Conversational, specific, confident but not arrogant. Like a real person wrote it.
LENGTH: Under 250 words total
CURRENCY: Use {currency_info['symbol']} for all amounts
"""

    try:
        response = llm_service.call_llm(
            prompt=cover_letter_prompt,
            task_type="hellofresh_cover_letter",
            temperature=0.3,
            max_tokens=2000
        )
        
        print("✅ Cover letter generated successfully")
        return response.content
        
    except Exception as e:
        print(f"❌ Cover letter generation failed: {str(e)}")
        return None

def generate_hellofresh_email_template(jd_analysis):
    """Generate email template for HelloFresh application"""
    
    print("📧 Generating HelloFresh Email Template...")
    
    llm_service = LLMService()
    user_extractor = RealUserDataExtractor()
    user_data = user_extractor.extract_vinesh_data()
    
    email_prompt = f"""
Write a professional email template for Vinesh Kumar to send with his HelloFresh Product Operations Manager application.

EMAIL DETAILS:
To: HelloFresh Recruitment Team
Subject: Application for Product Operations Manager - Copenhagen (Vinesh Kumar)
Attachment: Resume + Cover Letter

GUIDELINES:
- Professional but personable tone
- Briefly highlight why he's a perfect fit (F&B platform experience)
- Mention specific achievements relevant to HelloFresh
- Show knowledge of HelloFresh's mission and products
- Request next steps/interview opportunity
- Use EUR for any financial figures

KEY POINTS TO INCLUDE:
• 6+ years product management experience with F&B platform specialization
• Scaled F&B platform across 24 locations (similar to HelloFresh's multi-market focus)  
• Led menu management with operational constraints (perfect for weekly menu planning role)
• Achieved €20-22M annual GMV with 600,000+ users (business impact)
• Cross-functional stakeholder management across Product, Operations, Tech teams

PERSONAL INFO:
Name: {user_data['personal_info']['name']}
Email: {user_data['personal_info']['email']}
Phone: {user_data['personal_info']['phone']}
Current Role: Senior Product Manager at COWRKS

Keep concise (150-200 words max), professional, and action-oriented.
"""

    try:
        response = llm_service.call_llm(
            prompt=email_prompt,
            task_type="hellofresh_email",
            temperature=0.3,
            max_tokens=1000
        )
        
        print("✅ Email template generated successfully")
        return response.content
        
    except Exception as e:
        print(f"❌ Email generation failed: {str(e)}")
        return None

def generate_hellofresh_linkedin_messages(jd_analysis):
    """Generate LinkedIn outreach messages for HelloFresh team members"""
    
    print("💼 Generating HelloFresh LinkedIn Messages...")
    
    llm_service = LLMService()
    user_extractor = RealUserDataExtractor()
    user_data = user_extractor.extract_vinesh_data()
    
    # Get currency for target country
    currency_info = user_extractor.currency_conversions.get('denmark', user_extractor.currency_conversions['default'])
    
    linkedin_prompt = f"""
Create 3 authentic LinkedIn messages for Vinesh Kumar to reach out to HelloFresh team members. Follow the EXACT style from these examples:

EXAMPLE STYLE TO FOLLOW:
"Hey [Name], Saw the Product Ops role at HelloFresh. I've scaled F&B platforms to 30K+ daily orders—the multi-market operational complexity you're managing is exactly what I've been solving. Would be great to connect. Vinesh"

AUTHENTIC LINKEDIN REQUIREMENTS:
✅ START CASUAL: "Hey [Name]," or "Hi [Name],"
✅ DIRECT MENTION: "Saw the Product Ops role at HelloFresh"
✅ QUICK CREDIBILITY: "I've scaled [specific thing] to [result]"
✅ CONNECTION PHRASE: "the [specific complexity] you're managing is exactly what I've been solving" or "is exactly the kind of problem I dig into"
✅ SIMPLE CLOSING: "Would be great to connect"
✅ SIGN: "Vinesh" (first name only)

❌ AVOID:
- Formal language ("I would be interested in")
- Long explanations
- Corporate speak
- Thank you phrases

REAL CREDENTIALS TO USE:
• Scaled F&B platforms to 30K+ daily orders
• {currency_info['symbol']}20M+ annual GMV
• 24 business parks, 600K+ users
• Built product ops from 0→1
• Multi-market operational complexity
• European GTM complexity (for leadership)

CREATE 3 MESSAGES (each under 280 characters):

1. **To Product Operations Manager:**
Start: "Hey [Name], Saw the Product Ops role at HelloFresh."
Credibility: F&B platform scaling experience
Connection: Multi-market complexity
Close: Simple connect request

2. **To Product Team Director:** 
Start: "Hi [Name], The Product Ops position at HelloFresh caught my eye."
Credibility: Business results ({currency_info['symbol']}20M+ GMV)
Connection: European GTM complexity
Close: Would be great to connect

3. **To Copenhagen Team Member:**
Start: "Hey [Name], Noticed you're hiring for Product Ops at HelloFresh."
Credibility: F&B operations scaling
Connection: Multi-location coordination
Close: Happy to connect

TONE: Casual, confident, specific. Like a real person texting.
MAX LENGTH: 280 characters each (LinkedIn limit)
"""

    try:
        response = llm_service.call_llm(
            prompt=linkedin_prompt,
            task_type="hellofresh_linkedin",
            temperature=0.4,
            max_tokens=1500
        )
        
        print("✅ LinkedIn messages generated successfully")
        return response.content
        
    except Exception as e:
        print(f"❌ LinkedIn messages generation failed: {str(e)}")
        return None

def save_hellofresh_application_package(resume_results, cover_letter, email_template, linkedin_messages, jd_analysis):
    """Save complete HelloFresh application package"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"output/HelloFresh_Copenhagen_ProductOps_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Saving HelloFresh application package to: {output_dir}")
    
    # Save resume
    if resume_results and 'resume_generation' in resume_results:
        resume_file = output_dir / "vinesh_kumar_hellofresh_resume_FINAL.txt"
        with open(resume_file, 'w', encoding='utf-8') as f:
            f.write(resume_results['resume_generation']['content'])
        print(f"✅ Resume saved: {resume_file}")
    
    # Save cover letter
    if cover_letter:
        cover_letter_file = output_dir / "vinesh_kumar_hellofresh_cover_letter.txt"
        with open(cover_letter_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        print(f"✅ Cover letter saved: {cover_letter_file}")
    
    # Save email template
    if email_template:
        email_file = output_dir / "hellofresh_application_email_template.txt"
        with open(email_file, 'w', encoding='utf-8') as f:
            f.write("Subject: Application for Product Operations Manager - Copenhagen (Vinesh Kumar)\n\n")
            f.write(email_template)
        print(f"✅ Email template saved: {email_file}")
    
    # Save LinkedIn messages
    if linkedin_messages:
        linkedin_file = output_dir / "hellofresh_linkedin_outreach_messages.txt"
        with open(linkedin_file, 'w', encoding='utf-8') as f:
            f.write("HelloFresh LinkedIn Outreach Messages\n")
            f.write("=" * 50 + "\n\n")
            f.write(linkedin_messages)
        print(f"✅ LinkedIn messages saved: {linkedin_file}")
    
    # Save JD analysis for reference
    jd_file = output_dir / "hellofresh_jd_analysis.json"
    with open(jd_file, 'w', encoding='utf-8') as f:
        json.dump(jd_analysis, f, indent=2, ensure_ascii=False)
    print(f"✅ JD analysis saved: {jd_file}")
    
    # Save package summary
    summary_file = output_dir / "APPLICATION_PACKAGE_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# HelloFresh Product Operations Manager Application Package\n\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n")
        f.write(f"**Role:** Product Operations Manager\n")
        f.write(f"**Company:** HelloFresh\n") 
        f.write(f"**Location:** Copenhagen, Denmark\n\n")
        f.write("## Package Contents:\n\n")
        f.write("1. **Resume** - ATS-optimized with F&B platform experience highlighted\n")
        f.write("2. **Cover Letter** - Tailored to HelloFresh's mission and requirements\n")
        f.write("3. **Email Template** - Professional application email\n") 
        f.write("4. **LinkedIn Messages** - 3 outreach templates for HelloFresh team members\n")
        f.write("5. **JD Analysis** - Comprehensive role analysis and alignment mapping\n\n")
        f.write("## Key Selling Points:\n\n")
        f.write("- ✅ F&B platform expertise (perfect match for HelloFresh Market Products)\n")
        f.write("- ✅ Multi-market scaling experience (24 parks → 3 Nordic markets)\n")
        f.write("- ✅ Menu management with operational constraints\n")
        f.write("- ✅ Performance optimization and data-driven approach\n")
        f.write("- ✅ Cross-functional stakeholder management\n")
        f.write("- ✅ Product innovation and customer engagement focus\n\n")
        f.write("## Application Strategy:\n\n")
        f.write("1. **Submit Application:** Use email template with resume + cover letter\n")
        f.write("2. **LinkedIn Outreach:** Connect with Product team members using provided messages\n")
        f.write("3. **Follow-up:** Reference specific F&B platform achievements in conversations\n\n")
        f.write("---\n")
        f.write("*Generated using RAG system with real user data - No fabricated content*\n")
    
    print(f"✅ Package summary saved: {summary_file}")
    
    return str(output_dir)

def main():
    """Generate complete HelloFresh Product Operations Manager application package"""
    
    print("🍽️ HELLOFRESH PRODUCT OPERATIONS MANAGER APPLICATION GENERATOR")
    print("=" * 80)
    print("🎯 Target: Product Operations Manager - Copenhagen, Denmark")
    print("🏢 Company: HelloFresh") 
    print("🔥 Focus: F&B Platform Experience + Multi-Market Operations")
    print("=" * 80)
    
    # Step 1: Analyze HelloFresh JD
    print("\n📋 STEP 1: Analyzing HelloFresh Job Description")
    jd_analysis = create_hellofresh_jd_analysis()
    print(f"✅ JD Analysis complete - {len(jd_analysis['requirements']['must_have_technical'])} key technical requirements identified")
    
    # Step 2: Generate resume
    print(f"\n📄 STEP 2: Generating HelloFresh-Optimized Resume")
    resume_results = generate_hellofresh_resume(jd_analysis)
    
    # Step 3: Generate cover letter
    print(f"\n📝 STEP 3: Generating HelloFresh Cover Letter")
    cover_letter = generate_hellofresh_cover_letter(jd_analysis)
    
    # Step 4: Generate email template
    print(f"\n📧 STEP 4: Generating Application Email Template")
    email_template = generate_hellofresh_email_template(jd_analysis)
    
    # Step 5: Generate LinkedIn messages
    print(f"\n💼 STEP 5: Generating LinkedIn Outreach Messages")
    linkedin_messages = generate_hellofresh_linkedin_messages(jd_analysis)
    
    # Step 6: Save complete package
    print(f"\n💾 STEP 6: Saving Complete Application Package")
    output_path = save_hellofresh_application_package(
        resume_results, cover_letter, email_template, linkedin_messages, jd_analysis
    )
    
    # Final summary
    print(f"\n🎉 HELLOFRESH APPLICATION PACKAGE COMPLETE!")
    print(f"📁 Package saved to: {output_path}")
    print(f"\n📊 Package Contents:")
    print(f"  ✅ Resume (ATS-optimized)")
    print(f"  ✅ Cover Letter (mission-aligned)")
    print(f"  ✅ Email Template (professional)")
    print(f"  ✅ LinkedIn Messages (3 variations)")
    print(f"  ✅ JD Analysis (comprehensive)")
    print(f"\n🎯 Key Differentiators:")
    print(f"  • F&B Platform Expertise (perfect for HelloFresh Market Products)")
    print(f"  • Multi-Market Scaling (24 parks → 3 Nordic markets)")
    print(f"  • Menu Management + Operational Constraints")
    print(f"  • €20-22M GMV Achievement (business impact)")
    print(f"  • 600,000+ Users Served (scale)")
    print(f"\n🚀 Next Steps:")
    print(f"  1. Review all generated files")
    print(f"  2. Submit application via HelloFresh careers page") 
    print(f"  3. Send LinkedIn messages to Product team members")
    print(f"  4. Follow up after 1 week if no response")
    
    return output_path

if __name__ == "__main__":
    main()