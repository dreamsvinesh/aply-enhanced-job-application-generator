"""
Resume Generator Module
Creates tailored resumes based on job requirements with AI/ML emphasis and country-specific formatting.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from .country_config import CountryConfig

class ResumeGenerator:
    def __init__(self):
        self.country_config = CountryConfig()
        self.load_user_profile()
        
    def load_user_profile(self):
        """Load user profile from JSON file"""
        profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.user_profile = json.load(f)
    
    def generate(self, jd_data: Dict, country: str) -> Tuple[str, List[str]]:
        """
        Generate tailored resume based on JD requirements
        
        Args:
            jd_data: Parsed job description data
            country: Target country for formatting
            
        Returns:
            Tuple of (resume_content, list_of_changes_made)
        """
        changes_made = []
        
        # Analyze JD requirements and determine focus
        ai_ml_focus = jd_data.get('ai_ml_focus', 0.0)
        business_model = jd_data.get('b2b_vs_b2c', 'mixed')
        required_skills = jd_data.get('required_skills', [])
        preferred_skills = jd_data.get('preferred_skills', [])
        
        # Determine resume variant to emphasize
        resume_variant = self._determine_resume_variant(ai_ml_focus, business_model, required_skills)
        changes_made.append(f"Selected {resume_variant.upper()} resume variant based on JD analysis")
        
        # Generate optimized summary
        summary = self._generate_optimized_summary(jd_data, resume_variant, country)
        changes_made.append(f"Customized summary to emphasize {resume_variant} experience and AI/ML capabilities")
        
        # Optimize skills section
        skills_section, skill_changes = self._optimize_skills_section(jd_data, country)
        changes_made.extend(skill_changes)
        
        # Optimize experience section
        experience_section, exp_changes = self._optimize_experience_section(jd_data, resume_variant, country)
        changes_made.extend(exp_changes)
        
        # Get country-specific formatting
        country_format = self.country_config.get_resume_format(country)
        
        # Assemble final resume
        resume_content = self._assemble_resume(
            summary, skills_section, experience_section, 
            country_format, country
        )
        
        # Calculate and store ATS match score
        ats_score = self._calculate_ats_score(jd_data, resume_content)
        jd_data['ats_match_score'] = ats_score
        
        # Store matched/missing skills for output
        matched_skills, missing_skills, mapped_skills = self._analyze_skill_gaps(jd_data, resume_content)
        jd_data['matched_skills'] = matched_skills
        jd_data['missing_skills'] = missing_skills 
        jd_data['mapped_skills'] = mapped_skills
        
        if missing_skills:
            changes_made.append(f"Identified missing skills: {', '.join(missing_skills[:3])}{'...' if len(missing_skills) > 3 else ''}")
        
        return resume_content, changes_made
    
    def _determine_resume_variant(self, ai_ml_focus: float, business_model: str, required_skills: List[str]) -> str:
        """Determine which resume variant to emphasize"""
        
        # Check for explicit AI/ML skills in requirements
        ai_ml_keywords = ['ai', 'ml', 'machine learning', 'artificial intelligence', 'rag', 'llm', 
                         'deep learning', 'neural networks', 'tensorflow', 'pytorch', 'nlp']
        ai_ml_in_requirements = any(skill.lower() in ' '.join(required_skills).lower() 
                                   for skill in ai_ml_keywords)
        
        if ai_ml_focus > 0.3 or ai_ml_in_requirements:
            return 'aiml'
        elif business_model == 'b2b':
            return 'b2b'
        elif business_model == 'b2c':
            return 'b2c'
        else:
            return 'b2b'  # Default to B2B
    
    def _generate_optimized_summary(self, jd_data: Dict, variant: str, country: str) -> str:
        """Generate optimized professional summary"""
        
        base_summary = self.user_profile['summary']
        
        # Customize based on variant
        if variant == 'aiml':
            # Emphasize AI/ML projects and capabilities
            summary = f"""Senior Product Manager with 11 years in technology (7 in PM) specializing in **AI/ML systems, RAG architecture, and intelligent automation** across enterprise platforms. Built AI knowledge system achieving **94% accuracy serving 200+ users**, automated workflows reducing timelines from 42 days to 10 minutes (accelerating **$2M revenue**), and developed **ML-powered contract automation** saving 50+ resource hours daily. Expert in **RAG systems, vector databases, LLM integration**, Salesforce/SAP automation, and data-driven product strategy in Agile/SAFe environments."""
            
        elif variant == 'b2b':
            # Emphasize enterprise automation and Salesforce/SAP
            summary = f"""Senior Product Manager with 11 years in technology (7 in PM) specializing in **enterprise automation, Salesforce/SAP integration**, and B2B SaaS platforms. Built AI-powered systems achieving 94% accuracy, **automated contract workflows reducing timelines 99.6% (42 days→10 minutes)** accelerating **$2M revenue**, and streamlined 15+ operational processes achieving 60% support ticket reduction. Expert in **enterprise integration, workflow automation**, cross-functional leadership, and scalable B2B product strategy."""
            
        elif variant == 'b2c':
            # Emphasize mobile engagement and user experience
            summary = f"""Senior Product Manager with 11 years in technology (7 in PM) specializing in **mobile engagement, user experience optimization**, and B2C product innovation. Scaled **Converge F&B platform to 600K+ users with 30K+ daily orders**, achieved **91% NPS and 45% app engagement increase**, and automated user touchpoints serving 200+ users with AI-powered systems. Expert in **user-centric design, mobile optimization**, cross-functional leadership, and data-driven growth strategies."""
        
        # Apply country-specific tone
        summary = self.country_config.adapt_content_tone(summary, country, 'resume')
        
        return summary
    
    def _optimize_skills_section(self, jd_data: Dict, country: str) -> Tuple[str, List[str]]:
        """Optimize skills section based on JD requirements"""
        changes = []
        
        # Get base skills from profile
        profile_skills = self.user_profile['skills']
        required_skills = set(skill.lower() for skill in jd_data.get('required_skills', []))
        preferred_skills = set(skill.lower() for skill in jd_data.get('preferred_skills', []))
        
        # Build optimized skills sections
        optimized_skills = {}
        
        # Product Management skills (always include)
        pm_skills = profile_skills['product_management']
        optimized_skills['Product Management'] = pm_skills[:6]  # Top 6
        
        # AI/ML skills (emphasize based on JD)
        ai_ml_skills = profile_skills['ai_ml'].copy()
        
        # Add missing AI/ML skills from JD if relevant
        missing_ai_skills = self._find_missing_skills(ai_ml_skills, required_skills | preferred_skills, 'ai_ml')
        if missing_ai_skills:
            ai_ml_skills.extend(missing_ai_skills)
            changes.append(f"Added AI/ML skills from JD: {', '.join(missing_ai_skills)}")
        
        optimized_skills['AI/ML & Automation'] = ai_ml_skills[:8]  # Top 8
        
        # Technical skills
        tech_skills = profile_skills['technical'].copy()
        missing_tech_skills = self._find_missing_skills(tech_skills, required_skills | preferred_skills, 'technical')
        if missing_tech_skills:
            tech_skills.extend(missing_tech_skills)
            changes.append(f"Added technical skills from JD: {', '.join(missing_tech_skills)}")
        
        optimized_skills['Technical'] = tech_skills[:8]  # Top 8
        
        # Business skills  
        business_skills = profile_skills['business']
        optimized_skills['Business & Strategy'] = business_skills[:6]  # Top 6
        
        # Format skills section
        skills_content = ""
        for category, skills_list in optimized_skills.items():
            skills_content += f"**{category}:** {' | '.join(skills_list)}\n\n"
        
        return skills_content.strip(), changes
    
    def _find_missing_skills(self, user_skills: List[str], jd_skills: set, category: str) -> List[str]:
        """Find skills mentioned in JD that user doesn't explicitly have"""
        user_skills_lower = set(skill.lower() for skill in user_skills)
        
        # Skill mapping for common variations
        skill_mappings = {
            'ai_ml': {
                'tensorflow': ['TensorFlow', 'Deep Learning Frameworks'],
                'pytorch': ['PyTorch', 'Deep Learning Frameworks'], 
                'scikit-learn': ['Scikit-learn', 'ML Libraries'],
                'pandas': ['Pandas', 'Data Analysis'],
                'numpy': ['NumPy', 'Data Science'],
                'keras': ['Keras', 'Deep Learning'],
                'opencv': ['OpenCV', 'Computer Vision'],
                'gpt': ['GPT Models', 'Large Language Models'],
                'bert': ['BERT', 'Transformer Models'],
                'hugging face': ['Hugging Face', 'ML Model Hub'],
                'mlops': ['MLOps', 'Model Deployment'],
                'model deployment': ['Model Deployment', 'ML Engineering'],
                'data science': ['Data Science', 'Analytics'],
                'predictive modeling': ['Predictive Modeling', 'ML Algorithms']
            },
            'technical': {
                'kubernetes': ['Kubernetes', 'Container Orchestration'],
                'docker': ['Docker', 'Containerization'],
                'aws': ['AWS', 'Cloud Platforms'],
                'azure': ['Azure', 'Cloud Computing'],
                'gcp': ['GCP', 'Google Cloud'],
                'microservices': ['Microservices', 'System Architecture'],
                'devops': ['DevOps', 'CI/CD'],
                'jenkins': ['Jenkins', 'CI/CD Tools'],
                'terraform': ['Terraform', 'Infrastructure as Code'],
                'mongodb': ['MongoDB', 'NoSQL Databases'],
                'elasticsearch': ['Elasticsearch', 'Search Systems'],
                'kafka': ['Apache Kafka', 'Stream Processing'],
                'spark': ['Apache Spark', 'Big Data Processing']
            }
        }
        
        missing_skills = []
        category_mappings = skill_mappings.get(category, {})
        
        for jd_skill in jd_skills:
            jd_skill_clean = jd_skill.lower().strip()
            
            # Skip if user already has this skill
            if jd_skill_clean in user_skills_lower:
                continue
                
            # Check if we have a mapping for this skill
            if jd_skill_clean in category_mappings:
                mapped_skill = category_mappings[jd_skill_clean][0]
                if mapped_skill not in user_skills:  # Avoid duplicates
                    missing_skills.append(mapped_skill)
        
        return missing_skills[:3]  # Limit to 3 new skills per category
    
    def _optimize_experience_section(self, jd_data: Dict, variant: str, country: str) -> Tuple[str, List[str]]:
        """Optimize experience section based on JD and variant"""
        changes = []
        
        # Get base experience from profile
        base_experiences = self.user_profile['experience']
        
        # Reorder and emphasize projects based on variant
        if variant == 'aiml':
            # Lead with AI/ML projects
            primary_projects = ['rag_knowledge_system', 'contract_automation'] 
            secondary_projects = ['converge_fnb_platform', 'salesforce_sap_integration']
            changes.append("Emphasized AI/ML projects (RAG system, contract automation)")
            
        elif variant == 'b2b':
            # Lead with enterprise/B2B projects  
            primary_projects = ['contract_automation', 'salesforce_sap_integration']
            secondary_projects = ['rag_knowledge_system', 'converge_fnb_platform'] 
            changes.append("Emphasized enterprise automation and B2B integration projects")
            
        elif variant == 'b2c':
            # Lead with user-facing projects
            primary_projects = ['converge_fnb_platform', 'mobile_engagement_platform']
            secondary_projects = ['rag_knowledge_system', 'contract_automation']
            changes.append("Emphasized B2C and user engagement projects")
        
        # Build experience content
        experience_content = "## EXPERIENCE\n\n"
        
        for exp in base_experiences:
            if exp['title'] == 'Product Manager (Salesforce & SAP)':
                # Current role - emphasize based on variant and add project details
                exp_content = f"### {exp['title']}\n"
                exp_content += f"**{exp['company']}** | {exp['location']} | {exp['duration']}\n\n"
                
                # Add optimized highlights based on variant
                highlights = self._get_optimized_highlights(primary_projects, secondary_projects, jd_data)
                for highlight in highlights:
                    exp_content += f"• {highlight}\n"
                exp_content += "\n"
                
            else:
                # Other roles - use standard format with potential project emphasis
                exp_content = f"### {exp['title']}\n"
                exp_content += f"**{exp['company']}** | {exp['location']} | {exp['duration']}\n\n"
                
                for highlight in exp['highlights']:
                    exp_content += f"• {highlight}\n"
                exp_content += "\n"
            
            experience_content += exp_content
        
        return experience_content, changes
    
    def _get_optimized_highlights(self, primary_projects: List[str], secondary_projects: List[str], jd_data: Dict) -> List[str]:
        """Get optimized experience highlights based on project priority and JD requirements"""
        
        projects_data = self.user_profile['projects']
        highlights = []
        
        # Add primary project highlights (more detailed)
        for project_key in primary_projects:
            if project_key in projects_data:
                project = projects_data[project_key]
                highlight = f"{project['details']} -- {project['impact']}"
                highlights.append(highlight)
        
        # Add secondary project highlights (more concise)
        for project_key in secondary_projects[:2]:  # Limit to 2 secondary
            if project_key in projects_data:
                project = projects_data[project_key]
                highlight = f"{project['title']}: {project['impact']}"
                highlights.append(highlight)
        
        return highlights
    
    def _assemble_resume(self, summary: str, skills: str, experience: str, 
                        country_format: Dict, country: str) -> str:
        """Assemble the final resume based on country formatting preferences"""
        
        personal_info = self.user_profile['personal_info']
        education = self.user_profile['education']
        certifications = self.user_profile['certifications']
        languages = self.user_profile['languages']
        
        # Build header
        resume = f"# {personal_info['name']}\n"
        resume += f"**{personal_info['title']}**\n\n"
        resume += f"{personal_info['phone']} | {personal_info['email']} | {personal_info['linkedin']} | {personal_info['location']}\n\n"
        resume += "---\n\n"
        
        # Follow country-specific section ordering
        section_order = country_format.get('sections_order', 
                                           ['summary', 'experience', 'education', 'skills', 'certifications'])
        
        for section in section_order:
            if section == 'summary':
                resume += "## SUMMARY\n\n"
                resume += summary + "\n\n---\n\n"
                
            elif section == 'skills':
                resume += "## SKILLS\n\n"
                resume += skills + "\n\n---\n\n"
                
            elif section == 'experience':
                resume += experience + "---\n\n"
                
            elif section == 'education':
                resume += "## EDUCATION\n\n"
                resume += f"**{education['degree']}** | {education['university']} | {education['duration']}\n\n"
                resume += "---\n\n"
                
            elif section == 'certifications':
                resume += "## CERTIFICATIONS\n\n"
                for cert in certifications:
                    resume += f"**{cert['name']}** | {cert['issuer']}\n"
                resume += "\n---\n\n"
                
            elif section == 'languages':
                resume += "## LANGUAGES\n\n"
                for lang in languages:
                    resume += f"{lang['language']} ({lang['proficiency']})\n"
                resume += "\n"
        
        # Apply final country-specific tone adjustments
        resume = self.country_config.adapt_content_tone(resume, country, 'resume')
        
        return resume
    
    def _calculate_ats_score(self, jd_data: Dict, resume_content: str) -> int:
        """Calculate ATS match score based on keyword overlap"""
        
        required_skills = jd_data.get('required_skills', [])
        preferred_skills = jd_data.get('preferred_skills', [])
        
        resume_lower = resume_content.lower()
        
        # Check required skills (weighted higher)
        required_matches = 0
        for skill in required_skills:
            if skill.lower() in resume_lower:
                required_matches += 1
        
        # Check preferred skills
        preferred_matches = 0
        for skill in preferred_skills:
            if skill.lower() in resume_lower:
                preferred_matches += 1
        
        # Calculate score (required skills weighted 70%, preferred 30%)
        total_required = len(required_skills) if required_skills else 1
        total_preferred = len(preferred_skills) if preferred_skills else 1
        
        required_score = (required_matches / total_required) * 70
        preferred_score = (preferred_matches / total_preferred) * 30
        
        total_score = min(100, int(required_score + preferred_score))
        
        return total_score
    
    def _analyze_skill_gaps(self, jd_data: Dict, resume_content: str) -> Tuple[List[str], List[str], List[str]]:
        """Analyze skill gaps between JD requirements and resume"""
        
        required_skills = jd_data.get('required_skills', [])
        preferred_skills = jd_data.get('preferred_skills', [])
        all_jd_skills = set(required_skills + preferred_skills)
        
        resume_lower = resume_content.lower()
        
        matched_skills = []
        missing_skills = []
        mapped_skills = []
        
        for skill in all_jd_skills:
            skill_lower = skill.lower()
            if skill_lower in resume_lower:
                matched_skills.append(skill)
            else:
                # Check if we have a related skill we can map
                related_skill = self._find_related_skill(skill, resume_content)
                if related_skill:
                    mapped_skills.append(f"{skill} → {related_skill}")
                else:
                    missing_skills.append(skill)
        
        return matched_skills, missing_skills, mapped_skills
    
    def _find_related_skill(self, target_skill: str, resume_content: str) -> Optional[str]:
        """Find a related skill in resume that could map to target skill"""
        
        # Common skill mappings
        skill_mappings = {
            'tensorflow': 'Machine Learning',
            'pytorch': 'Deep Learning', 
            'kubernetes': 'Container Orchestration',
            'docker': 'Containerization',
            'react native': 'Mobile Development',
            'node.js': 'Backend Development',
            'mongodb': 'NoSQL Databases',
            'elasticsearch': 'Search Systems',
            'jenkins': 'CI/CD',
            'terraform': 'Infrastructure as Code'
        }
        
        target_lower = target_skill.lower()
        if target_lower in skill_mappings:
            mapped_skill = skill_mappings[target_lower]
            if mapped_skill.lower() in resume_content.lower():
                return mapped_skill
        
        return None