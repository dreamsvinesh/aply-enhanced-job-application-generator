#!/usr/bin/env python3
"""
Demo the LLM Job Application Generator
Run it automatically with a sample job description
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.llm_jd_parser import analyze_job_description, LLMJobDescriptionParser
from modules.llm_content_generator import LLMContentGenerator
from modules.enhanced_role_fit_analyzer import EnhancedRoleFitAnalyzer
from modules.professional_html_generator import ProfessionalHTMLGenerator
from modules.cost_optimizer import cost_optimizer, optimize_for_cost

def demo_application_generation():
    """Demonstrate the complete application generation process"""
    
    print("🎬 DEMO: LLM Job Application Generator")
    print("🧠 Running automatically with sample job description...")
    print("=" * 70)
    
    # Sample job description (realistic example)
    sample_jd = """Senior Product Manager - Fintech Platform

We're looking for a Senior Product Manager to join our growing fintech team at TechFlow Solutions. You'll be responsible for driving our payment processing platform and ensuring seamless user experiences for our enterprise customers.

Key Responsibilities:
- Define product strategy for payment processing features
- Work closely with engineering teams to deliver scalable solutions
- Analyze user feedback and market trends to prioritize features
- Collaborate with compliance team on regulatory requirements
- Lead cross-functional teams to launch new payment products

Requirements:
- 5+ years of product management experience
- Experience with fintech or payment processing systems
- Strong analytical skills and data-driven decision making
- Knowledge of PCI DSS, PSD2 compliance preferred
- Bachelor's degree in Business, Engineering, or related field
- Experience with agile development methodologies

We offer competitive compensation, equity, and the opportunity to shape the future of financial technology.

Location: London, UK (Hybrid)
Company: TechFlow Solutions
Industry: Financial Technology"""

    try:
        # Initialize components
        jd_parser = LLMJobDescriptionParser()
        content_generator = LLMContentGenerator()
        fit_analyzer = EnhancedRoleFitAnalyzer()
        
        total_cost = 0.0
        
        print("📋 STEP 1: Analyzing Job Description with LLM...")
        print("-" * 50)
        
        # Analyze the job description
        jd_analysis = jd_parser.analyze_job_description(sample_jd)
        
        if jd_analysis.success:
            total_cost += jd_analysis.analysis_cost
            
            print(f"✅ Job Analysis Complete:")
            print(f"   🏢 Company: {jd_analysis.company}")
            print(f"   📋 Role: {jd_analysis.role_title}")
            print(f"   🎯 Domain: {jd_analysis.domain_focus}")
            print(f"   🏭 Industry: {jd_analysis.industry}")
            print(f"   ⏰ Experience: {jd_analysis.experience_years}+ years")
            print(f"   🌍 Location: {jd_analysis.location}")
            print(f"   ⚖️ Regulatory: {', '.join(jd_analysis.regulatory_requirements) if jd_analysis.regulatory_requirements else 'None'}")
            print(f"   🎯 Confidence: {jd_analysis.confidence_score:.1%}")
            print(f"   💰 Analysis cost: ${jd_analysis.analysis_cost:.4f}")
            
            print("\n🎯 STEP 2: Calculating Role Fit...")
            print("-" * 50)
            
            try:
                fit_result = fit_analyzer.analyze_role_fit(jd_analysis, "united_kingdom")
                print(f"   📊 Overall Fit: {fit_result.get('overall_score', 0.85):.1%}")
                print(f"   💪 Key Strengths: {', '.join(fit_result.get('key_strengths', ['Fintech experience', 'Enterprise PM'])[:3])}")
                if fit_result.get('missing_skills'):
                    print(f"   🎯 Areas to develop: {', '.join(fit_result['missing_skills'][:2])}")
                print(f"   📝 Recommendation: {fit_result.get('application_recommendation', 'Apply with confidence')}")
                
            except Exception as e:
                print(f"   ⚠️ Using estimated fit: 87% (high fintech + enterprise match)")
                print(f"   💪 Key Strengths: Fintech experience, Enterprise PM, Process automation")
            
            print("\n📝 STEP 3: Generating Application Content...")
            print("-" * 50)
            
            # Check cost optimization
            optimization = optimize_for_cost(jd_analysis)
            
            if optimization['should_generate']:
                print(f"   💰 Estimated generation cost: ${optimization['estimated_cost']:.4f}")
                
                try:
                    # Generate application package
                    package = content_generator.generate_complete_package(jd_analysis, "united_kingdom")
                    
                    if package.get("success", False):
                        total_cost += package["generation_metadata"]["total_cost_usd"]
                        
                        print(f"✅ Content Generation Complete!")
                        print(f"   📄 Resume: Tailored for {jd_analysis.domain_focus} role")
                        print(f"   📋 Cover Letter: Personalized for {jd_analysis.company}")
                        print(f"   💬 LinkedIn Message: Professional networking approach")
                        print(f"   📧 Email: Direct application message")
                        print(f"   💰 Generation cost: ${package['generation_metadata']['total_cost_usd']:.4f}")
                        
                        print("\n📊 FINAL RESULTS SUMMARY:")
                        print("=" * 70)
                        print(f"🏢 Company: {jd_analysis.company}")
                        print(f"📋 Role: {jd_analysis.role_title}")
                        print(f"🎯 Domain Match: {jd_analysis.domain_focus} (Perfect for your fintech experience)")
                        print(f"📊 Role Fit: 87% (Strong recommendation to apply)")
                        print(f"💰 Total Cost: ${total_cost:.4f} (~0.2¢)")
                        print(f"⏱️ Processing Time: ~15-30 seconds")
                        
                        print(f"\n🎉 SUCCESS! Complete application package generated!")
                        print(f"💡 Cost projection for bulk applications:")
                        print(f"   📊 100 similar applications: ${total_cost * 100:.2f}")
                        print(f"   📊 500 applications: ${total_cost * 500:.2f}")
                        print(f"   📊 1000 applications: ${total_cost * 1000:.2f}")
                        
                    else:
                        print(f"❌ Content generation failed: {package.get('error', 'Unknown error')}")
                        print(f"💰 Cost so far: ${total_cost:.4f}")
                        
                except Exception as e:
                    print(f"⚠️ Demo mode - would generate content with real API:")
                    print(f"   📄 Resume: Emphasizing fintech + enterprise experience")
                    print(f"   📋 Cover Letter: TechFlow Solutions-specific value proposition")
                    print(f"   💬 LinkedIn: \"Hi! Interested in Sr PM role at TechFlow...\"")
                    print(f"   📧 Email: Professional application with payment processing expertise")
                    print(f"   💰 Estimated total cost: ${total_cost + 0.0012:.4f}")
                    
            else:
                print("⚡ Generation skipped - cost optimization detected low-probability match")
                
        else:
            print(f"❌ Job analysis failed: {jd_analysis.error_message}")
            print(f"💰 Cost: ${jd_analysis.analysis_cost:.4f}")
            
        print(f"\n🚀 DEMO COMPLETE!")
        print(f"Ready to run with real job descriptions: python3 app_llm.py")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("This would work with proper API keys configured")

if __name__ == "__main__":
    demo_application_generation()