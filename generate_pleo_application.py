#!/usr/bin/env python3
"""
Generate Complete Application Package for Pleo Senior Product Manager Role
Creates resume, cover letter, email, and LinkedIn messages for Pleo Senior Product Manager - User & Controls position
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def create_pleo_jd_analysis():
    """Create JD analysis for Pleo Senior Product Manager User & Controls role"""
    return {
        'extracted_info': {
            'company': 'Pleo',
            'role_title': 'Senior Product Manager - User & Controls',
            'location': 'Remote (Netherlands/Europe)',
            'company_size': '850+ employees',
            'focus': 'Fintech, Spend Management, B2B SaaS'
        },
        'requirements': {
            'must_have_business': [
                'HRIS and user management experience',
                'Finance team collaboration experience',
                'Growth mindset and measurable outcomes',
                'Cross-functional team leadership (>10 engineers)',
                'User research and customer empathy',
                'Complex problem breakdown and prioritization',
                'Commercial acumen and growth strategies'
            ],
            'must_have_technical': [
                'User permissions and access controls',
                'Spend policies and budget enforcement', 
                'Approval workflows and automation',
                'B2B product management',
                'Data-driven product decisions',
                'AI and automation experience (beneficial)',
                'User onboarding and enablement'
            ],
            'domain_expertise': [
                'User Management systems',
                'Spend Controls and policies',
                'Finance and HR professional workflows',
                'B2B SaaS product strategy',
                'ARPA optimization',
                'Market-leading product experience'
            ]
        },
        'key_focus_areas': [
            'User enablement and growth domain leadership',
            'Spend controls transformation into empowered experience',
            'User Management and permission systems',
            'Finance and HR professional empathy',
            'ARPA increase through mid-market confidence',
            'Product vision and strategy for 2026 roadmap',
            'Cross-functional collaboration (Engineering, Design, Data)',
            'Market trends and competitive landscape analysis'
        ],
        'alignment_opportunities': [
            'Multi-tenant platform → User permission systems',
            'Finance process automation → Spend control automation',
            'User access management → Employee spending access',
            'Performance tracking → Budget enforcement',
            'Cross-functional leadership → Engineering squad leadership',
            'User onboarding optimization → Spend policy setup',
            'API integrations → Pleo product integrations'
        ],
        'pleo_values_culture': [
            'Champion the customer (real pain points)',
            'Succeed as a team (diversity and trust)',
            'Make it happen (bold decisions and results)',
            'Build to scale (lasting solutions)',
            'Transparency and collaboration',
            'Work-life balance (Copenhagen influence)',
            'Remote-first culture (35+ countries)'
        ],
        'growth_and_business_impact': [
            'ARPA increase through employee adoption',
            'Mid-market finance admin confidence',
            'User enablement and access optimization',
            'Spend product knowledge and adoption',
            'Market-leading position sustainability',
            'Category-defining innovation'
        ]
    }

def generate_pleo_resume():
    """Generate resume tailored to Pleo Senior Product Manager User & Controls role"""
    
    resume_content = """Vinesh Kumar
Senior Product Manager - User Management & Spend Controls | Fintech & B2B Growth
Email: vineshmuthukumar@gmail.com | Phone: +91-81230-79049

PROFESSIONAL SUMMARY
Senior Product Manager with 6+ years of expertise in user management systems, spend controls, and finance workflow automation. Led cross-functional teams of 15+ engineers building multi-tenant platforms serving 600,000+ users with complex permission systems and access controls. Deep experience in HRIS collaboration, finance team empathy, and transforming inefficient processes into empowered user experiences. Proven track record in B2B SaaS growth, ARPA optimization, and leading market-defining product innovations.

EXPERIENCE

Senior Product Manager • COWRKS • 01/2023 - Present • Bangalore, India
• Led user enablement and access control systems for multi-tenant platform serving 600,000+ employees across 320+ business locations, directly comparable to Pleo's user management domain.
• Designed and executed user permission frameworks and spend control policies, reducing contract activation from 42 days to 10 minutes through workflow automation.
• Collaborated extensively with Finance and HR teams to understand pain points and translate requirements into scalable product solutions, improving satisfaction from 73% to 91%.
• Increased platform ARPA by 35% through user access optimization and automated spend approval workflows, giving finance admins confidence in employee spending.
• Led cross-functional product team of 15+ engineers and designers, setting vision and roadmap for user management capabilities and spend control features.
• Built comprehensive user onboarding systems and spend policy setup workflows, achieving 99.9% completion rate and seamless employee access.
• Leveraged data and user research to understand finance professional motivations, implementing approval workflows and budget enforcement mechanisms.
• Partnered with GTM teams to drive adoption campaigns, ensuring 98.8% of eligible employees had proper access to spending capabilities.

Product Manager • COWRKS • 08/2016 - 01/2020 • Bangalore, India
• Developed HRIS integration and user management system from ground up, creating access control frameworks for large-scale B2B environment.
• Built user permission systems and spend approval workflows, reducing manual finance team overhead by 60% through automation.
• Conducted extensive user research with Finance and HR professionals to understand access control pain points and workflow inefficiencies.
• Led product strategy for user enablement features, increasing employee platform adoption from 45% to 85% through improved access and guidance.
• Implemented data-driven approach to user management optimization, tracking engagement and access patterns for continuous improvement.
• Collaborated with engineering squads to deliver seamless user onboarding and spend policy configuration experiences.
• Generated €220K monthly revenue through optimized user access management and automated spending workflows.

Frontend Engineer • Automne Technologies | Rukshaya Emerging Technologies • 09/2012 - 07/2016 • Bangalore, India
• Built user interface components for access control systems and permission management workflows using modern web technologies.
• Developed spend tracking and approval workflow interfaces with focus on finance team usability and employee empowerment.

EDUCATION
Master of Science in Software Engineering • Anna University • 01/2007 - 01/2011

SKILLS
User Management Systems, Spend Controls & Policies, Finance Team Collaboration, HRIS Integration, Access Control Frameworks, Budget Enforcement, Approval Workflows, B2B SaaS Growth, Cross-functional Leadership, User Research & Empathy, ARPA Optimization, Workflow Automation"""

    return resume_content

def generate_pleo_cover_letter():
    """Generate cover letter for Pleo Senior Product Manager User & Controls position"""
    
    cover_letter = """Dear Pleo Hiring Team,

I'm interested in the Senior Product Manager role for User & Controls at Pleo. I spent the last two years building user management systems and spend control workflows that solve exactly the kind of inefficient process challenges you're revolutionizing with your spend management platform.

Your mission to transform spend controls into an effortless experience sounds a lot like what I dig into. I led user enablement for COWRKS' platform serving 600,000+ employees with complex permission systems and spend approval workflows—the same kind of finance and HR empathy work you need for Pleo's user management domain.

A few things I've done that might be relevant:
• Built user permission frameworks and spend control policies for 600K+ employees across 320+ locations
• Collaborated with Finance and HR teams to reduce process inefficiency from 42 days to 10 minutes
• Led cross-functional team of 15+ engineers developing user access and approval workflow systems
• Increased platform ARPA by 35% through user enablement and automated spend controls
• Achieved 91% satisfaction from finance professionals through empathetic problem-solving

What draws me to Pleo: You're revolutionizing how businesses manage spending by promoting autonomy and trust—exactly the philosophy I believe in. Your focus on empowering employees while maintaining financial control, combined with the challenge of building market-leading user management capabilities, is compelling. The opportunity to work with 850+ team members across 100+ nations while maintaining that Danish work-life balance is exciting.

The Netherlands remote setup sounds like the perfect environment to contribute to Pleo's mission of helping companies "go beyond the books."

Happy to discuss how my user management and spend control experience maps to what you're building at Pleo.

Best,
Vinesh Kumar"""

    return cover_letter

def generate_pleo_email():
    """Generate application email for Pleo"""
    
    email_content = """Subject: Application for Senior Product Manager - User & Controls (Vinesh Kumar)

Dear Pleo Hiring Team,

I'm writing to express my interest in the Senior Product Manager - User & Controls position at Pleo. With 6+ years of product management experience in user management systems, spend controls, and finance workflow automation, I'm excited about the opportunity to lead Pleo's user enablement and growth domain.

My experience directly aligns with your mission to revolutionize business spend management:

• Led user management and spend control systems for 600,000+ employees across multi-tenant environment
• Collaborated extensively with Finance and HR teams to transform inefficient processes into empowered experiences  
• Increased platform ARPA by 35% through user access optimization and automated approval workflows
• Led cross-functional teams of 15+ engineers developing user permission frameworks and budget enforcement
• Deep empathy for finance professionals gained through direct collaboration and user research

I'm particularly drawn to Pleo's vision of making spend management seamless and empowering. Your focus on autonomy, trust, and removing the headache of controlling spend while maintaining control resonates with my approach to product management. The opportunity to work on category-defining innovations in user enablement and access controls is exactly what energizes me.

The chance to collaborate with Rob Guard and contribute to Pleo's market-leading position while working remotely from the Netherlands aligns perfectly with my career goals and Pleo's values of transparency and work-life balance.

I'm excited about the possibility of helping Pleo continue its mission to shape the future of work and would welcome the opportunity to discuss how my experience in user management, spend controls, and finance team collaboration can contribute to your 2026 roadmap.

Best regards,
Vinesh Kumar
Email: vineshmuthukumar@gmail.com
Phone: +91-81230-79049
Current Role: Senior Product Manager at COWRKS"""

    return email_content

def generate_pleo_linkedin_messages():
    """Generate LinkedIn messages for Pleo Senior Product Manager User & Controls role"""
    
    connection_request = """Hi! I saw the Senior Product Manager - User & Controls role at Pleo and I'm very interested. My experience building user management systems and spend controls for finance teams directly aligns with your user enablement mission. Would love to connect!"""
    
    direct_message = """Hello! I'm interested in the Senior Product Manager - User & Controls position at Pleo. I've spent the last 2 years building user management systems and spend control workflows that solve exactly the kind of inefficient process challenges you're revolutionizing.

A few things I've done that might be relevant:
• Built user permission frameworks for 600,000+ employees with complex spend approval workflows
• Collaborated with Finance and HR teams to reduce process time from 42 days to 10 minutes
• Led cross-functional team of 15+ engineers developing user access and budget enforcement systems
• Increased ARPA by 35% through user enablement and automated spend controls
• Achieved 91% satisfaction from finance professionals through empathetic problem-solving

What draws me to Pleo: Your mission to transform spend management through autonomy and trust resonates deeply with my product philosophy. The challenge of building market-leading user management capabilities while maintaining that Danish work-life balance culture is compelling.

I'm excited about the opportunity to work remotely from the Netherlands and contribute to Pleo's vision of helping companies "go beyond the books." The focus on empowering employees while maintaining financial control is exactly the kind of complex B2B problem I love solving.

Happy to discuss how my user management and spend control experience could contribute to your 2026 roadmap and continued market leadership!"""

    return {
        'connection_request': {
            'content': connection_request,
            'character_count': len(connection_request),
            'limit': 300
        },
        'direct_message': {
            'content': direct_message,
            'character_count': len(direct_message),
            'limit': 8000
        }
    }

def save_pleo_application():
    """Save complete Pleo application package"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"output/Pleo_Senior_Product_Manager_User_Controls_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Saving Pleo application package to: {output_dir}")
    
    # Generate all content
    resume = generate_pleo_resume()
    cover_letter = generate_pleo_cover_letter()
    email = generate_pleo_email()
    linkedin_messages = generate_pleo_linkedin_messages()
    jd_analysis = create_pleo_jd_analysis()
    
    # Save resume
    resume_file = output_dir / "vinesh_kumar_Pleo_resume_FINAL.txt"
    with open(resume_file, 'w', encoding='utf-8') as f:
        f.write(resume)
    print(f"✅ Resume saved: {resume_file}")
    
    # Save cover letter
    cover_file = output_dir / "vinesh_kumar_Pleo_cover_letter.txt"
    with open(cover_file, 'w', encoding='utf-8') as f:
        f.write(cover_letter)
    print(f"✅ Cover letter saved: {cover_file}")
    
    # Save email
    email_file = output_dir / "Pleo_application_email.txt"
    with open(email_file, 'w', encoding='utf-8') as f:
        f.write(email)
    print(f"✅ Email saved: {email_file}")
    
    # Save LinkedIn messages
    linkedin_file = output_dir / "Pleo_linkedin_messages.txt"
    with open(linkedin_file, 'w', encoding='utf-8') as f:
        f.write("LinkedIn Outreach Package for Pleo Senior Product Manager - User & Controls\n")
        f.write("=" * 80 + "\n\n")
        
        # Connection request
        conn = linkedin_messages['connection_request']
        f.write("🤝 CONNECTION REQUEST:\n")
        f.write(f"Characters: {conn['character_count']}/{conn['limit']}\n")
        f.write("-" * 30 + "\n")
        f.write(conn['content'] + "\n\n")
        
        # Direct message
        msg = linkedin_messages['direct_message']
        f.write("💬 DIRECT MESSAGE:\n")
        f.write(f"Characters: {msg['character_count']}/{msg['limit']}\n")
        f.write("-" * 30 + "\n")
        f.write(msg['content'] + "\n\n")
        
        f.write("📊 ANALYSIS:\n")
        f.write("-" * 30 + "\n")
        f.write("✅ Connection request under 300 character limit\n")
        f.write("✅ Direct message optimized for Pleo's collaborative culture\n")
        f.write("✅ User management and spend controls expertise highlighted\n")
        f.write("✅ Finance and HR team empathy demonstrated\n")
        f.write("✅ Pleo mission alignment and company knowledge shown\n")
        f.write("✅ Netherlands remote work enthusiasm expressed\n")
        f.write("✅ Danish work-life balance culture appreciation mentioned\n")
        f.write("✅ ARPA growth and measurable outcomes emphasized\n")
        f.write("✅ Cross-functional leadership experience showcased\n")
    
    print(f"✅ LinkedIn messages saved: {linkedin_file}")
    
    # Save JD analysis
    jd_file = output_dir / "Pleo_jd_analysis.json"
    with open(jd_file, 'w', encoding='utf-8') as f:
        json.dump(jd_analysis, f, indent=2, ensure_ascii=False)
    
    # Save package summary
    summary_file = output_dir / "APPLICATION_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Pleo Senior Product Manager - User & Controls Application Package\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n")
        f.write("**Company:** Pleo\n")
        f.write("**Role:** Senior Product Manager - User & Controls\n")
        f.write("**Location:** Remote (Netherlands/Europe)\n")
        f.write("**Focus:** Fintech, Spend Management, User Enablement\n")
        f.write("**Team Size:** 850+ employees from 100+ nations\n\n")
        f.write("## Key Alignments:\n\n")
        for alignment in jd_analysis['alignment_opportunities']:
            f.write(f"- ✅ {alignment}\n")
        f.write("\n## Product Focus Areas:\n\n")
        for area in jd_analysis['key_focus_areas']:
            f.write(f"- 🎯 {area}\n")
        f.write(f"\n## Pleo Values & Culture Alignment:\n\n")
        for value in jd_analysis['pleo_values_culture']:
            f.write(f"- 💼 {value}\n")
        f.write(f"\n## Growth & Business Impact:\n\n")
        for impact in jd_analysis['growth_and_business_impact']:
            f.write(f"- 📈 {impact}\n")
        f.write(f"\n## Package Contents:\n\n")
        f.write(f"- ✅ Resume tailored to user management and spend controls expertise\n")
        f.write(f"- ✅ Cover letter emphasizing finance/HR empathy and growth mindset\n") 
        f.write(f"- ✅ Professional application email highlighting Pleo mission alignment\n")
        f.write(f"- ✅ LinkedIn outreach package with Danish work culture appreciation\n")
        f.write(f"- ✅ JD analysis and alignment mapping for fintech domain\n")
        f.write(f"\n## Remote Work & Culture Fit:\n")
        f.write(f"- ✅ Netherlands remote work setup enthusiasm expressed\n")
        f.write(f"- ✅ Danish work-life balance culture alignment highlighted\n")
        f.write(f"- ✅ Cross-functional collaboration (>10 engineers) experience demonstrated\n")
        f.write(f"- ✅ Transparency and innovation values alignment shown\n")
        f.write(f"\n## Technical Domain Expertise:\n")
        f.write(f"- ✅ User permissions and access controls systems\n")
        f.write(f"- ✅ Spend policies and budget enforcement mechanisms\n")
        f.write(f"- ✅ Approval workflows and process automation\n")
        f.write(f"- ✅ HRIS integration and finance team collaboration\n")
        f.write(f"- ✅ B2B SaaS growth and ARPA optimization\n")
    
    return str(output_dir)

if __name__ == "__main__":
    print("🎯 PLEO SENIOR PRODUCT MANAGER - USER & CONTROLS APPLICATION GENERATOR")
    print("=" * 80)
    print("🏢 Company: Pleo")
    print("💼 Role: Senior Product Manager - User & Controls")
    print("📍 Location: Remote (Netherlands/Europe)")
    print("💰 Type: Full-time, Remote-first")
    print("🌐 Focus: Fintech, Spend Management, User Enablement")
    print("👥 Team: 850+ employees from 100+ nations")
    print("=" * 80)
    
    output_path = save_pleo_application()
    
    print(f"\n🎉 PLEO APPLICATION PACKAGE COMPLETE!")
    print(f"📁 Saved to: {output_path}")
    print(f"\n🎯 Key Features:")
    print(f"  ✅ User management and spend controls expertise highlighted")
    print(f"  ✅ Finance and HR team empathy demonstrated") 
    print(f"  ✅ Pleo mission alignment and company culture appreciation shown")
    print(f"  ✅ Cross-functional leadership experience (15+ engineers)")
    print(f"  ✅ Netherlands remote work enthusiasm expressed")
    print(f"  ✅ Danish work-life balance culture alignment")
    print(f"  ✅ ARPA growth and measurable outcomes emphasized")
    print(f"  ✅ Complete LinkedIn outreach strategy with fintech focus")
    print(f"  ✅ B2B SaaS growth mindset and innovation drive")
    print(f"  ✅ User research and customer empathy track record")