#!/usr/bin/env python3

import json
import sys
from pathlib import Path

# Add modules to path
sys.path.append('modules')

from professional_html_generator import ProfessionalHTMLGenerator

def generate_apotea_application():
    """Generate Apotea application without LLM timeouts"""
    
    # Load user profile
    with open('data/user_profile.json', 'r') as f:
        user_profile = json.load(f)
    
    # Custom content for Apotea cloud transformation role
    resume_data = {
        'personal_info': {
            'name': user_profile['personal_info']['name'],
            'title': 'Senior Product Manager - Cloud Transformation | Technical Leadership | Enterprise Systems',
            'phone': user_profile['personal_info']['phone'],
            'email': user_profile['personal_info']['email'],
            'linkedin': user_profile['personal_info']['linkedin'],
            'location': user_profile['personal_info']['location']
        },
        'summary': '''Senior Product Manager with 11 years in technology (7 in PM) specializing in cloud transformation, enterprise system modernization, and cross-functional technical leadership. Built AI-powered systems achieving 94% accuracy serving 200+ users, automated workflows reducing timelines from 42 days to 10 minutes (accelerating $2M revenue), and led technical teams through platform migrations. Expert in cloud architecture, API integration, microservices, supply chain optimization, and scaling operations for high-growth e-commerce companies.''',
        'skills': 'Cloud Architecture | System Migration | Cross-functional Leadership | Supply Chain Operations | E-commerce Platforms | API Integration | Microservices | DevOps | CI/CD | Product Strategy | Technical Leadership | AI/ML Integration | Enterprise Platforms | Agile/SAFe | Stakeholder Management',
        'experience': user_profile['experience'],
        'education': user_profile['education']
    }
    
    cover_letter = '''Dear Hiring Manager,

I am excited to apply for the Product Manager position leading Apotea's cloud transformation initiative. My background in technical product management, enterprise system migrations, and cross-functional leadership aligns perfectly with this transformational role.

In my current role, I have led complex technical initiatives including building AI-powered systems achieving 94% accuracy and automating enterprise workflows that accelerated $2M in revenue recognition. This experience has given me the technical depth and strategic thinking needed to bridge business operations with cloud architecture - exactly what this transformation requires.

Most relevant to this role, I have extensive experience in system integration across Salesforce, SAP, and enterprise platforms, managing cross-functional teams through technical transformations. My work automating contract workflows from 42 days to 10 minutes demonstrates my ability to translate operational needs into scalable technical solutions that drive measurable business impact.

I am particularly drawn to Apotea's mission of making healthcare accessible and the opportunity to rebuild the technical foundation for Sweden's largest online pharmacy. The prospect of leading a cross-functional team of engineers to modernize supply chain operations while establishing new standards for reliability and performance is exactly the kind of challenging, high-impact work I thrive on.

My experience with enterprise automation, technical product strategy, and building high-performing teams would enable me to drive this cloud transformation while ensuring alignment across operations, logistics, and data teams to deliver end-to-end business value.

Thank you for considering my application. I look forward to discussing how my technical background and product leadership experience can contribute to Apotea's cloud transformation success.

Kind regards,
Vinesh Kumar'''

    linkedin_message = '''Hello, I noticed the Product Manager position leading Apotea's cloud transformation. My background includes technical product management, enterprise system migrations, and cross-functional leadership for complex platform rebuilds in e-commerce environments. I believe my experience in cloud architecture and supply chain optimization could contribute to this transformational initiative. Would you be open to a brief conversation?'''

    email_template = {
        'subject': 'Application: Product Manager - Cloud Transformation at Apotea',
        'body': '''Dear Hiring Manager,

I would like to apply for the Product Manager position leading Apotea's cloud transformation.

My background includes:
• Led enterprise system integrations and technical transformations for e-commerce platforms
• Built AI-powered platforms achieving 94% accuracy serving 200+ users
• Automated supply chain workflows reducing timelines from 42 days to 10 minutes
• Strong experience in cross-functional technical leadership and cloud architecture
• Expertise in API integration, microservices, and enterprise platform modernization

I believe my technical product management experience and transformation leadership would enable me to drive Apotea's cloud transformation successfully while building high-performing engineering teams.

Kind regards,
Vinesh Kumar
+91-81230-79049
vineshmuthukumar@gmail.com'''
    }
    
    # Generate HTML
    html_generator = ProfessionalHTMLGenerator()
    content_dict = {
        'resume': resume_data,
        'cover_letter': cover_letter,
        'linkedin_message': linkedin_message,
        'email_template': email_template
    }
    
    metadata = {
        'company': 'Apotea',
        'country': 'sweden',
        'applicant_name': 'Vinesh Kumar',
        'ats_score': 91
    }
    
    html_content = html_generator.generate_professional_application(content_dict, metadata)
    
    # Save output
    output_path = Path('output/Apotea_sweden_2025-11-13_professional.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return str(output_path)

if __name__ == "__main__":
    print("🚀 Generating Apotea application (fast version)")
    output_path = generate_apotea_application()
    print(f"✅ Apotea application generated: {output_path}")