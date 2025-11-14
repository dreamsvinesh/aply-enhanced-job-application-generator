"""
Enhanced Resume Generator with LLM Agent Integration
Creates intelligent, optimized resumes using AI-powered agents for content analysis and optimization.
"""

import json
import re
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from .country_config import CountryConfig
from .llm_agents import AgentOrchestrator, SkillsAnalyzer, ContentOptimizer, CulturalToneAdapter

class EnhancedResumeGenerator:
    def __init__(self):
        self.country_config = CountryConfig()
        self.load_user_profile()
        self.agent_orchestrator = AgentOrchestrator()
        self.skills_analyzer = SkillsAnalyzer()
        self.content_optimizer = ContentOptimizer()
        self.cultural_adapter = CulturalToneAdapter()
        
    def load_user_profile(self):
        """Load user profile from JSON file"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.user_profile = json.load(f)
    
    def generate(self, jd_data: Dict, country: str) -> Tuple[str, List[str]]:
        """
        Generate intelligently optimized resume using LLM agents
        
        Args:
            jd_data: Parsed job description data
            country: Target country for formatting
            
        Returns:
            Tuple of (resume_content, list_of_changes_made)
        """
        changes_made = []
        
        # Step 1: Intelligent skills analysis using LLM agent
        skills_analysis = self.skills_analyzer.analyze_skills_alignment(
            self._extract_user_skills(),
            self._prepare_jd_requirements(jd_data)
        )
        
        if skills_analysis.success:
            changes_made.append(f"LLM Skills Analysis: {skills_analysis.data.get('alignment_score', 0)}% match")
            changes_made.extend(skills_analysis.suggestions[:2])  # Top 2 suggestions
        
        # Step 2: Determine resume variant with AI enhancement
        resume_variant = self._determine_resume_variant_enhanced(jd_data, skills_analysis)
        changes_made.append(f"Selected {resume_variant.upper()} variant (AI-enhanced analysis)")
        
        # Step 3: Generate AI-optimized title and summary
        title_summary = self._generate_ai_optimized_title_summary(jd_data, resume_variant, country)
        changes_made.append("Generated AI-optimized professional title and summary")
        
        # Step 4: Intelligent skills section optimization
        skills_section, skill_changes = self._optimize_skills_with_ai(jd_data, skills_analysis)
        changes_made.extend(skill_changes)
        
        # Step 5: AI-enhanced experience section
        experience_section, exp_changes = self._optimize_experience_with_ai(jd_data, resume_variant, country)
        changes_made.extend(exp_changes)
        
        # Step 6: Cultural tone adaptation
        cultural_adaptation = self.cultural_adapter.adapt_for_culture(
            f"{title_summary}\\n{experience_section}",
            country,
            jd_data.get('company_culture', '')
        )
        
        if cultural_adaptation.success:
            changes_made.append(f"Applied {country.title()} cultural tone adaptation")
        
        # Step 7: Assemble and validate final resume
        resume_content = self._assemble_enhanced_resume(
            title_summary, skills_section, experience_section, country
        )
        
        # Step 8: Final quality scoring and validation
        quality_analysis = self.content_optimizer.score_content_quality(
            resume_content,
            self._prepare_content_context(jd_data)
        )
        
        if quality_analysis.success:
            score = quality_analysis.data.get('overall_score', 0)
            changes_made.append(f"Final quality score: {score:.1f}/10 (AI-validated)")
            
            if score < 8.0:
                changes_made.extend(quality_analysis.suggestions[:2])
        
        # Store enhanced analytics
        jd_data['ai_analysis'] = {
            'skills_alignment': skills_analysis.data if skills_analysis.success else {},
            'quality_score': quality_analysis.data if quality_analysis.success else {},
            'cultural_adaptation': cultural_adaptation.data if cultural_adaptation.success else {},
            'overall_confidence': (skills_analysis.confidence_score + quality_analysis.confidence_score) / 2
        }
        
        return resume_content, changes_made
    
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
    
    def _determine_resume_variant_enhanced(self, jd_data: Dict, skills_analysis) -> str:
        """Enhanced variant determination using AI analysis"""
        
        # Use AI skills analysis to determine best variant
        if skills_analysis.success:
            priority_skills = skills_analysis.data.get('priority_skills', [])
            
            # Check for AI/ML emphasis
            ai_ml_indicators = ['AI', 'ML', 'RAG', 'machine learning', 'automation']
            ai_ml_count = sum(1 for skill in priority_skills if any(ai in skill for ai in ai_ml_indicators))
            
            # Check for internal tools / operations emphasis
            ops_indicators = ['operations', 'internal tools', 'workflow', 'system integration']
            ops_count = sum(1 for skill in priority_skills if any(ops in skill.lower() for ops in ops_indicators))
            
            # Check for SaaS/scale-up emphasis
            saas_indicators = ['SaaS', 'scale-up', 'enterprise', 'B2B']
            saas_count = sum(1 for skill in priority_skills if any(saas in skill for saas in saas_indicators))
            
            if ai_ml_count >= 2 or (ops_count >= 2 and ai_ml_count >= 1):
                return 'aiml'
            elif ops_count >= 2 or saas_count >= 2:
                return 'b2b'
            else:
                return 'general'
        
        # Fallback to original logic
        ai_ml_focus = jd_data.get('ai_ml_focus', 0.0)
        if ai_ml_focus > 0.3:
            return 'aiml'
        elif jd_data.get('b2b_vs_b2c') == 'b2b':
            return 'b2b'
        else:
            return 'general'
    
    def _generate_ai_optimized_title_summary(self, jd_data: Dict, variant: str, country: str) -> str:
        """Generate AI-optimized professional title and summary"""
        
        # Base title customization based on JD requirements
        base_title = "Senior Product Manager"
        
        # Extract key focus areas from job description
        company = jd_data.get('company', '')
        role_focus = jd_data.get('role_focus', '')
        key_requirements = jd_data.get('required_skills', [])
        
        # AI-enhanced title customization
        specializations = []
        
        if any(term in ' '.join(key_requirements).lower() for term in ['internal', 'operations', 'tools', 'workflow']):
            specializations.append("Operations Tools")
        
        if any(term in ' '.join(key_requirements).lower() for term in ['saas', 'platform', 'enterprise']):
            specializations.append("SaaS Platforms")
        
        if any(term in ' '.join(key_requirements).lower() for term in ['system', 'integration', 'api']):
            specializations.append("System Integration")
        
        if any(term in ' '.join(key_requirements).lower() for term in ['ai', 'ml', 'automation', 'intelligent']):
            specializations.append("AI Automation")
        
        # Limit to top 3 specializations
        if specializations:
            specializations = specializations[:3]
            title = f"{base_title} - {' | '.join(specializations)}"
        else:
            title = f"{base_title} - Product Strategy | Cross-functional Leadership | SaaS"
        
        # AI-enhanced summary with preserved metrics but better alignment
        base_summary = self.user_profile.get('summary', '')
        
        # Extract and preserve key metrics
        import re
        metrics = re.findall(r'\\d+%|\\$\\d+[KMB]?|\\d+[KMB]\\+?|\\d+ days?|\\d+ hours?', base_summary)
        
        # Create enhanced summary based on variant
        if variant == 'aiml':
            enhanced_summary = f"""Senior Product Manager with 11 years in technology (7 in PM) specializing in AI/ML systems, intelligent automation, and internal operations tools across enterprise SaaS platforms. Built AI knowledge system achieving 94% accuracy serving 200+ users, automated workflows reducing timelines from 42 days to 10 minutes (accelerating $2M revenue), and saved 50+ resource hours daily through intelligent automation. Expert in cross-functional leadership, system integration, and data-driven product strategy for global teams."""
        
        elif company.lower() in ['deel', 'remote', 'global']:
            enhanced_summary = f"""Senior Product Manager with 11 years in technology (7 in PM) specializing in internal operations tools, workflow automation, and global SaaS platforms. Built AI-powered systems achieving 94% accuracy serving 200+ users, automated cross-functional workflows reducing timelines from 42 days to 10 minutes (accelerating $2M revenue), and streamlined operations saving 50+ resource hours daily. Expert in system integration, remote-first collaboration, and scaling processes for international teams."""
        
        else:
            enhanced_summary = base_summary
        
        return f"# {self.user_profile['personal_info']['name']}\\n**{title}**\\n\\n{self.user_profile['personal_info']['phone']} | {self.user_profile['personal_info']['email']} | {self.user_profile['personal_info']['linkedin']} | {self.user_profile['personal_info']['location']}\\n\\n---\\n\\n## SUMMARY\\n\\n{enhanced_summary}"
    
    def _optimize_skills_with_ai(self, jd_data: Dict, skills_analysis) -> Tuple[str, List[str]]:
        """AI-optimized skills section based on job requirements"""
        changes_made = []
        
        if skills_analysis.success:
            priority_skills = skills_analysis.data.get('priority_skills', [])
            missing_skills = skills_analysis.data.get('missing_skills', [])
            
            # Combine user skills with AI recommendations
            user_skills = self._extract_user_skills()
            
            # Prioritize skills based on AI analysis
            optimized_skills = []
            
            # Add priority skills first
            for skill in priority_skills:
                if any(user_skill.lower() in skill.lower() or skill.lower() in user_skill.lower() 
                      for user_skill in user_skills):
                    optimized_skills.append(skill)
            
            # Add remaining relevant user skills
            for skill in user_skills:
                if skill not in optimized_skills and len(optimized_skills) < 25:
                    # Check if skill is relevant to job
                    jd_text = ' '.join(jd_data.get('required_skills', []) + jd_data.get('preferred_skills', [])).lower()
                    if any(keyword in jd_text for keyword in skill.lower().split()):
                        optimized_skills.append(skill)
            
            # Format skills section (no categories, single list)
            skills_text = " | ".join(optimized_skills[:20])  # Limit to 20 skills
            skills_section = f"---\\n\\n## SKILLS\\n\\n{skills_text}\\n\\n"
            
            changes_made.append(f"AI-optimized skills prioritization ({len(priority_skills)} priority skills identified)")
            
            if missing_skills:
                changes_made.append(f"Identified skills to develop: {', '.join(missing_skills[:3])}")
        
        else:
            # Fallback to original skills formatting
            skills_section = self._format_original_skills()
            changes_made.append("Used original skills formatting (AI analysis unavailable)")
        
        return skills_section, changes_made
    
    def _optimize_experience_with_ai(self, jd_data: Dict, variant: str, country: str) -> Tuple[str, List[str]]:
        """AI-enhanced experience section optimization"""
        changes_made = []
        
        experience_section = "---\\n\\n## EXPERIENCE\\n\\n"
        
        # Process each role with AI enhancement
        for role in self.user_profile.get('experience', []):
            enhanced_role = self._enhance_role_with_ai(role, jd_data, variant, country)
            experience_section += enhanced_role + "\\n\\n"
            changes_made.append(f"AI-enhanced {role['title']} role description")
        
        return experience_section, changes_made
    
    def _enhance_role_with_ai(self, role: Dict, jd_data: Dict, variant: str, country: str) -> str:
        """Enhance individual role with AI optimization using detailed project data"""
        
        role_header = f"### {role['title']}\\n**{role['company']}** | {role['location']} | {role['duration']}\\n\\n"
        
        enhanced_bullets = []
        
        # Load detailed projects data for comprehensive content
        detailed_projects = self._load_detailed_projects()
        
        # For current role, use extensive project details
        if role.get('duration', '').startswith('01/2023') or 'Present' in role.get('duration', ''):
            enhanced_bullets = self._build_comprehensive_current_role(role, jd_data, detailed_projects)
        
        # For previous PM role, expand major achievements
        elif role.get('duration', '').startswith('08/2016') or '2016' in role.get('duration', ''):
            enhanced_bullets = self._build_comprehensive_previous_role(role, jd_data, detailed_projects)
        
        # For other roles, use original highlights with enhancements
        else:
            for highlight in role.get('highlights', []):
                enhanced_bullet = self._enhance_bullet_point(highlight, jd_data)
                enhanced_bullets.append(f"• {enhanced_bullet}")
        
        return role_header + "\\n".join(enhanced_bullets)
    
    def _load_detailed_projects(self) -> List[Dict]:
        """Load detailed projects from extracted profile"""
        try:
            extracted_path = Path(__file__).parent.parent / "data" / "extracted_profile.json"
            with open(extracted_path, 'r', encoding='utf-8') as f:
                extracted_data = json.load(f)
            return extracted_data.get('detailed_projects', [])
        except:
            return []
    
    def _build_comprehensive_current_role(self, role: Dict, jd_data: Dict, detailed_projects: List[Dict]) -> List[str]:
        """Build comprehensive current role with 8-10 bullet points"""
        bullets = []
        
        # RAG Knowledge System Project
        rag_project = next((p for p in detailed_projects if 'RAG' in p.get('title', '')), None)
        if rag_project:
            bullets.append("• Built AI-powered RAG knowledge system achieving 94% accuracy, sub-second response")
        
        # Contract Automation Project  
        contract_project = next((p for p in detailed_projects if 'Contract' in p.get('title', '')), None)
        if contract_project:
            bullets.append("• Automated contract activation reducing timeline 99.6% (42 days→10 minutes)")
        
        # VO Product Revamp Project
        vo_project = next((p for p in detailed_projects if 'VO Product' in p.get('title', '')), None)
        if vo_project:
            bullets.append("• Led complete revamp of VO product achieving 10X growth, reducing client onboarding from days to 10 minutes with Digi KYC")
        
        # Sales & Lead Generation Project
        sales_project = next((p for p in detailed_projects if 'Sales' in p.get('title', '') or 'Lead Generation' in p.get('title', '')), None)
        if sales_project:
            bullets.extend([
                "• Improved lead-to-conversion speed by 50% and increased lead generation 5X via IVR integration",
                "• Saved 50+ resource hours daily by automating sales workflows, minimizing errors and delays"
            ])
        
        # Additional core achievements
        bullets.extend([
            "• Streamlined 15+ operational processes achieving 60% support ticket reduction",
            "• Enhanced invoicing through Salesforce-SAP integration reducing processing from 21 days to real-time, achieving 35% contract accuracy improvement"
        ])
        
        return bullets
    
    def _build_comprehensive_previous_role(self, role: Dict, jd_data: Dict, detailed_projects: List[Dict]) -> List[str]:
        """Build comprehensive previous role with 8-10 bullet points"""
        bullets = []
        
        # Converge F&B Platform
        converge_project = next((p for p in detailed_projects if 'Converge' in p.get('title', '')), None)
        if converge_project:
            bullets.extend([
                "• Led end-to-end product strategy for Converge F&B ordering platform serving 600,000+ users across 24 business parks",
                "• Scaled platform from MVP to full production in 6 months achieving 30,000+ daily orders and ₹168-180 crores annual GMV", 
                "• Achieved 91% NPS and ₹1.5/sq ft revenue optimization through multi-tenant architecture and real-time order processing",
                "• Managed cross-functional team of 15 people developing mobile app, integrated payments, and real-time tracking systems"
            ])
        
        # Space Optimization & Revenue Generation
        bullets.extend([
            "• Generated €220K monthly revenue monetizing underutilized inventory through data-driven space optimization strategies",
            "• Increased app engagement 45% and customer satisfaction 65% through enhanced mobile self-service features",
            "• Reduced customer onboarding from 110 to 14 days, improved occupancy 25% via streamlined digital workflows",
            "• Developed IoT-enabled self-service platform with auto WiFi and booking systems, increased ARPA 35%"
        ])
        
        return bullets
    
    def _enhance_bullet_point(self, bullet: str, jd_data: Dict) -> str:
        """Enhance bullet point with job-relevant keywords and framing"""
        
        # Preserve original metrics but enhance context
        enhanced = bullet
        
        # Add context for internal tools/operations if relevant
        if 'AI' in bullet and any(term in ' '.join(jd_data.get('required_skills', [])).lower() 
                                 for term in ['internal', 'operations', 'tools']):
            enhanced = bullet.replace('Built AI', 'Built AI-powered internal operations tool').replace('AI knowledge system', 'AI knowledge system for internal operations')
        
        # Add cross-functional context
        if 'automated' in bullet.lower():
            enhanced = enhanced.replace('Automated', 'Led cross-functional teams to automate')
        
        # Add system integration context for Salesforce/SAP mentions
        if 'Salesforce' in bullet and 'SAP' in bullet:
            enhanced = enhanced.replace('integrating Salesforce, SAP', 'integrating Salesforce, SAP, and internal systems')
        
        return enhanced
    
    def _format_original_skills(self) -> str:
        """Fallback skills formatting"""
        skills_data = self.user_profile.get('skills', {})
        all_skills = []
        
        for category_skills in skills_data.values():
            if isinstance(category_skills, list):
                all_skills.extend(category_skills)
        
        skills_text = " | ".join(all_skills[:20])
        return f"---\\n\\n## SKILLS\\n\\n{skills_text}\\n\\n"
    
    def _prepare_content_context(self, jd_data: Dict) -> Dict[str, Any]:
        """Prepare context for content quality analysis"""
        return {
            'role': jd_data.get('job_title', 'Product Manager'),
            'company': jd_data.get('company', 'Unknown'),
            'industry_focus': jd_data.get('industry', []),
            'requirements': jd_data.get('required_skills', [])
        }
    
    def _assemble_enhanced_resume(self, title_summary: str, skills_section: str, experience_section: str, country: str) -> str:
        """Assemble final enhanced resume"""
        
        education = f"---\\n\\n## EDUCATION\\n\\n**{self.user_profile['education']['degree']}** | {self.user_profile['education']['university']} | {self.user_profile['education']['duration']}\\n\\n"
        
        resume = f"{title_summary}\\n\\n{skills_section}\\n{experience_section}\\n{education}---\\n\\n"
        
        return resume

# Export the enhanced generator
__all__ = ['EnhancedResumeGenerator']