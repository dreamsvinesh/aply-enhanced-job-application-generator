#!/usr/bin/env python3
"""
Dynamic Experience Generator
ChatGPT-powered experience bullet point generation based on strategic analysis
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path

try:
    from .content_strategy_engine import ContentStrategyEngine, ApplicationStrategy, StrengthMapping
    from .chatgpt_agent import ChatGPTAgent, ContentStrategy
    from .llm_service import llm_service, LLMResponse
except ImportError:
    from content_strategy_engine import ContentStrategyEngine, ApplicationStrategy, StrengthMapping
    from chatgpt_agent import ChatGPTAgent, ContentStrategy
    from llm_service import llm_service, LLMResponse

@dataclass
class BulletPointStrategy:
    """Strategy for generating specific bullet points"""
    project_focus: str  # Which project to emphasize
    impact_type: str  # "revenue", "efficiency", "technical", "leadership"
    quantified_metric: str  # Specific metric to highlight
    context_setting: str  # Background context for the achievement
    action_emphasis: str  # What action verb/approach to use

@dataclass
class ExperienceEnhancement:
    """Enhanced experience section with strategic positioning"""
    role_title: str
    company: str
    duration: str
    location: str
    strategic_bullets: List[str]  # AI-optimized bullets
    original_bullets: List[str]  # Original bullets for comparison
    enhancement_notes: List[str]  # What was improved
    metrics_preserved: List[str]  # Critical metrics maintained

class DynamicExperienceGenerator:
    """Advanced experience generator using strategic AI-powered optimization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.strategy_engine = ContentStrategyEngine()
        self.chatgpt_agent = ChatGPTAgent()
        
        # Load user data
        self.load_user_data()
        
        # Generation models - cost optimized
        self.experience_model = "gpt-4o-mini"  # Cheapest for content generation
        self.bullet_model = "gpt-4o-mini"
        self.optimization_model = "gpt-4o-mini"
        
        # Critical metrics that must be preserved
        self.critical_metrics = [
            "94%", "$2M", "€220K", "₹180 crores", "42 days", "10 minutes",
            "99.6%", "200+ users", "600,000+ users", "30,000+", "91% NPS",
            "50+ resource hours", "1,500+ weekly", "75%", "15+ processes"
        ]
    
    def load_user_data(self):
        """Load user profile and projects data"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.user_profile = json.load(f)
        
        # Try to load detailed projects if available
        try:
            detailed_path = Path(__file__).parent.parent / "data" / "extracted_profile.json"
            with open(detailed_path, 'r', encoding='utf-8') as f:
                detailed_data = json.load(f)
                self.detailed_projects = detailed_data.get('detailed_projects', {})
        except:
            self.detailed_projects = {}
    
    def generate_strategic_experience(self, jd_data: Dict, application_strategy: ApplicationStrategy) -> List[ExperienceEnhancement]:
        """Generate strategically optimized experience sections"""
        
        original_experience = self.user_profile.get('experience', [])
        enhanced_experience = []
        
        for i, role in enumerate(original_experience):
            # Determine strategic approach for this role
            role_strategy = self._determine_role_strategy(role, i, application_strategy)
            
            # Generate strategic bullets
            strategic_bullets = self._generate_strategic_bullets(
                role, role_strategy, jd_data, application_strategy
            )
            
            # Create enhancement
            enhancement = ExperienceEnhancement(
                role_title=role.get('title', ''),
                company=role.get('company', ''),
                duration=role.get('duration', ''),
                location=role.get('location', ''),
                strategic_bullets=strategic_bullets,
                original_bullets=role.get('highlights', []),
                enhancement_notes=self._analyze_enhancements(
                    role.get('highlights', []), strategic_bullets
                ),
                metrics_preserved=self._extract_preserved_metrics(strategic_bullets)
            )
            
            enhanced_experience.append(enhancement)
        
        return enhanced_experience
    
    def _determine_role_strategy(self, role: Dict, role_index: int, application_strategy: ApplicationStrategy) -> Dict:
        """Determine strategic approach for each role"""
        
        role_title = role.get('title', '').lower()
        
        if role_index == 0 and 'product manager' in role_title:
            # Current/most recent PM role - maximum strategic focus
            return {
                "bullet_count": 8,
                "priority_projects": application_strategy.priority_strengths[:4],
                "emphasis": "comprehensive",
                "metrics_density": "high",
                "technical_depth": "high" if "ai" in application_strategy.differentiation_angle else "medium"
            }
        elif 'product manager' in role_title:
            # Previous PM role - focused on platform achievements
            return {
                "bullet_count": 6,
                "priority_projects": application_strategy.priority_strengths[2:5],
                "emphasis": "platform_scale",
                "metrics_density": "medium",
                "technical_depth": "medium"
            }
        else:
            # Technical/other roles - concise technical focus
            return {
                "bullet_count": 2,
                "priority_projects": [],
                "emphasis": "technical_foundation",
                "metrics_density": "low",
                "technical_depth": "low"
            }
    
    def _generate_strategic_bullets(self, 
                                  role: Dict, 
                                  role_strategy: Dict, 
                                  jd_data: Dict,
                                  application_strategy: ApplicationStrategy) -> List[str]:
        """Generate strategic bullet points for a role using ChatGPT"""
        
        # Get existing bullets as foundation
        existing_bullets = role.get('highlights', [])
        
        # Build context for AI generation
        context = self._build_generation_context(role, role_strategy, jd_data, application_strategy)
        
        prompt = f"""
        Generate strategically optimized experience bullets for this Product Manager role.
        
        STRATEGIC CONTEXT:
        Role: {role.get('title', '')} at {role.get('company', '')}
        Target Company: {jd_data.get('company_name', 'Target Company')}
        Industry Focus: {application_strategy.differentiation_angle}
        
        POSITIONING STRATEGY:
        - Value Proposition: {application_strategy.value_proposition}
        - Content Themes: {', '.join(application_strategy.content_themes[:3])}
        - Key Strengths: {', '.join([s.user_strength for s in application_strategy.priority_strengths[:3]])}
        
        ROLE STRATEGY:
        - Target Bullets: {role_strategy.get('bullet_count', 6)}
        - Emphasis: {role_strategy.get('emphasis', 'comprehensive')}
        - Technical Depth: {role_strategy.get('technical_depth', 'medium')}
        
        AVAILABLE PROJECT DATA:
        {self._format_project_data(role, application_strategy)}
        
        EXISTING BULLETS (preserve metrics):
        {chr(10).join([f"- {bullet}" for bullet in existing_bullets[:4]])}
        
        REQUIREMENTS:
        1. Action-Impact-Measurement format: "Action verb + specific action + quantified impact"
        2. PRESERVE ALL METRICS: 94%, $2M, 42 days→10 minutes, 99.6%, etc.
        3. Emphasize {application_strategy.differentiation_angle} capabilities
        4. Include cross-functional leadership elements
        5. Each bullet 1-2 lines, high impact density
        6. Use power verbs: Built, Automated, Led, Achieved, Generated, Orchestrated
        7. Quantify everything possible with specific numbers
        8. Professional, confident tone
        
        Generate {role_strategy.get('bullet_count', 6)} optimized bullets:
        """
        
        response = llm_service.call_openai(prompt, model=self.experience_model, max_tokens=1200)
        
        if response.success and response.content:
            bullets = self._parse_bullets_from_response(response.content)
            
            # Validate and enhance bullets
            validated_bullets = self._validate_and_enhance_bullets(
                bullets, existing_bullets, role_strategy.get('bullet_count', 6)
            )
            
            return validated_bullets[:role_strategy.get('bullet_count', 6)]
        
        # Fallback to enhanced existing bullets
        return self._enhance_existing_bullets(existing_bullets, role_strategy)
    
    def _format_project_data(self, role: Dict, application_strategy: ApplicationStrategy) -> str:
        """Format relevant project data for AI context"""
        
        role_title = role.get('title', '').lower()
        
        if 'senior product manager' in role_title:
            return """
            RAG System Project:
            - Built AI-powered knowledge system using pgvector and prompt engineering
            - Achieved 94% accuracy with sub-second response times
            - Serves 200+ employees with 1,500+ weekly queries
            - Reduced support tickets 75% (500→125 monthly)
            
            Contract Automation:
            - Automated Salesforce-SAP-MuleSoft integration workflow
            - Reduced processing timeline 99.6% (42 days→10 minutes)
            - Accelerated $2M revenue recognition
            - Saved 50+ resource hours daily
            
            Cross-functional Process Automation:
            - Orchestrated automation across 15+ operational processes
            - Achieved 60% support ticket reduction
            - Enhanced invoice processing from 21 days to real-time
            - 35% improvement in contract accuracy
            """
        elif 'product manager' in role_title:
            return """
            Converge F&B Platform:
            - Led end-to-end product strategy serving 600,000+ users
            - 30,000+ daily orders across 24 business parks
            - ₹168-180 crores annual GMV with 91% NPS
            - Scaled MVP→production in 6 months
            
            Space Optimization:
            - Generated €220K monthly revenue from unutilized inventory
            - Data-driven space optimization strategies
            - Improved occupancy 25% via streamlined workflows
            
            Mobile Self-Service Platform:
            - Increased app engagement 45%, satisfaction 65%
            - IoT-enabled self-service with auto WiFi
            - Increased ARPA 35%
            """
        else:
            return """
            Frontend Development:
            - Built applications using HTML5, CSS3, Angular.JS
            - Served 50+ enterprise clients
            - End-to-end UX to UI development
            """
    
    def _parse_bullets_from_response(self, response_content: str) -> List[str]:
        """Parse bullet points from AI response"""
        
        bullets = []
        lines = response_content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or 
                        (line[0].isdigit() and '.' in line[:3])):
                # Clean up bullet formatting
                bullet = line.lstrip('- •0123456789. ').strip()
                if bullet and len(bullet) > 20:  # Valid bullet with substance
                    bullets.append(bullet)
        
        return bullets
    
    def _validate_and_enhance_bullets(self, 
                                    generated_bullets: List[str], 
                                    existing_bullets: List[str], 
                                    target_count: int) -> List[str]:
        """Validate generated bullets and enhance if needed"""
        
        validated_bullets = []
        
        # Check each generated bullet for quality and metric preservation
        for bullet in generated_bullets:
            if self._is_valid_bullet(bullet):
                validated_bullets.append(bullet)
        
        # If we don't have enough quality bullets, enhance with existing ones
        if len(validated_bullets) < target_count:
            for existing_bullet in existing_bullets:
                if len(validated_bullets) >= target_count:
                    break
                if existing_bullet not in validated_bullets:
                    validated_bullets.append(existing_bullet)
        
        # Ensure critical metrics are preserved
        validated_bullets = self._ensure_metric_preservation(validated_bullets, existing_bullets)
        
        return validated_bullets
    
    def _is_valid_bullet(self, bullet: str) -> bool:
        """Check if bullet meets quality standards"""
        
        if len(bullet) < 30:  # Too short
            return False
        
        if not any(verb in bullet[:20] for verb in ['Built', 'Led', 'Achieved', 'Generated', 'Automated', 'Orchestrated', 'Streamlined', 'Increased', 'Reduced']):
            return False  # No strong action verb
        
        # Should have some quantification
        has_number = any(char.isdigit() for char in bullet)
        if not has_number:
            return False
        
        return True
    
    def _ensure_metric_preservation(self, validated_bullets: List[str], existing_bullets: List[str]) -> List[str]:
        """Ensure critical metrics are preserved in bullets"""
        
        # Find metrics in existing bullets
        existing_metrics = set()
        for bullet in existing_bullets:
            for metric in self.critical_metrics:
                if metric in bullet:
                    existing_metrics.add(metric)
        
        # Check if metrics are preserved in validated bullets
        validated_text = ' '.join(validated_bullets)
        missing_metrics = []
        
        for metric in existing_metrics:
            if metric not in validated_text:
                missing_metrics.append(metric)
        
        # If critical metrics are missing, prioritize bullets that contain them
        if missing_metrics:
            self.logger.warning(f"Missing critical metrics: {missing_metrics}")
            
            # Find existing bullets with missing metrics
            for existing_bullet in existing_bullets:
                if any(metric in existing_bullet for metric in missing_metrics):
                    if existing_bullet not in validated_bullets:
                        validated_bullets.append(existing_bullet)
                        # Remove less important bullets if needed
                        if len(validated_bullets) > 8:
                            validated_bullets = validated_bullets[:8]
        
        return validated_bullets
    
    def _enhance_existing_bullets(self, existing_bullets: List[str], role_strategy: Dict) -> List[str]:
        """Fallback: enhance existing bullets when AI generation fails"""
        
        target_count = role_strategy.get('bullet_count', 6)
        emphasis = role_strategy.get('emphasis', 'comprehensive')
        
        enhanced_bullets = []
        
        for bullet in existing_bullets[:target_count]:
            # Apply minor enhancements based on strategy
            enhanced_bullet = bullet
            
            if emphasis == 'comprehensive':
                # Add context where appropriate
                enhanced_bullet = enhanced_bullet.replace(
                    'Built AI-powered RAG knowledge system',
                    'Built AI-powered RAG knowledge system using pgvector and prompt engineering'
                )
                
            elif emphasis == 'platform_scale':
                # Emphasize scale aspects
                enhanced_bullet = enhanced_bullet.replace(
                    'Led end-to-end product',
                    'Scaled and led end-to-end product'
                )
            
            enhanced_bullets.append(enhanced_bullet)
        
        return enhanced_bullets
    
    def _analyze_enhancements(self, original_bullets: List[str], strategic_bullets: List[str]) -> List[str]:
        """Analyze what enhancements were made"""
        
        enhancements = []
        
        # Compare bullet count
        if len(strategic_bullets) > len(original_bullets):
            enhancements.append(f"Expanded from {len(original_bullets)} to {len(strategic_bullets)} bullets")
        
        # Check for new technical details
        original_text = ' '.join(original_bullets).lower()
        strategic_text = ' '.join(strategic_bullets).lower()
        
        new_tech_terms = ['pgvector', 'prompt engineering', 'mulesoft', 'cross-functional']
        for term in new_tech_terms:
            if term in strategic_text and term not in original_text:
                enhancements.append(f"Added technical context: {term}")
        
        # Check for enhanced metrics
        if 'sub-second response' in strategic_text and 'sub-second' not in original_text:
            enhancements.append("Added performance metrics")
        
        return enhancements
    
    def _extract_preserved_metrics(self, bullets: List[str]) -> List[str]:
        """Extract preserved metrics from bullet points"""
        
        preserved_metrics = []
        bullets_text = ' '.join(bullets)
        
        for metric in self.critical_metrics:
            if metric in bullets_text:
                preserved_metrics.append(metric)
        
        return preserved_metrics
    
    def generate_role_specific_bullets(self, 
                                     role_type: str, 
                                     application_strategy: ApplicationStrategy,
                                     target_count: int = 8) -> List[str]:
        """Generate role-specific bullet points for specific scenarios"""
        
        if role_type == "current_pm":
            return self._generate_current_pm_bullets(application_strategy, target_count)
        elif role_type == "previous_pm":
            return self._generate_previous_pm_bullets(application_strategy, target_count)
        elif role_type == "technical":
            return self._generate_technical_bullets(application_strategy, target_count)
        
        return []
    
    def _generate_current_pm_bullets(self, application_strategy: ApplicationStrategy, target_count: int) -> List[str]:
        """Generate comprehensive bullets for current PM role"""
        
        prompt = f"""
        Generate comprehensive bullets for current Senior Product Manager role.
        
        STRATEGIC FOCUS: {application_strategy.differentiation_angle}
        VALUE PROPOSITION: {application_strategy.value_proposition}
        
        COMPREHENSIVE PROJECT DATA:
        - Built AI-powered RAG knowledge system achieving 94% accuracy serving 200+ users
        - Automated Salesforce-SAP-MuleSoft integration reducing 42 days→10 minutes, $2M revenue
        - Orchestrated cross-functional automation across 15+ operational processes
        - Achieved 60% support ticket reduction, saved 50+ resource hours daily
        - Led VO product revamp achieving 10X adoption growth
        - Implemented IVR integration improving lead conversion 50%, 5X generation
        - Enhanced invoicing from 21 days to real-time, 35% accuracy improvement
        - Designed automated sales workflows with error detection
        
        Generate {target_count} high-impact bullets using Action-Impact-Measurement format.
        Preserve ALL metrics. Use power verbs. Focus on {application_strategy.differentiation_angle} positioning.
        """
        
        response = llm_service.call_openai(prompt, model=self.bullet_model, max_tokens=1000)
        
        if response.success:
            return self._parse_bullets_from_response(response.content)[:target_count]
        
        # Fallback bullets
        return [
            "Built AI-powered RAG knowledge system using pgvector and prompt engineering, achieving 94% accuracy with sub-second response times serving 200+ employees with 1,500+ weekly queries",
            "Automated contract activation workflow through Salesforce-SAP-MuleSoft integration, reducing processing timeline by 99.6% from 42 days to 10 minutes and accelerating $2M revenue recognition",
            "Orchestrated cross-functional automation initiatives across 15+ operational processes, achieving 60% support ticket reduction and saving 50+ resource hours daily through intelligent workflow optimization",
            "Led complete VO product revamp implementing digital KYC and automated workflows, achieving 10X product adoption growth and reducing client onboarding from days to 10 minutes",
            "Implemented IVR integration strategy and automated lead routing system, improving lead-to-conversion speed by 50% and increasing overall lead generation by 5X",
            "Enhanced invoicing system through comprehensive Salesforce-SAP integration, reducing processing time from 21 days to real-time execution with 35% accuracy improvement",
            "Designed and deployed automated sales workflows with error detection and process optimization, saving 50+ resource hours daily while minimizing manual errors",
            "Streamlined enterprise invoice processing through complete system integration, reducing cycles from weeks to real-time execution with enhanced accuracy controls"
        ][:target_count]
    
    def get_bullet_analytics(self, bullets: List[str]) -> Dict:
        """Analyze bullet point quality and characteristics"""
        
        total_bullets = len(bullets)
        
        # Count metrics
        metric_count = 0
        for bullet in bullets:
            if any(metric in bullet for metric in self.critical_metrics):
                metric_count += 1
        
        # Analyze action verbs
        action_verbs = ['Built', 'Led', 'Achieved', 'Generated', 'Automated', 'Orchestrated', 'Streamlined']
        verb_usage = {verb: sum(1 for bullet in bullets if verb in bullet) for verb in action_verbs}
        
        # Calculate average length
        avg_length = sum(len(bullet.split()) for bullet in bullets) / total_bullets if bullets else 0
        
        return {
            "total_bullets": total_bullets,
            "quantified_bullets": metric_count,
            "quantification_rate": round(metric_count / total_bullets * 100, 1) if bullets else 0,
            "average_word_length": round(avg_length, 1),
            "action_verb_distribution": verb_usage,
            "critical_metrics_preserved": len([m for m in self.critical_metrics if any(m in bullet for bullet in bullets)]),
            "quality_score": self._calculate_quality_score(bullets)
        }
    
    def _calculate_quality_score(self, bullets: List[str]) -> float:
        """Calculate overall quality score for bullet points"""
        
        if not bullets:
            return 0.0
        
        score = 0.0
        
        # Quantification score (40% of total)
        quantified_count = sum(1 for bullet in bullets if any(char.isdigit() for char in bullet))
        quantification_score = (quantified_count / len(bullets)) * 0.4
        
        # Action verb score (30% of total)
        action_verbs = ['Built', 'Led', 'Achieved', 'Generated', 'Automated', 'Orchestrated']
        verb_count = sum(1 for bullet in bullets if any(verb in bullet for verb in action_verbs))
        verb_score = (verb_count / len(bullets)) * 0.3
        
        # Length score (20% of total) - prefer 15-25 words
        word_counts = [len(bullet.split()) for bullet in bullets]
        optimal_length_count = sum(1 for count in word_counts if 15 <= count <= 25)
        length_score = (optimal_length_count / len(bullets)) * 0.2
        
        # Critical metric preservation (10% of total)
        preserved_metrics = sum(1 for metric in self.critical_metrics if any(metric in bullet for bullet in bullets))
        metric_score = min(preserved_metrics / 5, 1.0) * 0.1  # Max 5 key metrics
        
        total_score = quantification_score + verb_score + length_score + metric_score
        
        return round(total_score, 2)

# Export the dynamic experience generator
__all__ = ['DynamicExperienceGenerator', 'ExperienceEnhancement', 'BulletPointStrategy']