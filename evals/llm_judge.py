#!/usr/bin/env python3
"""
Refactored LLM-as-Judge evaluation for Aply Job Application Generator
Simplified and modular design for better maintainability
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Local imports
from .evaluation_prompts import EvaluationPrompts
from .content_evaluator import ContentEvaluator

class LLMJudge:
    """
    Simplified LLM-as-Judge evaluator using modular components
    """
    
    def __init__(self, model="claude"):
        self.model = model
        self.prompts = EvaluationPrompts()
        self.evaluator = ContentEvaluator()
    
    def evaluate_content(self, content: str, content_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate content using appropriate prompt and evaluation logic
        
        Args:
            content: The content to evaluate
            content_type: Type of content ('resume', 'cover_letter', 'linkedin', 'holistic')
            context: Additional context (role, company, country, etc.)
        
        Returns:
            Evaluation results with scores and feedback
        """
        try:
            # Get appropriate prompt
            prompt_method_map = {
                "resume": self.prompts.get_resume_evaluation_prompt,
                "cover_letter": self.prompts.get_cover_letter_evaluation_prompt,
                "linkedin": self.prompts.get_linkedin_evaluation_prompt,
                "holistic": self.prompts.get_holistic_evaluation_prompt
            }
            
            if content_type not in prompt_method_map:
                raise ValueError(f"Unsupported content type: {content_type}")
            
            # Get and format prompt
            prompt_template = prompt_method_map[content_type]()
            formatted_prompt = prompt_template.format(
                content=content,
                role=context.get('role', 'Product Manager'),
                company=context.get('company', 'Company'),
                country=context.get('country', 'Netherlands')
            )
            
            # Evaluate content
            evaluation_result = self.evaluator.simulate_llm_evaluation(formatted_prompt, content_type)
            
            # Add metadata
            evaluation_result.update({
                'content_type': content_type,
                'evaluation_timestamp': datetime.now().isoformat(),
                'model_used': self.model,
                'context': context
            })
            
            return evaluation_result
            
        except Exception as e:
            return {
                'error': str(e),
                'content_type': content_type,
                'evaluation_timestamp': datetime.now().isoformat(),
                'success': False
            }
    
    def batch_evaluate(self, test_cases_file: str) -> Dict[str, Any]:
        """
        Run batch evaluation on test cases
        
        Args:
            test_cases_file: Path to JSON file with test cases
            
        Returns:
            Batch evaluation results
        """
        try:
            # Load test cases
            with open(test_cases_file, 'r', encoding='utf-8') as f:
                test_cases = json.load(f)
            
            batch_results = {
                'total_cases': len(test_cases.get('test_cases', [])),
                'evaluated_cases': 0,
                'results': [],
                'summary_stats': {},
                'batch_timestamp': datetime.now().isoformat()
            }
            
            for i, test_case in enumerate(test_cases.get('test_cases', [])):
                try:
                    # Extract test case data
                    generated_content = test_case.get('generated_content', '')
                    context = test_case.get('context', {})
                    
                    # Run evaluations for each content type
                    case_results = {
                        'case_id': i + 1,
                        'context': context,
                        'evaluations': {}
                    }
                    
                    # Extract and evaluate each section
                    sections_to_evaluate = [
                        ('resume', '## Resume', '## Cover Letter'),
                        ('cover_letter', '## Cover Letter', '## LinkedIn Message'),
                        ('linkedin', '## LinkedIn Message', '## Email Template'),
                        ('holistic', '', '')
                    ]
                    
                    for section_type, start_marker, end_marker in sections_to_evaluate:
                        if section_type == 'holistic':
                            section_content = generated_content
                        else:
                            section_content = self.evaluator.extract_section(
                                generated_content, start_marker, end_marker
                            )
                        
                        if section_content.strip():
                            evaluation = self.evaluate_content(section_content, section_type, context)
                            case_results['evaluations'][section_type] = evaluation
                    
                    batch_results['results'].append(case_results)
                    batch_results['evaluated_cases'] += 1
                    
                except Exception as e:
                    case_results = {
                        'case_id': i + 1,
                        'error': str(e),
                        'context': test_case.get('context', {})
                    }
                    batch_results['results'].append(case_results)
            
            # Calculate summary statistics
            batch_results['summary_stats'] = self._calculate_summary_stats(batch_results['results'])
            
            return batch_results
            
        except Exception as e:
            return {
                'error': f"Batch evaluation failed: {str(e)}",
                'batch_timestamp': datetime.now().isoformat()
            }
    
    def _calculate_summary_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics from batch results"""
        stats = {
            'average_scores': {},
            'score_distributions': {},
            'common_suggestions': {}
        }
        
        # Collect all scores by content type and dimension
        scores_by_type = {}
        suggestions_by_type = {}
        
        for result in results:
            if 'evaluations' in result:
                for content_type, evaluation in result['evaluations'].items():
                    if content_type not in scores_by_type:
                        scores_by_type[content_type] = {}
                        suggestions_by_type[content_type] = []
                    
                    # Collect scores for each dimension
                    for dimension, data in evaluation.items():
                        if isinstance(data, dict) and 'score' in data:
                            if dimension not in scores_by_type[content_type]:
                                scores_by_type[content_type][dimension] = []
                            scores_by_type[content_type][dimension].append(data['score'])
                    
                    # Collect suggestions
                    if 'improvement_suggestions' in evaluation:
                        suggestions_by_type[content_type].extend(evaluation['improvement_suggestions'])
        
        # Calculate averages
        for content_type, dimensions in scores_by_type.items():
            stats['average_scores'][content_type] = {}
            for dimension, scores in dimensions.items():
                if scores:
                    stats['average_scores'][content_type][dimension] = sum(scores) / len(scores)
        
        return stats

def main():
    """Main function for CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python llm_judge_refactored.py <test_cases_file>")
        sys.exit(1)
    
    test_cases_file = sys.argv[1]
    if not os.path.exists(test_cases_file):
        print(f"Error: Test cases file not found: {test_cases_file}")
        sys.exit(1)
    
    # Run evaluation
    judge = LLMJudge()
    results = judge.batch_evaluate(test_cases_file)
    
    # Save results
    output_file = f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Evaluation completed. Results saved to: {output_file}")
    print(f"📊 Evaluated {results.get('evaluated_cases', 0)} cases")

if __name__ == "__main__":
    main()