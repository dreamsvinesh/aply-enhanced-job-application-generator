#!/usr/bin/env python3
"""
Generate Lunar Senior Product Manager application with the specific JD provided
"""

import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent / 'modules'))

def generate_lunar_senior_pm():
    """Generate application for Lunar Senior Product Manager role"""
    
    from enhanced_main import EnhancedJobApplicationGenerator
    
    # Full Lunar JD as provided
    lunar_jd = """
    As a Senior Product Manager, you will ensure that the cards and account top-up experiences are so simple, intuitive and scalable that it becomes an automated and frictionlessly journey of the customer's financial life. Your ultimate goal: simplify and scale the card and account top up capabilities, so that it becomes highly automated and built for hyper-personal experiences.

At Lunar, we are democratizing the power of money and changing the way we all bank, pay, and invest. Since starting in Aarhus in 2015, we've grown rapidly and are now a major player in the Nordics, with offices in Copenhagen, Aarhus, and Stockholm 🚀

So, who are we? Are we a tech company or a bank? Well, we're both breaking free from the usual categories. At Lunar, tech isn't just a cool add-on; it's the core of how we do things. With our own banking license, we go head-to-head with traditional banks. What sets us apart is the mix of tech and financial services, giving us the power to shake up a dusty industry that's ready for a change.

As we continue our journey to becoming the best everyday bank in the Nordics, we are looking for a/an Senior Product Manager to ensure that the cards and account top-up experiences are so simple, intuitive and scalable so that we can become an automated and frictionlessly journey of the customer's financial life.

What will you do?

Product Strategy & roadmap: Define the strategy for card payments and account-top-ups that aligns with our Nordic presence ambitions, our core Invisible Banking differentiator and our Scalable banking mantra. Translate this into a clear roadmap.

Product Lifecycle: Lead the development of card issuing & processing and account-top-ups payment solutions for Lunar customers. Work intimately with Engineering (and other stakeholders) to build a hyper-efficient foundation.

Scale & compliance: Build and run a foundation that ensures our payment infrastructure is robust, fast, and compliant (PSD2, GDPR, etc.), turning scalability into a competitive advantage for our growth.

Vendor & Innovation pipeline: Proactively manage key partners and vendors, ensuring they power our future vision and feed an innovation pipeline that keeps Lunar at the cutting edge of fintech.

Performance: Be data-driven, defining and monitoring KPIs that measure effortlessness and efficiency, not just usage.

What are we looking for in you?

We're excited to welcome everyone to apply for this impactful role! We can't wait to follow up with talents who we believe are the best fit based on the following criteria:

Domain mastery (5+ years): Deep, hands-on experience in product management with a focus on payment products within a regulated fintech or banking environment.

Payments expertise: A strong understanding of the payments ecosystem, including card network rules (Visa/Mastercard), alternative payment methods foundations and payments processing flows.

Technical acumen: The ability to understand complex system architecture and engage effectively with engineering teams to build a fast, low-cost, high-velocity foundation for growth.

Strategic Leadership: Proven ability to define a product strategy, influence stakeholders across the organization (including senior leadership), and be able to guide and motivate a high-performing team. 

Nordic focus (desirable): Experience or a strong understanding of the unique Nordic payments landscape and its regulatory environment.
    """
    
    print("🚀 GENERATING LUNAR SENIOR PRODUCT MANAGER APPLICATION")
    print("=" * 60)
    print("🎯 Role: Senior Product Manager - Cards & Account Top-up")
    print("🏢 Company: Lunar")  
    print("📍 Location: Denmark")
    print("💳 Focus: Payment Infrastructure & Fintech")
    
    start_time = time.time()
    
    try:
        print(f"\n⏱️  Starting generation at {time.strftime('%H:%M:%S')}")
        
        # Initialize generator with full validation system
        generator = EnhancedJobApplicationGenerator()
        
        # Generate comprehensive application 
        result_path = generator.generate_professional_application(
            job_description=lunar_jd,
            country="denmark",
            company_name="Lunar"
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🎉 SUCCESS!")
        print(f"📁 Generated: {result_path}")
        print(f"⏱️  Total time: {duration:.1f} seconds")
        
        # Verify file details
        if result_path and Path(result_path).exists():
            file_size = Path(result_path).stat().st_size
            print(f"📊 File size: {file_size:,} bytes")
            
            # Quick content verification
            with open(result_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            sections_found = []
            if "📄 Resume" in content: sections_found.append("Resume")
            if "📝 Cover Letter" in content: sections_found.append("Cover Letter") 
            if "💬 LinkedIn Message" in content: sections_found.append("LinkedIn")
            if "📧 Email Template" in content: sections_found.append("Email")
            
            print(f"✅ Sections included: {', '.join(sections_found)}")
            
            # Check for fintech/payments content
            fintech_keywords = ["payment", "fintech", "card", "automation", "Lunar"]
            keywords_found = [kw for kw in fintech_keywords if kw.lower() in content.lower()]
            print(f"💳 Fintech keywords: {', '.join(keywords_found)}")
        
        return result_path
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n❌ FAILED after {duration:.1f} seconds")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = generate_lunar_senior_pm()
    if result:
        print(f"\n🎉 LUNAR APPLICATION READY!")
        print(f"📁 File: {result}")
        print(f"\n📋 Next steps:")
        print("   1. Open the HTML file in your browser")
        print("   2. Review the content and validation feedback")
        print("   3. Copy sections as needed for your application")
        print("   4. The content is optimized for Danish fintech market")
        print("\n✨ Features included:")
        print("   🛡️  3-tier validation system")
        print("   🤖 Human writing quality (avoiding AI patterns)")
        print("   💳 Fintech/payments domain optimization")
        print("   🇩🇰 Danish cultural adaptation")
    else:
        print("\n💥 Application generation failed")
        sys.exit(1)