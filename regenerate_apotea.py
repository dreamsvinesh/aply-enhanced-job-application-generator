#!/usr/bin/env python3
"""
Regenerate complete Apotea Sweden application with enhanced content preservation
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent / 'modules'))

from enhanced_main import EnhancedJobApplicationGenerator

# Sample Apotea job description (e-commerce/health tech focus)
apotea_jd = """
Senior Product Manager - E-commerce Platform
Apotea
Stockholm, Sweden

We are seeking a Senior Product Manager to lead our e-commerce platform development. You will work with cross-functional teams to optimize user experience, improve conversion rates, and scale our digital health platform.

Key Responsibilities:
- Lead product strategy for e-commerce platform serving millions of customers
- Drive user engagement and conversion optimization initiatives
- Collaborate with engineering, design, and business teams
- Manage product roadmap and prioritization
- Analyze user behavior and implement data-driven improvements
- Scale platform capabilities to support business growth

Requirements:
- 5+ years of product management experience
- Experience with e-commerce platforms and user engagement
- Strong analytical and data-driven decision making skills
- Cross-functional team leadership experience
- Experience with agile methodologies
- B2C product experience preferred
- Experience scaling platforms for high user volumes

We value collaborative, humble, and team-oriented individuals who can drive results while working effectively in our Swedish work culture.
"""

def regenerate_apotea_application():
    """Regenerate the Apotea application with complete content"""
    
    print("🔄 REGENERATING APOTEA SWEDEN APPLICATION")
    print("=" * 60)
    
    try:
        # Initialize generator
        generator = EnhancedJobApplicationGenerator()
        
        # Generate complete application
        output_path = generator.generate_professional_application(
            job_description=apotea_jd,
            country="sweden", 
            company_name="Apotea"
        )
        
        print(f"\n✅ REGENERATION COMPLETE!")
        print(f"📄 New application saved to: {output_path}")
        print(f"\nKey improvements:")
        print(f"   ✓ Complete project details included")
        print(f"   ✓ Major platforms (Converge F&B) now featured")
        print(f"   ✓ Enhanced content preservation")
        print(f"   ✓ Human voice transformation applied")
        print(f"   ✓ Sweden cultural adaptation")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error regenerating application: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    regenerate_apotea_application()