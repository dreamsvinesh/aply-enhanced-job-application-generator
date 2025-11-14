#!/usr/bin/env python3
"""
JD Intelligence Analyzer
Advanced job description analysis using ChatGPT for strategic content optimization
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path

try:
    from .chatgpt_agent import ChatGPTAgent, ContentStrategy
    from .llm_service import llm_service, LLMResponse
except ImportError:
    from chatgpt_agent import ChatGPTAgent, ContentStrategy
    from llm_service import llm_service, LLMResponse

@dataclass
class JDIntelligence:
    """Comprehensive job description intelligence"""
    # Core Analysis
    role_type: str  # "senior_pm", "principal_pm", "director_pm", etc.
    industry_focus: str  # "fintech", "enterprise_saas", "ai_ml", "consumer", etc.
    company_stage: str  # "startup", "growth", "enterprise", "public"
    technical_complexity: str  # "high", "medium", "low"
    
    # Requirements Analysis
    must_have_skills: List[str]  # Critical requirements
    nice_to_have_skills: List[str]  # Preferred but not essential
    experience_level: str  # "3-5", "5-8", "8-12", "12+"
    domain_requirements: List[str]  # Specific domain expertise needed
    
    # Strategic Insights
    key_challenges: List[str]  # Main problems the role will solve
    success_metrics: List[str]  # How success will be measured
    growth_opportunities: List[str]  # Career growth aspects
    team_structure: str  # "individual_contributor", "team_lead", "cross_functional"
    
    # Content Strategy Recommendations
    content_strategy: ContentStrategy
    priority_projects: List[str]  # Which user projects to emphasize
    messaging_angle: str  # Main value proposition angle
    risk_factors: List[str]  # Potential application risks to address

class JDIntelligenceAnalyzer:
    """Advanced job description analyzer using ChatGPT intelligence"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.chatgpt_agent = ChatGPTAgent()
        
        # Analysis models - optimized for cost
        self.analysis_model = "gpt-4o-mini"
        self.intelligence_model = "gpt-4o-mini"  # Sufficient for structured analysis
        
        # Industry patterns and keywords
        self.industry_patterns = {
            "fintech": ["payment", "banking", "financial", "card", "transaction", "compliance", "pci", "psd2"],
            "ai_ml": ["artificial intelligence", "machine learning", "llm", "rag", "vector", "model", "automation"],
            "enterprise_saas": ["enterprise", "b2b", "saas", "platform", "integration", "salesforce", "sap"],
            "internal_tools": ["internal", "operations", "workflow", "productivity", "employee", "admin"],
            "consumer": ["consumer", "b2c", "mobile", "app", "user experience", "engagement", "retention"]
        }
        
        # Role level patterns
        self.role_patterns = {
            "senior_pm": ["senior product manager", "sr product manager", "product manager ii"],
            "principal_pm": ["principal product manager", "staff product manager", "lead product manager"],
            "director_pm": ["director of product", "director product", "head of product"],
            "vp_pm": ["vp product", "vice president", "head of product management"]
        }
    
    def analyze_jd_intelligence(self, jd_data: Dict) -> JDIntelligence:
        """Perform comprehensive JD analysis using ChatGPT intelligence"""
        
        # Extract text content
        jd_text = self._extract_jd_text(jd_data)
        
        # Multi-step intelligent analysis
        core_analysis = self._analyze_core_requirements(jd_text, jd_data)
        strategic_insights = self._extract_strategic_insights(jd_text, jd_data)
        content_recommendations = self._generate_content_recommendations(jd_text, jd_data, core_analysis)
        
        # Combine into comprehensive intelligence
        return self._synthesize_intelligence(
            jd_data, core_analysis, strategic_insights, content_recommendations
        )
    
    def _extract_jd_text(self, jd_data: Dict) -> str:
        """Extract and clean JD text for analysis"""
        text_parts = []
        
        if jd_data.get('job_description'):
            text_parts.append(jd_data['job_description'])
        
        if jd_data.get('required_skills'):
            text_parts.append("Required: " + ', '.join(jd_data['required_skills']))
        
        if jd_data.get('preferred_skills'):
            text_parts.append("Preferred: " + ', '.join(jd_data['preferred_skills']))
        
        if jd_data.get('company_description'):
            text_parts.append("Company: " + jd_data['company_description'])
        
        return '\n\n'.join(text_parts)
    
    def _analyze_core_requirements(self, jd_text: str, jd_data: Dict) -> Dict:
        """Analyze core role requirements using ChatGPT"""
        
        prompt = f"""
        Analyze this Product Manager job description and extract core requirements.
        
        JOB DESCRIPTION:
        {jd_text[:2500]}
        
        Extract and categorize:
        1. ROLE_TYPE: What level? (senior_pm, principal_pm, director_pm, vp_pm)
        2. INDUSTRY_FOCUS: Primary industry (fintech, enterprise_saas, ai_ml, internal_tools, consumer)
        3. COMPANY_STAGE: Company maturity (startup, growth, enterprise, public)
        4. TECHNICAL_COMPLEXITY: Technical depth required (high, medium, low)
        5. MUST_HAVE_SKILLS: Critical technical/domain skills
        6. NICE_TO_HAVE_SKILLS: Preferred additional skills
        7. EXPERIENCE_LEVEL: Years required (3-5, 5-8, 8-12, 12+)
        8. DOMAIN_REQUIREMENTS: Specific industry/domain experience needed
        
        Respond in JSON format:
        {{
            "role_type": "senior_pm|principal_pm|director_pm|vp_pm",
            "industry_focus": "fintech|enterprise_saas|ai_ml|internal_tools|consumer",
            "company_stage": "startup|growth|enterprise|public", 
            "technical_complexity": "high|medium|low",
            "must_have_skills": ["skill1", "skill2"],
            "nice_to_have_skills": ["skill1", "skill2"],
            "experience_level": "5-8|8-12|etc",
            "domain_requirements": ["domain1", "domain2"]
        }}
        """
        
        response = llm_service.call_openai(prompt, model=self.analysis_model, max_tokens=800)
        
        if response.success:
            try:
                return json.loads(response.content.strip())
            except json.JSONDecodeError:
                pass
        
        # Fallback analysis
        return self._fallback_core_analysis(jd_text, jd_data)
    
    def _extract_strategic_insights(self, jd_text: str, jd_data: Dict) -> Dict:
        """Extract strategic insights using ChatGPT"""
        
        prompt = f"""
        Extract strategic insights from this Product Manager job description.
        
        JOB DESCRIPTION:
        {jd_text[:2000]}
        
        Identify:
        1. KEY_CHALLENGES: Main problems/challenges the role will solve (3-4 items)
        2. SUCCESS_METRICS: How success will likely be measured (3-4 items)
        3. GROWTH_OPPORTUNITIES: Career development aspects mentioned
        4. TEAM_STRUCTURE: Team setup (individual_contributor, team_lead, cross_functional)
        5. COMPANY_PRIORITIES: What the company seems to prioritize most
        
        Respond in JSON format:
        {{
            "key_challenges": ["challenge1", "challenge2"],
            "success_metrics": ["metric1", "metric2"],
            "growth_opportunities": ["opportunity1", "opportunity2"],
            "team_structure": "individual_contributor|team_lead|cross_functional",
            "company_priorities": ["priority1", "priority2"]
        }}
        """
        
        response = llm_service.call_openai(prompt, model=self.analysis_model, max_tokens=700)
        
        if response.success:
            try:
                return json.loads(response.content.strip())
            except json.JSONDecodeError:
                pass
        
        # Fallback insights
        return {
            "key_challenges": ["Product Strategy", "Cross-functional Execution", "User Experience"],
            "success_metrics": ["Feature Adoption", "User Engagement", "Revenue Impact"],
            "growth_opportunities": ["Technical Skills", "Leadership", "Strategy"],
            "team_structure": "cross_functional",
            "company_priorities": ["Innovation", "Growth", "Customer Success"]
        }
    
    def _generate_content_recommendations(self, jd_text: str, jd_data: Dict, core_analysis: Dict) -> Dict:
        """Generate content strategy recommendations using ChatGPT"""
        
        prompt = f"""
        Based on this job analysis, recommend content strategy for the application.
        
        ROLE ANALYSIS:
        - Industry: {core_analysis.get('industry_focus', 'enterprise_saas')}
        - Technical Level: {core_analysis.get('technical_complexity', 'medium')}
        - Role Level: {core_analysis.get('role_type', 'senior_pm')}
        
        AVAILABLE USER PROJECTS:
        - rag_system: AI-powered RAG knowledge system (94% accuracy, 200+ users)
        - contract_automation: Salesforce-SAP automation (42 days→10 min, $2M revenue)
        - converge_platform: F&B platform (600K users, ₹180 crores GMV)
        - space_optimization: Revenue generation (€220K monthly)
        - mobile_platform: Self-service features (45% engagement increase)
        - iot_platform: IoT-enabled systems (35% ARPA growth)
        
        Recommend:
        1. PRIORITY_PROJECTS: Top 3 projects to emphasize (from list above)
        2. MESSAGING_ANGLE: Main value proposition (automation_expert, ai_innovator, growth_driver, technical_pm)
        3. RISK_FACTORS: Potential concerns to address (experience_gaps, skill_mismatches, overqualification)
        4. CONTENT_FOCUS: What to emphasize (technical_depth, business_impact, leadership, innovation)
        
        Respond in JSON format:
        {{
            "priority_projects": ["project1", "project2", "project3"],
            "messaging_angle": "automation_expert|ai_innovator|growth_driver|technical_pm",
            "risk_factors": ["factor1", "factor2"],
            "content_focus": ["focus1", "focus2", "focus3"]
        }}
        """
        
        response = llm_service.call_openai(prompt, model=self.intelligence_model, max_tokens=600)
        
        if response.success:
            try:
                return json.loads(response.content.strip())
            except json.JSONDecodeError:
                pass
        
        # Fallback recommendations based on industry
        industry = core_analysis.get('industry_focus', 'enterprise_saas')
        
        if industry == 'fintech':
            return {
                "priority_projects": ["contract_automation", "converge_platform", "space_optimization"],
                "messaging_angle": "automation_expert",
                "risk_factors": ["fintech_compliance"],
                "content_focus": ["business_impact", "technical_depth", "compliance"]
            }
        elif industry == 'ai_ml':
            return {
                "priority_projects": ["rag_system", "contract_automation", "mobile_platform"],
                "messaging_angle": "ai_innovator",
                "risk_factors": ["ml_depth"],
                "content_focus": ["technical_depth", "innovation", "automation"]
            }
        else:
            return {
                "priority_projects": ["contract_automation", "converge_platform", "mobile_platform"],
                "messaging_angle": "growth_driver",
                "risk_factors": [],
                "content_focus": ["business_impact", "leadership", "scalability"]
            }
    
    def _synthesize_intelligence(self, 
                               jd_data: Dict, 
                               core_analysis: Dict, 
                               strategic_insights: Dict,
                               content_recommendations: Dict) -> JDIntelligence:
        """Synthesize all analysis into comprehensive intelligence"""
        
        # Generate content strategy using ChatGPT agent
        content_strategy = self.chatgpt_agent.analyze_jd_strategy(jd_data)
        
        return JDIntelligence(
            # Core Analysis
            role_type=core_analysis.get('role_type', 'senior_pm'),
            industry_focus=core_analysis.get('industry_focus', 'enterprise_saas'),
            company_stage=core_analysis.get('company_stage', 'growth'),
            technical_complexity=core_analysis.get('technical_complexity', 'medium'),
            
            # Requirements
            must_have_skills=core_analysis.get('must_have_skills', []),
            nice_to_have_skills=core_analysis.get('nice_to_have_skills', []),
            experience_level=core_analysis.get('experience_level', '5-8'),
            domain_requirements=core_analysis.get('domain_requirements', []),
            
            # Strategic Insights
            key_challenges=strategic_insights.get('key_challenges', []),
            success_metrics=strategic_insights.get('success_metrics', []),
            growth_opportunities=strategic_insights.get('growth_opportunities', []),
            team_structure=strategic_insights.get('team_structure', 'cross_functional'),
            
            # Content Strategy
            content_strategy=content_strategy,
            priority_projects=content_recommendations.get('priority_projects', []),
            messaging_angle=content_recommendations.get('messaging_angle', 'growth_driver'),
            risk_factors=content_recommendations.get('risk_factors', [])
        )
    
    def _fallback_core_analysis(self, jd_text: str, jd_data: Dict) -> Dict:
        """Fallback analysis using keyword detection"""
        
        jd_lower = jd_text.lower()
        
        # Determine role type
        role_type = "senior_pm"
        for role, patterns in self.role_patterns.items():
            if any(pattern in jd_lower for pattern in patterns):
                role_type = role
                break
        
        # Determine industry focus
        industry_focus = "enterprise_saas"
        for industry, patterns in self.industry_patterns.items():
            if any(pattern in jd_lower for pattern in patterns):
                industry_focus = industry
                break
        
        # Technical complexity based on keywords
        tech_keywords = ['api', 'integration', 'architecture', 'system', 'database', 'ml', 'ai']
        tech_complexity = "high" if sum(1 for kw in tech_keywords if kw in jd_lower) >= 3 else "medium"
        
        return {
            "role_type": role_type,
            "industry_focus": industry_focus,
            "company_stage": "growth",
            "technical_complexity": tech_complexity,
            "must_have_skills": jd_data.get('required_skills', [])[:5],
            "nice_to_have_skills": jd_data.get('preferred_skills', [])[:5],
            "experience_level": "5-8",
            "domain_requirements": [industry_focus]
        }
    
    def analyze_competitive_positioning(self, jd_intelligence: JDIntelligence) -> Dict:
        """Analyze competitive positioning based on JD intelligence"""
        
        prompt = f"""
        Analyze competitive positioning for this Product Manager application.
        
        ROLE INTELLIGENCE:
        - Industry: {jd_intelligence.industry_focus}
        - Role Level: {jd_intelligence.role_type}
        - Technical Complexity: {jd_intelligence.technical_complexity}
        - Must-Have Skills: {', '.join(jd_intelligence.must_have_skills[:5])}
        
        CANDIDATE PROFILE:
        - 11 years technology experience, 7 years PM
        - Built AI systems achieving 94% accuracy
        - Automated workflows saving $2M revenue
        - Led cross-functional teams across 15+ processes
        
        Analyze:
        1. COMPETITIVE_ADVANTAGES: Where candidate strongly differentiates
        2. POTENTIAL_GAPS: Areas where candidate might be weaker
        3. POSITIONING_STRATEGY: How to position against competition
        4. DIFFERENTIATION_POINTS: Unique value propositions to emphasize
        
        Respond in JSON format with analysis.
        """
        
        response = llm_service.call_openai(prompt, model=self.analysis_model, max_tokens=700)
        
        if response.success:
            try:
                return json.loads(response.content.strip())
            except json.JSONDecodeError:
                pass
        
        # Fallback competitive analysis
        return {
            "competitive_advantages": ["Automation Experience", "Technical Depth", "Quantified Results"],
            "potential_gaps": ["Industry Specific", "Team Size"],
            "positioning_strategy": "Technical PM with Business Impact",
            "differentiation_points": ["AI/ML Automation", "Revenue Impact", "Cross-functional Leadership"]
        }
    
    def get_intelligence_summary(self, jd_intelligence: JDIntelligence) -> Dict:
        """Get comprehensive intelligence summary"""
        
        return {
            "role_analysis": {
                "type": jd_intelligence.role_type,
                "industry": jd_intelligence.industry_focus,
                "complexity": jd_intelligence.technical_complexity,
                "team_structure": jd_intelligence.team_structure
            },
            "requirements": {
                "must_have": jd_intelligence.must_have_skills,
                "nice_to_have": jd_intelligence.nice_to_have_skills,
                "experience": jd_intelligence.experience_level,
                "domain": jd_intelligence.domain_requirements
            },
            "strategy": {
                "focus": jd_intelligence.content_strategy.primary_focus,
                "themes": jd_intelligence.content_strategy.key_themes,
                "messaging": jd_intelligence.messaging_angle,
                "priority_projects": jd_intelligence.priority_projects
            },
            "insights": {
                "challenges": jd_intelligence.key_challenges,
                "success_metrics": jd_intelligence.success_metrics,
                "risks": jd_intelligence.risk_factors,
                "opportunities": jd_intelligence.growth_opportunities
            }
        }

# Export the intelligence analyzer
__all__ = ['JDIntelligenceAnalyzer', 'JDIntelligence']