#!/usr/bin/env python3
"""
Enhanced Job Application Generator with LLM Agent Integration

This enhanced version uses AI-powered agents for intelligent content optimization,
cultural adaptation, and quality validation.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add modules to path
sys.path.append(str(Path(__file__).parent / 'modules'))

from modules.jd_parser import JobDescriptionParser
from modules.enhanced_resume_generator import EnhancedResumeGenerator
from modules.cover_letter_generator import CoverLetterGenerator
from modules.message_generator import MessageGenerator
from modules.html_output_generator import HTMLOutputGenerator
from modules.llm_agents import AgentOrchestrator

class EnhancedJobApplicationGenerator:
    """Enhanced job application generator with LLM agent integration"""
    
    def __init__(self):
        self.jd_parser = JobDescriptionParser()
        self.resume_generator = EnhancedResumeGenerator()
        self.cover_letter_generator = CoverLetterGenerator()
        self.message_generator = MessageGenerator()
        self.html_generator = HTMLOutputGenerator()
        self.agent_orchestrator = AgentOrchestrator()
        
        # Load user profile
        self.load_user_profile()
        
        print("🤖 Enhanced Job Application Generator with LLM Agents")
        print("=" * 60)
    
    def load_user_profile(self):
        """Load user profile from JSON file"""
        profile_path = Path(__file__).parent / "data" / "user_profile.json"
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                self.user_profile = json.load(f)
            print(f"✅ Loaded user profile for {self.user_profile['personal_info']['name']}")
        except FileNotFoundError:
            print("❌ User profile not found. Please ensure data/user_profile.json exists.")
            sys.exit(1)
    
    def generate_application_package(self, job_description: str, country: str, company_name: str = "") -> str:
        """
        Generate complete AI-enhanced application package
        
        Args:
            job_description: Raw job description text
            country: Target country for cultural adaptation
            company_name: Company name for personalization
            
        Returns:
            Path to generated HTML application file
        """
        
        print(f"🎯 Generating AI-enhanced application package for {country.title()}...")
        
        # Step 1: Parse job description with enhanced analysis
        print("📋 Parsing job description with AI analysis...")
        jd_data = self.jd_parser.parse(job_description)
        jd_data['country'] = country
        jd_data['company'] = company_name or jd_data.get('company', 'Company')
        
        # Step 2: Generate AI-enhanced resume
        print("📄 Generating AI-optimized resume...")
        start_time = time.time()
        resume_content, resume_changes = self.resume_generator.generate(jd_data, country)
        resume_time = time.time() - start_time
        
        # Step 3: Generate AI-enhanced cover letter
        print("📝 Generating AI-optimized cover letter...")
        start_time = time.time()
        cover_letter_content = self.cover_letter_generator.generate(jd_data, country, jd_data['company'])
        cl_changes = [f"Generated culturally adapted cover letter for {country.title()}"]
        cl_time = time.time() - start_time
        
        # Step 4: Generate AI-enhanced outreach messages
        print("💬 Generating AI-optimized outreach messages...")
        start_time = time.time()
        linkedin_message = self.message_generator.generate_linkedin_message(jd_data, country)
        email_template = self.message_generator.generate_email_message(jd_data, country, jd_data['company'])
        message_changes = [f"Generated optimized outreach messages for {country.title()}"]
        message_time = time.time() - start_time
        
        # Step 5: AI Content Orchestration and Final Optimization
        print("🤖 Running AI content orchestration...")
        start_time = time.time()
        
        # Combine all content for holistic optimization
        full_content = f"{resume_content}\\n\\n{cover_letter_content}\\n\\n{linkedin_message}"
        
        orchestration_result = self.agent_orchestrator.optimize_content_pipeline(
            full_content,
            jd_data,
            self.user_profile
        )
        
        orchestration_time = time.time() - start_time
        
        # Step 6: Generate HTML output
        print("📦 Compiling AI-enhanced application package...")
        
        # Prepare structured content
        content_dict = {
            'resume': self._parse_resume_content(resume_content),
            'cover_letter': cover_letter_content,
            'linkedin_message': linkedin_message,
            'email_template': email_template
        }
        
        # Prepare metadata with AI analysis
        metadata = {
            'company': jd_data['company'],
            'country': country,
            'applicant_name': self.user_profile['personal_info']['name'],
            'ats_score': jd_data.get('ats_match_score', 0),
            'changes_made': resume_changes + cl_changes + message_changes,
            'matched_skills': jd_data.get('matched_skills', []),
            'missing_skills': jd_data.get('missing_skills', []),
            'ai_analysis': jd_data.get('ai_analysis', {}),
            'orchestration_summary': {
                'overall_confidence': orchestration_result.get('overall_confidence', 0),
                'optimization_steps': orchestration_result.get('optimization_steps', []),
                'improvements_summary': orchestration_result.get('improvements_summary', [])
            },
            'performance_metrics': {
                'resume_generation_time': resume_time,
                'cover_letter_time': cl_time,
                'message_generation_time': message_time,
                'ai_orchestration_time': orchestration_time,
                'total_generation_time': resume_time + cl_time + message_time + orchestration_time
            }
        }
        
        # Generate HTML output
        html_content = self.html_generator.generate_html_application(content_dict, metadata)
        
        # Save to file
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        company_safe = "".join(c for c in jd_data['company'] if c.isalnum() or c in (' ', '-', '_')).strip()
        timestamp = datetime.now().strftime('%Y-%m-%d')
        output_filename = f"{company_safe}_{country}_{timestamp}_enhanced.html"
        output_path = output_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Print summary
        print("\\n" + "=" * 60)
        print("🎉 AI-ENHANCED APPLICATION PACKAGE GENERATED")
        print("=" * 60)
        print(f"📁 Output File: {output_path}")
        print(f"🎯 ATS Match Score: {jd_data.get('ats_match_score', 0)}%")
        print(f"🤖 AI Confidence: {orchestration_result.get('overall_confidence', 0):.2f}")
        print(f"⚡ Total Generation Time: {metadata['performance_metrics']['total_generation_time']:.2f}s")
        print(f"📊 AI Optimizations: {len(orchestration_result.get('optimization_steps', []))}")
        
        # Show key improvements
        improvements = orchestration_result.get('improvements_summary', [])
        if improvements:
            print(f"\\n🚀 Key AI Improvements:")
            for i, improvement in enumerate(improvements[:3], 1):
                print(f"   {i}. {improvement}")
        
        print("\\n✅ Ready to copy-paste from HTML file with preserved formatting!")
        print("=" * 60)
        
        return str(output_path)
    
    def _parse_resume_content(self, resume_markdown: str) -> Dict[str, Any]:
        """Parse resume markdown into structured data for HTML generation"""
        
        # Extract personal info (header section)
        lines = resume_markdown.split('\\n')
        personal_info = {}
        
        for i, line in enumerate(lines):
            if line.startswith('# '):
                personal_info['name'] = line[2:].strip()
            elif line.startswith('**') and line.endswith('**') and i < 5:
                personal_info['title'] = line[2:-2].strip()
            elif '@gmail.com' in line:
                # Parse contact line
                contact_parts = [part.strip() for part in line.split('|')]
                if len(contact_parts) >= 4:
                    personal_info['phone'] = contact_parts[0]
                    personal_info['email'] = contact_parts[1]
                    personal_info['linkedin'] = contact_parts[2]
                    personal_info['location'] = contact_parts[3]
        
        # Parse sections
        sections = self.html_generator.parse_markdown_to_html_structure(resume_markdown)
        
        # Extract summary
        summary = sections.get('summary', '')
        
        # Extract skills
        skills = sections.get('skills', '')
        
        # Extract experience
        experience = []
        experience_text = sections.get('experience', '')
        if experience_text:
            # Parse experience entries (simplified)
            exp_sections = experience_text.split('### ')
            for exp_section in exp_sections:
                if exp_section.strip():
                    exp_lines = exp_section.strip().split('\\n')
                    if exp_lines:
                        title = exp_lines[0].strip()
                        company_info = exp_lines[1] if len(exp_lines) > 1 else ""
                        
                        # Parse company info
                        company_parts = company_info.split('|')
                        company = company_parts[0].replace('**', '').strip() if company_parts else ""
                        location = company_parts[1].strip() if len(company_parts) > 1 else ""
                        duration = company_parts[2].strip() if len(company_parts) > 2 else ""
                        
                        # Parse highlights
                        highlights = []
                        for line in exp_lines[2:]:
                            if line.strip().startswith('•'):
                                highlights.append(line.strip()[1:].strip())
                        
                        experience.append({
                            'title': title,
                            'company': company,
                            'location': location,
                            'duration': duration,
                            'highlights': highlights
                        })
        
        # Extract education
        education = {}
        education_text = sections.get('education', '')
        if education_text:
            # Simple education parsing
            if '**' in education_text:
                degree = education_text.split('**')[1] if len(education_text.split('**')) > 1 else ""
                rest = education_text.replace(f'**{degree}**', '').strip()
                parts = rest.split('|')
                university = parts[0].strip() if parts else ""
                duration = parts[1].strip() if len(parts) > 1 else ""
                
                education = {
                    'degree': degree,
                    'university': university,
                    'duration': duration
                }
        
        return {
            'personal_info': personal_info,
            'summary': summary,
            'skills': skills,
            'experience': experience,
            'education': education
        }
    
    def interactive_mode(self):
        """Interactive mode for generating applications"""
        
        print("\\n🤖 Welcome to Enhanced Interactive Mode!")
        print("I'll help you generate AI-optimized job applications.\\n")
        
        while True:
            try:
                # Get job description
                print("📋 Please paste the job description (press Enter twice when done):")
                job_description_lines = []
                while True:
                    line = input()
                    if line == "" and job_description_lines and job_description_lines[-1] == "":
                        break
                    job_description_lines.append(line)
                
                job_description = "\\n".join(job_description_lines).strip()
                
                if not job_description:
                    print("❌ No job description provided. Please try again.\\n")
                    continue
                
                # Get country
                print("\\n🌍 Target country (e.g., netherlands, sweden, ireland):")
                country = input().strip().lower()
                
                if not country:
                    country = "netherlands"  # Default
                
                # Get company name (optional)
                print("\\n🏢 Company name (optional, press Enter to skip):")
                company_name = input().strip()
                
                # Generate application
                print("\\n🚀 Generating AI-enhanced application...")
                output_path = self.generate_application_package(job_description, country, company_name)
                
                print(f"\\n📄 Application saved to: {output_path}")
                print("\\n🔄 Generate another application? (y/n):")
                
                if input().strip().lower() not in ['y', 'yes']:
                    break
                    
                print("\\n" + "="*60 + "\\n")
                
            except KeyboardInterrupt:
                print("\\n\\n👋 Thanks for using Enhanced Job Application Generator!")
                break
            except Exception as e:
                print(f"\\n❌ Error: {str(e)}")
                print("Please try again.\\n")

def main():
    """Main entry point"""
    generator = EnhancedJobApplicationGenerator()
    
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "--interactive":
            generator.interactive_mode()
        else:
            print("Usage: python enhanced_main.py [--interactive]")
    else:
        # Default interactive mode
        generator.interactive_mode()

if __name__ == "__main__":
    main()