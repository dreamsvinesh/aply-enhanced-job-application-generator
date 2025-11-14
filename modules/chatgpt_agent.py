#!/usr/bin/env python3
"""
ChatGPT Agent Module
Specialized OpenAI ChatGPT integration for dynamic content generation with strategic prompting
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path

try:
    from .llm_service import llm_service, LLMResponse
except ImportError:
    from llm_service import llm_service, LLMResponse

@dataclass
class ContentStrategy:
    """Strategic content approach based on JD analysis"""
    primary_focus: str  # "payments", "ai_ml", "enterprise_saas", "internal_tools"
    key_themes: List[str]  # Main themes to emphasize
    technical_depth: str  # "high", "medium", "low"
    experience_priorities: List[str]  # Which projects to emphasize
    tone_style: str  # "technical", "business", "hybrid"
    metrics_to_highlight: List[str]  # Key metrics to emphasize

class ChatGPTAgent:
    """ChatGPT-powered agent for strategic content generation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Verify OpenAI is available
        if not llm_service.openai_client:
            self.logger.warning("OpenAI client not available - some features will be limited")
        
        # Cost-optimized model selection
        self.content_model = "gpt-4o-mini"  # Cheapest, fastest for content generation
        self.analysis_model = "gpt-4o-mini"  # Good balance for analysis
        
    def analyze_jd_strategy(self, jd_data: Dict) -> ContentStrategy:
        """Analyze JD to determine optimal content strategy using ChatGPT"""
        
        prompt = f"""
        Analyze this job description and determine the optimal content strategy for a Product Manager application.
        
        Job Description:
        Title: {jd_data.get('job_title', 'N/A')}
        Company: {jd_data.get('company_name', 'N/A')}
        Description: {jd_data.get('job_description', '')[:2000]}
        Required Skills: {', '.join(jd_data.get('required_skills', []))}
        Preferred Skills: {', '.join(jd_data.get('preferred_skills', []))}
        
        Based on this JD, determine:
        1. PRIMARY_FOCUS: What is the main domain? Options: payments, ai_ml, enterprise_saas, internal_tools
        2. KEY_THEMES: 3-4 main themes/capabilities the role emphasizes
        3. TECHNICAL_DEPTH: How technical should the resume be? Options: high, medium, low
        4. EXPERIENCE_PRIORITIES: Which project areas to emphasize? Options: rag_system, contract_automation, converge_platform, space_optimization, mobile_platform, iot_platform
        5. TONE_STYLE: What tone works best? Options: technical, business, hybrid
        6. METRICS_TO_HIGHLIGHT: Which specific metrics would be most impactful?
        
        Respond in JSON format:
        {{
            "primary_focus": "payments|ai_ml|enterprise_saas|internal_tools",
            "key_themes": ["theme1", "theme2", "theme3"],
            "technical_depth": "high|medium|low", 
            "experience_priorities": ["priority1", "priority2", "priority3"],
            "tone_style": "technical|business|hybrid",
            "metrics_to_highlight": ["metric1", "metric2", "metric3"]
        }}
        """
        
        response = llm_service.call_openai(prompt, model=self.analysis_model, max_tokens=800)
        
        if response.success:
            try:
                strategy_data = json.loads(response.content.strip())
                return ContentStrategy(**strategy_data)
            except (json.JSONDecodeError, TypeError) as e:
                self.logger.error(f"Failed to parse strategy JSON: {e}")
        
        # Fallback strategy based on keywords
        return self._fallback_strategy_analysis(jd_data)
    
    def _fallback_strategy_analysis(self, jd_data: Dict) -> ContentStrategy:
        """Fallback strategy analysis using keyword detection"""
        
        jd_text = ' '.join([
            jd_data.get('job_description', ''),
            ' '.join(jd_data.get('required_skills', [])),
            ' '.join(jd_data.get('preferred_skills', []))
        ]).lower()
        
        # Determine primary focus
        if any(term in jd_text for term in ['payment', 'fintech', 'card', 'transaction', 'banking']):
            primary_focus = "payments"
            key_themes = ["Payment Systems", "Fintech Innovation", "Transaction Processing"]
            experience_priorities = ["contract_automation", "converge_platform", "space_optimization"]
        elif any(term in jd_text for term in ['ai', 'ml', 'artificial intelligence', 'machine learning']):
            primary_focus = "ai_ml"
            key_themes = ["AI/ML Systems", "Automation", "Data Intelligence"]
            experience_priorities = ["rag_system", "contract_automation", "mobile_platform"]
        elif any(term in jd_text for term in ['internal', 'operations', 'tools', 'workflow']):
            primary_focus = "internal_tools"
            key_themes = ["Operations Tools", "Workflow Automation", "Process Optimization"]
            experience_priorities = ["rag_system", "contract_automation", "space_optimization"]
        else:
            primary_focus = "enterprise_saas"
            key_themes = ["Enterprise SaaS", "Product Strategy", "Cross-functional Leadership"]
            experience_priorities = ["contract_automation", "converge_platform", "mobile_platform"]
        
        return ContentStrategy(
            primary_focus=primary_focus,
            key_themes=key_themes,
            technical_depth="medium",
            experience_priorities=experience_priorities,
            tone_style="hybrid",
            metrics_to_highlight=["94%", "$2M", "42 days to 10 minutes"]
        )
    
    def generate_strategic_summary(self, user_profile: Dict, strategy: ContentStrategy) -> str:
        """Generate strategically optimized summary using ChatGPT"""
        
        # Extract key user data
        original_summary = user_profile.get('summary', '')
        key_achievements = user_profile.get('key_achievements', [])
        
        prompt = f"""
        Rewrite this Product Manager summary to align perfectly with a {strategy.primary_focus} role.
        
        STRATEGY:
        - Focus: {strategy.primary_focus}
        - Key Themes: {', '.join(strategy.key_themes)}
        - Technical Depth: {strategy.technical_depth}
        - Tone: {strategy.tone_style}
        
        CURRENT SUMMARY:
        {original_summary}
        
        KEY ACHIEVEMENTS TO PRESERVE:
        {chr(10).join(key_achievements[:5])}
        
        REQUIREMENTS:
        1. Keep ALL quantified metrics (94%, $2M, 42 days→10 minutes, etc.)
        2. Emphasize {strategy.primary_focus} experience early
        3. Include themes: {', '.join(strategy.key_themes)}
        4. Maintain 11 years experience, 7 in PM
        5. Keep professional, quantified tone
        6. 3-4 sentences max
        7. Start with role + experience, end with expertise areas
        
        Generate the optimized summary:
        """
        
        response = llm_service.call_openai(prompt, model=self.content_model, max_tokens=600)
        
        if response.success and response.content:
            return response.content.strip()
        
        # Fallback to original if ChatGPT fails
        return original_summary
    
    def generate_strategic_experience_bullets(self, 
                                           role_data: Dict, 
                                           user_projects: Dict, 
                                           strategy: ContentStrategy) -> List[str]:
        """Generate strategically optimized experience bullets using ChatGPT"""
        
        # Get priority projects based on strategy
        priority_projects = self._get_priority_projects(user_projects, strategy)
        
        prompt = f"""
        Generate optimized experience bullets for this Product Manager role aligned with {strategy.primary_focus} focus.
        
        STRATEGY:
        - Focus: {strategy.primary_focus} 
        - Key Themes: {', '.join(strategy.key_themes)}
        - Technical Depth: {strategy.technical_depth}
        - Tone: {strategy.tone_style}
        
        ROLE INFO:
        Title: {role_data.get('title', '')}
        Company: {role_data.get('company', '')}
        Duration: {role_data.get('duration', '')}
        
        PRIORITY PROJECTS TO FEATURE:
        {json.dumps(priority_projects, indent=2)}
        
        EXISTING BULLETS (preserve metrics):
        {chr(10).join(role_data.get('highlights', [])[:4])}
        
        REQUIREMENTS:
        1. Generate 8 bullet points total
        2. Use Action-Impact-Measurement format: "Action verb + specific action + quantified impact"
        3. Preserve ALL existing metrics (94%, $2M, 42 days→10 minutes, etc.)
        4. Emphasize {strategy.primary_focus} technologies and outcomes
        5. Include cross-functional leadership where relevant
        6. Each bullet should be 1-2 lines, packed with value
        7. Start with most impressive achievements
        8. Use power verbs: Built, Automated, Led, Achieved, Generated, etc.
        
        Generate 8 optimized bullets:
        """
        
        response = llm_service.call_openai(prompt, model=self.content_model, max_tokens=1200)
        
        if response.success and response.content:
            # Parse bullets from response
            bullets = []
            for line in response.content.strip().split('\n'):
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    # Clean up bullet formatting
                    bullet = line.lstrip('- •0123456789. ')
                    if bullet:
                        bullets.append(bullet)
            
            if len(bullets) >= 6:  # Must have at least 6 good bullets
                return bullets[:8]
        
        # Fallback to existing bullets if ChatGPT fails
        return role_data.get('highlights', [])
    
    def _get_priority_projects(self, user_projects: Dict, strategy: ContentStrategy) -> Dict:
        """Extract priority projects based on strategy"""
        
        priority_projects = {}
        
        for priority in strategy.experience_priorities[:3]:  # Top 3 priorities
            if priority in user_projects:
                priority_projects[priority] = user_projects[priority]
        
        return priority_projects
    
    def generate_strategic_cover_letter(self, 
                                      jd_data: Dict, 
                                      user_profile: Dict, 
                                      strategy: ContentStrategy) -> str:
        """Generate strategically aligned cover letter using ChatGPT"""
        
        company_name = jd_data.get('company_name', 'the company')
        role_title = jd_data.get('job_title', 'Product Manager')
        
        prompt = f"""
        Write a compelling cover letter for this Product Manager application.
        
        JOB DETAILS:
        Company: {company_name}
        Role: {role_title}
        Key Requirements: {', '.join(jd_data.get('required_skills', [])[:5])}
        
        STRATEGY:
        - Focus: {strategy.primary_focus}
        - Key Themes: {', '.join(strategy.key_themes)}
        - Tone: {strategy.tone_style}
        
        CANDIDATE HIGHLIGHTS:
        - Built AI-powered RAG system achieving 94% accuracy serving 200+ users
        - Automated workflows reducing timelines from 42 days to 10 minutes, accelerating $2M revenue
        - Led cross-functional teams across 15+ operational processes
        - 11 years in technology, 7 years in Product Management
        
        REQUIREMENTS:
        1. Professional, enthusiastic tone
        2. 4-5 short paragraphs
        3. Specific connection to {strategy.primary_focus} experience
        4. Include 2-3 quantified achievements
        5. Show understanding of {company_name}'s needs
        6. Natural, human-written style (avoid AI patterns)
        7. End with clear next steps
        
        Generate the cover letter:
        """
        
        response = llm_service.call_openai(prompt, model=self.content_model, max_tokens=800)
        
        if response.success and response.content:
            return response.content.strip()
        
        # Fallback cover letter
        return f"""Hi there,

I'm excited to apply for the {role_title} role at {company_name}. Your focus on {strategy.key_themes[0] if strategy.key_themes else 'innovation'} aligns perfectly with my experience building products that deliver measurable business value.

What excites me about this opportunity is how my hands-on {strategy.primary_focus} experience matches what you're looking for. I've built AI-powered systems achieving 94% accuracy and automated workflows reducing timelines from 42 days to 10 minutes, accelerating $2M in revenue.

I'm particularly drawn to {company_name}'s approach to {strategy.key_themes[0] if strategy.key_themes else 'product innovation'}. My experience leading cross-functional teams and delivering quantified results would enable me to make an immediate impact on your product goals.

Thanks for considering my application. I'd love to discuss how my {strategy.primary_focus} experience can help drive {company_name}'s continued success.

Best regards,
{user_profile.get('personal_info', {}).get('name', 'Vinesh Kumar')}"""
    
    def generate_strategic_linkedin_message(self, 
                                          jd_data: Dict, 
                                          strategy: ContentStrategy) -> str:
        """Generate strategic LinkedIn outreach message using ChatGPT"""
        
        company_name = jd_data.get('company_name', 'your company')
        role_title = jd_data.get('job_title', 'Product Manager')
        
        prompt = f"""
        Write a personalized LinkedIn message for this Product Manager role.
        
        DETAILS:
        Company: {company_name}
        Role: {role_title}
        Focus: {strategy.primary_focus}
        
        CANDIDATE STRENGTHS:
        - Built AI-powered systems achieving 94% accuracy
        - Automated workflows saving 50+ hours daily  
        - {strategy.key_themes[0] if strategy.key_themes else 'Cross-functional leadership'} experience
        
        REQUIREMENTS:
        1. Under 300 characters for LinkedIn limits
        2. Professional but friendly tone
        3. Specific value proposition for {strategy.primary_focus}
        4. Include one quantified achievement
        5. End with question/call to action
        6. Avoid overly formal language
        
        Generate the LinkedIn message:
        """
        
        response = llm_service.call_openai(prompt, model=self.content_model, max_tokens=400)
        
        if response.success and response.content:
            message = response.content.strip()
            if len(message) <= 300:
                return message
        
        # Fallback message
        return f"Hi! Your {role_title} role at {company_name} caught my attention. I've built {strategy.primary_focus} products achieving 94% accuracy and love solving complex challenges. Think there might be a fit? Would love to chat!"
    
    def get_usage_summary(self) -> Dict:
        """Get ChatGPT-specific usage summary"""
        usage = llm_service.get_usage_report()
        
        chatgpt_usage = {
            'total_requests': 0,
            'total_cost': 0.0,
            'models_used': []
        }
        
        for model, stats in usage.get('by_model', {}).items():
            if 'gpt' in model.lower():
                chatgpt_usage['total_requests'] += stats.get('requests', 0)
                chatgpt_usage['total_cost'] += stats.get('cost', 0.0)
                if model not in chatgpt_usage['models_used']:
                    chatgpt_usage['models_used'].append(model)
        
        return chatgpt_usage

# Export the ChatGPT agent
__all__ = ['ChatGPTAgent', 'ContentStrategy']