#!/usr/bin/env python3
"""
Adlina Writing Style Guide
Central repository for consistent, non-generic resume writing style
"""

from typing import Dict, List, Any
import re

class AdlinaStyleGuide:
    """Maintains Adlina's writing style standards for all resume generation"""
    
    FORBIDDEN_GENERIC_WORDS = [
        "innovative", "transformative", "cutting-edge", "leveraged", "strategic",
        "comprehensive", "synergistic", "paradigm", "holistic", "dynamic",
        "robust", "seamless", "scalable", "optimal", "enterprise-grade",
        "best-in-class", "world-class", "industry-leading", "next-generation",
        "revolutionary", "groundbreaking", "disruptive", "game-changing"
    ]
    
    PREFERRED_ACTION_VERBS = [
        "Built", "Reduced", "Led", "Scaled", "Achieved", "Generated", 
        "Implemented", "Optimized", "Automated", "Improved", "Created",
        "Delivered", "Increased", "Decreased", "Developed", "Designed",
        "Launched", "Executed", "Managed", "Coordinated", "Analyzed"
    ]
    
    PROJECT_SEPARATION_RULES = {
        'ai_rag_project': {
            'keywords': ['RAG', 'AI-powered', '94% accuracy', 'sub-second response'],
            'achievements': ['94% accuracy with sub-second response times'],
            'no_mixing_with': ['F&B platform', 'GMV', 'daily orders', 'business parks']
        },
        'fnb_platform_project': {
            'keywords': ['F&B platform', 'business parks', 'daily orders', 'GMV', 'outlets'],
            'achievements': ['€20-22M annual GMV', '1,330 to 30,000+ daily orders', '24 business parks'],
            'no_mixing_with': ['RAG', '94% accuracy', 'sub-second response']
        },
        'contract_automation_project': {
            'keywords': ['contract activation', '42 days', '10 minutes'],
            'achievements': ['42 days to 10 minutes activation time'],
            'no_mixing_with': ['F&B platform', 'RAG system', '94% accuracy']
        },
        'salesforce_automation_project': {
            'keywords': ['Salesforce', 'SAP integration', 'invoicing', 'real-time processing'],
            'achievements': ['21 days to real-time invoicing', 'Salesforce-SAP integration', '35% contract accuracy improvement'],
            'no_mixing_with': ['F&B platform', 'RAG system', '94% accuracy']
        }
    }

    ADLINA_STYLE_REQUIREMENTS = {
        'summary': {
            'word_count': (70, 90),
            'required_elements': [
                'Years of experience (specific number)',
                'User scale (specific numbers like 600,000+)',
                'Key achievements with metrics',
                'Revenue/business impact with currency',
                'Specialized skills relevant to target role'
            ],
            'format': 'Senior Product Manager with X+ years scaling platforms serving Y+ users. Built/Led/Achieved specific metric while generating €X revenue through specific method. Specialized in relevant skills—reducing X from Y to Z and improving metric by N percentage points through data-driven approach across N locations/markets.',
            'forbidden_starts': [
                'Innovative product leader',
                'Experienced professional',
                'Results-driven manager',
                'Strategic thinker',
                'Dynamic leader'
            ],
            'required_starts': [
                'Senior Product Manager with',
                'Product Manager with',
                '[Role] with X+ years'
            ]
        },
        'bullets': {
            'word_count': (15, 30),
            'structure': 'Action verb + specific context + measurable outcome',
            'required_elements': [
                'Specific numbers/metrics',
                'Business impact',
                'Technology/method used',
                'Time frame (when relevant)'
            ],
            'examples': {
                'good': [
                    'Built AI RAG system achieving 94% accuracy and serving 200+ employees through intelligent automation',
                    'Reduced contract workflow from 42 days to 10 minutes, accelerating €2M revenue recognition',
                    'Led F&B platform scaling from 1,330 to 30,000+ daily orders generating €20-22M annual GMV'
                ],
                'bad': [
                    'Successfully leveraged cutting-edge AI technologies to optimize operational workflows',
                    'Effectively facilitated cross-functional collaboration to streamline business processes',
                    'Strategically implemented robust automation solutions to transform organizational paradigms'
                ]
            }
        },
        'metrics': {
            'integration_style': 'natural',  # Weave into context, not standalone
            'specificity': 'exact',  # Use exact numbers, not ranges when possible
            'currency_handling': 'target_country',  # Convert to target country currency
            'percentage_format': 'natural',  # "18 percentage points" not "18% increase"
        }
    }
    
    @classmethod
    def validate_summary(cls, summary: str) -> Dict[str, Any]:
        """Validate professional summary against Adlina style"""
        issues = []
        suggestions = []
        
        # Check for forbidden words
        summary_lower = summary.lower()
        forbidden_found = [word for word in cls.FORBIDDEN_GENERIC_WORDS 
                          if word.lower() in summary_lower]
        if forbidden_found:
            issues.append(f"Contains generic words: {', '.join(forbidden_found)}")
        
        # Check word count
        word_count = len(summary.split())
        min_words, max_words = cls.ADLINA_STYLE_REQUIREMENTS['summary']['word_count']
        if word_count < min_words:
            issues.append(f"Too short: {word_count} words (minimum {min_words})")
        elif word_count > max_words:
            suggestions.append(f"Consider shortening: {word_count} words (recommended max {max_words})")
        
        # Check for specific metrics
        has_years = bool(re.search(r'\d+\+?\s*years?', summary))
        has_users = bool(re.search(r'\d+[,\d]*\+?\s*(users?|employees?|people)', summary))
        has_currency = bool(re.search(r'[€$£¥]\d+', summary))
        has_percentage = bool(re.search(r'\d+%|\d+\s*percentage\s*points?', summary))
        
        if not has_years:
            issues.append("Missing years of experience")
        if not has_users:
            suggestions.append("Consider adding user scale metrics")
        if not has_currency:
            suggestions.append("Consider adding revenue/business impact")
        if not has_percentage:
            suggestions.append("Consider adding percentage improvements")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'suggestions': suggestions,
            'metrics_found': {
                'years_experience': has_years,
                'user_scale': has_users, 
                'revenue_impact': has_currency,
                'percentage_improvements': has_percentage
            }
        }
    
    @classmethod
    def validate_bullet(cls, bullet: str) -> Dict[str, Any]:
        """Validate bullet point against Adlina style"""
        issues = []
        suggestions = []
        
        # Remove bullet point marker
        bullet_clean = bullet.replace('•', '').replace('-', '').strip()
        
        # Check word count
        word_count = len(bullet_clean.split())
        min_words, max_words = cls.ADLINA_STYLE_REQUIREMENTS['bullets']['word_count']
        if word_count < min_words:
            issues.append(f"Too short: {word_count} words (minimum {min_words})")
        elif word_count > max_words:
            issues.append(f"Too long: {word_count} words (maximum {max_words})")
        
        # Check for action verb start
        first_word = bullet_clean.split()[0] if bullet_clean.split() else ""
        if first_word not in cls.PREFERRED_ACTION_VERBS:
            suggestions.append(f"Consider starting with action verb: {', '.join(cls.PREFERRED_ACTION_VERBS[:5])}")
        
        # Check for metrics
        has_metrics = bool(re.search(r'\d+[%xX]|\d+\+|\$\d+|€\d+|£\d+|\d+\s*(minutes?|days?|hours?|users?|percentage\s*points?)', bullet_clean))
        if not has_metrics:
            suggestions.append("Consider adding specific metrics")
        
        # Check for forbidden words
        bullet_lower = bullet_clean.lower()
        forbidden_found = [word for word in cls.FORBIDDEN_GENERIC_WORDS 
                          if word.lower() in bullet_lower]
        if forbidden_found:
            issues.append(f"Contains generic words: {', '.join(forbidden_found)}")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'suggestions': suggestions,
            'word_count': word_count,
            'has_metrics': has_metrics,
            'starts_with_action': first_word in cls.PREFERRED_ACTION_VERBS
        }
    
    @classmethod
    def generate_style_prompt(cls, role_context: str = "") -> str:
        """Generate prompt instructions for Adlina style"""
        return f"""
📝 ADLINA WRITING STYLE REQUIREMENTS - MANDATORY FOR ALL CONTENT:

🚫 FORBIDDEN WORDS (Never use):
{', '.join(cls.FORBIDDEN_GENERIC_WORDS)}

✅ PREFERRED ACTION VERBS (Start bullets with):
{', '.join(cls.PREFERRED_ACTION_VERBS)}

📊 SUMMARY REQUIREMENTS:
- Start with "Senior Product Manager with X+ years" or similar
- Include specific metrics: years, user scale, revenue, percentages
- 70-90 words total
- Natural metric integration (not standalone numbers)
{f"- Focus on skills relevant to {role_context}" if role_context else ""}

🎯 BULLET REQUIREMENTS:
- 15-30 words each
- Action verb + context + measurable outcome
- Specific numbers woven naturally into context
- Business impact clearly stated
- No generic corporate speak

💰 CURRENCY HANDLING:
- Use target country currency (€ for EU, $ for US, £ for UK)
- Convert Indian amounts appropriately
- Natural integration: "generating €20M revenue" not "revenue: €20M"

📈 METRICS FORMAT:
- "18 percentage points" not "18% increase"  
- "from 42 days to 10 minutes" not "reduced by 76%"
- "600,000+ users" not "large user base"
- Exact numbers preferred over ranges
"""
    
    @classmethod
    def create_adlina_summary_template(cls, years_exp: int, user_scale: str, revenue: str, 
                                     specialization: str, key_achievement: str) -> str:
        """Create Adlina-style summary template"""
        return f"Senior Product Manager with {years_exp}+ years scaling digital platforms serving {user_scale} users. {key_achievement} while generating {revenue} through {specialization}. Specialized in [relevant skills]—[specific improvement] and [another metric] through data-driven [approach/method] across [scale/locations]."
    
    @classmethod
    def suggest_improvements(cls, content: str) -> List[str]:
        """Suggest specific improvements for content"""
        suggestions = []
        
        # Check each line/bullet
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for line in lines:
            if line.startswith('•') or line.startswith('-'):
                validation = cls.validate_bullet(line)
                if not validation['is_valid']:
                    suggestions.extend([f"Bullet '{line[:30]}...': {issue}" for issue in validation['issues']])
            elif 'SUMMARY' in content and any(keyword in line.upper() for keyword in ['SUMMARY', 'PROFILE']):
                # Find summary content (next non-empty line)
                pass
        
        return suggestions
    
    @classmethod
    def check_project_mixing(cls, content: str) -> Dict[str, Any]:
        """Check if different projects are incorrectly mixed together in SAME SENTENCE"""
        issues = []
        
        # Split content into sentences for analysis
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            projects_in_sentence = []
            
            # Identify which projects are mentioned in this sentence
            for project_name, project_info in cls.PROJECT_SEPARATION_RULES.items():
                project_keywords = project_info['keywords']
                
                if any(keyword.lower() in sentence_lower for keyword in project_keywords):
                    projects_in_sentence.append(project_name)
            
            # Check if multiple projects are mixed in the same sentence
            if len(projects_in_sentence) > 1:
                # Check if their achievements are being combined
                for project in projects_in_sentence:
                    project_info = cls.PROJECT_SEPARATION_RULES[project]
                    no_mixing_keywords = project_info['no_mixing_with']
                    
                    mixed_in_sentence = [keyword for keyword in no_mixing_keywords 
                                       if keyword.lower() in sentence_lower]
                    
                    if mixed_in_sentence:
                        issues.append({
                            'sentence_number': i + 1,
                            'sentence': sentence,
                            'violation': f"Sentence {i+1} mixes {project.replace('_', ' ')} achievements with {', '.join(mixed_in_sentence)}"
                        })
        
        return {
            'has_mixing': len(issues) > 0,
            'violations': issues,
            'clean_projects': len(issues) == 0
        }

def main():
    """Demo Adlina style validation"""
    
    style_guide = AdlinaStyleGuide()
    
    # Test generic vs Adlina-style summaries
    generic_summary = "Innovative product leader with extensive experience in leveraging cutting-edge technologies to drive transformative business outcomes and optimize organizational performance."
    
    adlina_summary = "Senior Product Manager with 6+ years scaling digital platforms serving 600,000+ users. Built AI-powered RAG system achieving 94% accuracy with sub-second response times. Led F&B platform scaling across 24 business parks, generating €20-22M annual GMV from 1,330 to 30,000+ daily orders. Specialized in automation and enterprise integration—reducing contract activation from 42 days to 10 minutes and accelerating invoicing from 21 days to real-time through Salesforce-SAP integration."
    
    print("🤖 Generic Summary Validation:")
    generic_result = style_guide.validate_summary(generic_summary)
    print(f"Valid: {'✅' if generic_result['is_valid'] else '❌'}")
    print(f"Issues: {generic_result['issues']}")
    
    print("\n👤 Adlina-Style Summary Validation:")  
    adlina_result = style_guide.validate_summary(adlina_summary)
    print(f"Valid: {'✅' if adlina_result['is_valid'] else '❌'}")
    print(f"Suggestions: {adlina_result['suggestions']}")
    
    print(f"\n📝 Style Prompt:")
    print(style_guide.generate_style_prompt("Product Operations at HelloFresh"))
    
    # Test project mixing detection
    print(f"\n🔍 Project Mixing Detection:")
    mixed_content = "Built AI-powered RAG system achieving 94% accuracy while generating €20-22M annual GMV through F&B platform optimization."
    clean_content = "Built AI-powered RAG system achieving 94% accuracy with sub-second response times. Led F&B platform scaling generating €20-22M annual GMV."
    
    mixed_result = style_guide.check_project_mixing(mixed_content)
    clean_result = style_guide.check_project_mixing(clean_content)
    
    print(f"Mixed content violations: {'❌' if mixed_result['has_mixing'] else '✅'}")
    if mixed_result['violations']:
        for violation in mixed_result['violations']:
            print(f"  - {violation['violation']}")
    
    print(f"Clean content violations: {'❌' if clean_result['has_mixing'] else '✅'}")

if __name__ == "__main__":
    main()