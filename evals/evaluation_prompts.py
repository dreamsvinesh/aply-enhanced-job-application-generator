#!/usr/bin/env python3
"""
Evaluation prompts for LLM-as-Judge assessment
Separated from main judge logic for maintainability
"""

from typing import Dict

class EvaluationPrompts:
    """Centralized evaluation prompts for different content types"""
    
    @staticmethod
    def get_resume_evaluation_prompt() -> str:
        """Resume evaluation prompt template"""
        return """
You are an expert HR professional and resume reviewer. Evaluate this resume for a {role} position in {country}.

RESUME TO EVALUATE:
{content}

EVALUATION CRITERIA:
Rate each dimension from 1-10 (10 = excellent, 1 = poor):

1. RELEVANCE TO ROLE: How well does the resume match the job requirements?
2. QUANTIFIED IMPACT: Are achievements presented with specific metrics and numbers?
3. PROFESSIONAL FORMATTING: Is the resume well-structured and professionally formatted?
4. SKILL ALIGNMENT: Do the highlighted skills match what's needed for this role?
5. CONTENT ACCURACY: Is the information presented believable and consistent?

COUNTRY-SPECIFIC CONSIDERATIONS for {country}:
- Netherlands: Direct, concise, results-focused
- Sweden/Finland/Denmark: Modest, collaborative, team-oriented
- Ireland: Warm but professional, relationship-focused
- Portugal: Formal, respectful, detailed

Respond in this exact JSON format:
{{
  "relevance_to_role": {{
    "score": [1-10],
    "reasoning": "Brief explanation"
  }},
  "quantified_impact": {{
    "score": [1-10], 
    "reasoning": "Brief explanation"
  }},
  "professional_formatting": {{
    "score": [1-10],
    "reasoning": "Brief explanation"
  }},
  "skill_alignment": {{
    "score": [1-10],
    "reasoning": "Brief explanation"
  }},
  "content_accuracy": {{
    "score": [1-10],
    "reasoning": "Brief explanation"
  }},
  "overall_assessment": "2-3 sentence summary",
  "improvement_suggestions": ["suggestion 1", "suggestion 2"]
}}
"""

    @staticmethod
    def get_cover_letter_evaluation_prompt() -> str:
        """Cover letter evaluation prompt template"""
        return """
You are an expert hiring manager evaluating cover letters. Review this cover letter for a {role} position at {company} in {country}.

COVER LETTER TO EVALUATE:
{content}

EVALUATION CRITERIA:
Rate each dimension from 1-10:

1. PERSONALIZATION: Is the letter tailored to the specific company and role?
2. TONE APPROPRIATENESS: Does the tone match cultural expectations for {country}?
3. COMPELLING NARRATIVE: Does it tell a coherent, engaging story?
4. SPECIFIC EXAMPLES: Are there concrete examples of relevant achievements?
5. PROFESSIONAL STRUCTURE: Proper greeting, body, and closing?

CULTURAL EXPECTATIONS for {country}:
- Netherlands: Direct, no-nonsense, focus on results
- Nordic countries: Modest, collaborative, avoid boasting
- Ireland: Warm, personable, relationship-focused
- Portugal: Formal, respectful, structured

Respond in JSON format:
{{
  "personalization": {{"score": [1-10], "reasoning": "explanation"}},
  "tone_appropriateness": {{"score": [1-10], "reasoning": "explanation"}},
  "compelling_narrative": {{"score": [1-10], "reasoning": "explanation"}},
  "specific_examples": {{"score": [1-10], "reasoning": "explanation"}},
  "professional_structure": {{"score": [1-10], "reasoning": "explanation"}},
  "overall_assessment": "summary",
  "improvement_suggestions": ["suggestion 1", "suggestion 2"]
}}
"""

    @staticmethod
    def get_linkedin_evaluation_prompt() -> str:
        """LinkedIn message evaluation prompt template"""
        return """
You are a recruiting expert evaluating LinkedIn outreach messages. Assess this message for effectiveness in {country}.

LINKEDIN MESSAGE TO EVALUATE:
{content}

EVALUATION CRITERIA:
Rate each dimension from 1-10:

1. BREVITY: Appropriate length (150-300 chars ideal)
2. PERSONALIZATION: References specific company/role details
3. PROFESSIONAL TONE: Appropriate formality for LinkedIn
4. CLEAR CTA: Has clear next steps/call to action
5. CULTURAL FIT: Appropriate for {country} business culture

Respond in JSON format:
{{
  "brevity": {{"score": [1-10], "reasoning": "explanation"}},
  "personalization": {{"score": [1-10], "reasoning": "explanation"}},
  "professional_tone": {{"score": [1-10], "reasoning": "explanation"}},
  "clear_cta": {{"score": [1-10], "reasoning": "explanation"}},
  "cultural_fit": {{"score": [1-10], "reasoning": "explanation"}},
  "overall_assessment": "summary",
  "improvement_suggestions": ["suggestion 1", "suggestion 2"]
}}
"""

    @staticmethod
    def get_holistic_evaluation_prompt() -> str:
        """Holistic application evaluation prompt template"""
        return """
You are a senior hiring manager reviewing a complete job application package. Evaluate the overall quality and coherence.

APPLICATION PACKAGE:
{content}

HOLISTIC EVALUATION CRITERIA:
Rate each dimension from 1-10:

1. CONSISTENCY: Are messaging, tone, and claims consistent across all components?
2. COMPLETENESS: Does the package address all key job requirements?
3. PROFESSIONAL QUALITY: Overall polish and presentation quality?
4. COMPELLING CASE: Does it make a persuasive argument for candidacy?
5. CULTURAL APPROPRIATENESS: Suitable for the target market?

Respond in JSON format:
{{
  "consistency": {{"score": [1-10], "reasoning": "explanation"}},
  "completeness": {{"score": [1-10], "reasoning": "explanation"}},
  "professional_quality": {{"score": [1-10], "reasoning": "explanation"}},
  "compelling_case": {{"score": [1-10], "reasoning": "explanation"}},
  "cultural_appropriateness": {{"score": [1-10], "reasoning": "explanation"}},
  "overall_assessment": "comprehensive summary",
  "improvement_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
}}
"""

    @staticmethod
    def get_all_prompts() -> Dict[str, str]:
        """Get all evaluation prompts as a dictionary"""
        return {
            "resume_quality": EvaluationPrompts.get_resume_evaluation_prompt(),
            "cover_letter_quality": EvaluationPrompts.get_cover_letter_evaluation_prompt(),
            "linkedin_message_quality": EvaluationPrompts.get_linkedin_evaluation_prompt(),
            "holistic_quality": EvaluationPrompts.get_holistic_evaluation_prompt()
        }