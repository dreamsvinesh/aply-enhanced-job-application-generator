#!/usr/bin/env python3
"""
Content Strategy Engine
Maps JD requirements to user strengths for optimal application positioning
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path

try:
    from .jd_intelligence_analyzer import JDIntelligenceAnalyzer, JDIntelligence
    from .chatgpt_agent import ChatGPTAgent, ContentStrategy
    from .llm_service import llm_service, LLMResponse
except ImportError:
    from jd_intelligence_analyzer import JDIntelligenceAnalyzer, JDIntelligence
    from chatgpt_agent import ChatGPTAgent, ContentStrategy
    from llm_service import llm_service, LLMResponse

@dataclass
class StrengthMapping:
    """Maps user strengths to JD requirements"""
    requirement: str  # JD requirement
    user_strength: str  # Matching user capability
    evidence_project: str  # Project that demonstrates this
    quantified_impact: str  # Specific metric/outcome
    confidence_score: float  # 0.0-1.0 match confidence

@dataclass
class ApplicationStrategy:
    """Comprehensive application strategy"""
    # Core Positioning
    value_proposition: str  # Main value statement
    differentiation_angle: str  # How to stand out
    positioning_narrative: str  # Overarching story
    
    # Content Strategy  
    priority_strengths: List[StrengthMapping]  # Top 5-8 strengths to highlight
    content_themes: List[str]  # Main themes to weave throughout
    messaging_hierarchy: List[str]  # Order of importance for messaging
    
    # Risk Mitigation
    potential_gaps: List[str]  # Areas where user might appear weak
    gap_mitigation_strategies: List[str]  # How to address gaps
    competitive_advantages: List[str]  # Clear differentiators
    
    # Tactical Recommendations
    title_recommendation: str  # Optimal title
    summary_focus_areas: List[str]  # What to emphasize in summary
    experience_prioritization: List[str]  # Which roles/projects to emphasize
    skills_emphasis: List[str]  # Key skills to highlight
    cover_letter_hooks: List[str]  # Compelling opening angles

class ContentStrategyEngine:
    """Advanced content strategy engine using AI-powered analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.jd_analyzer = JDIntelligenceAnalyzer()
        self.chatgpt_agent = ChatGPTAgent()
        
        # Load user profile
        self.load_user_profile()
        
        # Strategy models
        self.strategy_model = "gpt-4o-mini"  # Cost-optimized
        self.mapping_model = "gpt-4o-mini"
        
    def load_user_profile(self):
        """Load user profile and projects"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.user_profile = json.load(f)
    
    def develop_application_strategy(self, jd_data: Dict) -> ApplicationStrategy:
        """Develop comprehensive application strategy"""
        
        # Step 1: Analyze JD intelligence
        jd_intelligence = self.jd_analyzer.analyze_jd_intelligence(jd_data)
        
        # Step 2: Map strengths to requirements
        strength_mappings = self._map_strengths_to_requirements(jd_data, jd_intelligence)
        
        # Step 3: Develop positioning strategy
        positioning = self._develop_positioning_strategy(jd_data, jd_intelligence, strength_mappings)
        
        # Step 4: Create tactical recommendations
        tactical_recs = self._generate_tactical_recommendations(jd_data, jd_intelligence, positioning)
        
        # Step 5: Synthesize complete strategy
        return self._synthesize_application_strategy(
            jd_intelligence, strength_mappings, positioning, tactical_recs
        )
    
    def _map_strengths_to_requirements(self, jd_data: Dict, jd_intelligence: JDIntelligence) -> List[StrengthMapping]:
        """Map user strengths to JD requirements using ChatGPT"""
        
        user_projects = self.user_profile.get('projects', {})
        user_experience = self.user_profile.get('experience', [])
        
        prompt = f"""
        Map candidate strengths to job requirements for optimal positioning.
        
        JOB REQUIREMENTS:
        - Industry: {jd_intelligence.industry_focus}
        - Must-Have Skills: {', '.join(jd_intelligence.must_have_skills)}
        - Nice-to-Have: {', '.join(jd_intelligence.nice_to_have_skills)}
        - Key Challenges: {', '.join(jd_intelligence.key_challenges)}
        
        CANDIDATE STRENGTHS:
        
        RAG System Project:
        - Built AI-powered knowledge system achieving 94% accuracy
        - Serves 200+ employees with 1,500+ weekly queries
        - Reduced support tickets 75% (500→125 monthly)
        
        Contract Automation:
        - Automated Salesforce-SAP-MuleSoft integration
        - Reduced timeline 99.6% (42 days→10 minutes)
        - Accelerated $2M revenue recognition
        
        Converge Platform:
        - Led F&B platform serving 600,000+ users
        - 30,000+ daily orders, ₹180 crores annual GMV
        - Achieved 91% NPS, scaled MVP→production in 6 months
        
        Space Optimization:
        - Generated €220K monthly revenue from unutilized inventory
        - Data-driven space optimization strategies
        
        Mobile/IoT Platforms:
        - Increased app engagement 45%, satisfaction 65%
        - IoT-enabled self-service, increased ARPA 35%
        
        Map top 6 JD requirements to strongest user evidence. For each mapping:
        1. JD requirement (specific skill/challenge from job)
        2. User strength (specific capability)
        3. Evidence project (which project demonstrates it)
        4. Quantified impact (specific metric)
        5. Confidence score (0.0-1.0)
        
        Respond in JSON format:
        {{
            "mappings": [
                {{
                    "requirement": "specific requirement from JD",
                    "user_strength": "matching user capability",
                    "evidence_project": "project name",
                    "quantified_impact": "specific metric",
                    "confidence_score": 0.9
                }}
            ]
        }}
        """
        
        response = llm_service.call_openai(prompt, model=self.mapping_model, max_tokens=1000)
        
        if response.success:
            try:
                mapping_data = json.loads(response.content.strip())
                mappings = []
                for item in mapping_data.get('mappings', []):
                    mappings.append(StrengthMapping(
                        requirement=item.get('requirement', ''),
                        user_strength=item.get('user_strength', ''),
                        evidence_project=item.get('evidence_project', ''),
                        quantified_impact=item.get('quantified_impact', ''),
                        confidence_score=float(item.get('confidence_score', 0.8))
                    ))
                return mappings[:8]  # Top 8 mappings
            except (json.JSONDecodeError, ValueError):
                pass
        
        # Fallback strength mappings
        return self._fallback_strength_mappings(jd_intelligence)
    
    def _develop_positioning_strategy(self, 
                                   jd_data: Dict, 
                                   jd_intelligence: JDIntelligence,
                                   strength_mappings: List[StrengthMapping]) -> Dict:
        """Develop core positioning strategy using ChatGPT"""
        
        # Extract top strengths for analysis
        top_strengths = [mapping.user_strength for mapping in strength_mappings[:5]]
        evidence_metrics = [mapping.quantified_impact for mapping in strength_mappings[:5]]
        
        prompt = f"""
        Develop positioning strategy for this Product Manager application.
        
        ROLE CONTEXT:
        - Company: {jd_data.get('company_name', 'Target Company')}
        - Industry: {jd_intelligence.industry_focus}
        - Role Level: {jd_intelligence.role_type}
        - Key Challenges: {', '.join(jd_intelligence.key_challenges[:3])}
        
        TOP CANDIDATE STRENGTHS:
        {chr(10).join([f"- {strength}: {evidence}" for strength, evidence in zip(top_strengths, evidence_metrics)])}
        
        Develop:
        1. VALUE_PROPOSITION: Core value candidate brings (1 sentence)
        2. DIFFERENTIATION_ANGLE: How to stand out from other PMs (automation expert, AI innovator, growth driver, etc.)
        3. POSITIONING_NARRATIVE: Overarching story/theme (2-3 sentences)
        4. COMPETITIVE_ADVANTAGES: Top 3 unique differentiators
        5. POTENTIAL_GAPS: Areas where candidate might seem weak
        6. GAP_MITIGATION: How to address potential weaknesses
        
        Respond in JSON format:
        {{
            "value_proposition": "clear value statement",
            "differentiation_angle": "automation_expert|ai_innovator|growth_driver|technical_pm",
            "positioning_narrative": "compelling story",
            "competitive_advantages": ["advantage1", "advantage2", "advantage3"],
            "potential_gaps": ["gap1", "gap2"],
            "gap_mitigation_strategies": ["strategy1", "strategy2"]
        }}
        """
        
        response = llm_service.call_openai(prompt, model=self.strategy_model, max_tokens=800)
        
        if response.success:
            try:
                return json.loads(response.content.strip())
            except json.JSONDecodeError:
                pass
        
        # Fallback positioning
        return {
            "value_proposition": "Senior PM with proven automation expertise delivering quantified business impact",
            "differentiation_angle": "automation_expert",
            "positioning_narrative": "Product leader who transforms complex business processes into efficient automated systems, with proven track record of $2M+ revenue impact and 94% accuracy AI implementations.",
            "competitive_advantages": ["AI/ML Automation", "Enterprise Integration", "Quantified Results"],
            "potential_gaps": ["Domain Specific Experience"],
            "gap_mitigation_strategies": ["Emphasize transferable automation skills", "Highlight learning agility"]
        }
    
    def _generate_tactical_recommendations(self, 
                                        jd_data: Dict,
                                        jd_intelligence: JDIntelligence, 
                                        positioning: Dict) -> Dict:
        """Generate specific tactical recommendations using ChatGPT"""
        
        prompt = f"""
        Generate tactical content recommendations for this application.
        
        POSITIONING STRATEGY:
        - Value Proposition: {positioning.get('value_proposition', '')}
        - Differentiation: {positioning.get('differentiation_angle', '')}
        - Narrative: {positioning.get('positioning_narrative', '')}
        
        JOB CONTEXT:
        - Industry: {jd_intelligence.industry_focus}
        - Must-Have Skills: {', '.join(jd_intelligence.must_have_skills[:5])}
        - Role Level: {jd_intelligence.role_type}
        
        Generate tactical recommendations:
        1. TITLE_RECOMMENDATION: Optimal job title for resume header
        2. SUMMARY_FOCUS_AREAS: Top 4 areas to emphasize in summary
        3. EXPERIENCE_PRIORITIZATION: Which projects/roles to emphasize first
        4. SKILLS_EMPHASIS: Top 8 skills to highlight prominently
        5. COVER_LETTER_HOOKS: 3 compelling opening angles for cover letter
        6. MESSAGING_HIERARCHY: Order of importance for key messages
        
        Respond in JSON format with specific recommendations.
        """
        
        response = llm_service.call_openai(prompt, model=self.strategy_model, max_tokens=800)
        
        if response.success:
            try:
                return json.loads(response.content.strip())
            except json.JSONDecodeError:
                pass
        
        # Fallback recommendations
        industry = jd_intelligence.industry_focus
        if industry == 'fintech':
            focus_areas = ["Payment Systems", "Automation", "Compliance", "Revenue Impact"]
        elif industry == 'ai_ml':
            focus_areas = ["AI/ML Systems", "Automation", "Technical Implementation", "Innovation"]
        else:
            focus_areas = ["Enterprise SaaS", "Cross-functional Leadership", "Process Optimization", "Growth"]
        
        return {
            "title_recommendation": "Senior Product Manager",
            "summary_focus_areas": focus_areas,
            "experience_prioritization": ["Current Role Projects", "Converge Platform", "Technical Skills"],
            "skills_emphasis": ["Product Strategy", "Automation", "Cross-functional Leadership", "API Integration"],
            "cover_letter_hooks": ["Automation expertise", "Quantified results", "Technical background"],
            "messaging_hierarchy": ["Results", "Experience", "Skills", "Cultural Fit"]
        }
    
    def _synthesize_application_strategy(self, 
                                       jd_intelligence: JDIntelligence,
                                       strength_mappings: List[StrengthMapping],
                                       positioning: Dict,
                                       tactical_recs: Dict) -> ApplicationStrategy:
        """Synthesize all analysis into comprehensive strategy"""
        
        return ApplicationStrategy(
            # Core Positioning
            value_proposition=positioning.get('value_proposition', ''),
            differentiation_angle=positioning.get('differentiation_angle', 'automation_expert'),
            positioning_narrative=positioning.get('positioning_narrative', ''),
            
            # Content Strategy
            priority_strengths=strength_mappings,
            content_themes=tactical_recs.get('summary_focus_areas', []),
            messaging_hierarchy=tactical_recs.get('messaging_hierarchy', []),
            
            # Risk Mitigation
            potential_gaps=positioning.get('potential_gaps', []),
            gap_mitigation_strategies=positioning.get('gap_mitigation_strategies', []),
            competitive_advantages=positioning.get('competitive_advantages', []),
            
            # Tactical Recommendations
            title_recommendation=tactical_recs.get('title_recommendation', 'Senior Product Manager'),
            summary_focus_areas=tactical_recs.get('summary_focus_areas', []),
            experience_prioritization=tactical_recs.get('experience_prioritization', []),
            skills_emphasis=tactical_recs.get('skills_emphasis', []),
            cover_letter_hooks=tactical_recs.get('cover_letter_hooks', [])
        )
    
    def _fallback_strength_mappings(self, jd_intelligence: JDIntelligence) -> List[StrengthMapping]:
        """Fallback strength mappings based on industry focus"""
        
        if jd_intelligence.industry_focus == 'fintech':
            return [
                StrengthMapping(
                    requirement="Payment systems experience",
                    user_strength="Enterprise transaction processing",
                    evidence_project="converge_platform",
                    quantified_impact="₹180 crores annual GMV",
                    confidence_score=0.9
                ),
                StrengthMapping(
                    requirement="Process automation",
                    user_strength="Workflow automation expertise",
                    evidence_project="contract_automation",
                    quantified_impact="99.6% timeline reduction",
                    confidence_score=0.95
                )
            ]
        elif jd_intelligence.industry_focus == 'ai_ml':
            return [
                StrengthMapping(
                    requirement="AI/ML systems",
                    user_strength="AI-powered product development",
                    evidence_project="rag_system",
                    quantified_impact="94% accuracy serving 200+ users",
                    confidence_score=0.95
                ),
                StrengthMapping(
                    requirement="Technical implementation",
                    user_strength="Complex system integration",
                    evidence_project="contract_automation",
                    quantified_impact="Salesforce-SAP-MuleSoft integration",
                    confidence_score=0.9
                )
            ]
        else:
            return [
                StrengthMapping(
                    requirement="Cross-functional leadership",
                    user_strength="Team orchestration across 15+ processes",
                    evidence_project="current_role",
                    quantified_impact="50+ resource hours saved daily",
                    confidence_score=0.9
                ),
                StrengthMapping(
                    requirement="Revenue growth",
                    user_strength="Monetization and revenue optimization",
                    evidence_project="space_optimization",
                    quantified_impact="€220K monthly revenue generated",
                    confidence_score=0.85
                )
            ]
    
    def analyze_application_fit(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> Dict:
        """Analyze overall application fit and confidence"""
        
        # Calculate fit scores
        strength_scores = [mapping.confidence_score for mapping in application_strategy.priority_strengths]
        avg_strength_fit = sum(strength_scores) / len(strength_scores) if strength_scores else 0.7
        
        # Risk assessment
        risk_level = "low" if len(application_strategy.potential_gaps) <= 1 else "medium"
        
        # Competitive advantage assessment
        differentiation_strength = len(application_strategy.competitive_advantages)
        
        return {
            "overall_fit_score": round(avg_strength_fit, 2),
            "strength_coverage": f"{len(application_strategy.priority_strengths)}/8",
            "risk_level": risk_level,
            "competitive_advantages_count": differentiation_strength,
            "recommendation": "strong_fit" if avg_strength_fit >= 0.8 else "good_fit" if avg_strength_fit >= 0.6 else "moderate_fit",
            "key_differentiators": application_strategy.competitive_advantages,
            "mitigation_required": application_strategy.potential_gaps
        }
    
    def get_strategy_summary(self, application_strategy: ApplicationStrategy) -> Dict:
        """Get comprehensive strategy summary"""
        
        return {
            "positioning": {
                "value_proposition": application_strategy.value_proposition,
                "differentiation": application_strategy.differentiation_angle,
                "narrative": application_strategy.positioning_narrative
            },
            "content_focus": {
                "themes": application_strategy.content_themes,
                "title": application_strategy.title_recommendation,
                "summary_areas": application_strategy.summary_focus_areas,
                "experience_priority": application_strategy.experience_prioritization
            },
            "top_strengths": [
                {
                    "requirement": mapping.requirement,
                    "strength": mapping.user_strength,
                    "evidence": mapping.quantified_impact,
                    "confidence": mapping.confidence_score
                }
                for mapping in application_strategy.priority_strengths[:5]
            ],
            "risk_mitigation": {
                "gaps": application_strategy.potential_gaps,
                "strategies": application_strategy.gap_mitigation_strategies,
                "advantages": application_strategy.competitive_advantages
            }
        }

# Export the content strategy engine
__all__ = ['ContentStrategyEngine', 'ApplicationStrategy', 'StrengthMapping']