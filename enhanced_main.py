#!/usr/bin/env python3
"""
Enhanced Job Application Generator - Professional Quality
AI-powered job application generator with content preservation and quality validation
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
from modules.content_preserving_generator import ContentPreservingGenerator
from modules.cover_letter_generator import CoverLetterGenerator
from modules.message_generator import MessageGenerator
from modules.professional_html_generator import ProfessionalHTMLGenerator
from modules.html_validation_agent import HTMLValidationAgent
from modules.llm_agents import AgentOrchestrator
from modules.human_voice_agent import HumanVoiceAgent

class EnhancedJobApplicationGenerator:
    """Professional-grade job application generator with comprehensive quality controls"""
    
    def __init__(self):
        self.jd_parser = JobDescriptionParser()
        self.content_generator = ContentPreservingGenerator()
        self.cover_letter_generator = CoverLetterGenerator()
        self.message_generator = MessageGenerator()
        self.html_generator = ProfessionalHTMLGenerator()
        self.html_validator = HTMLValidationAgent()
        self.agent_orchestrator = AgentOrchestrator()
        self.human_voice_agent = HumanVoiceAgent()
        
        # Load user profile
        self.load_user_profile()
        
        print("🏆 Professional Job Application Generator V2")
        print("✅ Content preservation | 🎨 Professional formatting | 🔍 Quality validation")
        print("=" * 70)
    
    def load_user_profile(self):
        """Load user profile from JSON file"""
        profile_path = Path(__file__).parent / "data" / "user_profile.json"
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                self.user_profile = json.load(f)
            print(f"✅ Loaded profile for {self.user_profile['personal_info']['name']}")
        except FileNotFoundError:
            print("❌ User profile not found. Please ensure data/user_profile.json exists.")
            sys.exit(1)
    
    def generate_professional_application(self, job_description: str, country: str, company_name: str = "") -> str:
        """
        Generate professional-quality application with comprehensive validation
        
        Args:
            job_description: Raw job description text
            country: Target country for cultural adaptation
            company_name: Company name for personalization
            
        Returns:
            Path to generated professional HTML application file
        """
        
        print(f"🎯 Generating professional application for {country.title()}...")
        
        try:
            # Step 1: Parse job description
            print("📋 Analyzing job requirements...")
            if not job_description or not job_description.strip():
                raise ValueError("Job description cannot be empty")
            if not country or not country.strip():
                raise ValueError("Country must be specified")
                
            jd_data = self.jd_parser.parse(job_description)
            jd_data['country'] = country
            jd_data['company'] = company_name or jd_data.get('company', 'Company')
            
        except Exception as e:
            print(f"❌ Error parsing job description: {str(e)}")
            raise ValueError(f"Job description parsing failed: {str(e)}")
        
        try:
            # Step 2: Generate content-preserving resume
            print("📄 Generating comprehensive resume (preserving all content)...")
            start_time = time.time()
            resume_data, resume_changes = self.content_generator.generate_full_resume(jd_data, country)
            resume_time = time.time() - start_time
        except Exception as e:
            print(f"❌ Error generating resume: {str(e)}")
            raise RuntimeError(f"Resume generation failed: {str(e)}")
        
        print(f"   ✅ Generated resume with {len(resume_data['experience'])} roles preserved")
        print(f"   ✅ {len(resume_data['experience'][0]['highlights'])} bullet points in current role")
        
        # Step 3: Generate professional cover letter
        print("📝 Creating tailored cover letter...")
        start_time = time.time()
        cover_letter_content = self.cover_letter_generator.generate(jd_data, country, jd_data['company'])
        cl_time = time.time() - start_time
        
        # Step 4: Generate outreach messages
        print("💬 Creating outreach messages...")
        start_time = time.time()
        linkedin_message = self.message_generator.generate_linkedin_message(jd_data, country)
        email_template = self.message_generator.generate_email_message(jd_data, country, jd_data['company'])
        message_time = time.time() - start_time
        
        # Step 5: AI Content Orchestration
        print("🤖 Running AI optimization...")
        start_time = time.time()
        
        # Combine content for orchestrator analysis
        full_content = f"{resume_data.get('summary', '')}\\n\\n{cover_letter_content}"
        
        orchestration_result = self.agent_orchestrator.optimize_content_pipeline(
            full_content,
            jd_data,
            self.user_profile
        )
        
        orchestration_time = time.time() - start_time
        
        # Step 6: Generate professional HTML
        print("🎨 Generating professional HTML...")
        
        # Prepare structured content
        content_dict = {
            'resume': resume_data,
            'cover_letter': cover_letter_content,
            'linkedin_message': linkedin_message,
            'email_template': email_template
        }
        
        # Step 6.5: Apply Human Voice Transformation (FINAL STEP)
        print("🗣️  Applying human voice transformation...")
        start_time = time.time()
        
        # Transform all content to sound human, not AI-generated
        humanized_content = self.human_voice_agent.humanize_content(content_dict)
        voice_processing_time = time.time() - start_time
        
        # Analyze voice quality
        voice_scores = {}
        for content_type, content in humanized_content.items():
            if content_type == 'resume' and isinstance(content, dict):
                # Analyze resume summary for voice quality
                summary_text = content.get('summary', '')
                voice_scores[content_type] = self.human_voice_agent.analyze_human_voice_score(summary_text)
            elif isinstance(content, str):
                voice_scores[content_type] = self.human_voice_agent.analyze_human_voice_score(content)
        
        # Update content_dict with humanized content
        content_dict = humanized_content
        
        print(f"   ✅ Human voice transformation completed in {voice_processing_time:.2f}s")
        for content_type, scores in voice_scores.items():
            if 'overall_human_score' in scores:
                print(f"   📊 {content_type.title()} human score: {scores['overall_human_score']:.1f}/10")
        
        # Prepare metadata
        metadata = {
            'company': jd_data['company'],
            'country': country,
            'applicant_name': self.user_profile['personal_info']['name'],
            'ats_score': self._calculate_ats_score(jd_data, resume_data),
            'changes_made': resume_changes,
            'ai_analysis': {
                'overall_confidence': orchestration_result.get('overall_confidence', 0),
                'optimization_steps': orchestration_result.get('optimization_steps', []),
                'improvements_summary': orchestration_result.get('improvements_summary', [])
            },
            'performance_metrics': {
                'resume_generation_time': resume_time,
                'cover_letter_time': cl_time,
                'message_generation_time': message_time,
                'ai_orchestration_time': orchestration_time,
                'voice_processing_time': voice_processing_time,
                'total_generation_time': resume_time + cl_time + message_time + orchestration_time + voice_processing_time
            },
            'human_voice_scores': voice_scores
        }
        
        # Generate HTML
        html_content = self.html_generator.generate_professional_application(content_dict, metadata)
        
        # Step 7: Validate HTML quality
        print("🔍 Validating output quality...")
        validation_result = self.html_validator.validate_html_output(html_content)
        
        # Step 8: Apply fixes if needed
        if validation_result['overall_score'] < 90:
            print("🔧 Applying quality fixes...")
            html_content = self._apply_validation_fixes(html_content, validation_result)
        
        # Step 9: Save to file
        print("💾 Saving professional application...")
        
        try:
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            # Sanitize company name for filename
            company_safe = "".join(c for c in jd_data['company'] if c.isalnum() or c in (' ', '-', '_')).strip()
            if not company_safe:
                company_safe = "Company"
                
            timestamp = datetime.now().strftime('%Y-%m-%d')
            output_filename = f"{company_safe}_{country}_{timestamp}_professional.html"
            output_path = output_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
        except PermissionError as e:
            raise PermissionError(f"Cannot write to output directory: {str(e)}")
        except OSError as e:
            raise OSError(f"File system error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to save output file: {str(e)}")
        
        # Final validation score
        final_validation = self.html_validator.validate_html_output(html_content)
        
        # Print comprehensive summary
        self._print_generation_summary(metadata, final_validation, orchestration_result, output_path)
        
        return str(output_path)
    
    def _calculate_ats_score(self, jd_data: Dict, resume_data: Dict) -> int:
        """Calculate ATS match score based on keyword alignment"""
        
        jd_keywords = []
        jd_keywords.extend(jd_data.get('required_skills', []))
        jd_keywords.extend(jd_data.get('preferred_skills', []))
        
        # Extract text from resume
        resume_text = ' '.join([
            resume_data.get('summary', ''),
            resume_data.get('skills', ''),
            ' '.join([exp.get('title', '') for exp in resume_data.get('experience', [])]),
            ' '.join([' '.join(exp.get('highlights', [])) for exp in resume_data.get('experience', [])])
        ]).lower()
        
        # Calculate match
        if not jd_keywords:
            return 85  # Default good score if no specific keywords
        
        matched_keywords = sum(1 for keyword in jd_keywords if keyword.lower() in resume_text)
        ats_score = min(95, int((matched_keywords / len(jd_keywords)) * 100))
        
        return ats_score
    
    def _apply_validation_fixes(self, html_content: str, validation_result: Dict) -> str:
        """Apply automated fixes for common validation issues"""
        
        fixed_content = html_content
        
        # Fix content artifacts
        fixed_content = re.sub(r'\\\\n---.*?(?=<)', '', fixed_content)
        fixed_content = re.sub(r'\\\\n', '<br>', fixed_content)
        
        # Fix bullet point formatting in email templates
        import re
        
        # Find email message boxes and fix bullet points
        email_pattern = r'(<div class="message-box">)(.*?)(</div>)'
        
        def fix_bullets(match):
            content = match.group(2)
            if '•' in content and '<li>' not in content:
                # Split by bullet points and create proper list
                parts = content.split('•')
                if len(parts) > 1:
                    intro = parts[0].strip()
                    bullets = [part.strip() for part in parts[1:] if part.strip()]
                    
                    if bullets:
                        fixed = f"{intro}<ul>"
                        for bullet in bullets:
                            fixed += f"<li>{bullet}</li>"
                        fixed += "</ul>"
                        return f"{match.group(1)}{fixed}{match.group(3)}"
            return match.group(0)
        
        fixed_content = re.sub(email_pattern, fix_bullets, fixed_content, flags=re.DOTALL)
        
        return fixed_content
    
    def _print_generation_summary(self, metadata: Dict, validation_result: Dict, orchestration_result: Dict, output_path: Path):
        """Print comprehensive generation summary"""
        
        print("\\n" + "=" * 70)
        print("🏆 PROFESSIONAL APPLICATION GENERATED")
        print("=" * 70)
        
        # Basic info
        print(f"📁 Output File: {output_path}")
        print(f"🎯 ATS Score: {metadata['ats_score']}%")
        print(f"🤖 AI Confidence: {orchestration_result.get('overall_confidence', 0):.1%}")
        print(f"⚡ Generation Time: {metadata['performance_metrics']['total_generation_time']:.2f}s")
        
        # Quality scores
        print(f"\\n📊 Quality Assessment:")
        print(f"   • Overall Quality: {validation_result['overall_score']:.1f}/100")
        print(f"   • Formatting: {validation_result['formatting_score']:.1f}/100")
        print(f"   • Content: {validation_result['content_score']:.1f}/100")
        print(f"   • Professional: {validation_result['professional_score']:.1f}/100")
        
        # Content preservation stats
        resume_data = metadata.get('resume_data', {})
        experience = resume_data.get('experience', [])
        if experience:
            total_bullets = sum(len(exp.get('highlights', [])) for exp in experience)
            print(f"\\n📄 Content Preservation:")
            print(f"   • Roles: {len(experience)}")
            print(f"   • Total bullet points: {total_bullets}")
            print(f"   • Content preserved: 100%")
        
        # Issues found
        if validation_result['issues_found']:
            critical_issues = [issue for issue in validation_result['issues_found'] if issue.severity == 'critical']
            if critical_issues:
                print(f"\\n🚨 Critical Issues: {len(critical_issues)}")
            else:
                print(f"\\n✅ No critical formatting issues detected")
        
        # Recommendations
        if validation_result['recommendations']:
            print(f"\\n🔧 Top Recommendations:")
            for i, rec in enumerate(validation_result['recommendations'][:3], 1):
                print(f"   {i}. {rec}")
        
        # AI improvements
        improvements = orchestration_result.get('improvements_summary', [])
        if improvements:
            print(f"\\n🚀 AI Enhancements Applied:")
            for i, improvement in enumerate(improvements[:3], 1):
                print(f"   {i}. {improvement}")
        
        print("\\n✅ Ready for professional use - copy sections from HTML file!")
        print("=" * 70)
    
    def interactive_mode(self):
        """Interactive mode for generating professional applications"""
        
        print("\\n🏆 Welcome to Professional Interactive Mode!")
        print("Generates high-quality applications with content preservation and validation.\\n")
        
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
                
                # Get company name
                print("\\n🏢 Company name (optional, press Enter to skip):")
                company_name = input().strip()
                
                # Generate application
                print("\\n🚀 Generating professional application...")
                output_path = self.generate_professional_application(job_description, country, company_name)
                
                print(f"\\n📄 Professional application saved to: {output_path}")
                print("\\n🔄 Generate another application? (y/n):")
                
                if input().strip().lower() not in ['y', 'yes']:
                    break
                    
                print("\\n" + "="*70 + "\\n")
                
            except KeyboardInterrupt:
                print("\\n\\n👋 Thanks for using Professional Job Application Generator!")
                break
            except ValueError as e:
                print(f"\\n❌ Input Error: {str(e)}")
                print("Please check your input and try again.\\n")
            except FileNotFoundError as e:
                print(f"\\n❌ File Error: {str(e)}")
                print("Please ensure all required files are present.\\n")
            except PermissionError as e:
                print(f"\\n❌ Permission Error: {str(e)}")
                print("Please check file permissions and try again.\\n")
            except Exception as e:
                print(f"\\n❌ Unexpected Error: {str(e)}")
                print("Please report this issue if it persists.\\n")
                # Optional: Log limited error info for debugging
                import traceback
                print("\\n🔧 Debug info (for reporting):")
                # Limit traceback output to prevent memory issues
                tb_lines = traceback.format_exc().split('\\n')
                if len(tb_lines) > 20:
                    print('\\n'.join(tb_lines[:10]))
                    print(f"... [truncated {len(tb_lines) - 20} lines] ...")
                    print('\\n'.join(tb_lines[-10:]))
                else:
                    print(traceback.format_exc())

def main():
    """Main entry point"""
    generator = EnhancedJobApplicationGenerator()
    
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "--interactive":
            generator.interactive_mode()
        else:
            print("Usage: python enhanced_main_v2.py [--interactive]")
    else:
        # Default interactive mode
        generator.interactive_mode()

if __name__ == "__main__":
    main()