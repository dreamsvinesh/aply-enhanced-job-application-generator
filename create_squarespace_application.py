#!/usr/bin/env python3
"""
Create complete job application package for Squarespace role
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Add modules to path
sys.path.append(str(Path(__file__).parent / 'modules'))

from modules.jd_parser import JobDescriptionParser
from modules.resume_generator import ResumeGenerator
from modules.cover_letter_generator import CoverLetterGenerator
from modules.message_generator import MessageGenerator

def main():
    # Job description
    jd_text = """At Squarespace, we empower product teams to solve meaningful customer and business problems. We're looking for a Product Manager to lead Acuity Communications, the team responsible for the tools and infrastructure that help businesses communicate with their clients throughout the scheduling journey.

For appointment-based businesses, client relationships are at the core of long-term success. Communications like confirmations, reminders, reschedules, and follow-ups, help businesses stay connected with clients and reduce no-shows. By overseeing the systems that deliver these messages at scale, you'll help customers operate more efficiently and build the strong client relationships that fuel growth.

You'll own our communication products: emails, reminders, notifications, and lifecycle messaging, while also managing the platform that ensures messages are delivered reliably and securely. You will blend platform ownership with B2B2C product design: empowering businesses with simple, intuitive tools, and ensuring their clients receive clear, timely communication that strengthens the relationship.

This is a hybrid role, requiring 3 days a week in our Aveiro, Portugal office. You will report to the Senior Group Product Manager on the Acuity Scheduling team.

What You'll Do

Execute the roadmap for Acuity's client communication products across email and SMS
Partner with engineering to deliver a scalable, compliant, and resilient messaging platform
Work with external communication partners to optimize current integrations and evaluate new functionality—ensuring Acuity adopts the latest capabilities and can invest in the opportunistic messaging experiences
Build intuitive tools that let businesses easily create, customize, and automate communications
Collaborate across Acuity product teams to support new triggers and lifecycle messaging use cases
Monitor system health, reliability, abuse risks, and cost efficiency—and lead improvements that maintain trust
Use data and research to measure impact and inform prioritization

Who We're Looking For

5–6+ years of Product Management experience, ideally in communications, messaging platforms, or lifecycle automation
Proven ability to tackle complex technical challenges across API-driven and service-oriented systems.
Expertise in owning relationships with external platform partners and driving roadmap alignment, integration improvements, or adoption of new capabilities
Background of communicating complex technical concepts to a variety of audiences.
History of customer-focused roles and shipping impactful product improvements

Nice to Have

Background in communication-heavy products (reminders, lifecycle messaging, automation, CRM)
Previous exposure to scheduling, SaaS, or SMB productivity tools."""

    country = "portugal"
    company = "Squarespace"
    
    print("🚀 Creating Squarespace Application Package...")
    print("=" * 50)
    
    try:
        # Initialize modules
        jd_parser = JobDescriptionParser()
        resume_generator = ResumeGenerator()
        cover_letter_generator = CoverLetterGenerator()
        message_generator = MessageGenerator()
        
        # Parse job description
        print("📋 Parsing job description...")
        jd_data = jd_parser.parse(jd_text)
        jd_data['company_name'] = company
        
        # Generate resume
        print("📄 Generating tailored resume...")
        resume_content, resume_changes = resume_generator.generate(jd_data, country)
        
        # Generate cover letter
        print("✉️  Generating cover letter...")
        cover_letter_content = cover_letter_generator.generate(jd_data, country, company)
        cover_changes = ["Customized cover letter for Portugal market", "Emphasized communication platform experience"]
        
        # Generate messages
        print("💬 Generating outreach messages...")
        linkedin_message = message_generator.generate_linkedin_message(jd_data, country)
        email_data = message_generator.generate_email_message(jd_data, country, company)
        email_message = email_data.get('body', '') if isinstance(email_data, dict) else str(email_data)
        message_changes = ["Optimized LinkedIn message for Portugal", "Created professional email outreach template"]
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("output") / f"Squarespace_{country}_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save files
        print(f"💾 Saving files to {output_dir}...")
        
        with open(output_dir / "resume.txt", "w", encoding="utf-8") as f:
            f.write(resume_content)
            
        with open(output_dir / "cover_letter.txt", "w", encoding="utf-8") as f:
            f.write(cover_letter_content)
            
        with open(output_dir / "linkedin_message.txt", "w", encoding="utf-8") as f:
            f.write(linkedin_message)
            
        with open(output_dir / "email_outreach.txt", "w", encoding="utf-8") as f:
            f.write(email_message)
            
        # Create summary
        summary = f"""
# Squarespace Acuity Communications Product Manager Application

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Target Country: {country.title()}
Company: {company}

## Job Analysis
- Role: {jd_data.get('role_title', 'Product Manager')}
- Seniority: {jd_data.get('seniority_level', 'Senior')}
- ATS Match Score: {jd_data.get('ats_match_score', 0)}%

## Generated Components
✅ Resume - Tailored for communication platforms & messaging infrastructure
✅ Cover Letter - Emphasizing relevant product management experience  
✅ LinkedIn Message - Professional outreach optimized for {country.title()}
✅ Email Outreach - Formal application message

## Key Optimizations Made
Resume Changes:
{chr(10).join(['- ' + change for change in resume_changes[:5]])}

Cover Letter Changes:
{chr(10).join(['- ' + change for change in cover_changes[:3]])}

Message Optimizations:
{chr(10).join(['- ' + change for change in message_changes[:3]])}

## Files Generated
- resume.txt
- cover_letter.txt  
- linkedin_message.txt
- email_outreach.txt
- summary.txt (this file)
"""
        
        with open(output_dir / "summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
            
        print("\n🎉 Application package created successfully!")
        print(f"📁 Files saved in: {output_dir}")
        print("\n📋 Summary:")
        print(f"   ATS Match Score: {jd_data.get('ats_match_score', 0)}%")
        print(f"   Resume Changes: {len(resume_changes)}")
        print(f"   Cover Letter Changes: {len(cover_changes)}")
        print(f"   Message Optimizations: {len(message_changes)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())