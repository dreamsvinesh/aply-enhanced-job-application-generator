#!/usr/bin/env python3
"""Quick Apotea generation without timeout issues"""

import sys
from pathlib import Path

# Simple approach - use the content generator directly 
sys.path.append(str(Path(__file__).parent / 'modules'))

try:
    from content_preserving_generator import ContentPreservingGenerator
    from cover_letter_generator import CoverLetterGenerator 
    from message_generator import MessageGenerator
    from professional_html_generator import ProfessionalHTMLGenerator
    from human_voice_agent import HumanVoiceAgent
    
    # Sample JD data
    jd_data = {
        'job_description': 'Senior Product Manager role for e-commerce platform at Apotea in Sweden',
        'company': 'Apotea',
        'country': 'sweden',
        'required_skills': ['product management', 'e-commerce', 'user engagement', 'scaling'],
        'job_title': 'Senior Product Manager',
        'role_title': 'Senior Product Manager'
    }
    
    print("🔄 Generating Apotea application components...")
    
    # Generate each component
    content_gen = ContentPreservingGenerator()
    resume_data, changes = content_gen.generate_full_resume(jd_data, 'sweden')
    
    cover_gen = CoverLetterGenerator()
    cover_letter = cover_gen.generate(jd_data, 'sweden', 'Apotea')
    
    message_gen = MessageGenerator()
    linkedin_msg = message_gen.generate_linkedin_message(jd_data, 'sweden')
    email_template = message_gen.generate_email_message(jd_data, 'sweden', 'Apotea')
    
    # Apply human voice
    voice_agent = HumanVoiceAgent()
    content_dict = {
        'resume': resume_data,
        'cover_letter': cover_letter,
        'linkedin_message': linkedin_msg,
        'email_template': email_template
    }
    
    humanized_content = voice_agent.humanize_content(content_dict)
    
    # Generate HTML
    html_gen = ProfessionalHTMLGenerator()
    metadata = {
        'company': 'Apotea',
        'country': 'sweden',
        'applicant_name': 'VINESH KUMAR',
        'ats_score': 91,
        'changes_made': changes
    }
    
    html_content = html_gen.generate_professional_application(humanized_content, metadata)
    
    # Save file
    output_path = Path(__file__).parent / "output" / "Apotea_sweden_2025-11-13_FIXED.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated: {output_path}")
    
    # Analyze the content
    experience = humanized_content['resume']['experience']
    total_bullets = sum(len(role['highlights']) for role in experience)
    
    print(f"📊 Content Analysis:")
    print(f"   Experience roles: {len(experience)}")
    print(f"   Total bullet points: {total_bullets}")
    
    # Check for Converge platform
    all_content = str(humanized_content)
    has_converge = 'converge' in all_content.lower() or '30,000' in all_content
    has_gmv = '168' in all_content or '180' in all_content
    
    print(f"   Has Converge F&B Platform: {'✅' if has_converge else '❌'}")
    print(f"   Has GMV metrics: {'✅' if has_gmv else '❌'}")
    
    if has_converge and has_gmv:
        print(f"\n🎉 SUCCESS! Major platform now included with full metrics!")
    else:
        print(f"\n⚠️ Issues may remain in content generation")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()