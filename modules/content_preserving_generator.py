"""
Content Preserving Generator
Ensures all original resume content is preserved while enhancing for job alignment
"""

import json
import re
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from .country_config import CountryConfig
try:
    from .llm_agents import AgentOrchestrator, SkillsAnalyzer, ContentOptimizer, CulturalToneAdapter
except ImportError:
    from llm_agents import AgentOrchestrator, SkillsAnalyzer, ContentOptimizer, CulturalToneAdapter

class ContentPreservingGenerator:
    """Preserves all original content while enhancing for job requirements"""
    
    def __init__(self):
        self.country_config = CountryConfig()
        self.load_user_profile()
        self.agent_orchestrator = AgentOrchestrator()
        self.skills_analyzer = SkillsAnalyzer()
        
    def load_user_profile(self):
        """Load user profile from JSON file"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.user_profile = json.load(f)
    
    def generate_full_resume(self, jd_data: Dict, country: str) -> Tuple[Dict[str, Any], List[str]]:
        """Generate resume preserving ALL original content while enhancing for JD"""
        
        changes_made = []
        
        # Step 1: Analyze job requirements
        skills_analysis = self.skills_analyzer.analyze_skills_alignment(
            self._extract_user_skills(),
            self._prepare_jd_requirements(jd_data)
        )
        
        # Step 2: Generate customized title based on JD
        customized_title = self._generate_job_specific_title(jd_data, skills_analysis)
        changes_made.append(f"Customized title based on job requirements: {customized_title}")
        
        # Step 3: Preserve and enhance summary
        enhanced_summary = self._preserve_and_enhance_summary(jd_data, country)
        changes_made.append("Enhanced summary while preserving all original metrics")
        
        # Step 4: Preserve ALL experience content with enhancements
        enhanced_experience = self._preserve_and_enhance_experience(jd_data)
        changes_made.append(f"Enhanced {len(enhanced_experience)} roles while preserving all content")
        
        # Step 5: Generate comprehensive skills section
        skills_section = self._generate_comprehensive_skills(jd_data, skills_analysis)
        changes_made.append("Generated job-aligned skills section")
        
        # Assemble resume data
        resume_data = {
            'personal_info': {
                'name': self.user_profile['personal_info']['name'],
                'title': customized_title,
                'phone': self.user_profile['personal_info']['phone'],
                'email': self.user_profile['personal_info']['email'],
                'linkedin': self.user_profile['personal_info']['linkedin'],
                'location': self.user_profile['personal_info']['location']
            },
            'summary': enhanced_summary,
            'skills': skills_section,
            'experience': enhanced_experience,
            'education': self.user_profile['education']
        }
        
        return resume_data, changes_made
    
    def _generate_job_specific_title(self, jd_data: Dict, skills_analysis) -> str:
        """Generate job-specific title - use 'Senior Product Manager' unless B2B SaaS specific"""
        
        # Analyze JD requirements for B2B SaaS specific focus
        jd_text = ' '.join([
            jd_data.get('job_description', ''),
            ' '.join(jd_data.get('required_skills', [])),
            ' '.join(jd_data.get('preferred_skills', []))
        ]).lower()
        
        # Only add specializations if the JD is specifically for B2B SaaS roles
        if any(term in jd_text for term in ['b2b saas', 'enterprise saas', 'saas platform', 'saas product']):
            base_title = "Senior Product Manager - "
            specializations = []
            
            # Check for specific focuses mentioned in JD
            if any(term in jd_text for term in ['ai', 'ml', 'artificial intelligence', 'machine learning', 'automation']):
                specializations.append("AI Automation")
            
            if any(term in jd_text for term in ['system', 'integration', 'api', 'technical']):
                specializations.append("System Integration")
            
            if any(term in jd_text for term in ['enterprise', 'saas', 'platform']):
                specializations.append("Enterprise SaaS")
            
            # Use top 2 most relevant specializations for B2B SaaS roles
            if specializations:
                return base_title + " | ".join(specializations[:2])
        
        # For all other roles, just use "Senior Product Manager"
        return "Senior Product Manager"
    
    def _preserve_and_enhance_summary(self, jd_data: Dict, country: str) -> str:
        """Preserve original summary content while enhancing for JD alignment"""
        
        original_summary = self.user_profile.get('summary', '')
        
        # Extract and preserve all metrics from original summary
        metrics = re.findall(r'\\d+%|\\$\\d+[KMB]?|\\d+[KMB]\\+?|\\d+ days?|\\d+ hours?|\\d+\\+', original_summary)
        
        # Key elements to preserve
        core_elements = {
            'years_experience': "11 years in technology (7 in PM)",
            'key_metrics': "94% accuracy serving 200+ users",
            'automation_impact': "42 days to 10 minutes (accelerating $2M revenue)",
            'daily_savings': "50+ resource hours daily"
        }
        
        # Customize based on JD focus while preserving metrics
        jd_text = jd_data.get('job_description', '').lower()
        
        if any(term in jd_text for term in ['internal', 'operations', 'tools']):
            # Emphasize operations tools experience
            enhanced_summary = f"""Senior Product Manager with 11 years in technology (7 in PM) specializing in internal operations tools, workflow automation, and enterprise SaaS platforms. Built AI-powered systems achieving 94% accuracy serving 200+ users, automated cross-functional workflows reducing timelines from 42 days to 10 minutes (accelerating $2M revenue), and streamlined operations saving 50+ resource hours daily. Expert in system integration, cross-functional leadership, and scaling processes for global teams."""
        
        elif any(term in jd_text for term in ['ai', 'ml', 'artificial intelligence']):
            # Emphasize AI/ML experience
            enhanced_summary = f"""Senior Product Manager with 11 years in technology (7 in PM) specializing in AI/ML systems, RAG architecture, and intelligent automation across enterprise platforms. Built AI knowledge system achieving 94% accuracy serving 200+ users, automated workflows reducing timelines from 42 days to 10 minutes (accelerating $2M revenue), and developed ML-powered contract automation saving 50+ resource hours daily. Expert in RAG systems, vector databases, LLM integration, Salesforce/SAP automation, and data-driven product strategy in Agile/SAFe environments."""
        
        else:
            # Use enhanced version of original summary
            enhanced_summary = original_summary
        
        return enhanced_summary
    
    def _preserve_and_enhance_experience(self, jd_data: Dict) -> List[Dict[str, Any]]:
        """Preserve ALL original experience content while adding major projects for completeness"""
        
        original_experience = self.user_profile.get('experience', [])
        enhanced_experience = []
        
        for i, role in enumerate(original_experience):
            enhanced_role = {
                'title': role.get('title', ''),
                'company': role.get('company', ''),
                'duration': role.get('duration', ''),
                'location': role.get('location', ''),
                'highlights': []
            }
            
            # Preserve ALL original highlights while enhancing context
            original_highlights = role.get('highlights', [])
            
            for highlight in original_highlights:
                enhanced_highlight = self._enhance_highlight_for_jd(highlight, jd_data)
                enhanced_role['highlights'].append(enhanced_highlight)
            
            # For the first Product Manager role (current), add major projects if they're missing
            if i == 0 and ('Product Manager' in role.get('title', '')) and len(enhanced_role['highlights']) < 8:
                self._add_major_project_highlights(enhanced_role, jd_data)
            
            # For the second Product Manager role, ensure Converge F&B platform is included
            elif i == 1 and role.get('title', '') == 'Product Manager' and not any('30,000' in h or 'converge' in h.lower() for h in enhanced_role['highlights']):
                self._add_converge_platform_highlights(enhanced_role)
            
            enhanced_experience.append(enhanced_role)
        
        return enhanced_experience
    
    def _enhance_highlight_for_jd(self, original_highlight: str, jd_data: Dict) -> str:
        """Enhance individual highlight while preserving all original content"""
        
        jd_text = jd_data.get('job_description', '').lower()
        enhanced = original_highlight
        
        # Add context for internal operations tools if relevant
        if 'built ai' in original_highlight.lower() and any(term in jd_text for term in ['internal', 'operations', 'tools']):
            enhanced = original_highlight.replace(
                'Built AI-powered RAG knowledge system',
                'Built AI-powered internal operations system with RAG knowledge base'
            )
        
        # Add cross-functional context where appropriate
        if 'automated' in original_highlight.lower() and 'cross-functional' in jd_text:
            enhanced = enhanced.replace(
                'Automated',
                'Led cross-functional teams to automate'
            )
        
        # Add system integration context for Salesforce/SAP mentions
        if all(term in original_highlight for term in ['Salesforce', 'SAP']) and 'integration' in jd_text:
            enhanced = enhanced.replace(
                'integrating Salesforce, SAP',
                'integrating Salesforce, SAP, and internal systems'
            )
        
        # Add workflow context where relevant
        if 'workflows' in original_highlight.lower() and 'workflow' in jd_text:
            enhanced = enhanced.replace(
                'workflows',
                'cross-functional workflows'
            )
        
        return enhanced
    
    def _add_major_project_highlights(self, role: Dict[str, Any], jd_data: Dict):
        """Add major project highlights from detailed projects to ensure completeness"""
        
        # Load detailed projects from extracted profile
        try:
            extracted_path = Path(__file__).parent.parent / "data" / "extracted_profile.json"
            with open(extracted_path, 'r', encoding='utf-8') as f:
                extracted_data = json.load(f)
            detailed_projects = extracted_data.get('detailed_projects', [])
        except:
            detailed_projects = []
        
        # Current achievements from your latest resume that should be included
        missing_achievements = []
        
        # Check if VO Product revamp is missing
        if not any('10X growth' in h or 'VO product' in h for h in role['highlights']):
            missing_achievements.append("Led complete VO product revamp implementing digital KYC and automated workflows, achieving 10X product adoption growth and reducing client onboarding from days to 10 minutes with 100% digital verification")
        
        # Check if lead generation improvements are missing  
        if not any('lead-to-conversion' in h or '5X' in h for h in role['highlights']):
            missing_achievements.extend([
                "Implemented IVR integration strategy and automated lead routing system, improving lead-to-conversion speed by 50% and increasing overall lead generation by 5X with enhanced qualification process",
                "Designed and deployed automated sales workflows with error detection and process optimization, saving 50+ resource hours daily while minimizing manual errors and reducing sales cycle delays"
            ])
        
        # Check if invoicing enhancement is missing
        if not any('invoicing' in h.lower() or '21 days to real-time' in h for h in role['highlights']):
            missing_achievements.append("Enhanced invoicing system through comprehensive Salesforce-SAP integration and automated workflow design, reducing processing time from 21 days to real-time execution and achieving 35% improvement in contract accuracy")
        
        # Add missing achievements to reach 8 total bullet points
        for achievement in missing_achievements:
            if len(role['highlights']) < 8:
                role['highlights'].append(achievement)
    
    def _add_converge_platform_highlights(self, role: Dict[str, Any]):
        """Add Converge F&B platform highlights which are major achievements"""
        projects = self.user_profile.get('projects', {})
        
        if 'converge_fnb_platform' in projects:
            converge_project = projects['converge_fnb_platform']
            # Add the major platform achievement
            role['highlights'].insert(0, 
                "Led end-to-end product strategy for Converge F&B ordering platform serving 600,000+ users across 24 business parks with 30,000+ daily orders achieving ₹168-180 crores annual GMV"
            )
            # Add the scaling achievement  
            role['highlights'].insert(1,
                "Scaled Converge platform from MVP to full production in 6 months achieving 91% NPS and ₹1.5/sq ft revenue optimization"
            )
    
    def _generate_comprehensive_skills(self, jd_data: Dict, skills_analysis) -> str:
        """Generate comprehensive skills section without categories"""
        
        # Get all user skills
        all_user_skills = []
        for category_skills in self.user_profile.get('skills', {}).values():
            if isinstance(category_skills, list):
                all_user_skills.extend(category_skills)
        
        # Get priority skills from AI analysis
        priority_skills = []
        if skills_analysis.success:
            priority_skills = skills_analysis.data.get('priority_skills', [])
        
        # Combine and prioritize skills
        prioritized_skills = []
        
        # Add priority skills first
        for skill in priority_skills:
            matching_user_skills = [s for s in all_user_skills if skill.lower() in s.lower() or s.lower() in skill.lower()]
            prioritized_skills.extend(matching_user_skills)
        
        # Add remaining relevant skills
        jd_keywords = ' '.join([
            jd_data.get('job_description', ''),
            ' '.join(jd_data.get('required_skills', [])),
            ' '.join(jd_data.get('preferred_skills', []))
        ]).lower()
        
        for skill in all_user_skills:
            if skill not in prioritized_skills:
                # Check if skill is relevant to JD
                skill_words = skill.lower().split()
                if any(word in jd_keywords for word in skill_words):
                    prioritized_skills.append(skill)
        
        # Add remaining skills to ensure comprehensive coverage
        for skill in all_user_skills:
            if skill not in prioritized_skills and len(prioritized_skills) < 25:
                prioritized_skills.append(skill)
        
        # Return skills as pipe-separated string (for compatibility)
        return " | ".join(prioritized_skills[:20])
    
    def _extract_user_skills(self) -> List[str]:
        """Extract all user skills from profile"""
        all_skills = []
        skills_data = self.user_profile.get('skills', {})
        
        for category in skills_data.values():
            if isinstance(category, list):
                all_skills.extend(category)
        
        return all_skills
    
    def _prepare_jd_requirements(self, jd_data: Dict) -> Dict[str, Any]:
        """Prepare job description data for skills analysis"""
        return {
            'required_skills': jd_data.get('required_skills', []),
            'preferred_skills': jd_data.get('preferred_skills', []),
            'focus_areas': jd_data.get('focus_areas', []),
            'company_context': jd_data.get('company_description', ''),
            'role_emphasis': jd_data.get('role_focus', '')
        }

    def generate_dynamic_resume(self, jd_data: Dict, application_strategy: 'ApplicationStrategy') -> Tuple[Dict[str, Any], List[str]]:
        """Generate strategically optimized resume using application strategy"""
        
        try:
            # Import dynamic generators (avoid circular imports)
            from .dynamic_summary_generator import DynamicSummaryGenerator
            from .dynamic_experience_generator import DynamicExperienceGenerator
            
            dynamic_summary_gen = DynamicSummaryGenerator()
            dynamic_experience_gen = DynamicExperienceGenerator()
            
            changes_made = []
            
            # Step 1: Generate strategic summary
            strategic_summary = dynamic_summary_gen.generate_strategic_summary(jd_data, application_strategy)
            changes_made.append("Generated strategic summary using AI optimization")
            
            # Step 2: Generate strategic experience
            strategic_experience_list = dynamic_experience_gen.generate_strategic_experience(jd_data, application_strategy)
            
            # Convert to standard format
            enhanced_experience = []
            for exp_enhancement in strategic_experience_list:
                enhanced_experience.append({
                    'title': exp_enhancement.role_title,
                    'company': exp_enhancement.company,
                    'duration': exp_enhancement.duration,
                    'location': exp_enhancement.location,
                    'highlights': exp_enhancement.strategic_bullets
                })
            
            changes_made.append(f"Generated {len(enhanced_experience)} roles with strategic optimization")
            
            # Step 3: Generate strategic title
            strategic_title = application_strategy.title_recommendation
            changes_made.append(f"Applied strategic title: {strategic_title}")
            
            # Step 4: Generate strategic skills
            strategic_skills = self._generate_strategic_skills_from_strategy(application_strategy)
            changes_made.append("Generated strategic skills alignment")
            
            # Assemble strategic resume data
            resume_data = {
                'personal_info': {
                    'name': self.user_profile['personal_info']['name'],
                    'title': strategic_title,
                    'phone': self.user_profile['personal_info']['phone'],
                    'email': self.user_profile['personal_info']['email'],
                    'linkedin': self.user_profile['personal_info']['linkedin'],
                    'location': self.user_profile['personal_info']['location']
                },
                'summary': strategic_summary,
                'skills': strategic_skills,
                'experience': enhanced_experience,
                'education': self.user_profile['education']
            }
            
            return resume_data, changes_made
            
        except Exception as e:
            # Fallback to standard generation if dynamic fails
            print(f"   ⚠️  Dynamic generation failed: {e}, falling back to standard")
            return self.generate_full_resume(jd_data, jd_data.get('country', 'netherlands'))
    
    def _generate_strategic_skills_from_strategy(self, application_strategy: 'ApplicationStrategy') -> str:
        """Generate strategic skills based on application strategy"""
        
        # Extract skills from priority strengths
        priority_skills = []
        
        for strength_mapping in application_strategy.priority_strengths[:6]:
            # Map strength descriptions to actual skills
            strength_text = strength_mapping.user_strength.lower()
            
            if 'automation' in strength_text:
                priority_skills.extend(['Process Automation', 'Workflow Optimization'])
            elif 'ai' in strength_text or 'rag' in strength_text:
                priority_skills.extend(['AI/ML Systems', 'RAG Architecture'])
            elif 'cross-functional' in strength_text:
                priority_skills.append('Cross-functional Leadership')
            elif 'revenue' in strength_text or 'growth' in strength_text:
                priority_skills.append('Revenue Growth')
            elif 'integration' in strength_text:
                priority_skills.extend(['API Integration', 'System Integration'])
            elif 'platform' in strength_text:
                priority_skills.append('Platform Development')
        
        # Add core PM skills
        core_pm_skills = ['Product Strategy', 'Product Management', 'Stakeholder Management', 'Agile/SAFe']
        
        # Get relevant technical skills from user profile
        all_user_skills = []
        for category_skills in self.user_profile.get('skills', {}).values():
            if isinstance(category_skills, list):
                all_user_skills.extend(category_skills)
        
        # Select technical skills that align with strategy themes
        strategy_themes = [theme.lower() for theme in application_strategy.content_themes]
        relevant_tech_skills = []
        
        for skill in all_user_skills:
            skill_lower = skill.lower()
            if any(theme in skill_lower for theme in strategy_themes):
                relevant_tech_skills.append(skill)
        
        # Combine and deduplicate
        all_skills = priority_skills + core_pm_skills + relevant_tech_skills[:8]
        unique_skills = []
        seen = set()
        
        for skill in all_skills:
            if skill.lower() not in seen:
                unique_skills.append(skill)
                seen.add(skill.lower())
        
        # Limit to 15-20 skills for readability
        return ' • '.join(unique_skills[:18])

# Export the content preserving generator
__all__ = ['ContentPreservingGenerator']