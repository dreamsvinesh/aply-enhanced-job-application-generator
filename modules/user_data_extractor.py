#!/usr/bin/env python3
"""
User Data Extractor
Extracts and structures factual information from user's actual resume
to prevent LLM from fabricating company names and personal details.
"""

import json
from typing import Dict, List, Any
from pathlib import Path

class UserDataExtractor:
    """Extracts factual user data that must be preserved during content generation"""
    
    def __init__(self):
        self.factual_data = {}
    
    def extract_vinesh_data(self) -> Dict[str, Any]:
        """Extract Vinesh Kumar's actual resume data"""
        
        factual_data = {
            'personal_info': {
                'name': 'Vinesh Kumar',
                'title': 'Senior Product Manager | B2B & B2C Product Innovation | AI & Automation',
                'phone': '+91-81230-79049',
                'email': 'vineshmuthukumar@gmail.com',
                'linkedin': 'https://www.linkedin.com/in/vinukum',
                'location': 'Bangalore, India'
            },
            
            'professional_summary': {
                'years_experience': '11 years in technology (7 in PM)',
                'specialization': 'AI/ML systems, RAG architecture, and enterprise automation across B2B SaaS platforms',
                'key_achievements': [
                    'Built AI knowledge system achieving 94% accuracy serving 200+ users',
                    'Automated workflows reducing timelines from 42 days to 10 minutes (accelerating $2M revenue)',
                    'Saved 50+ resource hours daily through intelligent automation'
                ]
            },
            
            'work_experience': [
                {
                    'role': 'Senior Product Manager',
                    'company': 'COWRKS',
                    'duration': '01/2023 - Present',
                    'location': 'Bangalore, India',
                    'exact_achievements': [
                        'Defined product vision and roadmap for enterprise automation. Analyzed competitive landscape (3-5 days vs. 42 days). Identified operational efficiency as a strategic differentiator. Secured CEO approval and $2M investment through ROI presentations.',
                        'Created AI RAG system with pgvector, choosing it over traditional search. Achieved 94% accuracy, sub-second responses. Cut support tickets 75% (500→125 monthly), aiding 200+ employees in 1,500+ weekly queries through prompt engineering and hybrid search.',
                        'Automated contract activation workflow integrating Salesforce, SAP, and MuleSoft APIs, reducing timeline 99.6% from 42 days to 10 minutes - accelerated $2M revenue recognition, saved 50+ resource hours daily, and established new industry benchmark through cross-functional execution',
                        'Led automation rollout and change management, creating training and conducting presentations for 5 departments. Achieved 100% adoption in 2 weeks, boosting team efficiency for revenue-generating activities.',
                        'Automated sales workflows with Salesforce Flow and API integrations, saving 50+ hours daily and minimizing errors - improved lead conversion speed 50% faster and scaled lead generation 5X via IVR integration'
                    ]
                },
                {
                    'role': 'Product Manager',
                    'company': 'COWRKS',
                    'duration': '08/2016 - 01/2020',
                    'location': 'Bangalore, India',
                    'exact_achievements': [
                        'Developed mobile app features (auto WiFi, room booking, food ordering) based on user research and market analysis - increased app engagement 45% and customer satisfaction 65%, drove 30% higher amenity utilization across 80+ locations',
                        'Identified and executed go-to-market strategy for monetizing underutilized non-desk inventory (parking, lounges), defining pricing and positioning - generated €220K monthly revenue creating 15% new revenue stream per location',
                        'Reduced lead conversion time 32% and accelerated onboarding from 110 days to 14 days through process redesign and stakeholder alignment - improved occupancy rates 25%, enabling faster time-to-value for clients'
                    ]
                },
                {
                    'role': 'Frontend Engineer',
                    'company': 'Automne Technologies | Rukshaya Emerging Technologies',
                    'duration': '09/2012 - 07/2016',
                    'location': 'Bangalore, India',
                    'exact_achievements': [
                        'Built and maintained front-end web applications using HTML5, CSS3, and Angular.JS for 50+ enterprise clients across banking and e-commerce sectors - handled end-to-end UX to UI development.'
                    ]
                }
            ],
            
            'education': [
                {
                    'degree': 'Master of Science in Software Engineering',
                    'institution': 'Anna University',
                    'duration': '01/2007 - 01/2011'
                }
            ],
            
            'skills': {
                'product_management': [
                    'Vision & Roadmap', 'Market Positioning', 'Go-to-Market', 'Prioritization',
                    'Cross-Functional Teams', 'Stakeholder Management', 'Agile/SAFe'
                ],
                'technical_research': [
                    'Discovery', 'Design Thinking', 'User Research'
                ],
                'ai_automation': [
                    'Process Optimization', 'RAG Architecture', 'Multi-Agent Systems',
                    'Prompt Engineering', 'Vector DBs (pgvector)', 'LLM Integration'
                ],
                'platforms': ['Salesforce']
            },
            
            'core_competencies': [
                {
                    'area': 'Business Transformation',
                    'description': 'Identifying and executing high-ROI automation opportunities that dramatically improve operational efficiency'
                },
                {
                    'area': 'Technical Translation',
                    'description': 'Bridging business needs and technical implementation to deliver solutions that solve real problems'
                },
                {
                    'area': 'User-Centered Design',
                    'description': 'Creating intuitive user experiences that drive adoption and enhance customer satisfaction'
                }
            ],
            
            'certifications': [
                'Machine Learning Foundations for Product Managers - Duke University',
                'SAFe® Product Owner & Product Manager - Scaled Agile Framework (SAFe)'
            ],
            
            'languages': [
                {'language': 'English', 'proficiency': 'Proficient'},
                {'language': 'Tamil', 'proficiency': 'Native'}
            ]
        }
        
        self.factual_data = factual_data
        return factual_data
    
    def get_preservation_constraints(self) -> Dict[str, List[str]]:
        """Get specific constraints for what must be preserved vs what can be customized"""
        
        constraints = {
            'preserve_exactly': [
                # Personal information - NEVER change
                'Vinesh Kumar',
                '+91-81230-79049',
                'vineshmuthukumar@gmail.com',
                'https://www.linkedin.com/in/vinukum',
                'Bangalore, India',
                
                # Company names - NEVER fabricate
                'COWRKS',
                'Automne Technologies',
                'Rukshaya Emerging Technologies',
                
                # Educational institution
                'Anna University',
                'Master of Science in Software Engineering',
                
                # Certifications
                'Duke University',
                'Machine Learning Foundations for Product Managers',
                'SAFe® Product Owner & Product Manager',
                
                # Specific metrics and timeframes
                '94% accuracy',
                '42 days to 10 minutes',
                '$2M revenue',
                '50+ resource hours daily',
                '99.6%',
                '500→125 monthly',
                '45% and customer satisfaction 65%',
                '€220K monthly revenue',
                '110 days to 14 days',
                '11 years in technology (7 in PM)'
            ],
            
            'customize_presentation': [
                # These can be reframed/emphasized based on role
                'job descriptions',
                'achievement ordering',
                'skill emphasis',
                'experience framing',
                'competency highlighting'
            ],
            
            'never_fabricate': [
                'company names',
                'personal details',
                'contact information',
                'education details',
                'certification sources',
                'specific metrics',
                'employment dates'
            ]
        }
        
        return constraints
    
    def validate_content_against_facts(self, generated_content: str) -> Dict[str, Any]:
        """Validate that generated content doesn't fabricate factual information"""
        
        validation_result = {
            'is_valid': True,
            'violations': [],
            'suggestions': []
        }
        
        constraints = self.get_preservation_constraints()
        
        # Check for fabricated company names
        fabricated_companies = ['TechCorp', 'ScaleupCo', 'InnovateCorp', 'StartupX', 'TechStart']
        for company in fabricated_companies:
            if company in generated_content:
                validation_result['is_valid'] = False
                validation_result['violations'].append({
                    'type': 'fabricated_company',
                    'found': company,
                    'should_be': 'COWRKS or other real companies from user history'
                })
        
        # Check for preserved elements
        real_companies = ['COWRKS', 'Automne Technologies', 'Rukshaya Emerging Technologies']
        found_real_company = any(company in generated_content for company in real_companies)
        
        if not found_real_company:
            validation_result['violations'].append({
                'type': 'missing_real_company',
                'issue': 'No real company names found in generated content',
                'should_include': real_companies
            })
        
        return validation_result
    
    def create_llm_constraints_prompt(self) -> str:
        """Create prompt constraints for LLM to preserve factual data"""
        
        constraints_prompt = f"""
CRITICAL CONTENT GENERATION CONSTRAINTS:

PRESERVE EXACTLY (NEVER CHANGE):
• Personal Info: {self.factual_data['personal_info']['name']}, {self.factual_data['personal_info']['email']}, {self.factual_data['personal_info']['phone']}
• Real Companies: COWRKS, Automne Technologies, Rukshaya Emerging Technologies
• Education: Anna University, Master of Science in Software Engineering
• Real Metrics: 94% accuracy, 42 days to 10 minutes, $2M revenue, 99.6% reduction
• Certifications: Duke University, SAFe® certification

NEVER FABRICATE:
• Company names (NO TechCorp, ScaleupCo, InnovateCorp, etc.)
• Personal details or contact information
• Educational institutions or degrees
• Specific metrics or timeframes
• Employment dates or durations

WRITING STYLE REQUIREMENTS:
• Write with confidence and impact - focus on outcomes, not just activities
• Lead with business results: revenue impact, efficiency gains, user/team scale
• Be specific with metrics and context rather than generic statements
• Show transformation and leadership naturally in the narrative
• Avoid corporate buzzwords and overly formal language

WRITING GUIDANCE:
Instead of describing what you did, describe the impact you delivered.
Instead of listing features, highlight the business value created.
Instead of process-focused language, use outcome-focused language.

REAL WORK HISTORY TO USE:
1. COWRKS (2023-Present): Senior Product Manager - AI/RAG systems, enterprise automation
   REQUIREMENT: EXACTLY 5 bullet points, 100-150 words total
   Real achievements: 94% accuracy, $2M revenue acceleration, 99.6% reduction, 75% support ticket reduction
2. COWRKS (2016-2020): Product Manager - Mobile apps, process optimization  
   REQUIREMENT: 3-5 bullet points, 60-100 words total
   Real achievements: 45% engagement increase, €220K monthly revenue, 32% conversion improvement
3. Automne/Rukshaya (2012-2016): Frontend Engineer - Web applications
   REQUIREMENT: 1-2 bullet points, 30-50 words total  
   Real achievements: 50+ enterprise clients, banking/e-commerce sectors

TONE: Professional, confident, results-oriented. Write as someone who delivers measurable business impact.
Remember: Use your REAL achievements with strong, natural presentation.
"""
        return constraints_prompt
    
    def save_extracted_data(self, output_path: str = "user_factual_data.json"):
        """Save extracted factual data to file"""
        with open(output_path, 'w') as f:
            json.dump(self.factual_data, f, indent=2)
        
        return output_path

def main():
    """Demo the user data extraction"""
    extractor = UserDataExtractor()
    
    print("🔍 EXTRACTING USER FACTUAL DATA")
    print("=" * 50)
    
    # Extract Vinesh's data
    factual_data = extractor.extract_vinesh_data()
    
    print("✅ Extracted Personal Info:")
    print(f"• Name: {factual_data['personal_info']['name']}")
    print(f"• Email: {factual_data['personal_info']['email']}")
    print(f"• Experience: {factual_data['professional_summary']['years_experience']}")
    
    print("\n✅ Real Companies (NEVER fabricate):")
    for exp in factual_data['work_experience']:
        print(f"• {exp['company']} ({exp['duration']})")
    
    print("\n✅ Preservation Constraints:")
    constraints = extractor.get_preservation_constraints()
    print(f"• Must preserve exactly: {len(constraints['preserve_exactly'])} items")
    print(f"• Never fabricate: {len(constraints['never_fabricate'])} categories")
    
    print("\n🛡️ LLM Constraints Prompt:")
    print(extractor.create_llm_constraints_prompt())
    
    # Save data
    output_file = extractor.save_extracted_data()
    print(f"\n💾 Saved factual data to: {output_file}")

if __name__ == "__main__":
    main()