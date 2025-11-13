#!/usr/bin/env python3
"""
Content Quality Metrics for Aply Job Application Generator

Implements standard NLP metrics for evaluating generated text quality:
- BLEU scores for n-gram overlap
- ROUGE scores for summary quality
- Semantic similarity using embeddings
- Readability metrics
- Content coherence measures
"""

import re
import sys
import os
import json
import math
import statistics
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import Counter, defaultdict
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

class ContentQualityMetrics:
    """
    Implements various content quality metrics for evaluating generated text
    """
    
    def __init__(self):
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are', 
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall'
        }
    
    def calculate_bleu_score(self, candidate: str, reference: str, n_gram_weights: List[float] = [0.25, 0.25, 0.25, 0.25]) -> Dict[str, float]:
        """
        Calculate BLEU score between candidate and reference text
        
        Args:
            candidate: Generated text to evaluate
            reference: Reference text for comparison
            n_gram_weights: Weights for 1-gram, 2-gram, 3-gram, 4-gram
            
        Returns:
            Dictionary with BLEU scores and component metrics
        """
        
        # Tokenize and normalize
        candidate_tokens = self._tokenize(candidate.lower())
        reference_tokens = self._tokenize(reference.lower())
        
        if not candidate_tokens or not reference_tokens:
            return {
                'bleu_score': 0.0,
                'precision_scores': [0.0, 0.0, 0.0, 0.0],
                'brevity_penalty': 1.0,
                'length_ratio': 0.0
            }
        
        # Calculate n-gram precisions
        precision_scores = []
        
        for n in range(1, 5):  # 1-gram to 4-gram
            candidate_ngrams = self._get_ngrams(candidate_tokens, n)
            reference_ngrams = self._get_ngrams(reference_tokens, n)
            
            if not candidate_ngrams:
                precision_scores.append(0.0)
                continue
            
            # Count matches
            matches = 0
            reference_counts = Counter(reference_ngrams)
            
            for ngram in candidate_ngrams:
                if ngram in reference_counts and reference_counts[ngram] > 0:
                    matches += 1
                    reference_counts[ngram] -= 1
            
            precision = matches / len(candidate_ngrams)
            precision_scores.append(precision)
        
        # Calculate brevity penalty
        candidate_length = len(candidate_tokens)
        reference_length = len(reference_tokens)
        
        if candidate_length > reference_length:
            brevity_penalty = 1.0
        else:
            brevity_penalty = math.exp(1 - reference_length / candidate_length) if candidate_length > 0 else 0.0
        
        # Calculate geometric mean of precisions
        if all(p > 0 for p in precision_scores):
            geometric_mean = math.exp(sum(w * math.log(p) for w, p in zip(n_gram_weights, precision_scores)))
        else:
            geometric_mean = 0.0
        
        bleu_score = brevity_penalty * geometric_mean
        
        return {
            'bleu_score': bleu_score,
            'precision_scores': precision_scores,
            'brevity_penalty': brevity_penalty,
            'length_ratio': candidate_length / reference_length if reference_length > 0 else 0.0
        }
    
    def calculate_rouge_scores(self, candidate: str, reference: str) -> Dict[str, float]:
        """
        Calculate ROUGE-1, ROUGE-2, and ROUGE-L scores
        
        Args:
            candidate: Generated text to evaluate
            reference: Reference text for comparison
            
        Returns:
            Dictionary with ROUGE scores
        """
        
        candidate_tokens = self._tokenize(candidate.lower())
        reference_tokens = self._tokenize(reference.lower())
        
        if not candidate_tokens or not reference_tokens:
            return {
                'rouge_1_f1': 0.0,
                'rouge_1_precision': 0.0,
                'rouge_1_recall': 0.0,
                'rouge_2_f1': 0.0,
                'rouge_2_precision': 0.0,
                'rouge_2_recall': 0.0,
                'rouge_l_f1': 0.0,
                'rouge_l_precision': 0.0,
                'rouge_l_recall': 0.0
            }
        
        results = {}
        
        # ROUGE-1 (unigram overlap)
        rouge_1 = self._calculate_rouge_n(candidate_tokens, reference_tokens, 1)
        results.update({
            'rouge_1_f1': rouge_1['f1'],
            'rouge_1_precision': rouge_1['precision'],
            'rouge_1_recall': rouge_1['recall']
        })
        
        # ROUGE-2 (bigram overlap)
        rouge_2 = self._calculate_rouge_n(candidate_tokens, reference_tokens, 2)
        results.update({
            'rouge_2_f1': rouge_2['f1'],
            'rouge_2_precision': rouge_2['precision'],
            'rouge_2_recall': rouge_2['recall']
        })
        
        # ROUGE-L (longest common subsequence)
        rouge_l = self._calculate_rouge_l(candidate_tokens, reference_tokens)
        results.update({
            'rouge_l_f1': rouge_l['f1'],
            'rouge_l_precision': rouge_l['precision'],
            'rouge_l_recall': rouge_l['recall']
        })
        
        return results
    
    def calculate_readability_metrics(self, text: str) -> Dict[str, float]:
        """
        Calculate readability metrics for the text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with readability scores
        """
        
        if not text.strip():
            return {
                'flesch_kincaid_grade': 0.0,
                'flesch_reading_ease': 0.0,
                'avg_sentence_length': 0.0,
                'avg_syllables_per_word': 0.0,
                'total_sentences': 0,
                'total_words': 0
            }
        
        # Basic text analysis
        sentences = self._split_sentences(text)
        words = self._tokenize(text)
        
        total_sentences = len(sentences)
        total_words = len(words)
        
        if total_sentences == 0 or total_words == 0:
            return {
                'flesch_kincaid_grade': 0.0,
                'flesch_reading_ease': 0.0,
                'avg_sentence_length': 0.0,
                'avg_syllables_per_word': 0.0,
                'total_sentences': total_sentences,
                'total_words': total_words
            }
        
        # Calculate averages
        avg_sentence_length = total_words / total_sentences
        
        # Count syllables
        total_syllables = sum(self._count_syllables(word) for word in words)
        avg_syllables_per_word = total_syllables / total_words if total_words > 0 else 0
        
        # Flesch-Kincaid Grade Level
        flesch_kincaid_grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
        
        # Flesch Reading Ease
        flesch_reading_ease = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        
        return {
            'flesch_kincaid_grade': max(0, flesch_kincaid_grade),
            'flesch_reading_ease': max(0, min(100, flesch_reading_ease)),
            'avg_sentence_length': avg_sentence_length,
            'avg_syllables_per_word': avg_syllables_per_word,
            'total_sentences': total_sentences,
            'total_words': total_words
        }
    
    def calculate_semantic_coherence(self, text: str) -> Dict[str, float]:
        """
        Calculate semantic coherence metrics for the text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with coherence scores
        """
        
        sentences = self._split_sentences(text)
        
        if len(sentences) < 2:
            return {
                'lexical_cohesion': 0.0,
                'topic_consistency': 0.0,
                'transition_quality': 0.0,
                'semantic_coherence_score': 0.0
            }
        
        # Lexical cohesion - word overlap between sentences
        sentence_words = [set(self._tokenize(sent.lower())) - self.stopwords for sent in sentences]
        
        overlaps = []
        for i in range(len(sentence_words) - 1):
            if sentence_words[i] and sentence_words[i + 1]:
                overlap = len(sentence_words[i] & sentence_words[i + 1])
                total_unique = len(sentence_words[i] | sentence_words[i + 1])
                overlaps.append(overlap / total_unique if total_unique > 0 else 0)
        
        lexical_cohesion = statistics.mean(overlaps) if overlaps else 0.0
        
        # Topic consistency - consistency of professional/technical terms
        tech_terms = {'product', 'management', 'experience', 'team', 'project', 'business', 
                     'strategy', 'development', 'leadership', 'performance', 'results', 'growth'}
        
        tech_term_density = []
        for sent in sentences:
            sent_words = set(self._tokenize(sent.lower()))
            density = len(sent_words & tech_terms) / len(sent_words) if sent_words else 0
            tech_term_density.append(density)
        
        topic_consistency = 1.0 - (statistics.stdev(tech_term_density) if len(tech_term_density) > 1 else 0)
        
        # Transition quality - presence of connecting words
        transition_words = {'however', 'moreover', 'furthermore', 'additionally', 'consequently',
                           'therefore', 'meanwhile', 'subsequently', 'similarly', 'likewise',
                           'in contrast', 'on the other hand', 'as a result', 'for example'}
        
        transitions_found = 0
        for sent in sentences:
            sent_lower = sent.lower()
            if any(trans in sent_lower for trans in transition_words):
                transitions_found += 1
        
        transition_quality = transitions_found / (len(sentences) - 1) if len(sentences) > 1 else 0
        
        # Overall semantic coherence
        semantic_coherence_score = (lexical_cohesion + topic_consistency + transition_quality) / 3
        
        return {
            'lexical_cohesion': lexical_cohesion,
            'topic_consistency': topic_consistency,
            'transition_quality': transition_quality,
            'semantic_coherence_score': semantic_coherence_score
        }
    
    def calculate_professional_quality(self, text: str, text_type: str) -> Dict[str, float]:
        """
        Calculate professional quality metrics specific to job application content
        
        Args:
            text: Text to analyze
            text_type: Type of text (resume, cover_letter, linkedin)
            
        Returns:
            Dictionary with professional quality scores
        """
        
        metrics = {}
        
        # Professional vocabulary score
        professional_terms = {
            'achieved', 'accomplished', 'delivered', 'managed', 'led', 'developed',
            'implemented', 'optimized', 'improved', 'increased', 'reduced',
            'streamlined', 'enhanced', 'collaborated', 'coordinated', 'facilitated'
        }
        
        words = set(self._tokenize(text.lower()))
        prof_term_count = len(words & professional_terms)
        professional_vocab_score = min(1.0, prof_term_count / 10)  # Normalize to max 1.0
        
        # Quantification score - presence of metrics and numbers
        quantification_patterns = [
            r'\d+%',           # Percentages
            r'\$\d+[KMB]?',    # Money amounts
            r'\d+[KMB]\+?',    # Large numbers
            r'\d+ (days?|hours?|years?|months?)', # Time periods
            r'\d+x',           # Multipliers
            r'(\d+)-(\d+)'     # Ranges
        ]
        
        total_quantifications = 0
        for pattern in quantification_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            total_quantifications += len(matches)
        
        expected_quantifications = {'resume': 8, 'cover_letter': 3, 'linkedin': 2}
        expected = expected_quantifications.get(text_type, 5)
        quantification_score = min(1.0, total_quantifications / expected)
        
        # Action orientation score
        action_verbs = {
            'built', 'created', 'designed', 'launched', 'established', 'founded',
            'generated', 'produced', 'executed', 'completed', 'delivered',
            'transformed', 'revolutionized', 'pioneered', 'initiated'
        }
        
        action_count = len(words & action_verbs)
        expected_actions = {'resume': 6, 'cover_letter': 3, 'linkedin': 2}
        expected = expected_actions.get(text_type, 4)
        action_orientation_score = min(1.0, action_count / expected)
        
        # Technical relevance (for PM roles)
        tech_terms = {
            'ai', 'ml', 'machine learning', 'artificial intelligence', 'rag',
            'salesforce', 'sap', 'api', 'integration', 'automation',
            'agile', 'scrum', 'kanban', 'product management', 'stakeholder'
        }
        
        text_lower = text.lower()
        tech_mentions = sum(1 for term in tech_terms if term in text_lower)
        expected_tech = {'resume': 8, 'cover_letter': 4, 'linkedin': 3}
        expected = expected_tech.get(text_type, 5)
        technical_relevance_score = min(1.0, tech_mentions / expected)
        
        # Overall professional quality
        overall_score = (
            professional_vocab_score + 
            quantification_score + 
            action_orientation_score + 
            technical_relevance_score
        ) / 4
        
        return {
            'professional_vocab_score': professional_vocab_score,
            'quantification_score': quantification_score,
            'action_orientation_score': action_orientation_score,
            'technical_relevance_score': technical_relevance_score,
            'overall_professional_quality': overall_score
        }
    
    def evaluate_application_package(self, application_content: str, reference_content: str = None) -> Dict[str, Any]:
        """
        Comprehensive evaluation of an application package using multiple metrics
        
        Args:
            application_content: Generated application content
            reference_content: Optional reference content for comparison
            
        Returns:
            Comprehensive evaluation results
        """
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'content_length': len(application_content),
            'sections_evaluated': {},
            'overall_metrics': {}
        }
        
        # Extract individual sections
        sections = {
            'resume': self._extract_section(application_content, "## Resume", "## Cover Letter"),
            'cover_letter': self._extract_section(application_content, "## Cover Letter", "## LinkedIn Message"),
            'linkedin_message': self._extract_section(application_content, "## LinkedIn Message", "## Email Template")
        }
        
        # Evaluate each section
        for section_name, section_content in sections.items():
            if not section_content.strip():
                continue
                
            section_metrics = {}
            
            # Readability metrics
            section_metrics['readability'] = self.calculate_readability_metrics(section_content)
            
            # Semantic coherence
            section_metrics['coherence'] = self.calculate_semantic_coherence(section_content)
            
            # Professional quality
            section_metrics['professional_quality'] = self.calculate_professional_quality(
                section_content, section_name
            )
            
            # BLEU and ROUGE if reference provided
            if reference_content:
                ref_section = self._extract_section(reference_content, f"## {section_name.title()}", "##")
                if ref_section.strip():
                    section_metrics['bleu'] = self.calculate_bleu_score(section_content, ref_section)
                    section_metrics['rouge'] = self.calculate_rouge_scores(section_content, ref_section)
            
            results['sections_evaluated'][section_name] = section_metrics
        
        # Calculate overall metrics
        if results['sections_evaluated']:
            # Average readability across sections
            readability_scores = []
            coherence_scores = []
            professional_scores = []
            
            for section_metrics in results['sections_evaluated'].values():
                if 'readability' in section_metrics:
                    readability_scores.append(section_metrics['readability']['flesch_reading_ease'])
                if 'coherence' in section_metrics:
                    coherence_scores.append(section_metrics['coherence']['semantic_coherence_score'])
                if 'professional_quality' in section_metrics:
                    professional_scores.append(section_metrics['professional_quality']['overall_professional_quality'])
            
            results['overall_metrics'] = {
                'average_readability': statistics.mean(readability_scores) if readability_scores else 0,
                'average_coherence': statistics.mean(coherence_scores) if coherence_scores else 0,
                'average_professional_quality': statistics.mean(professional_scores) if professional_scores else 0
            }
            
            # Composite quality score
            composite_score = (
                results['overall_metrics']['average_readability'] / 100 * 0.2 +  # Normalize and weight
                results['overall_metrics']['average_coherence'] * 0.4 +
                results['overall_metrics']['average_professional_quality'] * 0.4
            )
            
            results['overall_metrics']['composite_quality_score'] = composite_score
        
        return results
    
    # Helper methods
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        return re.findall(r'\b\w+\b', text.lower())
    
    def _get_ngrams(self, tokens: List[str], n: int) -> List[Tuple[str, ...]]:
        """Generate n-grams from tokens"""
        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    
    def _calculate_rouge_n(self, candidate_tokens: List[str], reference_tokens: List[str], n: int) -> Dict[str, float]:
        """Calculate ROUGE-N scores"""
        candidate_ngrams = self._get_ngrams(candidate_tokens, n)
        reference_ngrams = self._get_ngrams(reference_tokens, n)
        
        if not candidate_ngrams or not reference_ngrams:
            return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
        
        candidate_counts = Counter(candidate_ngrams)
        reference_counts = Counter(reference_ngrams)
        
        # Calculate overlap
        overlap = sum((candidate_counts & reference_counts).values())
        
        precision = overlap / sum(candidate_counts.values()) if sum(candidate_counts.values()) > 0 else 0
        recall = overlap / sum(reference_counts.values()) if sum(reference_counts.values()) > 0 else 0
        
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        
        return {'precision': precision, 'recall': recall, 'f1': f1}
    
    def _calculate_rouge_l(self, candidate_tokens: List[str], reference_tokens: List[str]) -> Dict[str, float]:
        """Calculate ROUGE-L (longest common subsequence) scores"""
        def lcs_length(seq1, seq2):
            m, n = len(seq1), len(seq2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if seq1[i-1] == seq2[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            
            return dp[m][n]
        
        if not candidate_tokens or not reference_tokens:
            return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
        
        lcs_len = lcs_length(candidate_tokens, reference_tokens)
        
        precision = lcs_len / len(candidate_tokens)
        recall = lcs_len / len(reference_tokens)
        
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        
        return {'precision': precision, 'recall': recall, 'f1': f1}
    
    def _split_sentences(self, text: str) -> List[str]:
        """Simple sentence splitting"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count for a word"""
        word = word.lower()
        if not word:
            return 0
        
        # Remove non-alphabetic characters
        word = re.sub(r'[^a-z]', '', word)
        
        if not word:
            return 0
        
        # Basic syllable counting rules
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        # Every word has at least one syllable
        return max(1, syllable_count)
    
    def _extract_section(self, content: str, start_marker: str, end_marker: str) -> str:
        """Extract a specific section from content"""
        try:
            start_idx = content.find(start_marker)
            if start_idx == -1:
                return ""
            
            end_idx = content.find(end_marker, start_idx + len(start_marker))
            if end_idx == -1:
                return content[start_idx + len(start_marker):].strip()
            
            return content[start_idx + len(start_marker):end_idx].strip()
        except Exception:
            return ""

def main():
    """Command line interface for content metrics evaluation"""
    
    if len(sys.argv) < 2:
        print("Usage: python content_metrics.py <generated_content_file> [reference_content_file]")
        return
    
    content_file = sys.argv[1]
    reference_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        reference_content = None
        if reference_file:
            with open(reference_file, 'r', encoding='utf-8') as f:
                reference_content = f.read()
        
        metrics = ContentQualityMetrics()
        results = metrics.evaluate_application_package(content, reference_content)
        
        # Print summary
        print("📊 Content Quality Metrics Analysis")
        print("=" * 50)
        
        if 'overall_metrics' in results:
            overall = results['overall_metrics']
            print(f"🎯 Composite Quality Score: {overall.get('composite_quality_score', 0):.3f}")
            print(f"📖 Average Readability: {overall.get('average_readability', 0):.1f}")
            print(f"🔗 Average Coherence: {overall.get('average_coherence', 0):.3f}")
            print(f"💼 Professional Quality: {overall.get('average_professional_quality', 0):.3f}")
        
        print(f"\n📄 Sections Analyzed: {len(results['sections_evaluated'])}")
        
        for section, metrics_data in results['sections_evaluated'].items():
            print(f"\n{section.title()}:")
            if 'readability' in metrics_data:
                flesch = metrics_data['readability']['flesch_reading_ease']
                print(f"  📖 Readability: {flesch:.1f} (Flesch Reading Ease)")
            
            if 'professional_quality' in metrics_data:
                prof_qual = metrics_data['professional_quality']['overall_professional_quality']
                print(f"  💼 Professional Quality: {prof_qual:.3f}")
            
            if 'bleu' in metrics_data:
                bleu = metrics_data['bleu']['bleu_score']
                print(f"  🔍 BLEU Score: {bleu:.3f}")
        
        # Save detailed results
        output_file = f"content_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed results saved to: {output_file}")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()