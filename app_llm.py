#!/usr/bin/env python3
"""
LLM-Enhanced Job Application Generator
Intelligent job application generation using LLM analysis and content generation
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.llm_jd_parser import analyze_job_description, LLMJobDescriptionParser
from modules.llm_content_generator import LLMContentGenerator
from modules.enhanced_role_fit_analyzer import EnhancedRoleFitAnalyzer
from modules.professional_html_generator import ProfessionalHTMLGenerator
from modules.cost_optimizer import cost_optimizer, optimize_for_cost

class LLMJobApplicationGenerator:
    """Next-generation job application generator powered by LLM intelligence"""
    
    def __init__(self):
        self.jd_parser = LLMJobDescriptionParser()
        self.content_generator = LLMContentGenerator()
        self.fit_analyzer = EnhancedRoleFitAnalyzer()
        self.html_generator = ProfessionalHTMLGenerator()
        
        print("🚀 LLM-Enhanced Job Application Generator")
        print("🧠 Intelligent analysis | 📝 Tailored content | 🎯 Perfect fit scoring | 💰 0.3¢ per application")
        print("=" * 70)
    
    def analyze_job(self, job_description: str) -> Dict[str, Any]:
        """Analyze job description using LLM intelligence"""
        
        print("\n🔍 Analyzing job description with LLM...")
        
        # Use LLM to analyze the job description
        jd_analysis = self.jd_parser.analyze_job_description(job_description)
        
        if not jd_analysis.success:
            return {
                "success": False,
                "error": f"Job analysis failed: {jd_analysis.error_message}",
                "cost": jd_analysis.analysis_cost
            }
        
        # Display analysis results
        print(f"\n✅ Job Analysis Complete:")
        print(f"   🏢 Company: {jd_analysis.company}")
        print(f"   📋 Role: {jd_analysis.role_title}")
        print(f"   🎯 Domain: {jd_analysis.domain_focus}")
        print(f"   🏭 Industry: {jd_analysis.industry}")
        print(f"   ⏰ Experience: {jd_analysis.experience_years}+ years")
        print(f"   🌍 Location: {jd_analysis.location}")
        print(f"   💰 Analysis cost: ${jd_analysis.analysis_cost:.4f}")
        
        if jd_analysis.regulatory_requirements:
            print(f"   ⚖️  Regulatory: {', '.join(jd_analysis.regulatory_requirements)}")
        
        return {
            "success": True,
            "analysis": jd_analysis,
            "cost": jd_analysis.analysis_cost
        }
    
    def calculate_fit_score(self, jd_analysis, country: str = "united_states") -> Dict[str, Any]:
        """Calculate role fit using enhanced analyzer"""
        
        print(f"\n🎯 Calculating role fit for {country.replace('_', ' ').title()}...")
        
        try:
            fit_result = self.fit_analyzer.analyze_role_fit(jd_analysis, country)
            
            print(f"   📊 Overall Fit: {fit_result.get('overall_score', 0):.1%}")
            print(f"   💪 Strengths: {', '.join(fit_result.get('key_strengths', [])[:3])}")
            
            if fit_result.get('missing_skills'):
                print(f"   🎯 To develop: {', '.join(fit_result['missing_skills'][:2])}")
            
            return fit_result
            
        except Exception as e:
            print(f"   ⚠️  Fit analysis error: {e}")
            return {"overall_score": 0.75, "application_recommendation": "apply_with_customization"}
    
    def generate_applications(self, jd_analysis, country: str) -> Dict[str, Any]:
        """Generate complete application package using LLM with cost optimization"""
        
        # Check if generation is cost-effective
        optimization = optimize_for_cost(jd_analysis)
        
        if not optimization['should_generate']:
            print(f"\n⚡ Skipping generation - not cost-effective for this role")
            print(f"   Reason: Low confidence or poor fit detected")
            return {"success": False, "error": "Generation skipped for cost optimization", "cost": 0.0}
        
        estimated_cost = optimization['estimated_cost']
        print(f"\n📝 Generating application package (est. ${estimated_cost:.4f})...")
        
        try:
            # Generate complete package using LLM
            package = self.content_generator.generate_complete_package(jd_analysis, country)
            
            if not package.get("success", False):
                return {
                    "success": False,
                    "error": package.get("error", "Content generation failed"),
                    "cost": package.get("total_cost", 0.0)
                }
            
            print(f"   ✅ Complete package generated!")
            print(f"   📄 Resume: Tailored for {jd_analysis.domain_focus} role")
            print(f"   📋 Cover letter: Company-specific content")
            print(f"   💬 LinkedIn message: Professional outreach")
            print(f"   📧 Email: Direct approach message")
            
            return package
            
        except Exception as e:
            print(f"   ❌ Generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "cost": 0.0
            }
    
    def save_results(self, package: Dict[str, Any], jd_analysis) -> str:
        """Save results to files and generate HTML"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        company_clean = jd_analysis.company.replace(" ", "_").replace("/", "_")
        output_dir = Path("output") / f"{company_clean}_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save individual files
        files_created = []
        
        try:
            # Resume
            resume_file = output_dir / "resume.md"
            with open(resume_file, 'w', encoding='utf-8') as f:
                f.write(package["generated_content"]["resume"])
            files_created.append(str(resume_file))
            
            # Cover letter
            cover_file = output_dir / "cover_letter.md"
            with open(cover_file, 'w', encoding='utf-8') as f:
                f.write(package["generated_content"]["cover_letter"])
            files_created.append(str(cover_file))
            
            # Messages
            messages_file = output_dir / "messages.json"
            with open(messages_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "linkedin": package["generated_content"]["linkedin_message"],
                    "email": package["generated_content"]["email"]
                }, f, indent=2)
            files_created.append(str(messages_file))
            
            # Job analysis
            analysis_file = output_dir / "job_analysis.json"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "company": jd_analysis.company,
                    "role_title": jd_analysis.role_title,
                    "domain_focus": jd_analysis.domain_focus,
                    "industry": jd_analysis.industry,
                    "confidence_score": jd_analysis.confidence_score,
                    "required_skills": jd_analysis.required_skills,
                    "regulatory_requirements": jd_analysis.regulatory_requirements
                }, f, indent=2)
            files_created.append(str(analysis_file))
            
            # Generate HTML version
            print("\n🎨 Generating professional HTML...")
            html_content = self.generate_html(package, jd_analysis)
            
            html_file = output_dir / "application_package.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            files_created.append(str(html_file))
            
            print(f"\n✅ Files saved to: {output_dir}")
            for file_path in files_created:
                print(f"   📁 {file_path}")
            
            return str(output_dir)
            
        except Exception as e:
            print(f"❌ Error saving files: {e}")
            return ""
    
    def generate_html(self, package: Dict[str, Any], jd_analysis) -> str:
        """Generate professional HTML presentation"""
        
        # Prepare data for HTML generator
        html_data = {
            "job_info": {
                "company": jd_analysis.company,
                "role_title": jd_analysis.role_title,
                "location": jd_analysis.location,
                "domain": jd_analysis.domain_focus,
                "industry": jd_analysis.industry
            },
            "content": {
                "resume": package["generated_content"]["resume"],
                "cover_letter": package["generated_content"]["cover_letter"],
                "linkedin_message": package["generated_content"]["linkedin_message"],
                "email_subject": package["generated_content"]["email"].get("subject", ""),
                "email_body": package["generated_content"]["email"].get("body", "")
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "confidence_score": jd_analysis.confidence_score,
                "total_cost": package["generation_metadata"]["total_cost_usd"],
                "llm_generated": True
            }
        }
        
        return self.html_generator.generate_comprehensive_html(html_data)
    
    def run_interactive(self):
        """Run interactive job application generator"""
        
        total_cost = 0.0
        
        try:
            # Get job description
            print("\n📋 Paste the job description (press Enter twice when done):")
            job_lines = []
            empty_lines = 0
            
            while True:
                line = input()
                if line.strip() == "":
                    empty_lines += 1
                    if empty_lines >= 2:
                        break
                else:
                    empty_lines = 0
                    job_lines.append(line)
            
            job_description = "\n".join(job_lines).strip()
            
            if not job_description:
                print("❌ No job description provided!")
                return
            
            # Get country
            print("\n🌍 Select country:")
            countries = [
                "united_states", "canada", "united_kingdom", "germany", 
                "netherlands", "sweden", "denmark", "australia"
            ]
            
            for i, country in enumerate(countries, 1):
                print(f"   {i}. {country.replace('_', ' ').title()}")
            
            try:
                choice = int(input("\nEnter number (default: 1): ").strip() or "1")
                country = countries[choice - 1] if 1 <= choice <= len(countries) else countries[0]
            except ValueError:
                country = countries[0]
            
            print(f"Selected: {country.replace('_', ' ').title()}")
            
            # Start processing
            start_time = time.time()
            
            # Step 1: Analyze job
            analysis_result = self.analyze_job(job_description)
            if not analysis_result["success"]:
                print(f"❌ {analysis_result['error']}")
                return
            
            total_cost += analysis_result["cost"]
            jd_analysis = analysis_result["analysis"]
            
            # Step 2: Calculate fit
            fit_result = self.calculate_fit_score(jd_analysis, country)
            
            # Step 3: Generate applications
            package = self.generate_applications(jd_analysis, country)
            if not package["success"]:
                print(f"❌ Content generation failed: {package['error']}")
                return
            
            total_cost += package["generation_metadata"]["total_cost_usd"]
            
            # Step 4: Save results
            output_dir = self.save_results(package, jd_analysis)
            
            # Summary
            processing_time = time.time() - start_time
            print(f"\n🎉 APPLICATION PACKAGE COMPLETE!")
            print(f"   ⏱️  Processing time: {processing_time:.1f} seconds")
            print(f"   💰 Total cost: ${total_cost:.4f} (~0.3¢)")
            print(f"   🎯 Role fit: {fit_result.get('overall_score', 0.75):.1%}")
            print(f"   📁 Saved to: {output_dir}")
            
            # Cost projection for bulk applications
            if total_cost > 0:
                cost_per_500 = total_cost * 500
                print(f"\n💡 Cost projection:")
                print(f"   📊 500 applications: ${cost_per_500:.2f}")
                print(f"   📈 1000 applications: ${cost_per_500 * 2:.2f}")
            
            if output_dir:
                html_file = Path(output_dir) / "application_package.html"
                print(f"\n🌐 View in browser: file://{html_file.absolute()}")
            
        except KeyboardInterrupt:
            print(f"\n\n⚡ Interrupted. Total cost so far: ${total_cost:.4f}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print(f"💰 Cost incurred: ${total_cost:.4f}")

def main():
    """Main entry point"""
    
    # Check if API keys are available
    import os
    if not (os.getenv('ANTHROPIC_API_KEY') or os.getenv('OPENAI_API_KEY')):
        print("⚠️  WARNING: No API keys detected!")
        print("Set ANTHROPIC_API_KEY or OPENAI_API_KEY to use LLM features.")
        print("Running in demo mode...\n")
    
    generator = LLMJobApplicationGenerator()
    generator.run_interactive()

if __name__ == "__main__":
    main()