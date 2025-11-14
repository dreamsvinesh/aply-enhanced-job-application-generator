#!/usr/bin/env python3
"""
Dynamic Enhanced Job Application Generator
AI-powered job application generator with strategic dynamic content generation
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add modules to path
sys.path.append(str(Path(__file__).parent / 'modules'))

# Import existing modules
from modules.jd_parser import JobDescriptionParser
from modules.cover_letter_generator import CoverLetterGenerator
from modules.message_generator import MessageGenerator
from modules.professional_html_generator import ProfessionalHTMLGenerator
from modules.html_validation_agent import HTMLValidationAgent
from modules.pre_generation_validator import PreGenerationValidator
from modules.content_quality_validator import ContentQualityValidator
from modules.llm_agents import AgentOrchestrator
from modules.human_voice_agent import HumanVoiceAgent

# Import new dynamic content modules
from modules.content_strategy_engine import ContentStrategyEngine, ApplicationStrategy
from modules.jd_intelligence_analyzer import JDIntelligenceAnalyzer
from modules.dynamic_summary_generator import DynamicSummaryGenerator
from modules.dynamic_experience_generator import DynamicExperienceGenerator
from modules.chatgpt_agent import ChatGPTAgent

class DynamicEnhancedJobApplicationGenerator:
    """Strategic job application generator with dynamic AI-powered content optimization"""
    
    def __init__(self, enable_dynamic_mode: bool = True):
        # Core generators
        self.jd_parser = JobDescriptionParser()
        self.cover_letter_generator = CoverLetterGenerator()
        self.message_generator = MessageGenerator()
        self.html_generator = ProfessionalHTMLGenerator()
        
        # Validation agents
        self.html_validator = HTMLValidationAgent()
        self.pre_generation_validator = PreGenerationValidator()
        self.content_quality_validator = ContentQualityValidator()
        self.agent_orchestrator = AgentOrchestrator()
        self.human_voice_agent = HumanVoiceAgent()
        
        # Dynamic content system
        self.enable_dynamic_mode = enable_dynamic_mode
        if enable_dynamic_mode:
            self.strategy_engine = ContentStrategyEngine()
            self.jd_analyzer = JDIntelligenceAnalyzer()
            self.dynamic_summary_generator = DynamicSummaryGenerator()
            self.dynamic_experience_generator = DynamicExperienceGenerator()
            self.chatgpt_agent = ChatGPTAgent()
        
        # Load user profile
        self.load_user_profile()
        
        print("🚀 Dynamic Enhanced Job Application Generator V3")
        print("✨ Strategic AI-powered content optimization | 🎯 JD-specific adaptation")
        print("🔍 Intelligent analysis | 📊 Strategic positioning | 💎 Premium quality")
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
    
    def generate_strategic_application(self, job_description: str, country: str, company_name: str = "") -> str:
        """
        Generate strategically optimized application using dynamic content generation
        
        Args:
            job_description: Raw job description text
            country: Target country for cultural adaptation
            company_name: Company name for personalization
            
        Returns:
            Path to generated strategic application file
        """
        
        print(f"🎯 Generating strategic application for {country.title()}...")
        
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
        
        # Step 2: Strategic Analysis (if dynamic mode enabled)
        if self.enable_dynamic_mode:
            print("🧠 Performing strategic JD intelligence analysis...")
            start_time = time.time()
            
            try:
                # Analyze JD intelligence
                jd_intelligence = self.jd_analyzer.analyze_jd_intelligence(jd_data)
                
                # Develop application strategy
                application_strategy = self.strategy_engine.develop_application_strategy(jd_data)
                
                strategic_analysis_time = time.time() - start_time
                
                print(f"   ✅ Strategic analysis completed in {strategic_analysis_time:.2f}s")
                print(f"   🎯 Focus: {application_strategy.differentiation_angle}")
                print(f"   📊 Strategy confidence: {self.strategy_engine.analyze_application_fit(jd_data, application_strategy)['overall_fit_score']}")
                
            except Exception as e:
                print(f"⚠️  Strategic analysis failed: {e}")
                print("   🔄 Falling back to standard generation mode")
                self.enable_dynamic_mode = False
                application_strategy = None
                jd_intelligence = None
        else:
            application_strategy = None
            jd_intelligence = None
        
        # Step 2.5: Pre-Generation Validation
        print("🛡️  Running pre-generation validation...")
        pre_validation_result = self.pre_generation_validator.validate_pre_generation(
            self.user_profile, jd_data
        )
        self.pre_generation_validator.print_validation_report(pre_validation_result)
        
        if not pre_validation_result.should_proceed:
            raise ValueError(f"Pre-generation validation failed: {pre_validation_result.summary}")
        
        if pre_validation_result.decision == 'PROCEED_WITH_WARNINGS':
            print("⚠️  Proceeding with warnings - please review final output carefully")
        
        # Step 3: Generate Strategic Content
        if self.enable_dynamic_mode and application_strategy:
            resume_data = self._generate_strategic_resume(jd_data, application_strategy)
            cover_letter_content = self._generate_strategic_cover_letter(jd_data, application_strategy)
            linkedin_message = self._generate_strategic_linkedin_message(jd_data, application_strategy)
            email_template = self._generate_strategic_email(jd_data, application_strategy)
        else:
            # Fallback to standard generation
            resume_data = self._generate_standard_resume(jd_data, country)
            cover_letter_content = self.cover_letter_generator.generate(jd_data, country, jd_data['company'])
            linkedin_message = self.message_generator.generate_linkedin_message(jd_data, country)
            email_template = self.message_generator.generate_email_message(jd_data, country, jd_data['company'])
        
        # Step 4: AI Content Orchestration
        print("🤖 Running AI optimization...")
        start_time = time.time()
        
        full_content = f"{resume_data.get('summary', '')}\n\n{cover_letter_content}"
        
        orchestration_result = self.agent_orchestrator.optimize_content_pipeline(
            full_content,
            jd_data,
            self.user_profile
        )
        
        orchestration_time = time.time() - start_time
        
        # Step 5: Prepare Content Dictionary
        content_dict = {
            'resume': resume_data,
            'cover_letter': cover_letter_content,
            'linkedin_message': linkedin_message,
            'email_template': email_template
        }
        
        # Step 6: Human Voice Transformation
        print("🗣️  Applying human voice transformation...")
        start_time = time.time()
        
        humanized_content = self.human_voice_agent.humanize_content(content_dict)
        voice_processing_time = time.time() - start_time
        
        # Analyze voice quality
        voice_scores = {}
        for content_type, content in humanized_content.items():
            if content_type == 'resume' and isinstance(content, dict):
                summary_text = content.get('summary', '')
                voice_scores[content_type] = self.human_voice_agent.analyze_human_voice_score(summary_text)
            elif isinstance(content, str):
                voice_scores[content_type] = self.human_voice_agent.analyze_human_voice_score(content)
        
        content_dict = humanized_content
        
        print(f"   ✅ Human voice transformation completed in {voice_processing_time:.2f}s")
        for content_type, scores in voice_scores.items():
            if 'overall_human_score' in scores:
                print(f"   📊 {content_type.title()} human score: {scores['overall_human_score']:.1f}/10")
        
        # Step 7: Enhanced Content Quality Validation
        print("🔍 Validating content quality...")
        content_validation_result = self.content_quality_validator.validate_generated_content(
            content_dict, self.user_profile, jd_data
        )
        self.content_quality_validator.print_validation_report(content_validation_result)
        
        if content_validation_result.should_regenerate:
            print("🔄 Content quality issues detected - would regenerate in production")
            print("   ⚠️  Continuing for demo purposes, but review output carefully")
        
        # Step 8: Prepare Enhanced Metadata
        metadata = self._prepare_enhanced_metadata(
            jd_data, country, resume_data, application_strategy, 
            jd_intelligence, orchestration_result, voice_scores,
            pre_validation_result, content_validation_result
        )
        
        # Step 9: Generate and Save Application
        print("🎨 Generating strategic HTML...")
        
        html_content = self.html_generator.generate_professional_application(content_dict, metadata)
        
        # HTML validation and fixes
        print("🔍 Validating output quality...")
        validation_result = self.html_validator.validate_html_output(html_content)
        
        if validation_result['overall_score'] < 90:
            print("🔧 Applying quality fixes...")
            html_content = self._apply_validation_fixes(html_content, validation_result)
        
        # Save to file
        print("💾 Saving strategic application...")
        output_path = self._save_application_file(html_content, jd_data, country)
        
        # Final validation and summary
        final_validation = self.html_validator.validate_html_output(html_content)
        self._print_strategic_generation_summary(
            metadata, final_validation, orchestration_result, 
            application_strategy, jd_intelligence, output_path
        )
        
        return str(output_path)
    
    def _generate_strategic_resume(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> Dict:
        """Generate strategically optimized resume using dynamic generators"""
        
        print("📄 Generating strategic resume...")
        start_time = time.time()
        
        try:
            # Generate strategic summary
            strategic_summary = self.dynamic_summary_generator.generate_strategic_summary(
                jd_data, application_strategy
            )
            
            # Generate strategic experience
            strategic_experience_list = self.dynamic_experience_generator.generate_strategic_experience(
                jd_data, application_strategy
            )
            
            # Convert to standard resume format
            experience_data = []
            for exp_enhancement in strategic_experience_list:
                experience_data.append({
                    'title': exp_enhancement.role_title,
                    'company': exp_enhancement.company,
                    'duration': exp_enhancement.duration,
                    'location': exp_enhancement.location,
                    'highlights': exp_enhancement.strategic_bullets
                })
            
            # Generate strategic title
            strategic_title = self._generate_strategic_title(jd_data, application_strategy)
            
            # Generate strategic skills
            strategic_skills = self._generate_strategic_skills(jd_data, application_strategy)
            
            resume_data = {
                'personal_info': {
                    'name': self.user_profile['personal_info']['name'],
                    'title': strategic_title,
                    'phone': self.user_profile['personal_info']['phone'],
                    'email': self.user_profile['personal_info']['email'],
                    'linkedin': self.user_profile['personal_info']['linkedin'],
                    'location': self.user_profile['personal_info']['location']
                },
                'summary': strategic_summary,
                'skills': strategic_skills,
                'experience': experience_data,
                'education': self.user_profile.get('education', {})
            }
            
            generation_time = time.time() - start_time
            print(f"   ✅ Strategic resume generated in {generation_time:.2f}s")
            
            # Analyze strategic enhancements
            total_bullets = sum(len(exp['highlights']) for exp in experience_data)
            print(f"   📊 {len(experience_data)} roles with {total_bullets} strategic bullets")
            
            return resume_data
            
        except Exception as e:
            print(f"   ⚠️  Strategic resume generation failed: {e}")
            print("   🔄 Falling back to standard resume generation")
            return self._generate_standard_resume(jd_data, jd_data.get('country', 'netherlands'))
    
    def _generate_strategic_title(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate strategic job title based on application strategy"""
        return application_strategy.title_recommendation
    
    def _generate_strategic_skills(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate strategic skills section"""
        # Use the prioritized skills from the strategy
        priority_skills = []
        
        # Add skills based on application strategy
        for strength_mapping in application_strategy.priority_strengths[:8]:
            # Extract skill keywords from the strength mapping
            strength_text = strength_mapping.user_strength.lower()
            if 'automation' in strength_text:
                priority_skills.append("Process Automation")
            elif 'ai' in strength_text or 'ml' in strength_text:
                priority_skills.append("AI/ML Systems")
            elif 'cross-functional' in strength_text:
                priority_skills.append("Cross-functional Leadership")
            elif 'revenue' in strength_text:
                priority_skills.append("Revenue Growth")
        
        # Add core PM skills
        core_skills = ["Product Strategy", "Product Management", "Stakeholder Management", "Agile/SAFe"]
        
        # Add technical skills from user profile
        user_technical_skills = self.user_profile.get('skills', {}).get('technical', [])
        relevant_tech_skills = [skill for skill in user_technical_skills[:6]]
        
        # Combine and deduplicate
        all_skills = priority_skills + core_skills + relevant_tech_skills
        unique_skills = []
        seen = set()
        for skill in all_skills:
            if skill not in seen:
                unique_skills.append(skill)
                seen.add(skill)
        
        return " • ".join(unique_skills[:15])  # Limit to 15 skills
    
    def _generate_strategic_cover_letter(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate strategic cover letter using ChatGPT agent"""
        
        print("📝 Creating strategic cover letter...")
        start_time = time.time()
        
        try:
            strategic_cover_letter = self.chatgpt_agent.generate_strategic_cover_letter(
                jd_data, self.user_profile, application_strategy.content_strategy
            )
            
            generation_time = time.time() - start_time
            print(f"   ✅ Strategic cover letter generated in {generation_time:.2f}s")
            
            return strategic_cover_letter
            
        except Exception as e:
            print(f"   ⚠️  Strategic cover letter generation failed: {e}")
            print("   🔄 Falling back to standard cover letter")
            return self.cover_letter_generator.generate(jd_data, jd_data.get('country', 'netherlands'), jd_data['company'])
    
    def _generate_strategic_linkedin_message(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate strategic LinkedIn message"""
        
        print("💬 Creating strategic LinkedIn message...")
        
        try:
            strategic_message = self.chatgpt_agent.generate_strategic_linkedin_message(
                jd_data, application_strategy.content_strategy
            )
            
            return strategic_message
            
        except Exception as e:
            print(f"   ⚠️  Strategic LinkedIn message generation failed: {e}")
            return self.message_generator.generate_linkedin_message(jd_data, jd_data.get('country', 'netherlands'))
    
    def _generate_strategic_email(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate strategic email template"""
        
        try:
            # Use the strategic cover letter approach for email
            return self.message_generator.generate_email_message(jd_data, jd_data.get('country', 'netherlands'), jd_data['company'])
            
        except Exception as e:
            print(f"   ⚠️  Strategic email generation failed: {e}")
            return self.message_generator.generate_email_message(jd_data, jd_data.get('country', 'netherlands'), jd_data['company'])
    
    def _generate_standard_resume(self, jd_data: Dict, country: str) -> Dict:
        """Fallback to standard resume generation"""
        
        print("📄 Generating standard resume...")
        
        # Import the content preserving generator for fallback
        from modules.content_preserving_generator import ContentPreservingGenerator
        
        content_generator = ContentPreservingGenerator()
        resume_data, _ = content_generator.generate_full_resume(jd_data, country)
        
        return resume_data
    
    def _prepare_enhanced_metadata(self, 
                                 jd_data: Dict,
                                 country: str, 
                                 resume_data: Dict,
                                 application_strategy: Optional[ApplicationStrategy],
                                 jd_intelligence: Optional[Any],
                                 orchestration_result: Dict,
                                 voice_scores: Dict,
                                 pre_validation_result: Any,
                                 content_validation_result: Any) -> Dict:
        """Prepare enhanced metadata with strategic analysis"""
        
        metadata = {
            'company': jd_data['company'],
            'country': country,
            'applicant_name': self.user_profile['personal_info']['name'],
            'ats_score': self._calculate_ats_score(jd_data, resume_data),
            'generation_mode': 'strategic' if self.enable_dynamic_mode else 'standard',
            'ai_analysis': {
                'overall_confidence': orchestration_result.get('overall_confidence', 0),
                'optimization_steps': orchestration_result.get('optimization_steps', []),
                'improvements_summary': orchestration_result.get('improvements_summary', [])
            },
            'human_voice_scores': voice_scores,
            'validation_results': {
                'pre_generation': {
                    'decision': pre_validation_result.decision,
                    'confidence': pre_validation_result.confidence_score,
                    'issues_count': len(pre_validation_result.issues)
                },
                'content_quality': {
                    'decision': content_validation_result.decision,
                    'overall_score': content_validation_result.scores['overall_content_score'],
                    'factual_accuracy': content_validation_result.scores['factual_accuracy_score'],
                    'completeness': content_validation_result.scores['content_completeness_score'],
                    'professional_standards': content_validation_result.scores['professional_standards_score'],
                    'human_writing_quality': content_validation_result.scores['human_writing_score'],
                    'issues_count': len(content_validation_result.issues)
                }
            }
        }
        
        # Add strategic analysis metadata if available
        if application_strategy and jd_intelligence:
            fit_analysis = self.strategy_engine.analyze_application_fit(jd_data, application_strategy)
            
            metadata['strategic_analysis'] = {
                'differentiation_angle': application_strategy.differentiation_angle,
                'value_proposition': application_strategy.value_proposition,
                'fit_score': fit_analysis['overall_fit_score'],
                'recommendation': fit_analysis['recommendation'],
                'industry_focus': jd_intelligence.industry_focus,
                'role_type': jd_intelligence.role_type,
                'key_strengths_count': len(application_strategy.priority_strengths),
                'competitive_advantages': application_strategy.competitive_advantages
            }
        
        return metadata
    
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
        
        if not jd_keywords:
            return 85  # Default good score
        
        matched_keywords = sum(1 for keyword in jd_keywords if keyword.lower() in resume_text)
        ats_score = min(95, int((matched_keywords / len(jd_keywords)) * 100))
        
        return ats_score
    
    def _apply_validation_fixes(self, html_content: str, validation_result: Dict) -> str:
        """Apply automated fixes for common validation issues"""
        
        import re
        
        fixed_content = html_content
        
        # Fix content artifacts
        fixed_content = re.sub(r'\\\\n---.*?(?=<)', '', fixed_content)
        fixed_content = re.sub(r'\\\\n', '<br>', fixed_content)
        
        # Fix bullet point formatting in email templates
        email_pattern = r'(<div class="message-box">)(.*?)(</div>)'
        
        def fix_bullets(match):
            content = match.group(2)
            if '•' in content and '<li>' not in content:
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
    
    def _save_application_file(self, html_content: str, jd_data: Dict, country: str) -> Path:
        """Save application to file with strategic naming"""
        
        try:
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            # Sanitize company name for filename
            company_safe = "".join(c for c in jd_data['company'] if c.isalnum() or c in (' ', '-', '_')).strip()
            if not company_safe:
                company_safe = "Company"
                
            timestamp = datetime.now().strftime('%Y-%m-%d')
            mode_suffix = "strategic" if self.enable_dynamic_mode else "professional"
            output_filename = f"{company_safe}_{country}_{timestamp}_{mode_suffix}.html"
            output_path = output_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            return output_path
                
        except Exception as e:
            raise RuntimeError(f"Failed to save output file: {str(e)}")
    
    def _print_strategic_generation_summary(self, 
                                          metadata: Dict, 
                                          validation_result: Dict, 
                                          orchestration_result: Dict,
                                          application_strategy: Optional[ApplicationStrategy],
                                          jd_intelligence: Optional[Any],
                                          output_path: Path):
        """Print comprehensive strategic generation summary"""
        
        print("\n" + "=" * 70)
        print("🚀 STRATEGIC APPLICATION GENERATED")
        print("=" * 70)
        
        # Basic info
        print(f"📁 Output File: {output_path}")
        print(f"🎯 ATS Score: {metadata['ats_score']}%")
        print(f"🔧 Generation Mode: {metadata['generation_mode'].upper()}")
        
        # Strategic analysis results
        if metadata.get('strategic_analysis'):
            strategic_data = metadata['strategic_analysis']
            print(f"\n🧠 Strategic Analysis:")
            print(f"   • Industry Focus: {strategic_data['industry_focus']}")
            print(f"   • Role Type: {strategic_data['role_type']}")
            print(f"   • Differentiation: {strategic_data['differentiation_angle']}")
            print(f"   • Fit Score: {strategic_data['fit_score']:.2f}/1.0")
            print(f"   • Recommendation: {strategic_data['recommendation']}")
            print(f"   • Key Strengths: {strategic_data['key_strengths_count']}")
            
            if strategic_data['competitive_advantages']:
                print(f"   • Advantages: {', '.join(strategic_data['competitive_advantages'][:3])}")
        
        # Validation results
        validation_results = metadata.get('validation_results', {})
        if validation_results:
            print(f"\n🛡️  Validation Results:")
            
            pre_gen = validation_results.get('pre_generation', {})
            print(f"   • Pre-generation: {pre_gen.get('decision', 'N/A')} ({pre_gen.get('confidence', 0):.1%})")
            
            content_qual = validation_results.get('content_quality', {})
            print(f"   • Content Quality: {content_qual.get('decision', 'N/A')} ({content_qual.get('overall_score', 0):.1f}/100)")
        
        # HTML quality
        print(f"\n📊 Output Quality:")
        print(f"   • Overall Quality: {validation_result['overall_score']:.1f}/100")
        print(f"   • Professional Standards: {validation_result['professional_score']:.1f}/100")
        
        # Content statistics
        print(f"\n📄 Content Statistics:")
        if metadata.get('strategic_analysis'):
            print(f"   • Strategic optimization: ENABLED")
        else:
            print(f"   • Strategic optimization: DISABLED (fallback mode)")
        
        print(f"   • AI confidence: {orchestration_result.get('overall_confidence', 0):.1%}")
        
        if validation_result.get('recommendations'):
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(validation_result['recommendations'][:2], 1):
                print(f"   {i}. {rec}")
        
        print("\n✅ Strategic application ready for professional use!")
        print("=" * 70)
    
    def interactive_mode(self):
        """Interactive mode for strategic application generation"""
        
        print("\n🚀 Welcome to Strategic Interactive Mode!")
        print("Advanced AI-powered application generation with strategic optimization.\n")
        
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
                
                job_description = "\n".join(job_description_lines).strip()
                
                if not job_description:
                    print("❌ No job description provided. Please try again.\n")
                    continue
                
                # Get country
                print("\n🌍 Target country (e.g., netherlands, sweden, ireland):")
                country = input().strip().lower()
                
                if not country:
                    country = "netherlands"  # Default
                
                # Get company name
                print("\n🏢 Company name (optional, press Enter to skip):")
                company_name = input().strip()
                
                # Ask about strategic mode
                if self.enable_dynamic_mode:
                    print("\n🧠 Use strategic AI optimization? (Y/n):")
                    use_strategic = input().strip().lower() not in ['n', 'no']
                    self.enable_dynamic_mode = use_strategic
                
                # Generate application
                print("\n🚀 Generating strategic application...")
                output_path = self.generate_strategic_application(job_description, country, company_name)
                
                print(f"\n📄 Strategic application saved to: {output_path}")
                print("\n🔄 Generate another application? (y/n):")
                
                if input().strip().lower() not in ['y', 'yes']:
                    break
                    
                print("\n" + "="*70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using Strategic Job Application Generator!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please check your input and try again.\n")

def main():
    """Main entry point"""
    enable_dynamic = True
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if "--standard" in sys.argv:
            enable_dynamic = False
        
    generator = DynamicEnhancedJobApplicationGenerator(enable_dynamic_mode=enable_dynamic)
    generator.interactive_mode()

if __name__ == "__main__":
    main()