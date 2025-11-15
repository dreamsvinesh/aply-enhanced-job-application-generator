#!/usr/bin/env python3
"""
Human Writing Style Validator
Ensures content sounds natural and human-written, not LLM-generated.
Uses Adlina's profile as reference for natural writing patterns.
"""

import re
from typing import Dict, List, Any, Tuple
from collections import Counter

class HumanWritingValidator:
    """Validates writing style to ensure natural, human-like content"""
    
    def __init__(self):
        # LLM detection patterns (things that sound artificial)
        self.llm_indicators = {
            'overused_power_words': [
                'leverage', 'utilize', 'facilitate', 'optimize', 'enhance', 'streamline',
                'revolutionize', 'transform', 'innovative', 'cutting-edge', 'synergy',
                'paradigm', 'seamless', 'robust', 'comprehensive', 'strategic',
                'dynamic', 'proactive', 'holistic', 'scalable', 'actionable'
            ],
            'formulaic_phrases': [
                'resulting in', 'leading to', 'thereby', 'furthermore', 'in addition to',
                'as a result of', 'in order to', 'with the goal of', 'aimed at',
                'focused on achieving', 'contributed to', 'played a key role in'
            ],
            'excessive_adjectives': [
                'significant', 'substantial', 'remarkable', 'exceptional', 'outstanding',
                'impressive', 'notable', 'considerable', 'tremendous', 'extensive',
                'comprehensive', 'thorough', 'meticulous', 'sophisticated'
            ],
            'generic_action_starters': [
                'successfully', 'effectively', 'efficiently', 'consistently',
                'strategically', 'systematically', 'comprehensively'
            ]
        }
        
        # Natural human writing patterns (based on Adlina's style)
        self.natural_patterns = {
            'direct_action_verbs': [
                'built', 'created', 'launched', 'developed', 'designed', 'implemented',
                'managed', 'led', 'delivered', 'achieved', 'reduced', 'increased',
                'generated', 'saved', 'improved', 'scaled', 'automated'
            ],
            'natural_connectors': [
                'and', 'while', 'through', 'by', 'via', 'across', 'with', 'for',
                'during', 'within', 'including', 'enabling'
            ],
            'business_outcomes': [
                'revenue', 'growth', 'efficiency', 'adoption', 'satisfaction',
                'conversion', 'engagement', 'retention', 'performance', 'impact'
            ],
            'natural_metrics_phrases': [
                'achieving X%', 'reducing X to Y', 'increasing X by Y%', 'from X to Y',
                'X% improvement', 'saving X hours', 'generating $X', 'serving X+ users'
            ]
        }
        
        # Sentence structure patterns that sound natural
        self.natural_structures = [
            r'^[A-Z][a-z]+ .+ \d+% .+',  # Action + outcome + metric
            r'^[A-Z][a-z]+ .+ from \d+ .+ to \d+ .+',  # Before/after metrics
            r'^[A-Z][a-z]+ .+ - .+ \d+% .+',  # Action - description + metric
            r'^[A-Z][a-z]+ .+ across \d+ .+',  # Scale indicators
            r'^[A-Z][a-z]+ .+ for \d+ .+',  # Scope indicators
        ]
        
        # Adlina-style writing characteristics
        self.adlina_style_markers = {
            'concise_bullets': True,  # Short, punchy bullet points
            'metrics_integrated': True,  # Numbers naturally woven in
            'action_focused': True,  # Starts with strong verbs
            'outcome_driven': True,  # Emphasizes results
            'technical_precise': True,  # Specific technical terms when relevant
            'business_context': True,  # Business impact clear
        }
    
    def validate_human_writing(self, content: str) -> Dict[str, Any]:
        """Validate content for human-like writing style"""
        
        validation_result = {
            'is_human_like': True,
            'human_score': 0,  # 0-100 scale
            'llm_indicators_found': [],
            'style_issues': [],
            'suggestions': [],
            'natural_patterns_found': [],
            'adlina_style_alignment': {}
        }
        
        # Check for LLM indicators
        llm_score = self._detect_llm_patterns(content, validation_result)
        
        # Check for natural patterns
        natural_score = self._detect_natural_patterns(content, validation_result)
        
        # Check Adlina style alignment
        adlina_score = self._check_adlina_style_alignment(content, validation_result)
        
        # Calculate overall human score
        validation_result['human_score'] = (natural_score + adlina_score - llm_score) / 2
        validation_result['human_score'] = max(0, min(100, validation_result['human_score']))
        
        # Determine if human-like (more reasonable threshold)
        validation_result['is_human_like'] = validation_result['human_score'] >= 60
        
        # Generate suggestions
        self._generate_humanization_suggestions(validation_result)
        
        return validation_result
    
    def _detect_llm_patterns(self, content: str, result: Dict[str, Any]) -> float:
        """Detect LLM-generated patterns (higher score = more LLM-like)"""
        
        llm_penalty_score = 0
        content_lower = content.lower()
        
        # Check for overused power words
        power_word_count = 0
        for word in self.llm_indicators['overused_power_words']:
            count = len(re.findall(r'\b' + word.lower() + r'\b', content_lower))
            power_word_count += count
            if count > 1:  # Multiple uses of same power word
                result['llm_indicators_found'].append(f"Overused power word: '{word}' ({count} times)")
                llm_penalty_score += count * 5
        
        # Check for formulaic phrases
        for phrase in self.llm_indicators['formulaic_phrases']:
            if phrase.lower() in content_lower:
                result['llm_indicators_found'].append(f"Formulaic phrase: '{phrase}'")
                llm_penalty_score += 10
        
        # Check for excessive adjectives
        adjective_count = 0
        for adj in self.llm_indicators['excessive_adjectives']:
            count = len(re.findall(r'\b' + adj.lower() + r'\b', content_lower))
            adjective_count += count
            if count > 0:
                result['llm_indicators_found'].append(f"Generic adjective: '{adj}'")
                llm_penalty_score += count * 3
        
        # Check for generic action starters
        sentences = re.split(r'[.!?]', content)
        for sentence in sentences:
            sentence = sentence.strip()
            for starter in self.llm_indicators['generic_action_starters']:
                if sentence.lower().startswith(starter.lower()):
                    result['llm_indicators_found'].append(f"Generic starter: '{starter}'")
                    llm_penalty_score += 8
        
        # Check sentence structure diversity
        sentence_starts = [sentence.strip().split()[0] if sentence.strip().split() else '' 
                          for sentence in sentences if sentence.strip()]
        
        if len(sentence_starts) > 3:
            start_variety = len(set(sentence_starts)) / len(sentence_starts)
            if start_variety < 0.6:  # Low variety indicates formulaic writing
                result['llm_indicators_found'].append("Low sentence starter variety")
                llm_penalty_score += 15
        
        return min(llm_penalty_score, 100)
    
    def _detect_natural_patterns(self, content: str, result: Dict[str, Any]) -> float:
        """Detect natural human writing patterns (higher score = more natural)"""
        
        natural_score = 0
        content_lower = content.lower()
        
        # Check for direct action verbs
        action_verb_count = 0
        for verb in self.natural_patterns['direct_action_verbs']:
            if verb.lower() in content_lower:
                action_verb_count += 1
                result['natural_patterns_found'].append(f"Natural action verb: '{verb}'")
                natural_score += 5
        
        # Check for natural connectors
        connector_count = 0
        for connector in self.natural_patterns['natural_connectors']:
            count = len(re.findall(r'\b' + connector.lower() + r'\b', content_lower))
            connector_count += count
            if count > 0:
                natural_score += count * 2
        
        # Check for business outcome focus
        outcome_count = 0
        for outcome in self.natural_patterns['business_outcomes']:
            if outcome.lower() in content_lower:
                outcome_count += 1
                result['natural_patterns_found'].append(f"Business outcome focus: '{outcome}'")
                natural_score += 3
        
        # Check for natural metrics integration
        metrics_patterns = [
            r'\d+%\s+\w+',  # "45% increase"
            r'from \d+.+ to \d+',  # "from 42 days to 10 minutes"
            r'\$\d+[kKmMbB]?\s+\w+',  # "$2M revenue"
            r'\d+→\d+',  # "500→125"
        ]
        
        natural_metrics = 0
        for pattern in metrics_patterns:
            matches = re.findall(pattern, content)
            natural_metrics += len(matches)
            if matches:
                result['natural_patterns_found'].append(f"Natural metrics: {len(matches)} instances")
                natural_score += len(matches) * 4
        
        # Check sentence structure variety
        sentences = [s.strip() for s in re.split(r'[.!?]', content) if s.strip()]
        if len(sentences) > 2:
            lengths = [len(s.split()) for s in sentences]
            length_variety = len(set(lengths)) / len(lengths) if lengths else 0
            if length_variety > 0.5:
                natural_score += 10
                result['natural_patterns_found'].append("Good sentence length variety")
        
        return min(natural_score, 100)
    
    def _check_adlina_style_alignment(self, content: str, result: Dict[str, Any]) -> float:
        """Check alignment with Adlina's natural writing style"""
        
        adlina_score = 0
        alignment = {}
        
        # Check for concise bullets (15-30 words per bullet)
        bullets = re.findall(r'•\s*(.+)', content)
        if bullets:
            bullet_lengths = [len(bullet.split()) for bullet in bullets]
            concise_bullets = sum(1 for length in bullet_lengths if 15 <= length <= 30)
            concise_ratio = concise_bullets / len(bullets) if bullets else 0
            alignment['concise_bullets'] = concise_ratio
            
            if concise_ratio >= 0.7:
                adlina_score += 20
                result['natural_patterns_found'].append("Adlina-style concise bullets")
            elif concise_ratio < 0.4:
                result['style_issues'].append("Bullets not concise (Adlina style)")
        
        # Check for metrics integration (numbers naturally woven in)
        metric_integration = len(re.findall(r'\w+\s+\d+%|\d+[xX]\s+\w+|\$\d+[kKmMbB]?\s+\w+', content))
        if metric_integration >= 3:
            alignment['metrics_integrated'] = True
            adlina_score += 15
            result['natural_patterns_found'].append("Natural metrics integration")
        else:
            alignment['metrics_integrated'] = False
            result['style_issues'].append("Metrics not naturally integrated")
        
        # Check for action-focused starts (focus on bullet points only)
        bullet_lines = [line.strip() for line in content.split('\n') if line.strip().startswith('•') and len(line.strip()) > 1]
        if bullet_lines:
            action_starts = sum(1 for line in bullet_lines 
                               if line.replace('•', '').strip().split()[0].lower() in self.natural_patterns['direct_action_verbs'] if line.replace('•', '').strip().split())
            action_ratio = action_starts / len(bullet_lines)
        else:
            action_ratio = 0
        alignment['action_focused'] = action_ratio
        
        if action_ratio >= 0.6:
            adlina_score += 20
            result['natural_patterns_found'].append("Strong action-focused writing")
        elif action_ratio < 0.3:
            result['style_issues'].append("Not enough action-focused sentences")
        
        # Check for outcome-driven content
        outcome_words = ['achieved', 'resulting', 'enabling', 'creating', 'generating', 'saving', 'improving']
        outcome_count = sum(1 for word in outcome_words if word in content.lower())
        alignment['outcome_driven'] = outcome_count >= 3
        
        if outcome_count >= 3:
            adlina_score += 15
        else:
            result['style_issues'].append("Needs more outcome-driven language")
        
        # Check for business context clarity
        business_terms = ['revenue', 'ROI', 'investment', 'efficiency', 'adoption', 'growth', 'impact']
        business_count = sum(1 for term in business_terms if term.lower() in content.lower())
        alignment['business_context'] = business_count >= 2
        
        if business_count >= 2:
            adlina_score += 10
        else:
            result['style_issues'].append("Needs clearer business context")
        
        result['adlina_style_alignment'] = alignment
        return min(adlina_score, 100)
    
    def _generate_humanization_suggestions(self, result: Dict[str, Any]) -> None:
        """Generate specific suggestions to make writing more human-like"""
        
        if result['human_score'] < 60:
            result['suggestions'].append("Overall writing needs humanization")
        
        # Address LLM indicators
        if 'Overused power word' in str(result['llm_indicators_found']):
            result['suggestions'].append("Replace overused power words with direct action verbs")
        
        if 'Formulaic phrase' in str(result['llm_indicators_found']):
            result['suggestions'].append("Replace formulaic phrases with natural connectors")
        
        if 'Generic adjective' in str(result['llm_indicators_found']):
            result['suggestions'].append("Remove excessive adjectives, focus on concrete actions and results")
        
        if 'Generic starter' in str(result['llm_indicators_found']):
            result['suggestions'].append("Start sentences with specific action verbs instead of adverbs")
        
        # Address style issues
        if 'Bullets not concise' in result['style_issues']:
            result['suggestions'].append("Make bullets more concise (15-30 words each)")
        
        if 'Metrics not naturally integrated' in result['style_issues']:
            result['suggestions'].append("Integrate numbers more naturally into sentences")
        
        if 'Not enough action-focused sentences' in result['style_issues']:
            result['suggestions'].append("Start more sentences with strong action verbs")
        
        if 'Needs more outcome-driven language' in result['style_issues']:
            result['suggestions'].append("Emphasize results and outcomes more clearly")
        
        if 'Needs clearer business context' in result['style_issues']:
            result['suggestions'].append("Include more business impact and context")
    
    def humanize_content(self, content: str, target_style: str = "adlina") -> str:
        """Automatically humanize content based on validation results"""
        
        validation = self.validate_human_writing(content)
        
        if validation['human_score'] >= 80:
            return content  # Already human-like enough
        
        humanized = content
        
        # Replace overused power words
        for word in self.llm_indicators['overused_power_words']:
            if humanized.count(word) > 1:
                # Replace with more natural alternatives
                natural_replacements = {
                    'leverage': 'use',
                    'utilize': 'use', 
                    'facilitate': 'enable',
                    'optimize': 'improve',
                    'enhance': 'improve',
                    'streamline': 'simplify'
                }
                if word in natural_replacements:
                    humanized = humanized.replace(word, natural_replacements[word], 1)
        
        # Replace formulaic phrases
        for phrase in self.llm_indicators['formulaic_phrases']:
            natural_replacements = {
                'resulting in': 'creating',
                'leading to': 'enabling',
                'thereby': 'and',
                'in order to': 'to'
            }
            if phrase in humanized and phrase in natural_replacements:
                humanized = humanized.replace(phrase, natural_replacements[phrase])
        
        return humanized

def main():
    """Demo human writing validation"""
    print("✍️ HUMAN WRITING STYLE VALIDATOR DEMO")
    print("=" * 55)
    
    # Sample LLM-like content
    llm_content = """
• Successfully leveraged cutting-edge AI technologies to optimize and enhance operational workflows, resulting in significant improvements to efficiency metrics
• Effectively facilitated cross-functional collaboration aimed at streamlining comprehensive business processes, thereby achieving substantial revenue optimization
• Strategically implemented robust automation solutions in order to transform organizational paradigms and revolutionize operational excellence
"""
    
    # Sample human-like content (Adlina style)
    human_content = """
• Built AI RAG system achieving 94% accuracy and serving 200+ employees through intelligent automation
• Automated contract workflow reducing timeline from 42 days to 10 minutes, accelerating $2M revenue recognition
• Led automation rollout across 5 departments with 100% adoption in 2 weeks, boosting team efficiency
"""
    
    validator = HumanWritingValidator()
    
    print("🤖 Testing LLM-like content:")
    llm_result = validator.validate_human_writing(llm_content)
    print(f"Human Score: {llm_result['human_score']:.1f}/100")
    print(f"Is Human-like: {'✅' if llm_result['is_human_like'] else '❌'}")
    print(f"LLM Indicators: {len(llm_result['llm_indicators_found'])}")
    
    print("\n👤 Testing Human-like content:")
    human_result = validator.validate_human_writing(human_content)
    print(f"Human Score: {human_result['human_score']:.1f}/100")
    print(f"Is Human-like: {'✅' if human_result['is_human_like'] else '❌'}")
    print(f"Natural Patterns: {len(human_result['natural_patterns_found'])}")
    
    print("\n🔧 Humanizing LLM content:")
    humanized = validator.humanize_content(llm_content)
    print("Original:", llm_content[:100] + "...")
    print("Humanized:", humanized[:100] + "...")
    
    print("\n✅ Human writing validation demo complete!")

if __name__ == "__main__":
    main()