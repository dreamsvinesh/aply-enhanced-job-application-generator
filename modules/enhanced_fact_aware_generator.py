#!/usr/bin/env python3
"""
Enhanced Fact-Aware Content Generator
Integrates all validation systems: workflow validation, content depth, human writing style,
and ATS optimization for comprehensive resume generation.
"""

import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from modules.user_data_extractor import UserDataExtractor
from modules.llm_service import LLMService
from modules.content_quality_validator import ContentQualityValidator
from modules.ats_scoring_engine import ATSScoringEngine
from modules.ats_resume_optimizer import ATSResumeOptimizer
from modules.workflow_validation_agent import (
    BrutalWorkflowValidator, 
    validate_data_extraction,
    validate_resume_generation, 
    validate_ats_scoring,
    validate_optimization
)
from modules.content_depth_validator import ContentDepthValidator
from modules.human_writing_validator import HumanWritingValidator

class EnhancedFactAwareGenerator:
    """
    Complete resume generation system with:
    - Brutal workflow validation
    - Enhanced data extraction with F&B projects
    - Content depth validation (6-8 bullets for Senior PM)
    - Human writing style validation
    - ATS optimization with retry logic
    - Comprehensive reporting
    """
    
    def __init__(self, 
                 ats_optimization_enabled: bool = True,
                 target_ats_score: float = 85.0,
                 enable_brutal_validation: bool = True):
        
        # Core components
        self.user_extractor = UserDataExtractor()
        self.llm_service = LLMService()
        self.quality_validator = ContentQualityValidator()
        self.ats_scoring = ATSScoringEngine()
        self.depth_validator = ContentDepthValidator()
        self.writing_validator = HumanWritingValidator()
        
        # ATS optimization
        self.ats_optimization_enabled = ats_optimization_enabled
        self.target_ats_score = target_ats_score
        if ats_optimization_enabled:
            self.ats_optimizer = ATSResumeOptimizer(target_score=target_ats_score)
        
        # Workflow validation
        self.enable_brutal_validation = enable_brutal_validation
        self.workflow_validator = BrutalWorkflowValidator() if enable_brutal_validation else None
        
        # User data
        self.factual_data = self.user_extractor.extract_vinesh_data()
        
    def generate_comprehensive_resume(self, jd_analysis: Dict, country: str = "netherlands") -> Dict[str, Any]:
        """Generate comprehensive resume with full validation workflow"""
        
        if self.enable_brutal_validation:
            # Start brutal workflow validation
            self.workflow_validator.start_workflow_validation("Comprehensive Resume Generation")
        
        print(f"🚀 ENHANCED FACT-AWARE RESUME GENERATION")
        print(f"📊 Target: {jd_analysis['extracted_info']['company']} - {jd_analysis['extracted_info']['role_title']}")
        print(f"🎯 ATS Target: {self.target_ats_score}%")
        print(f"🔥 Brutal Validation: {'ENABLED' if self.enable_brutal_validation else 'DISABLED'}")
        print("=" * 80)
        
        results = {}
        
        # STEP 1: Enhanced Data Extraction
        print("\n📋 STEP 1: Enhanced Data Extraction")
        step1_success = self._execute_data_extraction_step(results)
        
        if not step1_success:
            return self._handle_critical_failure("Data extraction failed", results)
        
        # STEP 2: Generate Initial Resume with Content Depth Validation
        print("\n📝 STEP 2: Generate Resume with Content Depth Validation")
        step2_success = self._execute_resume_generation_step(jd_analysis, country, results)
        
        if not step2_success:
            return self._handle_critical_failure("Resume generation failed", results)
        
        # STEP 3: Human Writing Style Validation
        print("\n✍️ STEP 3: Human Writing Style Validation")
        step3_success = self._execute_writing_validation_step(results)
        
        if not step3_success:
            return self._handle_critical_failure("Writing validation failed", results)
        
        # STEP 4: ATS Scoring
        print("\n🎯 STEP 4: ATS Scoring Analysis")
        step4_success = self._execute_ats_scoring_step(jd_analysis, results)
        
        if not step4_success:
            return self._handle_critical_failure("ATS scoring failed", results)
        
        # STEP 5: ATS Optimization (if needed)
        if self.ats_optimization_enabled:
            print("\n⚡ STEP 5: ATS Optimization")
            step5_success = self._execute_ats_optimization_step(jd_analysis, results)
            
            if not step5_success:
                print("⚠️ ATS optimization failed, using original resume")
        
        # STEP 6: Final Validation
        print("\n🔍 STEP 6: Final Comprehensive Validation")
        step6_success = self._execute_final_validation_step(results)
        
        # Complete workflow validation
        if self.enable_brutal_validation:
            workflow_result = self.workflow_validator.finish_workflow_validation()
            results['workflow_validation'] = workflow_result
        
        # Generate summary
        results['generation_summary'] = self._generate_comprehensive_summary(results)
        
        print(f"\n🎉 ENHANCED GENERATION COMPLETE!")
        return results
    
    def _execute_data_extraction_step(self, results: Dict[str, Any]) -> bool:
        """Execute and validate data extraction step"""
        
        def extract_data(input_data):
            return self.factual_data
        
        if self.enable_brutal_validation:
            step = self.workflow_validator.add_validation_step(
                "001", "Enhanced Data Extraction", {}, "dict", validate_data_extraction
            )
            success = self.workflow_validator.execute_and_validate_step(step, extract_data)
            results['data_extraction'] = {
                'data': step.output_data,
                'validation': step.validation_details,
                'success': success
            }
            return success
        else:
            results['data_extraction'] = {
                'data': self.factual_data,
                'success': True
            }
            return True
    
    def _execute_resume_generation_step(self, jd_analysis: Dict, country: str, results: Dict[str, Any]) -> bool:
        """Execute resume generation with depth validation"""
        
        def generate_resume(extracted_data):
            return self._generate_resume_with_depth_validation(extracted_data, jd_analysis, country)
        
        if self.enable_brutal_validation:
            step = self.workflow_validator.add_validation_step(
                "002", "Resume Generation with Depth Validation", 
                results['data_extraction']['data'], "dict", validate_resume_generation
            )
            success = self.workflow_validator.execute_and_validate_step(step, generate_resume)
            results['resume_generation'] = step.output_data
            return success
        else:
            results['resume_generation'] = generate_resume(results['data_extraction']['data'])
            return results['resume_generation'] is not None
    
    def _execute_writing_validation_step(self, results: Dict[str, Any]) -> bool:
        """Execute human writing style validation"""
        
        def validate_writing_style(resume_data):
            content = resume_data.get('content', '')
            writing_validation = self.writing_validator.validate_human_writing(content)
            
            # If writing is too LLM-like, try to humanize
            if not writing_validation['is_human_like']:
                print("⚠️ Content detected as LLM-like, attempting humanization...")
                humanized_content = self.writing_validator.humanize_content(content)
                
                # Re-validate humanized content
                writing_validation_retry = self.writing_validator.validate_human_writing(humanized_content)
                
                if writing_validation_retry['is_human_like']:
                    print("✅ Content successfully humanized")
                    resume_data['content'] = humanized_content
                    writing_validation = writing_validation_retry
                    writing_validation['humanized'] = True
                else:
                    print("❌ Humanization failed")
                    writing_validation['humanized'] = False
            
            return {
                'writing_validation': writing_validation,
                'content': resume_data['content'],
                'is_human_like': writing_validation['is_human_like'],
                'human_score': writing_validation['human_score']
            }
        
        def validate_writing_step(input_data, output_data):
            if not isinstance(output_data, dict):
                return {"is_valid": False, "error": "Output must be dict"}
            
            if not output_data.get('is_human_like', False):
                return {"is_valid": False, "error": f"Content not human-like (score: {output_data.get('human_score', 0)})"}
            
            return {"is_valid": True, "human_score": output_data.get('human_score', 0)}
        
        if self.enable_brutal_validation:
            step = self.workflow_validator.add_validation_step(
                "003", "Human Writing Style Validation", 
                results['resume_generation'], "dict", validate_writing_step
            )
            success = self.workflow_validator.execute_and_validate_step(step, validate_writing_style)
            
            # Update resume content if humanized
            if success and step.output_data:
                results['resume_generation']['content'] = step.output_data['content']
                results['writing_validation'] = step.output_data['writing_validation']
            
            return success
        else:
            validation_result = validate_writing_style(results['resume_generation'])
            results['writing_validation'] = validation_result['writing_validation']
            return validation_result['is_human_like']
    
    def _execute_ats_scoring_step(self, jd_analysis: Dict, results: Dict[str, Any]) -> bool:
        """Execute ATS scoring step"""
        
        def score_ats(resume_data):
            content = resume_data.get('content', '')
            jd_text = self._extract_jd_text_from_analysis(jd_analysis)
            return self.ats_scoring.score_resume_against_jd(content, jd_analysis, jd_text)
        
        if self.enable_brutal_validation:
            step = self.workflow_validator.add_validation_step(
                "004", "ATS Scoring Analysis", 
                results['resume_generation'], "dict", validate_ats_scoring
            )
            success = self.workflow_validator.execute_and_validate_step(step, score_ats)
            results['ats_scoring'] = step.output_data
            return success
        else:
            results['ats_scoring'] = score_ats(results['resume_generation'])
            return results['ats_scoring'] is not None
    
    def _execute_ats_optimization_step(self, jd_analysis: Dict, results: Dict[str, Any]) -> bool:
        """Execute ATS optimization if score below target"""
        
        current_score = results['ats_scoring']['overall_ats_score']
        
        if current_score >= self.target_ats_score:
            print(f"✅ ATS score ({current_score:.1f}%) already meets target ({self.target_ats_score}%)")
            results['ats_optimization'] = {'skipped': True, 'reason': 'Target already achieved'}
            return True
        
        def optimize_ats(input_data):
            content = results['resume_generation']['content']
            jd_text = self._extract_jd_text_from_analysis(jd_analysis)
            return self.ats_optimizer.optimize_resume_for_ats(content, jd_analysis, jd_text)
        
        if self.enable_brutal_validation:
            step = self.workflow_validator.add_validation_step(
                "005", "ATS Optimization", 
                results['resume_generation'], "dict", validate_optimization
            )
            success = self.workflow_validator.execute_and_validate_step(step, optimize_ats)
            
            if success and step.output_data:
                # Update resume content with optimized version
                results['resume_generation']['content'] = step.output_data['optimized_resume']
                results['ats_optimization'] = step.output_data
                
                # Re-run ATS scoring on optimized content
                optimized_score = step.output_data['final_ats_score']
                results['ats_scoring'] = optimized_score
                
                print(f"📈 ATS optimization: {current_score:.1f}% → {optimized_score['overall_ats_score']:.1f}%")
            
            return success
        else:
            optimization_result = optimize_ats({})
            if optimization_result:
                results['resume_generation']['content'] = optimization_result['optimized_resume']
                results['ats_optimization'] = optimization_result
                results['ats_scoring'] = optimization_result['final_ats_score']
                return True
            return False
    
    def _execute_final_validation_step(self, results: Dict[str, Any]) -> bool:
        """Execute final comprehensive validation"""
        
        final_content = results['resume_generation']['content']
        
        # Final fact preservation check
        fact_validation = self.user_extractor.validate_content_against_facts(final_content)
        
        # Final content depth check
        jd_analysis = results.get('jd_analysis', {})
        depth_validation = self.depth_validator.validate_content_depth(final_content, jd_analysis)
        
        # Final writing style check
        writing_validation = self.writing_validator.validate_human_writing(final_content)
        
        final_validation = {
            'fact_preservation': fact_validation,
            'content_depth': depth_validation,
            'writing_style': writing_validation,
            'overall_valid': (fact_validation['is_valid'] and 
                            depth_validation['is_valid'] and 
                            writing_validation['is_human_like'])
        }
        
        results['final_validation'] = final_validation
        
        return final_validation['overall_valid']
    
    def _generate_resume_with_depth_validation(self, extracted_data: Dict, jd_analysis: Dict, country: str) -> Dict[str, Any]:
        """Generate resume with content depth validation"""
        
        constraints_prompt = self.user_extractor.create_llm_constraints_prompt()
        
        # EXPLICIT ACHIEVEMENT EXTRACTION for better prompting
        senior_pm_achievements = extracted_data['work_experience'][0]['exact_achievements'] if extracted_data['work_experience'] else []
        pm_achievements = extracted_data['work_experience'][1]['exact_achievements'] if len(extracted_data['work_experience']) > 1 else []
        engineer_achievements = extracted_data['work_experience'][2]['exact_achievements'] if len(extracted_data['work_experience']) > 2 else []
        
        # Enhanced prompt with explicit achievement requirements
        prompt = f"""
{constraints_prompt}

TASK: Create resume for {extracted_data['personal_info']['name']} for Product Operations role at Dealfront.

CRITICAL: You MUST use ALL achievements listed below. Do NOT summarize or shorten them.

SENIOR PM ROLE - COWRKS (01/2023 - Present):
REQUIREMENT: Write exactly {len(senior_pm_achievements)} bullets using these EXACT achievements:
{chr(10).join([f"• {achievement}" for achievement in senior_pm_achievements])}

PM ROLE - COWRKS (08/2016 - 01/2020):
REQUIREMENT: Write exactly {len(pm_achievements)} bullets using these EXACT achievements:
{chr(10).join([f"• {achievement}" for achievement in pm_achievements])}

ENGINEER ROLE - Automne/Rukshaya (09/2012 - 07/2016):
REQUIREMENT: Write exactly {len(engineer_achievements)} bullets using these EXACT achievements:
{chr(10).join([f"• {achievement}" for achievement in engineer_achievements])}

WRITING STYLE: Human, direct, action-focused. NO words like "comprehensive", "facilitate", "leverage".
BULLET LENGTH: Each bullet 20-35 words (current ones are perfect length).
SECTIONS: Include "PROFESSIONAL SUMMARY", "EXPERIENCE", "EDUCATION" headers.
FORMAT: Role • Company • Duration • Location

Create the resume now using ALL achievements exactly as provided above.
"""
        
        try:
            response = self.llm_service.call_llm(
                prompt=prompt,
                task_type="comprehensive_resume_generation",
                temperature=0.1,  # Low temperature for consistency
                max_tokens=3000   # Increased for comprehensive content
            )
            
            # Validate content depth
            depth_validation = self.depth_validator.validate_content_depth(response.content, jd_analysis)
            
            # Basic fact validation
            fact_validation = self.user_extractor.validate_content_against_facts(response.content)
            
            return {
                'content': response.content,
                'depth_validation': depth_validation,
                'fact_validation': fact_validation,
                'preserves_facts': fact_validation['is_valid'],
                'meets_depth_requirements': depth_validation['is_valid'],
                'depth_score': depth_validation['depth_score']
            }
            
        except Exception as e:
            print(f"❌ Resume generation failed: {str(e)}")
            return None
    
    def _extract_jd_text_from_analysis(self, jd_analysis: Dict) -> str:
        """Extract JD text from analysis for ATS scoring"""
        jd_text_parts = []
        
        if 'extracted_info' in jd_analysis:
            info = jd_analysis['extracted_info']
            if 'company' in info:
                jd_text_parts.append(f"Company: {info['company']}")
            if 'role_title' in info:
                jd_text_parts.append(f"Role: {info['role_title']}")
        
        if 'requirements' in jd_analysis:
            req = jd_analysis['requirements']
            if 'must_have_technical' in req:
                jd_text_parts.append(f"Required Skills: {', '.join(req['must_have_technical'])}")
            if 'nice_to_have_technical' in req:
                jd_text_parts.append(f"Preferred Skills: {', '.join(req['nice_to_have_technical'])}")
            if 'domain_expertise' in req:
                jd_text_parts.append(f"Domain Expertise: {', '.join(req['domain_expertise'])}")
        
        if 'original_jd' in jd_analysis:
            jd_text_parts.append(jd_analysis['original_jd'])
        
        return "\n".join(jd_text_parts)
    
    def _handle_critical_failure(self, failure_reason: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """Handle critical failures in workflow"""
        
        print(f"💀 CRITICAL FAILURE: {failure_reason}")
        
        results['critical_failure'] = {
            'reason': failure_reason,
            'timestamp': datetime.now().isoformat(),
            'partial_results': True
        }
        
        if self.enable_brutal_validation:
            workflow_result = self.workflow_validator.finish_workflow_validation()
            results['workflow_validation'] = workflow_result
        
        return results
    
    def _generate_comprehensive_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive summary of generation process"""
        
        summary = {
            'generation_timestamp': datetime.now().isoformat(),
            'workflow_completed': 'critical_failure' not in results,
            'steps_completed': [],
            'validations_passed': {},
            'final_metrics': {}
        }
        
        # Track completed steps
        if 'data_extraction' in results:
            summary['steps_completed'].append('Data Extraction')
        if 'resume_generation' in results:
            summary['steps_completed'].append('Resume Generation')
        if 'writing_validation' in results:
            summary['steps_completed'].append('Writing Validation')
        if 'ats_scoring' in results:
            summary['steps_completed'].append('ATS Scoring')
        if 'ats_optimization' in results:
            summary['steps_completed'].append('ATS Optimization')
        if 'final_validation' in results:
            summary['steps_completed'].append('Final Validation')
        
        # Track validations
        if 'final_validation' in results:
            fv = results['final_validation']
            summary['validations_passed'] = {
                'fact_preservation': fv['fact_preservation']['is_valid'],
                'content_depth': fv['content_depth']['is_valid'],
                'writing_style': fv['writing_style']['is_human_like'],
                'overall': fv['overall_valid']
            }
        
        # Track final metrics
        if 'ats_scoring' in results:
            summary['final_metrics']['ats_score'] = results['ats_scoring']['overall_ats_score']
            summary['final_metrics']['ats_grade'] = results['ats_scoring']['grade']
        
        if 'writing_validation' in results:
            summary['final_metrics']['human_score'] = results['writing_validation']['human_score']
        
        if 'resume_generation' in results and 'depth_score' in results['resume_generation']:
            summary['final_metrics']['depth_score'] = results['resume_generation']['depth_score']
        
        return summary
    
    def save_comprehensive_package(self, results: Dict, output_dir: str) -> str:
        """Save complete package with all validation reports"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save final resume
        if 'resume_generation' in results and 'content' in results['resume_generation']:
            with open(output_path / "enhanced_resume.txt", "w") as f:
                f.write(results['resume_generation']['content'])
        
        # Save all validation reports
        with open(output_path / "comprehensive_validation_report.json", "w") as f:
            # Clean results for JSON serialization
            clean_results = self._clean_results_for_json(results)
            json.dump(clean_results, f, indent=2, default=str)
        
        # Save workflow validation report if available
        if 'workflow_validation' in results:
            from modules.workflow_validation_agent import BrutalWorkflowValidator
            validator = BrutalWorkflowValidator()
            validator.save_validation_report(results['workflow_validation'], str(output_path))
        
        return str(output_path)
    
    def _clean_results_for_json(self, results: Dict) -> Dict:
        """Clean results for JSON serialization"""
        clean_results = {}
        
        for key, value in results.items():
            if key == 'workflow_validation':
                # Skip workflow validation (saved separately)
                continue
            elif hasattr(value, '__dict__'):
                # Convert objects to dict
                clean_results[key] = value.__dict__
            else:
                clean_results[key] = value
        
        return clean_results

def main():
    """Demo enhanced fact-aware generation"""
    print("🚀 ENHANCED FACT-AWARE GENERATOR DEMO")
    print("=" * 60)
    
    # Mock JD analysis
    jd_analysis = {
        'extracted_info': {
            'company': 'Dealfront',
            'role_title': 'Product Operations (Founding Role)',
            'location': 'Denmark'
        },
        'requirements': {
            'must_have_technical': ['Product Operations', 'AI Automation', 'Process Design'],
            'must_have_business': ['Strategic Operations', 'Team Enablement', 'Decision-making'],
            'nice_to_have_technical': ['Platform', 'Go-to-market', 'Product Analytics']
        },
        'original_jd': 'Product Operations founding role with AI automation, team enablement, and strategic operations'
    }
    
    # Initialize enhanced generator
    generator = EnhancedFactAwareGenerator(
        ats_optimization_enabled=True,
        target_ats_score=85.0,
        enable_brutal_validation=True
    )
    
    # Generate comprehensive resume
    results = generator.generate_comprehensive_resume(jd_analysis, country="denmark")
    
    # Save complete package
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output/enhanced_dealfront_{timestamp}"
    saved_path = generator.save_comprehensive_package(results, output_dir)
    
    print(f"\n📊 Enhanced generation complete!")
    print(f"📁 Complete package saved to: {saved_path}")
    
    # Show summary
    if 'generation_summary' in results:
        summary = results['generation_summary']
        print(f"\n📈 Summary:")
        print(f"• Steps completed: {len(summary['steps_completed'])}")
        print(f"• Workflow completed: {'✅' if summary['workflow_completed'] else '❌'}")
        
        if 'final_metrics' in summary:
            metrics = summary['final_metrics']
            if 'ats_score' in metrics:
                print(f"• Final ATS Score: {metrics['ats_score']:.1f}%")
            if 'human_score' in metrics:
                print(f"• Human Writing Score: {metrics['human_score']:.1f}%")

if __name__ == "__main__":
    main()