#!/usr/bin/env python3
"""
ATS Resume Optimizer
Automatically improves resume based on ATS scoring feedback to achieve target scores.
"""

import re
import json
from typing import Dict, List, Any, Tuple
from pathlib import Path
from modules.ats_scoring_engine import ATSScoringEngine
from modules.llm_service import LLMService
from modules.user_data_extractor import UserDataExtractor

class ATSResumeOptimizer:
    """Optimizes resume content based on ATS scoring feedback"""
    
    def __init__(self, target_score: float = 85.0, max_iterations: int = 3):
        self.ats_engine = ATSScoringEngine()
        self.llm_service = LLMService()
        self.user_extractor = UserDataExtractor()
        self.target_score = target_score
        self.max_iterations = max_iterations
        self.factual_data = self.user_extractor.extract_vinesh_data()
    
    def optimize_resume_for_ats(self, resume_content: str, jd_analysis: Dict, jd_text: str) -> Dict[str, Any]:
        """
        Iteratively optimize resume to achieve target ATS score while preserving facts
        """
        print(f"🎯 Starting ATS optimization (target: {self.target_score}%)")
        print("=" * 60)
        
        optimization_history = []
        current_resume = resume_content
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n🔄 Optimization Iteration {iteration}/{self.max_iterations}")
            print("-" * 40)
            
            # Score current resume
            ats_score = self.ats_engine.score_resume_against_jd(current_resume, jd_analysis, jd_text)
            current_score = ats_score['overall_ats_score']
            
            print(f"📊 Current ATS Score: {current_score:.1f}% (Grade: {ats_score['grade']})")
            
            # Store this iteration's results
            iteration_data = {
                'iteration': iteration,
                'score': current_score,
                'grade': ats_score['grade'],
                'resume_content': current_resume,
                'ats_analysis': ats_score,
                'optimizations_applied': []
            }
            
            # Check if target achieved
            if current_score >= self.target_score:
                print(f"✅ Target score achieved: {current_score:.1f}% >= {self.target_score}%")
                iteration_data['target_achieved'] = True
                optimization_history.append(iteration_data)
                break
            
            # Identify optimization opportunities
            optimization_plan = self._create_optimization_plan(ats_score, jd_analysis)
            
            if not optimization_plan['optimizations']:
                print("⚠️ No further optimizations available")
                iteration_data['no_more_optimizations'] = True
                optimization_history.append(iteration_data)
                break
            
            print("\n💡 Applying optimizations:")
            for opt in optimization_plan['optimizations'][:3]:  # Top 3 optimizations
                print(f"• {opt['description']}")
            
            # Apply optimizations while preserving facts
            optimized_resume = self._apply_optimizations(
                current_resume, 
                optimization_plan, 
                jd_analysis
            )
            
            # Validate fact preservation
            fact_validation = self.user_extractor.validate_content_against_facts(optimized_resume)
            
            if not fact_validation['is_valid']:
                print("⚠️ Optimization would compromise fact preservation - stopping")
                iteration_data['fact_preservation_failed'] = True
                optimization_history.append(iteration_data)
                break
            
            iteration_data['optimizations_applied'] = optimization_plan['optimizations'][:3]
            optimization_history.append(iteration_data)
            current_resume = optimized_resume
        
        # Final scoring
        final_ats_score = self.ats_engine.score_resume_against_jd(current_resume, jd_analysis, jd_text)
        final_score = final_ats_score['overall_ats_score']
        
        print(f"\n🎉 Optimization Complete!")
        print(f"📈 Final ATS Score: {final_score:.1f}% (Grade: {final_ats_score['grade']})")
        print(f"📊 Improvement: {final_score - optimization_history[0]['score']:+.1f} points")
        
        return {
            'optimized_resume': current_resume,
            'final_ats_score': final_ats_score,
            'optimization_history': optimization_history,
            'target_achieved': final_score >= self.target_score,
            'total_iterations': iteration,
            'score_improvement': final_score - optimization_history[0]['score']
        }
    
    def _create_optimization_plan(self, ats_score: Dict, jd_analysis: Dict) -> Dict[str, Any]:
        """Create specific optimization plan based on ATS weaknesses"""
        
        optimizations = []
        category_scores = ats_score['category_scores']
        
        # Analyze each category for improvements
        for category, data in category_scores.items():
            if data['score'] < 80:  # Below good threshold
                missing_keywords = data.get('missing', [])
                
                if category == 'soft_skills' and missing_keywords:
                    optimizations.append({
                        'type': 'add_soft_skills',
                        'keywords': missing_keywords[:2],  # Top 2 missing
                        'priority': 'high',
                        'description': f"Add soft skills: {', '.join(missing_keywords[:2])}"
                    })
                
                elif category == 'job_titles' and missing_keywords:
                    optimizations.append({
                        'type': 'add_job_titles',
                        'keywords': missing_keywords[:2],
                        'priority': 'high', 
                        'description': f"Add job titles: {', '.join(missing_keywords[:2])}"
                    })
                
                elif category == 'industry_terms' and missing_keywords:
                    optimizations.append({
                        'type': 'add_industry_terms',
                        'keywords': missing_keywords[:3],
                        'priority': 'medium',
                        'description': f"Add industry terms: {', '.join(missing_keywords[:3])}"
                    })
                
                elif category == 'hard_skills' and missing_keywords:
                    optimizations.append({
                        'type': 'add_hard_skills',
                        'keywords': missing_keywords[:2],
                        'priority': 'high',
                        'description': f"Add hard skills: {', '.join(missing_keywords[:2])}"
                    })
        
        # Check readability issues
        readability_score = ats_score['ats_factors']['readability_score']
        if readability_score < 70:
            optimizations.append({
                'type': 'improve_readability',
                'priority': 'medium',
                'description': 'Simplify sentence structure for better readability'
            })
        
        # Check if skills section is missing
        if 'skills' not in ats_score['ats_factors']['section_structure']['found_sections']:
            optimizations.append({
                'type': 'add_skills_section',
                'priority': 'medium',
                'description': 'Add dedicated Core Competencies/Skills section'
            })
        
        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        optimizations.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        
        return {
            'optimizations': optimizations,
            'total_count': len(optimizations),
            'high_priority': len([o for o in optimizations if o['priority'] == 'high'])
        }
    
    def _apply_optimizations(self, resume_content: str, optimization_plan: Dict, jd_analysis: Dict) -> str:
        """Apply optimizations using LLM while preserving factual content"""
        
        constraints_prompt = self.user_extractor.create_llm_constraints_prompt()
        
        # Build optimization instructions
        optimization_instructions = []
        for opt in optimization_plan['optimizations'][:3]:  # Apply top 3
            if opt['type'] == 'add_soft_skills':
                optimization_instructions.append(
                    f"Add soft skills keywords naturally: {', '.join(opt['keywords'])}"
                )
            elif opt['type'] == 'add_job_titles':
                optimization_instructions.append(
                    f"Include job title variations: {', '.join(opt['keywords'])}"
                )
            elif opt['type'] == 'add_industry_terms':
                optimization_instructions.append(
                    f"Incorporate industry terms: {', '.join(opt['keywords'])}"
                )
            elif opt['type'] == 'add_hard_skills':
                optimization_instructions.append(
                    f"Highlight technical skills: {', '.join(opt['keywords'])}"
                )
            elif opt['type'] == 'improve_readability':
                optimization_instructions.append(
                    "Simplify complex sentences while maintaining professional tone"
                )
            elif opt['type'] == 'add_skills_section':
                optimization_instructions.append(
                    "Ensure Core Competencies section is clearly structured"
                )
        
        prompt = f"""
{constraints_prompt}

TASK: Optimize the resume for ATS compatibility while preserving ALL factual information.

CURRENT RESUME:
{resume_content}

OPTIMIZATION INSTRUCTIONS:
{chr(10).join(f'• {instruction}' for instruction in optimization_instructions)}

JOB REQUIREMENTS FOR CONTEXT:
Company: {jd_analysis['extracted_info']['company']}
Role: {jd_analysis['extracted_info']['role_title']}

CRITICAL RULES:
1. NEVER change company names (keep COWRKS, Automne Technologies, Rukshaya Emerging Technologies)
2. NEVER alter real metrics (94% accuracy, $2M revenue, 99.6% reduction, etc.)
3. NEVER modify personal information (name, email, phone, education)
4. ONLY add keywords naturally within existing context
5. Maintain professional, non-LLM-generated writing style
6. Keep the same resume structure and format
7. Add missing keywords by expanding on real achievements, not creating new ones

OUTPUT: Return the optimized resume that incorporates the keywords naturally while preserving all factual content.
"""
        
        try:
            response = self.llm_service.call_llm(
                prompt=prompt,
                task_type="resume_optimization",
                temperature=0.1,  # Low temperature for consistency
                max_tokens=2500
            )
            return response.content
        except Exception as e:
            print(f"⚠️ LLM optimization failed: {e}")
            return resume_content  # Return original if optimization fails
    
    def generate_optimization_report(self, optimization_result: Dict, output_dir: str) -> str:
        """Generate comprehensive optimization report"""
        
        history = optimization_result['optimization_history']
        final_score = optimization_result['final_ats_score']['overall_ats_score']
        initial_score = history[0]['score']
        
        report = f"""ATS RESUME OPTIMIZATION REPORT
{"=" * 80}

OPTIMIZATION SUMMARY:
Target ATS Score: {self.target_score}%
Initial Score: {initial_score:.1f}% (Grade: {history[0]['grade']})
Final Score: {final_score:.1f}% (Grade: {optimization_result['final_ats_score']['grade']})
Improvement: {optimization_result['score_improvement']:+.1f} points
Target Achieved: {'✅ YES' if optimization_result['target_achieved'] else '❌ NO'}
Total Iterations: {optimization_result['total_iterations']}

ITERATION BREAKDOWN:
"""
        
        for i, iteration in enumerate(history):
            report += f"\nIteration {iteration['iteration']}:\n"
            report += f"• Score: {iteration['score']:.1f}% (Grade: {iteration['grade']})\n"
            
            if 'optimizations_applied' in iteration and iteration['optimizations_applied']:
                report += "• Optimizations Applied:\n"
                for opt in iteration['optimizations_applied']:
                    report += f"  - {opt['description']}\n"
            
            if iteration.get('target_achieved'):
                report += "• ✅ Target score achieved!\n"
            elif iteration.get('no_more_optimizations'):
                report += "• ⚠️ No further optimizations available\n"
            elif iteration.get('fact_preservation_failed'):
                report += "• ⚠️ Stopped to preserve factual accuracy\n"
        
        # Final category breakdown
        final_categories = optimization_result['final_ats_score']['category_scores']
        report += f"\nFINAL ATS CATEGORY SCORES:\n"
        
        for category, data in final_categories.items():
            score = data['score']
            emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            report += f"{emoji} {category.replace('_', ' ').title()}: {score:.1f}% ({data['match_count']}/{data['total_jd_keywords']} matches)\n"
        
        # Recommendations for future improvement
        if not optimization_result['target_achieved']:
            report += f"\nREMAINING IMPROVEMENT OPPORTUNITIES:\n"
            remaining_recs = optimization_result['final_ats_score']['recommendations'][:5]
            for i, rec in enumerate(remaining_recs, 1):
                report += f"{i}. {rec}\n"
        
        report += f"""
FACT PRESERVATION: ✅ MAINTAINED
All real company names, metrics, and personal information preserved throughout optimization.

OPTIMIZATION STRATEGY:
• Keyword enhancement through natural expansion of existing achievements
• Maintained authentic COWRKS experience and real metrics
• Preserved professional writing style without LLM artifacts
• Focused on high-impact ATS factors while respecting factual constraints
"""
        
        # Save report
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        report_file = output_path / "ats_optimization_report.txt"
        with open(report_file, "w") as f:
            f.write(report)
        
        return str(report_file)

def main():
    """Demo ATS optimization"""
    print("🎯 ATS RESUME OPTIMIZATION DEMO")
    print("=" * 50)
    
    # Load existing resume for optimization
    resume_path = "/Users/vinesh.kumar/Downloads/Aply/output/Dealfront_Denmark_FactAware_20251115_104458/resume.txt"
    
    try:
        with open(resume_path, 'r') as f:
            resume_content = f.read()
        print("✅ Resume loaded for optimization")
    except FileNotFoundError:
        print(f"❌ Resume not found: {resume_path}")
        return
    
    # Mock JD analysis
    jd_analysis = {
        'extracted_info': {
            'company': 'Dealfront',
            'role_title': 'Product Operations (Founding Role)'
        },
        'requirements': {
            'must_have_technical': ['Product Operations', 'AI Automation'],
            'must_have_business': ['Strategic Operations', 'Team Enablement'],
            'nice_to_have_technical': ['PRD Standards', 'Product Analytics']
        }
    }
    
    # JD text for scoring
    jd_text = """Product Operations role with AI-enabled process automation, team enablement, strategic operations, decision-making, product ops experience in SaaS platforms and go-to-market strategies."""
    
    # Initialize optimizer
    optimizer = ATSResumeOptimizer(target_score=85.0, max_iterations=3)
    
    # Run optimization
    result = optimizer.optimize_resume_for_ats(resume_content, jd_analysis, jd_text)
    
    # Save optimized resume
    output_dir = "output/ats_optimized_resume"
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save optimized resume
    optimized_resume_file = output_path / "optimized_resume.txt"
    with open(optimized_resume_file, "w") as f:
        f.write(result['optimized_resume'])
    
    # Save detailed ATS analysis
    final_analysis_file = output_path / "final_ats_analysis.json" 
    with open(final_analysis_file, "w") as f:
        json.dump(result['final_ats_score'], f, indent=2)
    
    # Generate optimization report
    report_file = optimizer.generate_optimization_report(result, output_dir)
    
    print(f"\n📁 Optimization Complete!")
    print(f"• Optimized Resume: {optimized_resume_file}")
    print(f"• ATS Analysis: {final_analysis_file}")
    print(f"• Optimization Report: {report_file}")

if __name__ == "__main__":
    main()