#!/usr/bin/env python3
"""
Dynamic Summary Generator
ChatGPT-powered summary rewriting based on job description analysis and content strategy
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path

try:
    from .content_strategy_engine import ContentStrategyEngine, ApplicationStrategy
    from .chatgpt_agent import ChatGPTAgent, ContentStrategy
    from .llm_service import llm_service, LLMResponse
except ImportError:
    from content_strategy_engine import ContentStrategyEngine, ApplicationStrategy
    from chatgpt_agent import ChatGPTAgent, ContentStrategy
    from llm_service import llm_service, LLMResponse

@dataclass
class SummaryVariant:
    """Different summary variants for testing"""
    variant_type: str  # "technical", "business", "leadership", "hybrid"
    summary_text: str
    focus_areas: List[str]
    tone_style: str
    target_audience: str

class DynamicSummaryGenerator:
    """Advanced summary generator using strategic AI-powered rewriting"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.strategy_engine = ContentStrategyEngine()
        self.chatgpt_agent = ChatGPTAgent()
        
        # Load user profile
        self.load_user_profile()
        
        # Generation models - cost optimized
        self.summary_model = "gpt-4o-mini"  # Cheapest for content generation
        self.optimization_model = "gpt-4o-mini"
        
        # Core metrics that must be preserved in all variants
        self.core_metrics = [
            "11 years in technology (7 in PM)",
            "94% accuracy",
            "200+ users",
            "$2M revenue",
            "42 days to 10 minutes",
            "50+ resource hours daily"
        ]
    
    def load_user_profile(self):
        """Load user profile data"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.user_profile = json.load(f)
    
    def generate_strategic_summary(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate strategically optimized summary based on application strategy"""
        
        # Get original summary as foundation
        original_summary = self.user_profile.get('summary', '')
        
        # Build strategic context
        strategy_context = {
            "value_proposition": application_strategy.value_proposition,
            "differentiation": application_strategy.differentiation_angle,
            "focus_areas": application_strategy.summary_focus_areas,
            "content_themes": application_strategy.content_themes,
            "competitive_advantages": application_strategy.competitive_advantages
        }
        
        # Generate optimized summary
        optimized_summary = self._generate_optimized_summary(
            jd_data, original_summary, strategy_context
        )
        
        # Validate and refine
        return self._validate_and_refine_summary(optimized_summary, original_summary)
    
    def _generate_optimized_summary(self, jd_data: Dict, original_summary: str, strategy_context: Dict) -> str:
        """Generate strategically optimized summary using ChatGPT"""
        
        company_name = jd_data.get('company_name', 'the company')
        industry_focus = strategy_context.get('differentiation', 'automation_expert')
        
        prompt = f"""
        Rewrite this Product Manager summary to optimally position for this specific role.
        
        TARGET ROLE:
        Company: {company_name}
        Job Title: {jd_data.get('job_title', 'Product Manager')}
        Industry Focus: {jd_data.get('industry', 'technology')}
        Key Requirements: {', '.join(jd_data.get('required_skills', [])[:5])}
        
        STRATEGIC POSITIONING:
        - Value Proposition: {strategy_context.get('value_proposition', '')}
        - Differentiation Angle: {strategy_context.get('differentiation', '')}
        - Focus Areas: {', '.join(strategy_context.get('focus_areas', []))}
        - Competitive Advantages: {', '.join(strategy_context.get('competitive_advantages', []))}
        
        ORIGINAL SUMMARY:
        {original_summary}
        
        CRITICAL REQUIREMENTS:
        1. PRESERVE ALL METRICS: 11 years experience, 94% accuracy, $2M revenue, 42 days→10 minutes, 50+ hours saved
        2. LEAD WITH DIFFERENTIATION: Start with unique value for this specific role
        3. INDUSTRY ALIGNMENT: Tailor language to {industry_focus} context
        4. QUANTIFIED IMPACT: Emphasize measurable business outcomes
        5. LENGTH: 3-4 sentences maximum
        6. TONE: Professional, confident, results-focused
        7. FLOW: Experience → Specialization → Key Achievements → Expertise Areas
        
        Generate the optimized summary:
        """
        
        response = llm_service.call_openai(prompt, model=self.summary_model, max_tokens=600)
        
        if response.success and response.content:
            return response.content.strip()
        
        # Fallback to strategic enhancement of original
        return self._enhance_original_summary(original_summary, strategy_context)
    
    def _enhance_original_summary(self, original_summary: str, strategy_context: Dict) -> str:
        """Fallback enhancement of original summary"""
        
        differentiation = strategy_context.get('differentiation', 'automation_expert')
        
        if differentiation == 'ai_innovator':
            return original_summary.replace(
                "Senior Product Manager with 11 years in technology",
                "Senior Product Manager with 11 years in technology (7 in PM) specializing in AI/ML systems, RAG architecture, and intelligent automation"
            )
        elif differentiation == 'automation_expert':
            return original_summary.replace(
                "automation across B2B SaaS platforms",
                "automation across enterprise platforms with proven track record of 99.6% process improvement"
            )
        elif differentiation == 'growth_driver':
            return original_summary.replace(
                "serving 200+ users",
                "serving 200+ users while driving $2M+ revenue acceleration and 50+ hour daily savings"
            )
        
        return original_summary
    
    def _validate_and_refine_summary(self, optimized_summary: str, original_summary: str) -> str:
        """Validate that all critical metrics are preserved"""
        
        # Check for metric preservation
        missing_metrics = []
        for metric in self.core_metrics:
            if metric not in optimized_summary and metric in original_summary:
                missing_metrics.append(metric)
        
        # If metrics are missing, merge them back
        if missing_metrics:
            self.logger.warning(f"Restoring missing metrics: {missing_metrics}")
            return self._merge_missing_metrics(optimized_summary, missing_metrics)
        
        return optimized_summary
    
    def _merge_missing_metrics(self, summary: str, missing_metrics: List[str]) -> str:
        """Merge missing metrics back into summary"""
        
        # For critical metrics, ensure they're included
        enhanced_summary = summary
        
        if "11 years" in missing_metrics[0] if missing_metrics else False:
            enhanced_summary = enhanced_summary.replace(
                "Senior Product Manager",
                "Senior Product Manager with 11 years in technology (7 in PM)"
            )
        
        if any("94%" in metric for metric in missing_metrics):
            if "94%" not in enhanced_summary:
                enhanced_summary = enhanced_summary.replace(
                    "Built AI",
                    "Built AI-powered systems achieving 94% accuracy"
                )
        
        if any("$2M" in metric for metric in missing_metrics):
            if "$2M" not in enhanced_summary:
                enhanced_summary = enhanced_summary.replace(
                    "revenue",
                    "$2M revenue"
                )
        
        return enhanced_summary
    
    def generate_summary_variants(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> List[SummaryVariant]:
        """Generate multiple summary variants for A/B testing"""
        
        variants = []
        
        # Variant 1: Technical Focus
        technical_variant = self._generate_technical_variant(jd_data, application_strategy)
        variants.append(SummaryVariant(
            variant_type="technical",
            summary_text=technical_variant,
            focus_areas=["Technical Implementation", "System Architecture", "AI/ML"],
            tone_style="technical",
            target_audience="Engineering Teams"
        ))
        
        # Variant 2: Business Impact Focus
        business_variant = self._generate_business_variant(jd_data, application_strategy)
        variants.append(SummaryVariant(
            variant_type="business",
            summary_text=business_variant,
            focus_areas=["Revenue Growth", "Business Impact", "ROI"],
            tone_style="business",
            target_audience="Business Stakeholders"
        ))
        
        # Variant 3: Leadership Focus
        leadership_variant = self._generate_leadership_variant(jd_data, application_strategy)
        variants.append(SummaryVariant(
            variant_type="leadership",
            summary_text=leadership_variant,
            focus_areas=["Cross-functional Leadership", "Team Building", "Strategy"],
            tone_style="leadership",
            target_audience="Senior Management"
        ))
        
        # Variant 4: Hybrid (Default Strategic)
        hybrid_variant = self.generate_strategic_summary(jd_data, application_strategy)
        variants.append(SummaryVariant(
            variant_type="hybrid",
            summary_text=hybrid_variant,
            focus_areas=application_strategy.content_themes,
            tone_style="professional",
            target_audience="All Stakeholders"
        ))
        
        return variants
    
    def _generate_technical_variant(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate technically focused summary variant"""
        
        prompt = f"""
        Create a technically focused Product Manager summary for this role.
        
        ROLE CONTEXT:
        - {jd_data.get('job_title', 'Product Manager')} at {jd_data.get('company_name', 'target company')}
        - Technical requirements: {', '.join(jd_data.get('required_skills', [])[:5])}
        
        CANDIDATE TECHNICAL ACHIEVEMENTS:
        - Built AI-powered RAG knowledge system using pgvector achieving 94% accuracy
        - Automated Salesforce-SAP-MuleSoft integration reducing timeline 99.6%
        - Implemented IoT-enabled self-service platform with auto WiFi systems
        - Developed complex API integrations across 15+ operational processes
        
        REQUIREMENTS:
        1. Technical depth and implementation details
        2. Preserve all metrics: 94%, $2M, 42 days→10 minutes, 50+ hours
        3. Emphasize system architecture and technical leadership
        4. 3-4 sentences max
        5. Professional technical tone
        
        Generate technical summary:
        """
        
        response = llm_service.call_openai(prompt, model=self.summary_model, max_tokens=500)
        
        if response.success:
            return response.content.strip()
        
        # Fallback technical summary
        return "Senior Product Manager with 11 years in technology (7 in PM) specializing in AI/ML systems, RAG architecture, and complex enterprise integrations. Built AI-powered knowledge system achieving 94% accuracy using pgvector, automated Salesforce-SAP workflows reducing timelines from 42 days to 10 minutes (accelerating $2M revenue), and orchestrated 15+ technical process integrations saving 50+ resource hours daily. Expert in API architecture, database optimization, and cross-functional technical leadership."
    
    def _generate_business_variant(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate business impact focused summary variant"""
        
        prompt = f"""
        Create a business-impact focused Product Manager summary for this role.
        
        ROLE CONTEXT:
        - {jd_data.get('job_title', 'Product Manager')} at {jd_data.get('company_name', 'target company')}
        - Business focus: Revenue growth, operational efficiency, customer value
        
        CANDIDATE BUSINESS ACHIEVEMENTS:
        - Accelerated $2M revenue recognition through process automation
        - Generated €220K monthly revenue from space optimization
        - Achieved ₹180 crores annual GMV with 91% NPS on platform
        - Saved 50+ resource hours daily through workflow optimization
        
        REQUIREMENTS:
        1. Business impact and ROI focus
        2. Preserve all metrics: $2M, €220K, ₹180 crores, 50+ hours
        3. Emphasize revenue growth and operational efficiency
        4. 3-4 sentences max
        5. Business-oriented professional tone
        
        Generate business summary:
        """
        
        response = llm_service.call_openai(prompt, model=self.summary_model, max_tokens=500)
        
        if response.success:
            return response.content.strip()
        
        # Fallback business summary
        return "Senior Product Manager with 11 years driving technology-enabled business growth (7 years in PM) across enterprise SaaS and automation platforms. Delivered quantified business impact including $2M revenue acceleration, €220K monthly recurring revenue generation, and 50+ resource hours daily savings through strategic process optimization. Led product initiatives achieving ₹180 crores annual GMV with 91% NPS while reducing operational timelines by 99.6% (42 days to 10 minutes). Expert in revenue optimization, cross-functional execution, and scaling products for measurable business outcomes."
    
    def _generate_leadership_variant(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> str:
        """Generate leadership focused summary variant"""
        
        prompt = f"""
        Create a leadership-focused Product Manager summary for this role.
        
        ROLE CONTEXT:
        - {jd_data.get('job_title', 'Product Manager')} at {jd_data.get('company_name', 'target company')}
        - Leadership aspects: Team building, cross-functional collaboration, strategic vision
        
        CANDIDATE LEADERSHIP ACHIEVEMENTS:
        - Orchestrated cross-functional automation initiatives across 15+ operational processes
        - Led end-to-end product strategy for platform serving 600,000+ users
        - Scaled teams and processes from MVP to full production in 6 months
        - Built and managed relationships across Engineering, Sales, Operations teams
        
        REQUIREMENTS:
        1. Leadership and team collaboration focus
        2. Preserve key metrics: 600K+ users, 15+ processes, 6 months scaling
        3. Emphasize strategic vision and cross-functional execution
        4. 3-4 sentences max
        5. Leadership-oriented professional tone
        
        Generate leadership summary:
        """
        
        response = llm_service.call_openai(prompt, model=self.summary_model, max_tokens=500)
        
        if response.success:
            return response.content.strip()
        
        # Fallback leadership summary
        return "Senior Product Manager with 11 years in technology leadership (7 in PM) specializing in cross-functional team orchestration and strategic product execution. Led end-to-end product strategy for platform serving 600,000+ users, scaled MVP to full production in 6 months achieving 91% NPS, and orchestrated automation initiatives across 15+ operational processes with multiple engineering and business teams. Delivered proven leadership results including $2M revenue acceleration and 50+ resource hours daily savings through strategic cross-functional collaboration. Expert in stakeholder management, agile leadership, and building high-performing product teams in complex technical environments."
    
    def optimize_summary_for_ats(self, summary: str, jd_data: Dict) -> str:
        """Optimize summary for ATS keyword matching"""
        
        required_skills = jd_data.get('required_skills', [])
        preferred_skills = jd_data.get('preferred_skills', [])
        
        # Key skills to potentially incorporate
        ats_keywords = []
        for skill in required_skills + preferred_skills:
            if any(term in skill.lower() for term in ['product', 'management', 'strategy', 'agile', 'api', 'data']):
                ats_keywords.append(skill)
        
        if not ats_keywords:
            return summary
        
        prompt = f"""
        Optimize this Product Manager summary for ATS keyword matching while preserving content quality.
        
        CURRENT SUMMARY:
        {summary}
        
        TARGET KEYWORDS: {', '.join(ats_keywords[:8])}
        
        REQUIREMENTS:
        1. Naturally integrate relevant keywords from the list
        2. Preserve ALL existing metrics and achievements
        3. Maintain professional tone and readability
        4. Do NOT compromise content quality for keyword stuffing
        5. Only add keywords that genuinely fit the context
        
        Generate ATS-optimized summary:
        """
        
        response = llm_service.call_openai(prompt, model=self.optimization_model, max_tokens=500)
        
        if response.success and response.content:
            optimized = response.content.strip()
            # Validate that metrics are preserved
            if all(metric in optimized for metric in ["11 years", "94%", "$2M"]):
                return optimized
        
        return summary  # Return original if optimization fails
    
    def get_summary_analytics(self, summary: str) -> Dict:
        """Analyze summary metrics and characteristics"""
        
        words = summary.split()
        sentences = summary.split('.')
        
        # Count quantified metrics
        metrics_count = 0
        for metric_pattern in ["94%", "$2M", "€220K", "₹180", "42 days", "10 minutes", "50+"]:
            if metric_pattern in summary:
                metrics_count += 1
        
        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "character_count": len(summary),
            "quantified_metrics": metrics_count,
            "reading_level": "professional",
            "keyword_density": self._calculate_keyword_density(summary),
            "metric_preservation": metrics_count >= 4  # Should have at least 4 key metrics
        }
    
    def _calculate_keyword_density(self, summary: str) -> Dict:
        """Calculate keyword density for important terms"""
        
        keywords = {
            "product": summary.lower().count("product"),
            "management": summary.lower().count("management"),
            "automation": summary.lower().count("automation"),
            "ai": summary.lower().count("ai"),
            "revenue": summary.lower().count("revenue"),
            "experience": summary.lower().count("experience")
        }
        
        total_words = len(summary.split())
        return {k: round(v / total_words * 100, 2) for k, v in keywords.items()}

# Export the dynamic summary generator
__all__ = ['DynamicSummaryGenerator', 'SummaryVariant']