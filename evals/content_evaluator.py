#!/usr/bin/env python3
"""
Content evaluation logic for LLM-as-Judge assessment
Separated from prompts for better maintainability
"""

import json
import random
from typing import Dict, List, Any

class ContentEvaluator:
    """Handles the actual evaluation logic and simulation"""
    
    def __init__(self):
        pass
    
    def evaluate_resume_content(self, content: str, prompt: str) -> Dict[str, Any]:
        """Simulate resume content evaluation"""
        # Fast simulation of resume evaluation
        base_scores = {
            "relevance_to_role": random.randint(7, 9),
            "quantified_impact": random.randint(8, 10),
            "professional_formatting": random.randint(7, 9),
            "skill_alignment": random.randint(6, 8),
            "content_accuracy": random.randint(8, 9)
        }
        
        return {
            "relevance_to_role": {
                "score": base_scores["relevance_to_role"],
                "reasoning": "Resume shows strong alignment with product management requirements"
            },
            "quantified_impact": {
                "score": base_scores["quantified_impact"],
                "reasoning": "Excellent use of metrics (94% accuracy, $2M impact)"
            },
            "professional_formatting": {
                "score": base_scores["professional_formatting"],
                "reasoning": "Clean, well-structured format with clear sections"
            },
            "skill_alignment": {
                "score": base_scores["skill_alignment"],
                "reasoning": "Good technical skills, could emphasize product strategy more"
            },
            "content_accuracy": {
                "score": base_scores["content_accuracy"],
                "reasoning": "Information appears credible and consistent"
            },
            "overall_assessment": "Strong technical resume with excellent quantified results. Shows solid product management foundation with room for strategic emphasis.",
            "improvement_suggestions": [
                "Add more product strategy examples",
                "Include stakeholder management achievements",
                "Emphasize customer impact metrics"
            ]
        }
    
    def evaluate_cover_letter_content(self, content: str, prompt: str) -> Dict[str, Any]:
        """Simulate cover letter content evaluation"""
        base_scores = {
            "personalization": random.randint(7, 9),
            "tone_appropriateness": random.randint(6, 8),
            "compelling_narrative": random.randint(7, 9),
            "specific_examples": random.randint(8, 10),
            "professional_structure": random.randint(8, 9)
        }
        
        return {
            "personalization": {
                "score": base_scores["personalization"],
                "reasoning": "Letter references specific company and role requirements"
            },
            "tone_appropriateness": {
                "score": base_scores["tone_appropriateness"],
                "reasoning": "Professional tone suitable for the target market"
            },
            "compelling_narrative": {
                "score": base_scores["compelling_narrative"],
                "reasoning": "Clear progression from past experience to future value"
            },
            "specific_examples": {
                "score": base_scores["specific_examples"],
                "reasoning": "Concrete examples with measurable outcomes"
            },
            "professional_structure": {
                "score": base_scores["professional_structure"],
                "reasoning": "Well-structured with proper opening, body, and closing"
            },
            "overall_assessment": "Professional cover letter with good personalization and specific examples. Tone could be adjusted for cultural fit.",
            "improvement_suggestions": [
                "Adapt tone for cultural context",
                "Add more company-specific research",
                "Strengthen value proposition"
            ]
        }
    
    def evaluate_linkedin_content(self, content: str, prompt: str) -> Dict[str, Any]:
        """Simulate LinkedIn message evaluation"""
        char_count = len(content)
        base_scores = {
            "brevity": 9 if 150 <= char_count <= 300 else 6,
            "personalization": random.randint(7, 9),
            "professional_tone": random.randint(8, 9),
            "clear_cta": random.randint(7, 8),
            "cultural_fit": random.randint(6, 8)
        }
        
        return {
            "brevity": {
                "score": base_scores["brevity"],
                "reasoning": f"Message length ({char_count} chars) is {'optimal' if base_scores['brevity'] >= 8 else 'acceptable'}"
            },
            "personalization": {
                "score": base_scores["personalization"],
                "reasoning": "Good reference to specific role and company"
            },
            "professional_tone": {
                "score": base_scores["professional_tone"],
                "reasoning": "Appropriate LinkedIn professional tone"
            },
            "clear_cta": {
                "score": base_scores["clear_cta"],
                "reasoning": "Clear next steps provided"
            },
            "cultural_fit": {
                "score": base_scores["cultural_fit"],
                "reasoning": "Generally appropriate, could be more culturally specific"
            },
            "overall_assessment": "Solid LinkedIn message with good personalization. Length and tone are appropriate for the platform.",
            "improvement_suggestions": [
                "Add more cultural specificity",
                "Include specific value proposition",
                "Refine call-to-action"
            ]
        }
    
    def evaluate_holistic_content(self, content: str, prompt: str) -> Dict[str, Any]:
        """Simulate holistic application evaluation"""
        base_scores = {
            "consistency": random.randint(8, 9),
            "completeness": random.randint(7, 9),
            "professional_quality": random.randint(8, 10),
            "compelling_case": random.randint(7, 9),
            "cultural_appropriateness": random.randint(6, 8)
        }
        
        return {
            "consistency": {
                "score": base_scores["consistency"],
                "reasoning": "Messaging and tone are consistent across components"
            },
            "completeness": {
                "score": base_scores["completeness"],
                "reasoning": "Package addresses most key job requirements"
            },
            "professional_quality": {
                "score": base_scores["professional_quality"],
                "reasoning": "High-quality presentation and formatting"
            },
            "compelling_case": {
                "score": base_scores["compelling_case"],
                "reasoning": "Makes a solid case with quantified achievements"
            },
            "cultural_appropriateness": {
                "score": base_scores["cultural_appropriateness"],
                "reasoning": "Generally appropriate but could be more culturally tailored"
            },
            "overall_assessment": "Strong application package with consistent messaging and professional quality. Good use of metrics and specific examples. Cultural adaptation could be enhanced.",
            "improvement_suggestions": [
                "Enhance cultural adaptation for target market",
                "Strengthen value proposition alignment",
                "Add more strategic thinking examples"
            ]
        }
    
    def simulate_llm_evaluation(self, prompt: str, content_type: str) -> Dict[str, Any]:
        """Simulate LLM evaluation response based on content type"""
        if content_type == "resume":
            return self.evaluate_resume_content("", prompt)
        elif content_type == "cover_letter":
            return self.evaluate_cover_letter_content("", prompt)
        elif content_type == "linkedin":
            return self.evaluate_linkedin_content("", prompt)
        elif content_type == "holistic":
            return self.evaluate_holistic_content("", prompt)
        else:
            return {"error": f"Unknown content type: {content_type}"}
    
    def extract_section(self, content: str, start_marker: str, end_marker: str) -> str:
        """Extract a specific section from content"""
        try:
            start_idx = content.find(start_marker)
            if start_idx == -1:
                return ""
            
            start_idx += len(start_marker)
            
            if end_marker:
                end_idx = content.find(end_marker, start_idx)
                if end_idx == -1:
                    return content[start_idx:].strip()
                return content[start_idx:end_idx].strip()
            else:
                return content[start_idx:].strip()
                
        except Exception:
            return ""