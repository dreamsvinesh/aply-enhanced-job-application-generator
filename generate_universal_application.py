#!/usr/bin/env python3
"""
Universal Application Generator
Creates tailored application packages for any company/role using Adlina-style writing
"""

import json
import os
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from modules.enhanced_fact_aware_generator import EnhancedFactAwareGenerator
from modules.real_user_data_extractor import RealUserDataExtractor
from modules.llm_service import LLMService
from modules.adlina_style_guide import AdlinaStyleGuide
from modules.dynamic_email_linkedin_generator import DynamicEmailLinkedInGenerator

def create_universal_jd_analysis(company: str, role: str, location: str, jd_text: str, 
                               requirements: list = None, focus_areas: list = None) -> Dict[str, Any]:
    """Create JD analysis for any company/role"""
    
    # Parse basic info
    extracted_info = {
        'company': company,
        'role_title': role,
        'location': location,
        'original_jd': jd_text[:500] + "..." if len(jd_text) > 500 else jd_text
    }
    
    # Default requirements if not provided
    if not requirements:
        requirements = [
            'Product Management experience',
            'Cross-functional collaboration',
            'Data-driven decision making',
            'Strategic thinking',
            'Customer-centric approach'
        ]
    
    # Default focus areas if not provided
    if not focus_areas:
        focus_areas = [
            'Product strategy and execution',
            'Team leadership and stakeholder management',
            'Process optimization and automation',
            'Business impact and growth metrics'
        ]
    
    return {
        'extracted_info': extracted_info,
        'requirements': {
            'must_have_business': requirements[:3],
            'must_have_technical': requirements[3:] if len(requirements) > 3 else [],
            'nice_to_have': focus_areas
        },
        'key_focus_areas': focus_areas,
        'alignment_opportunities': [
            'F&B platform experience → Product operations',
            'Multi-market scaling → Business growth',
            'AI/automation expertise → Technical innovation',
            'Cross-functional leadership → Team collaboration',
            '€20-22M revenue generation → Business impact'
        ],
        'original_jd': jd_text
    }

def generate_universal_resume(jd_analysis: Dict[str, Any], country: str = "netherlands") -> Dict[str, Any]:
    """Generate resume using Adlina style for any company"""
    
    print(f"📄 Generating {jd_analysis['extracted_info']['company']} Resume...")
    
    # Initialize with Adlina style validation
    generator = EnhancedFactAwareGenerator(
        ats_optimization_enabled=True,
        target_ats_score=85.0,
        enable_brutal_validation=True
    )
    
    # Generate with specific styling
    results = generator.generate_comprehensive_resume(jd_analysis, country=country)
    
    if 'resume_generation' in results and 'content' in results['resume_generation']:
        print("✅ Resume generated successfully")
        
        # Validate against Adlina style
        content = results['resume_generation']['content']
        
        # Extract and validate summary
        summary_start = content.find('PROFESSIONAL SUMMARY')
        if summary_start != -1:
            summary_end = content.find('EXPERIENCE', summary_start)
            if summary_end != -1:
                summary = content[summary_start:summary_end].replace('PROFESSIONAL SUMMARY', '').strip()
                adlina_validation = AdlinaStyleGuide.validate_summary(summary)
                
                if not adlina_validation['is_valid']:
                    print(f"⚠️ Adlina style issues: {adlina_validation['issues']}")
                else:
                    print("✅ Summary passes Adlina style validation")
        
        return results
    else:
        print("❌ Resume generation failed")
        return None

def generate_universal_cover_letter(jd_analysis: Dict[str, Any], country: str = "netherlands") -> str:
    """Generate cover letter for any company using Adlina principles"""
    
    print(f"📝 Generating {jd_analysis['extracted_info']['company']} Cover Letter...")
    
    llm_service = LLMService()
    user_extractor = RealUserDataExtractor()
    user_data = user_extractor.extract_vinesh_data()
    
    # Get target country currency
    currency_info = user_extractor.currency_conversions.get(country.lower(), user_extractor.currency_conversions['default'])
    
    cover_letter_prompt = f"""
Write an authentic, conversational cover letter for Vinesh Kumar applying to {jd_analysis['extracted_info']['company']}.

AUTHENTIC WRITING STYLE - FOLLOW THESE PATTERNS:
✅ DIRECT OPENING: "Dear Hiring Manager, I'm interested in the {jd_analysis['extracted_info']['role_title']} role at {jd_analysis['extracted_info']['company']} in {jd_analysis['extracted_info']['location']}."
✅ CREDIBILITY STATEMENT: "I spent the last two years scaling COWRKS' food platform from 1,330 to 30,000+ daily orders (22.5X growth, {currency_info['symbol']}20M+ GMV)."
✅ NATURAL CONNECTION: "The [specific challenge/complexity] sounds a lot like what you're managing" or "is exactly the kind of problem I dig into"
✅ CASUAL BULLETS: "A few things I've done that might be relevant:"
✅ AUTHENTIC INTEREST: "What draws me to {jd_analysis['extracted_info']['company']}: [specific reason about the company/challenge]"
✅ SIMPLE CLOSING: "Happy to discuss how my experience maps to what you're building."

❌ FORBIDDEN CORPORATE CLICHÉS:
- "I am writing to express my interest"
- "I am confident that my experience"
- "I would welcome the opportunity" 
- "Thank you for considering my application"
- "I look forward to hearing from you"

COMPANY-SPECIFIC CONNECTION:
Company: {jd_analysis['extracted_info']['company']}
Role: {jd_analysis['extracted_info']['role_title']}
Location: {jd_analysis['extracted_info']['location']}

REAL ACHIEVEMENTS (with specific numbers):
• Scaled F&B platform from 1,330 to 30,000+ daily orders (22.5X growth, {currency_info['symbol']}20M+ GMV)
• Increased NPS from 73% to 91% by fixing the friction points customers actually cared about
• Automated contract workflows (42 days → 10 minutes) using AI, which freed up teams to focus on harder problems
• Built operations layer for 30K+ daily orders across 24 locations

STRUCTURE:
1. Direct opening with role interest
2. Quick credibility with F&B platform metrics
3. Connection to company's specific challenges
4. "A few things I've done that might be relevant:" + 3 bullet points with real numbers
5. "What draws me to [Company]:" + specific reason
6. "[Location] seems like the right place to keep working on this problem."
7. "Happy to discuss how my experience maps to what you're building."

TONE: Conversational, confident but not arrogant. Sounds like a real person wrote it.
LENGTH: Under 250 words
CURRENCY: Use {currency_info['symbol']} for all amounts

PERSONAL SIGNATURE:
Best,
{user_data['personal_info']['name']}
"""

    try:
        response = llm_service.call_llm(
            prompt=cover_letter_prompt,
            task_type=f"{jd_analysis['extracted_info']['company'].lower()}_cover_letter",
            temperature=0.3,
            max_tokens=2000
        )
        
        print("✅ Cover letter generated successfully")
        return response.content
        
    except Exception as e:
        print(f"❌ Cover letter generation failed: {str(e)}")
        return None

def generate_universal_email(jd_analysis: Dict[str, Any]) -> str:
    """Generate application email for any company"""
    
    print(f"📧 Generating {jd_analysis['extracted_info']['company']} Email...")
    
    llm_service = LLMService()
    user_extractor = RealUserDataExtractor()
    user_data = user_extractor.extract_vinesh_data()
    
    email_prompt = f"""
Write a professional application email for Vinesh Kumar applying to {jd_analysis['extracted_info']['company']}.

{AdlinaStyleGuide.generate_style_prompt()}

EMAIL DETAILS:
To: Hiring Team at {jd_analysis['extracted_info']['company']}
Subject: Application for {jd_analysis['extracted_info']['role_title']} - {jd_analysis['extracted_info']['location']} (Vinesh Kumar)

KEY POINTS TO INCLUDE:
• 6+ years product management with F&B platform specialization
• Scaled platform across 24 locations serving 600,000+ users  
• Generated €20-22M annual GMV through product operations
• Expertise directly relevant to {jd_analysis['extracted_info']['role_title']} role
• Interest in {jd_analysis['extracted_info']['location']} opportunity

PERSONAL INFO:
Name: {user_data['personal_info']['name']}
Email: {user_data['personal_info']['email']}
Phone: {user_data['personal_info']['phone']}
Current Role: Senior Product Manager at COWRKS

TONE: Professional but personable, showing specific company interest
LENGTH: 150-200 words maximum
FORMAT: Business email with clear subject line and call-to-action
"""

    try:
        response = llm_service.call_llm(
            prompt=email_prompt,
            task_type=f"{jd_analysis['extracted_info']['company'].lower()}_email",
            temperature=0.3,
            max_tokens=1000
        )
        
        print("✅ Email generated successfully")
        return response.content
        
    except Exception as e:
        print(f"❌ Email generation failed: {str(e)}")
        return None

def generate_universal_linkedin_messages(jd_analysis: Dict[str, Any], country: str = "netherlands") -> Dict[str, Any]:
    """Generate LinkedIn messages for any company using DynamicEmailLinkedInGenerator"""
    
    print(f"💼 Generating {jd_analysis['extracted_info']['company']} LinkedIn Messages...")
    
    linkedin_generator = DynamicEmailLinkedInGenerator()
    user_extractor = RealUserDataExtractor()
    user_profile = user_extractor.extract_vinesh_data()
    
    try:
        # Generate complete LinkedIn outreach package
        linkedin_package = linkedin_generator.generate_complete_outreach_package(
            jd_analysis, user_profile, country
        )
        
        if 'error' not in linkedin_package:
            print("✅ LinkedIn messages generated successfully")
            return linkedin_package
        else:
            print(f"❌ LinkedIn generation failed: {linkedin_package['error']}")
            return None
            
    except Exception as e:
        print(f"❌ LinkedIn message generation failed: {str(e)}")
        return None

def save_universal_package(company: str, role: str, resume_results: Dict, cover_letter: str, 
                         email: str, linkedin_messages: Dict, jd_analysis: Dict) -> str:
    """Save complete application package for any company"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_safe = company.replace(" ", "_").replace("/", "_")
    role_safe = role.replace(" ", "_").replace("/", "_")
    output_dir = Path(f"output/{company_safe}_{role_safe}_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Saving {company} application package to: {output_dir}")
    
    # Save resume
    if resume_results and 'resume_generation' in resume_results:
        resume_file = output_dir / f"vinesh_kumar_{company_safe}_resume_FINAL.txt"
        with open(resume_file, 'w', encoding='utf-8') as f:
            f.write(resume_results['resume_generation']['content'])
        print(f"✅ Resume saved: {resume_file}")
    
    # Save cover letter
    if cover_letter:
        cover_file = output_dir / f"vinesh_kumar_{company_safe}_cover_letter.txt"
        with open(cover_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        print(f"✅ Cover letter saved: {cover_file}")
    
    # Save email
    if email:
        email_file = output_dir / f"{company_safe}_application_email.txt"
        with open(email_file, 'w', encoding='utf-8') as f:
            f.write(f"Subject: Application for {role} - {jd_analysis['extracted_info']['location']} (Vinesh Kumar)\n\n")
            f.write(email)
        print(f"✅ Email saved: {email_file}")
    
    # Save LinkedIn messages
    if linkedin_messages:
        linkedin_file = output_dir / f"{company_safe}_linkedin_messages.txt"
        with open(linkedin_file, 'w', encoding='utf-8') as f:
            f.write(f"LinkedIn Outreach Package for {company} {role}\n")
            f.write("=" * 60 + "\n\n")
            
            # Connection request
            if 'linkedin_connection' in linkedin_messages:
                conn = linkedin_messages['linkedin_connection']
                f.write("🤝 CONNECTION REQUEST:\n")
                f.write(f"Characters: {conn.get('character_count', 0)}/{300}\n")
                f.write("-" * 30 + "\n")
                f.write(conn.get('content', 'No content') + "\n\n")
            
            # Direct message
            if 'linkedin_message' in linkedin_messages:
                msg = linkedin_messages['linkedin_message']
                f.write("💬 DIRECT MESSAGE:\n")
                f.write(f"Characters: {msg.get('character_count', 0)}/{400}\n")
                f.write("-" * 30 + "\n")
                f.write(msg.get('content', 'No content') + "\n\n")
            
            # Email template (if included)
            if 'email_template' in linkedin_messages:
                email_template = linkedin_messages['email_template']
                f.write("📧 EMAIL TEMPLATE:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Subject: {email_template.get('subject', 'No subject')}\n\n")
                f.write(f"Body:\n{email_template.get('body', 'No body')}\n\n")
        
        print(f"✅ LinkedIn messages saved: {linkedin_file}")
    
    # Save JD analysis
    jd_file = output_dir / f"{company_safe}_jd_analysis.json"
    with open(jd_file, 'w', encoding='utf-8') as f:
        json.dump(jd_analysis, f, indent=2, ensure_ascii=False)
    
    # Save package summary
    summary_file = output_dir / "APPLICATION_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"# {company} {role} Application Package\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n")
        f.write(f"**Company:** {company}\n")
        f.write(f"**Role:** {role}\n")
        f.write(f"**Location:** {jd_analysis['extracted_info']['location']}\n\n")
        f.write("## Key Alignments:\n\n")
        for alignment in jd_analysis['alignment_opportunities']:
            f.write(f"- ✅ {alignment}\n")
        f.write(f"\n## Generated with Adlina Style Guide\n")
        f.write(f"- ✅ No generic language\n")
        f.write(f"- ✅ Specific metrics integration\n") 
        f.write(f"- ✅ Action-focused content\n")
        f.write(f"- ✅ Target country currency\n")
        f.write(f"- ✅ RAG-based content only\n")
    
    return str(output_dir)

def main():
    """Command line interface for universal application generator"""
    
    parser = argparse.ArgumentParser(description='Generate tailored application package for any company')
    parser.add_argument('--company', required=True, help='Company name (e.g., "Spotify")')
    parser.add_argument('--role', required=True, help='Role title (e.g., "Senior Product Manager")')
    parser.add_argument('--location', required=True, help='Location (e.g., "Stockholm, Sweden")')
    parser.add_argument('--country', default='netherlands', help='Target country for currency (e.g., "sweden", "uk", "usa")')
    parser.add_argument('--jd-file', help='Path to job description text file')
    parser.add_argument('--requirements', nargs='*', help='Key requirements for the role')
    
    args = parser.parse_args()
    
    # Load JD text
    jd_text = ""
    if args.jd_file and os.path.exists(args.jd_file):
        with open(args.jd_file, 'r', encoding='utf-8') as f:
            jd_text = f.read()
    
    print(f"🎯 UNIVERSAL APPLICATION GENERATOR")
    print(f"=" * 60)
    print(f"🏢 Company: {args.company}")
    print(f"💼 Role: {args.role}")
    print(f"📍 Location: {args.location}")
    print(f"💰 Currency: {args.country}")
    print(f"=" * 60)
    
    # Create JD analysis
    jd_analysis = create_universal_jd_analysis(
        args.company, args.role, args.location, jd_text, args.requirements
    )
    
    # Generate complete package
    print(f"\n📄 Generating Resume...")
    resume_results = generate_universal_resume(jd_analysis, args.country)
    
    print(f"\n📝 Generating Cover Letter...")
    cover_letter = generate_universal_cover_letter(jd_analysis, args.country)
    
    print(f"\n📧 Generating Email...")
    email = generate_universal_email(jd_analysis)
    
    print(f"\n💼 Generating LinkedIn Messages...")
    linkedin_messages = generate_universal_linkedin_messages(jd_analysis, args.country)
    
    print(f"\n💾 Saving Package...")
    package_path = save_universal_package(
        args.company, args.role, resume_results, cover_letter, email, linkedin_messages, jd_analysis
    )
    
    print(f"\n🎉 APPLICATION PACKAGE COMPLETE!")
    print(f"📁 Saved to: {package_path}")
    print(f"\n🎯 Key Features:")
    print(f"  ✅ Adlina-style writing (no generic language)")
    print(f"  ✅ Target country currency ({args.country})")
    print(f"  ✅ F&B platform experience highlighted")
    print(f"  ✅ Specific metrics and achievements")
    print(f"  ✅ Company-tailored content")

# Example usage when imported
def generate_application_for_company(company: str, role: str, location: str, 
                                   country: str = "netherlands", jd_text: str = "", 
                                   requirements: list = None) -> str:
    """Programmatic interface for generating applications"""
    
    jd_analysis = create_universal_jd_analysis(company, role, location, jd_text, requirements)
    
    resume_results = generate_universal_resume(jd_analysis, country)
    cover_letter = generate_universal_cover_letter(jd_analysis, country) 
    email = generate_universal_email(jd_analysis)
    linkedin_messages = generate_universal_linkedin_messages(jd_analysis, country)
    
    return save_universal_package(company, role, resume_results, cover_letter, email, linkedin_messages, jd_analysis)

if __name__ == "__main__":
    main()