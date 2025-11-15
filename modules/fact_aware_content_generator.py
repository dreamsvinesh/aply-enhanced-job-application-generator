#!/usr/bin/env python3
"""
Fact-Aware Content Generator
Enhanced content generator that preserves user's factual information
while customizing presentation for target roles.
"""

import json
from typing import Dict, List, Any, Tuple
from pathlib import Path
from modules.user_data_extractor import UserDataExtractor
from modules.llm_service import LLMService
from modules.content_quality_validator import ContentQualityValidator

class FactAwareContentGenerator:
    """Generates content while preserving factual user data"""
    
    def __init__(self):
        self.user_extractor = UserDataExtractor()
        self.llm_service = LLMService()
        self.quality_validator = ContentQualityValidator()
        self.factual_data = self.user_extractor.extract_vinesh_data()
    
    def generate_fact_aware_resume(self, jd_analysis: Dict, country: str = "netherlands") -> Dict[str, Any]:
        """Generate resume preserving real work history at COWRKS"""
        
        constraints_prompt = self.user_extractor.create_llm_constraints_prompt()
        
        prompt = f"""
{constraints_prompt}

TASK: Create a resume for {self.factual_data['personal_info']['name']} targeting this role:

JOB REQUIREMENTS:
{json.dumps(jd_analysis, indent=2)}

COUNTRY STYLE: {country}

REAL WORK HISTORY TO USE:
{json.dumps(self.factual_data['work_experience'], indent=2)}

REAL EDUCATION:
{json.dumps(self.factual_data['education'], indent=2)}

INSTRUCTIONS:
1. Use ONLY the real companies: COWRKS, Automne Technologies, Rukshaya Emerging Technologies
2. Preserve exact contact info: {self.factual_data['personal_info']['email']}, {self.factual_data['personal_info']['phone']}
3. Keep real metrics: 94% accuracy, 42 days to 10 minutes, $2M revenue, etc.
4. Customize ONLY the presentation, emphasis, and ordering for this specific role
5. Use Netherlands communication style: direct, efficient, results-focused
6. Emphasize relevant achievements from COWRKS for this role

Generate a professional resume that uses real facts but customizes presentation.
"""
        
        response = self.llm_service.call_llm(
            prompt=prompt,
            task_type="resume_generation",
            temperature=0.2,
            max_tokens=2000
        )
        
        # Validate content doesn't fabricate
        fact_validation = self.user_extractor.validate_content_against_facts(response.content)
        
        # Validate content quality and word count
        quality_validation = self.quality_validator.validate_content_quality(response.content, 'resume')
        
        return {
            'content': response.content,
            'fact_validation': fact_validation,
            'quality_validation': quality_validation,
            'preserves_facts': fact_validation['is_valid'],
            'quality_score': quality_validation['score'],
            'word_count': quality_validation['word_count'],
            'issues': fact_validation['violations'] + quality_validation['issues'],
            'suggestions': quality_validation['suggestions']
        }
    
    def generate_fact_aware_cover_letter(self, jd_analysis: Dict, country: str = "netherlands") -> Dict[str, Any]:
        """Generate cover letter preserving real company history"""
        
        constraints_prompt = self.user_extractor.create_llm_constraints_prompt()
        
        prompt = f"""
{constraints_prompt}

TASK: Create a cover letter for {self.factual_data['personal_info']['name']} targeting this role:

COMPANY: {jd_analysis['extracted_info']['company']}
ROLE: {jd_analysis['extracted_info']['role_title']}

JOB REQUIREMENTS:
{json.dumps(jd_analysis['requirements'], indent=2)}

REAL ACHIEVEMENTS TO REFERENCE:
• At COWRKS (current): Built AI RAG system (94% accuracy), automated workflows (42 days → 10 minutes), $2M revenue acceleration
• At COWRKS (previous): Mobile app features, process optimization, €220K monthly revenue generation
• Total experience: {self.factual_data['professional_summary']['years_experience']}

INSTRUCTIONS:
1. Reference ONLY real companies and achievements from COWRKS experience
2. Use specific metrics: 94% accuracy, $2M revenue, 99.6% reduction, etc.
3. Connect real COWRKS experience to target role requirements
4. Netherlands style: direct, professional, results-focused
5. NEVER mention TechCorp, ScaleupCo, or any fabricated companies

Generate compelling cover letter using real facts.
"""
        
        response = self.llm_service.call_llm(
            prompt=prompt,
            task_type="cover_letter",
            temperature=0.3,
            max_tokens=1000
        )
        
        validation = self.user_extractor.validate_content_against_facts(response.content)
        
        return {
            'content': response.content,
            'validation': validation,
            'preserves_facts': validation['is_valid']
        }
    
    def generate_fact_aware_email(self, jd_analysis: Dict, country: str = "netherlands") -> Dict[str, Any]:
        """Generate email template preserving real experience"""
        
        constraints_prompt = self.user_extractor.create_llm_constraints_prompt()
        
        prompt = f"""
{constraints_prompt}

TASK: Create professional email for {self.factual_data['personal_info']['name']} applying to:

COMPANY: {jd_analysis['extracted_info']['company']}
ROLE: {jd_analysis['extracted_info']['role_title']}

KEY REAL ACHIEVEMENTS:
• COWRKS Senior PM: AI RAG system (94% accuracy), workflow automation ($2M revenue impact)
• COWRKS PM: Mobile features (45% engagement increase), process optimization
• Technical background: Frontend Engineer at Automne Technologies & Rukshaya Emerging Technologies
• Education: Master of Science in Software Engineering, Anna University

INSTRUCTIONS:
1. Reference only real companies: COWRKS, Automne Technologies, Rukshaya Emerging Technologies
2. Use real metrics and achievements
3. Professional email format with subject line
4. Netherlands style: concise, direct, results-oriented
5. Contact info: {self.factual_data['personal_info']['email']}

Generate professional email using factual background.
"""
        
        response = self.llm_service.call_llm(
            prompt=prompt,
            task_type="email_template",
            temperature=0.2,
            max_tokens=800
        )
        
        validation = self.user_extractor.validate_content_against_facts(response.content)
        
        return {
            'content': response.content,
            'validation': validation,
            'preserves_facts': validation['is_valid']
        }
    
    def generate_fact_aware_linkedin_messages(self, jd_analysis: Dict, country: str = "netherlands") -> Dict[str, Any]:
        """Generate LinkedIn messages preserving real background"""
        
        constraints_prompt = self.user_extractor.create_llm_constraints_prompt()
        
        prompt = f"""
{constraints_prompt}

TASK: Create LinkedIn messages for {self.factual_data['personal_info']['name']} targeting:

COMPANY: {jd_analysis['extracted_info']['company']}
ROLE: {jd_analysis['extracted_info']['role_title']}

REAL BACKGROUND TO REFERENCE:
• Current: Senior Product Manager at COWRKS (AI systems, enterprise automation)
• Key results: 94% AI accuracy, $2M revenue acceleration, 99.6% timeline reduction
• Experience: {self.factual_data['professional_summary']['years_experience']}

INSTRUCTIONS:
1. Create CONNECTION REQUEST (under 300 chars) and DIRECT MESSAGE (under 400 chars)
2. Reference only COWRKS and real achievements
3. Use specific metrics: 94% accuracy, $2M impact
4. Netherlands style: direct, professional
5. NEVER mention fictional companies

Generate LinkedIn messages using real background.
"""
        
        response = self.llm_service.call_llm(
            prompt=prompt,
            task_type="linkedin_messages",
            temperature=0.3,
            max_tokens=600
        )
        
        validation = self.user_extractor.validate_content_against_facts(response.content)
        
        return {
            'content': response.content,
            'validation': validation,
            'preserves_facts': validation['is_valid']
        }
    
    def generate_complete_fact_aware_package(self, jd_analysis: Dict, country: str = "netherlands") -> Dict[str, Any]:
        """Generate complete application package preserving all factual information"""
        
        print(f"🛡️ Generating fact-aware package for {self.factual_data['personal_info']['name']}")
        print(f"📊 Target: {jd_analysis['extracted_info']['company']} - {jd_analysis['extracted_info']['role_title']}")
        print()
        
        results = {}
        
        # Generate all content types with fact preservation
        print("📄 Generating fact-aware resume...")
        results['resume'] = self.generate_fact_aware_resume(jd_analysis, country)
        
        print("📝 Generating fact-aware cover letter...")
        results['cover_letter'] = self.generate_fact_aware_cover_letter(jd_analysis, country)
        
        print("📧 Generating fact-aware email...")
        results['email'] = self.generate_fact_aware_email(jd_analysis, country)
        
        print("💼 Generating fact-aware LinkedIn messages...")
        results['linkedin'] = self.generate_fact_aware_linkedin_messages(jd_analysis, country)
        
        # Overall validation
        all_valid = all(result['preserves_facts'] for result in results.values())
        
        package_summary = {
            'all_content_preserves_facts': all_valid,
            'content_types': list(results.keys()),
            'validation_details': {k: v['validation'] for k, v in results.items()},
            'fact_preservation_score': sum(1 for r in results.values() if r['preserves_facts']) / len(results) * 100
        }
        
        results['package_summary'] = package_summary
        
        print(f"✅ Fact preservation score: {package_summary['fact_preservation_score']:.1f}%")
        
        return results
    
    def save_fact_aware_package(self, results: Dict, output_dir: str) -> str:
        """Save fact-aware content package to files"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save each content type
        if 'resume' in results and results['resume']['preserves_facts']:
            with open(output_path / "fact_aware_resume.txt", "w") as f:
                f.write(results['resume']['content'])
        
        if 'cover_letter' in results and results['cover_letter']['preserves_facts']:
            with open(output_path / "fact_aware_cover_letter.txt", "w") as f:
                f.write(results['cover_letter']['content'])
        
        if 'email' in results and results['email']['preserves_facts']:
            with open(output_path / "fact_aware_email.txt", "w") as f:
                f.write(results['email']['content'])
        
        if 'linkedin' in results and results['linkedin']['preserves_facts']:
            with open(output_path / "fact_aware_linkedin.txt", "w") as f:
                f.write(results['linkedin']['content'])
        
        # Save validation report
        with open(output_path / "fact_validation_report.json", "w") as f:
            json.dump(results['package_summary'], f, indent=2)
        
        return str(output_path)

def main():
    """Demo fact-aware content generation"""
    print("🛡️ FACT-AWARE CONTENT GENERATION DEMO")
    print("=" * 60)
    
    generator = FactAwareContentGenerator()
    
    # Mock JD analysis for demo
    dealfront_analysis = {
        'extracted_info': {
            'company': 'Dealfront',
            'company_name': 'Dealfront',
            'role_title': 'Product Operations (Founding Role)'
        },
        'requirements': {
            'must_have_technical': ['Product Operations', 'Process Design', 'AI Automation'],
            'experience_years': '6+ years',
            'domain_expertise': ['Product Ops', 'Process Automation', '0→1 Experience']
        },
        'credibility_score': 9
    }
    
    print("🎯 Target Role Analysis:")
    print(f"• Company: {dealfront_analysis['extracted_info']['company']}")
    print(f"• Role: {dealfront_analysis['extracted_info']['role_title']}")
    print(f"• Requirements: {dealfront_analysis['requirements']['domain_expertise']}")
    print()
    
    # Generate fact-aware package
    results = generator.generate_complete_fact_aware_package(dealfront_analysis)
    
    print("\n📊 FACT PRESERVATION RESULTS:")
    print("-" * 40)
    for content_type, result in results.items():
        if content_type != 'package_summary':
            status = "✅ PRESERVES FACTS" if result['preserves_facts'] else "❌ HAS VIOLATIONS"
            print(f"• {content_type.title()}: {status}")
            
            if result['validation']['violations']:
                for violation in result['validation']['violations']:
                    print(f"  ⚠️ {violation['type']}: {violation.get('found', violation.get('issue'))}")
    
    print(f"\n🎯 Overall Score: {results['package_summary']['fact_preservation_score']:.1f}%")
    
    # Save package
    output_dir = "output/fact_aware_dealfront"
    saved_path = generator.save_fact_aware_package(results, output_dir)
    print(f"💾 Saved to: {saved_path}")

if __name__ == "__main__":
    main()