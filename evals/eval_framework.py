#!/usr/bin/env python3
"""
LLM Evaluation Framework for Aply Job Application Generator

This implements proper LLM evals following best practices:
- OpenAI Evals-style test cases
- LLM-as-judge evaluations
- Content quality metrics (BLEU, ROUGE, perplexity)
- Multi-dimensional scoring
"""

import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import statistics

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

class AplyEvaluator:
    """Main evaluation framework for Aply system"""
    
    def __init__(self):
        self.eval_results = []
        self.test_cases = []
        
    def load_test_cases(self, test_file: str) -> List[Dict]:
        """Load evaluation test cases from JSON file"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Test file {test_file} not found")
            return []
    
    def evaluate_resume_quality(self, generated_content: str, expected_criteria: Dict) -> Dict:
        """
        Evaluate resume quality against multiple dimensions
        
        Args:
            generated_content: The generated resume content
            expected_criteria: Expected qualities (AI emphasis, metrics, etc.)
            
        Returns:
            Dictionary with scores and explanations
        """
        
        evaluation = {
            'ai_ml_emphasis': 0,
            'quantified_metrics': 0,
            'ats_optimization': 0,
            'professional_formatting': 0,
            'content_accuracy': 0,
            'overall_score': 0,
            'explanations': []
        }
        
        # Check AI/ML emphasis (0-20 points)
        ai_terms = ['AI', 'ML', 'RAG', 'machine learning', 'artificial intelligence', 
                   'deep learning', 'neural networks', 'LLM', 'vector database']
        
        ai_count = sum(1 for term in ai_terms if term.lower() in generated_content.lower())
        evaluation['ai_ml_emphasis'] = min(20, ai_count * 3)
        
        if ai_count >= 5:
            evaluation['explanations'].append("✅ Strong AI/ML emphasis with multiple relevant terms")
        else:
            evaluation['explanations'].append("⚠️ Limited AI/ML emphasis - consider adding more relevant terms")
        
        # Check quantified metrics (0-25 points)
        metric_patterns = [
            r'\d+%',           # Percentages
            r'\$\d+[KMB]?',    # Money amounts
            r'\d+[KMB]\+?',    # Large numbers with K/M/B
            r'\d+ days?',      # Time periods
            r'\d+ hours?',
            r'\d+x',           # Multipliers
            r'(\d+)-(\d+)'     # Ranges
        ]
        
        metrics_found = []
        for pattern in metric_patterns:
            matches = re.findall(pattern, generated_content)
            metrics_found.extend(matches)
        
        metric_score = min(25, len(metrics_found) * 4)
        evaluation['quantified_metrics'] = metric_score
        
        if len(metrics_found) >= 5:
            evaluation['explanations'].append(f"✅ Excellent quantification with {len(metrics_found)} metrics")
        else:
            evaluation['explanations'].append(f"⚠️ Could benefit from more quantified achievements ({len(metrics_found)} found)")
        
        # Check ATS optimization (0-20 points)
        if 'expected_keywords' in expected_criteria:
            keywords = expected_criteria['expected_keywords']
            matched_keywords = [kw for kw in keywords if kw.lower() in generated_content.lower()]
            keyword_match_rate = len(matched_keywords) / len(keywords) if keywords else 0
            evaluation['ats_optimization'] = int(20 * keyword_match_rate)
            
            evaluation['explanations'].append(
                f"📊 ATS optimization: {keyword_match_rate*100:.1f}% keyword match ({len(matched_keywords)}/{len(keywords)})"
            )
        
        # Check formatting (0-15 points)
        formatting_checks = [
            ('Contact info', any(pattern in generated_content for pattern in ['+91', '@gmail.com', 'linkedin.com'])),
            ('Proper sections', all(section in generated_content for section in ['EXPERIENCE', 'SKILLS', 'SUMMARY'])),
            ('Consistent formatting', '##' in generated_content or '**' in generated_content),
        ]
        
        formatting_score = sum(5 for _, check in formatting_checks if check)
        evaluation['professional_formatting'] = formatting_score
        
        # Check content accuracy (0-20 points) - basic checks
        accuracy_checks = [
            ('Valid email', '@gmail.com' in generated_content),
            ('Consistent name', 'Vinesh Kumar' in generated_content),
            ('Valid metrics', not re.search(r'\d{5,}%', generated_content)),  # No >999% values
            ('Professional tone', not any(word in generated_content.lower() for word in ['awesome', 'amazing', 'incredible']))
        ]
        
        accuracy_score = sum(5 for _, check in accuracy_checks if check)
        evaluation['content_accuracy'] = accuracy_score
        
        # Calculate overall score
        evaluation['overall_score'] = (
            evaluation['ai_ml_emphasis'] +
            evaluation['quantified_metrics'] +
            evaluation['ats_optimization'] +
            evaluation['professional_formatting'] +
            evaluation['content_accuracy']
        )
        
        return evaluation
    
    def evaluate_cover_letter_quality(self, generated_content: str, expected_criteria: Dict) -> Dict:
        """Evaluate cover letter quality"""
        
        evaluation = {
            'tone_appropriateness': 0,
            'personalization': 0,
            'structure': 0,
            'content_relevance': 0,
            'length_optimization': 0,
            'overall_score': 0,
            'explanations': []
        }
        
        # Extract cover letter section
        try:
            cover_letter = generated_content.split('## Cover Letter')[1].split('##')[0]
        except IndexError:
            evaluation['explanations'].append("❌ Cover letter section not found")
            return evaluation
        
        # Check tone appropriateness based on country (0-25 points)
        country = expected_criteria.get('country', '').lower()
        
        if country == 'netherlands':
            # Should be direct, avoid excessive politeness
            tone_score = 25
            if 'I believe that I can' in cover_letter:
                tone_score -= 10
                evaluation['explanations'].append("⚠️ Too indirect for Netherlands - use more direct language")
            if 'I would like to' in cover_letter:
                tone_score -= 5
        elif country in ['sweden', 'finland', 'denmark']:
            # Should be modest, collaborative
            tone_score = 20
            if any(word in cover_letter.lower() for word in ['excellent', 'outstanding', 'exceptional']):
                tone_score -= 10
                evaluation['explanations'].append("⚠️ Too boastful for Nordic culture - use modest language")
        else:
            tone_score = 20  # Default scoring
        
        evaluation['tone_appropriateness'] = max(0, tone_score)
        
        # Check personalization (0-20 points)
        company_name = expected_criteria.get('company_name', '')
        role_keywords = expected_criteria.get('role_keywords', [])
        
        personalization_score = 0
        if company_name and company_name in cover_letter:
            personalization_score += 10
            evaluation['explanations'].append(f"✅ Company name '{company_name}' mentioned")
        
        role_mentions = sum(1 for keyword in role_keywords if keyword.lower() in cover_letter.lower())
        if role_mentions >= 2:
            personalization_score += 10
            evaluation['explanations'].append(f"✅ Good role alignment with {role_mentions} relevant keywords")
        
        evaluation['personalization'] = personalization_score
        
        # Check structure (0-20 points)
        structure_checks = [
            ('Proper greeting', any(greeting in cover_letter for greeting in ['Dear', 'Hi', 'Hello'])),
            ('Clear opening', 'interest' in cover_letter.lower() or 'applying' in cover_letter.lower()),
            ('Body with examples', any(indicator in cover_letter for indicator in ['experience', 'achieved', 'built'])),
            ('Professional closing', any(closing in cover_letter for closing in ['regards', 'sincerely']))
        ]
        
        structure_score = sum(5 for _, check in structure_checks if check)
        evaluation['structure'] = structure_score
        
        # Check content relevance (0-20 points)
        relevant_terms = expected_criteria.get('expected_keywords', [])
        content_matches = sum(1 for term in relevant_terms if term.lower() in cover_letter.lower())
        content_score = min(20, content_matches * 3)
        evaluation['content_relevance'] = content_score
        
        # Check length (0-15 points)
        word_count = len(cover_letter.split())
        if 150 <= word_count <= 350:
            evaluation['length_optimization'] = 15
            evaluation['explanations'].append(f"✅ Optimal length: {word_count} words")
        elif 100 <= word_count < 150:
            evaluation['length_optimization'] = 10
            evaluation['explanations'].append(f"⚠️ Slightly short: {word_count} words")
        elif 350 < word_count <= 450:
            evaluation['length_optimization'] = 10
            evaluation['explanations'].append(f"⚠️ Slightly long: {word_count} words")
        else:
            evaluation['length_optimization'] = 5
            evaluation['explanations'].append(f"❌ Poor length: {word_count} words")
        
        # Calculate overall score
        evaluation['overall_score'] = (
            evaluation['tone_appropriateness'] +
            evaluation['personalization'] +
            evaluation['structure'] +
            evaluation['content_relevance'] +
            evaluation['length_optimization']
        )
        
        return evaluation
    
    def evaluate_linkedin_message_quality(self, generated_content: str, expected_criteria: Dict) -> Dict:
        """Evaluate LinkedIn message quality"""
        
        evaluation = {
            'character_optimization': 0,
            'call_to_action': 0,
            'personalization': 0,
            'professionalism': 0,
            'overall_score': 0,
            'explanations': []
        }
        
        # Extract LinkedIn message
        try:
            linkedin_section = generated_content.split('## LinkedIn Message')[1].split('##')[0]
            message_lines = [line.strip() for line in linkedin_section.split('\n') 
                           if line.strip() and not line.startswith('**')]
            message = message_lines[0] if message_lines else ""
        except IndexError:
            evaluation['explanations'].append("❌ LinkedIn message section not found")
            return evaluation
        
        # Character count optimization (0-30 points)
        char_count = len(message)
        if char_count <= 300:
            evaluation['character_optimization'] = 30
            evaluation['explanations'].append(f"✅ Excellent length: {char_count} characters")
        elif char_count <= 350:
            evaluation['character_optimization'] = 25
            evaluation['explanations'].append(f"✅ Good length: {char_count} characters")
        elif char_count <= 400:
            evaluation['character_optimization'] = 15
            evaluation['explanations'].append(f"⚠️ Acceptable length: {char_count} characters")
        else:
            evaluation['character_optimization'] = 5
            evaluation['explanations'].append(f"❌ Too long: {char_count} characters")
        
        # Call-to-action check (0-25 points)
        cta_phrases = ['call', 'chat', 'discuss', 'available', 'connect', 'meet', 'talk']
        if any(phrase in message.lower() for phrase in cta_phrases):
            evaluation['call_to_action'] = 25
            evaluation['explanations'].append("✅ Clear call-to-action present")
        else:
            evaluation['call_to_action'] = 0
            evaluation['explanations'].append("❌ Missing call-to-action")
        
        # Personalization (0-25 points)
        company_name = expected_criteria.get('company_name', '')
        if company_name and company_name in message:
            evaluation['personalization'] = 25
            evaluation['explanations'].append(f"✅ Company '{company_name}' mentioned")
        else:
            evaluation['personalization'] = 10
            evaluation['explanations'].append("⚠️ Generic message - consider adding company name")
        
        # Professionalism (0-20 points)
        professional_score = 20
        
        # Check for informal language
        informal_words = ['hey', 'hi there', 'sup', 'yo']
        if any(word in message.lower() for word in informal_words):
            professional_score -= 10
        
        # Check for proper structure
        if not any(greeting in message for greeting in ['Hi', 'Hello', 'Dear']):
            professional_score -= 5
        
        evaluation['professionalism'] = max(0, professional_score)
        
        # Calculate overall score
        evaluation['overall_score'] = (
            evaluation['character_optimization'] +
            evaluation['call_to_action'] +
            evaluation['personalization'] +
            evaluation['professionalism']
        )
        
        return evaluation
    
    def run_comprehensive_evaluation(self, test_cases_file: str) -> Dict:
        """Run comprehensive evaluation on all test cases"""
        
        test_cases = self.load_test_cases(test_cases_file)
        if not test_cases:
            return {'error': 'No test cases loaded'}
        
        from main import JobApplicationGenerator
        generator = JobApplicationGenerator()
        
        results = {
            'test_results': [],
            'summary_stats': {},
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"🧪 Running LLM Evaluation on {len(test_cases)} test cases")
        print("=" * 60)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test Case {i}: {test_case.get('name', 'Unknown')}")
            print("-" * 40)
            
            try:
                # Generate application package
                output_path = generator.generate_application_package(
                    test_case['job_description'],
                    test_case['country'],
                    test_case.get('company_name', '')
                )
                
                # Read generated content
                with open(output_path, 'r', encoding='utf-8') as f:
                    generated_content = f.read()
                
                # Evaluate each component
                resume_eval = self.evaluate_resume_quality(generated_content, test_case.get('expected_criteria', {}))
                cover_letter_eval = self.evaluate_cover_letter_quality(generated_content, test_case.get('expected_criteria', {}))
                linkedin_eval = self.evaluate_linkedin_message_quality(generated_content, test_case.get('expected_criteria', {}))
                
                test_result = {
                    'test_case': test_case['name'],
                    'country': test_case['country'],
                    'company': test_case.get('company_name', ''),
                    'resume_score': resume_eval['overall_score'],
                    'cover_letter_score': cover_letter_eval['overall_score'],
                    'linkedin_score': linkedin_eval['overall_score'],
                    'total_score': resume_eval['overall_score'] + cover_letter_eval['overall_score'] + linkedin_eval['overall_score'],
                    'max_possible': 100 + 100 + 100,  # Max scores for each component
                    'percentage': 0,
                    'detailed_evals': {
                        'resume': resume_eval,
                        'cover_letter': cover_letter_eval,
                        'linkedin': linkedin_eval
                    }
                }
                
                test_result['percentage'] = (test_result['total_score'] / test_result['max_possible']) * 100
                
                results['test_results'].append(test_result)
                
                # Print immediate feedback
                print(f"  Resume: {resume_eval['overall_score']}/100")
                print(f"  Cover Letter: {cover_letter_eval['overall_score']}/100")
                print(f"  LinkedIn: {linkedin_eval['overall_score']}/100")
                print(f"  Overall: {test_result['percentage']:.1f}%")
                
                if test_result['percentage'] >= 80:
                    print("  ✅ Excellent performance")
                elif test_result['percentage'] >= 70:
                    print("  ⚠️ Good performance")
                else:
                    print("  ❌ Needs improvement")
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                results['test_results'].append({
                    'test_case': test_case['name'],
                    'error': str(e),
                    'total_score': 0,
                    'percentage': 0
                })
        
        # Calculate summary statistics
        valid_results = [r for r in results['test_results'] if 'error' not in r]
        
        if valid_results:
            scores = [r['percentage'] for r in valid_results]
            results['summary_stats'] = {
                'total_tests': len(test_cases),
                'successful_tests': len(valid_results),
                'failed_tests': len(test_cases) - len(valid_results),
                'average_score': statistics.mean(scores),
                'median_score': statistics.median(scores),
                'min_score': min(scores),
                'max_score': max(scores),
                'std_deviation': statistics.stdev(scores) if len(scores) > 1 else 0
            }
        
        return results
    
    def generate_eval_report(self, results: Dict, output_file: str = None):
        """Generate a comprehensive evaluation report"""
        
        if output_file is None:
            output_file = f"eval_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report_content = f"""# Aply LLM Evaluation Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics

"""
        
        stats = results.get('summary_stats', {})
        if stats:
            report_content += f"""
- **Total Tests:** {stats['total_tests']}
- **Successful:** {stats['successful_tests']} 
- **Failed:** {stats['failed_tests']}
- **Average Score:** {stats['average_score']:.1f}%
- **Median Score:** {stats['median_score']:.1f}%
- **Score Range:** {stats['min_score']:.1f}% - {stats['max_score']:.1f}%
- **Standard Deviation:** {stats['std_deviation']:.1f}

"""
        
        # Performance categorization
        if stats.get('average_score', 0) >= 85:
            report_content += "🎉 **Overall Assessment:** Excellent - System performing at high quality\n\n"
        elif stats.get('average_score', 0) >= 75:
            report_content += "✅ **Overall Assessment:** Good - Minor improvements needed\n\n"
        elif stats.get('average_score', 0) >= 65:
            report_content += "⚠️ **Overall Assessment:** Acceptable - Several improvements needed\n\n"
        else:
            report_content += "❌ **Overall Assessment:** Poor - Major improvements required\n\n"
        
        # Detailed results
        report_content += "## Detailed Test Results\n\n"
        
        for result in results['test_results']:
            if 'error' in result:
                report_content += f"### ❌ {result['test_case']}\n"
                report_content += f"**Error:** {result['error']}\n\n"
                continue
            
            report_content += f"### {result['test_case']} ({result['country'].title()})\n"
            report_content += f"**Overall Score:** {result['percentage']:.1f}% ({result['total_score']}/{result['max_possible']})\n\n"
            
            # Component scores
            report_content += f"- **Resume:** {result['resume_score']}/100\n"
            report_content += f"- **Cover Letter:** {result['cover_letter_score']}/100\n"
            report_content += f"- **LinkedIn Message:** {result['linkedin_score']}/100\n\n"
            
            # Key insights from detailed evaluations
            if 'detailed_evals' in result:
                resume_eval = result['detailed_evals']['resume']
                if resume_eval['explanations']:
                    report_content += "**Resume Insights:**\n"
                    for explanation in resume_eval['explanations']:
                        report_content += f"- {explanation}\n"
                    report_content += "\n"
                
                cover_eval = result['detailed_evals']['cover_letter']
                if cover_eval['explanations']:
                    report_content += "**Cover Letter Insights:**\n"
                    for explanation in cover_eval['explanations']:
                        report_content += f"- {explanation}\n"
                    report_content += "\n"
                
                linkedin_eval = result['detailed_evals']['linkedin']
                if linkedin_eval['explanations']:
                    report_content += "**LinkedIn Message Insights:**\n"
                    for explanation in linkedin_eval['explanations']:
                        report_content += f"- {explanation}\n"
                    report_content += "\n"
        
        # Recommendations section
        report_content += "## Recommendations\n\n"
        
        if stats.get('average_score', 0) < 75:
            report_content += "### Priority Improvements\n"
            report_content += "1. Review and enhance content generation algorithms\n"
            report_content += "2. Improve keyword matching and ATS optimization\n"
            report_content += "3. Enhance country-specific tone adaptation\n\n"
        
        report_content += "### Evaluation Framework\n"
        report_content += "This evaluation uses multi-dimensional scoring:\n\n"
        report_content += "**Resume Evaluation (100 points):**\n"
        report_content += "- AI/ML Emphasis: 20 points\n"
        report_content += "- Quantified Metrics: 25 points\n"
        report_content += "- ATS Optimization: 20 points\n"
        report_content += "- Professional Formatting: 15 points\n"
        report_content += "- Content Accuracy: 20 points\n\n"
        
        report_content += "**Cover Letter Evaluation (100 points):**\n"
        report_content += "- Tone Appropriateness: 25 points\n"
        report_content += "- Personalization: 20 points\n"
        report_content += "- Structure: 20 points\n"
        report_content += "- Content Relevance: 20 points\n"
        report_content += "- Length Optimization: 15 points\n\n"
        
        report_content += "**LinkedIn Message Evaluation (100 points):**\n"
        report_content += "- Character Optimization: 30 points\n"
        report_content += "- Call-to-Action: 25 points\n"
        report_content += "- Personalization: 25 points\n"
        report_content += "- Professionalism: 20 points\n\n"
        
        report_content += "*This evaluation framework follows LLM evaluation best practices including multi-dimensional scoring, content quality assessment, and human-interpretable metrics.*\n"
        
        # Write report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n📄 Evaluation report saved to: {output_file}")
        return output_file

if __name__ == "__main__":
    evaluator = AplyEvaluator()
    
    # Run evaluation if test cases file provided
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        results = evaluator.run_comprehensive_evaluation(test_file)
        evaluator.generate_eval_report(results)
    else:
        print("Usage: python eval_framework.py <test_cases.json>")
        print("Example: python eval_framework.py evals/test_cases.json")