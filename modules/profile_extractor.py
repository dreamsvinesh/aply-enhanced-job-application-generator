#!/usr/bin/env python3
"""
Profile Extractor
One-time extraction of comprehensive user profile from Claude Skills and other sources
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass

from .llm_service import call_llm

@dataclass
class ExtractionResult:
    """Result of profile extraction"""
    success: bool
    profile_data: Dict[str, Any]
    confidence_score: float
    sources_used: List[str]
    extraction_cost: float
    timestamp: str
    errors: List[str]

class ProfileExtractor:
    """Extract comprehensive profile from various sources"""
    
    def __init__(self):
        self.profile_file = Path(__file__).parent.parent / "data" / "extracted_profile.json"
        self.backup_dir = Path(__file__).parent.parent / "data" / "profile_backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def extract_from_claude_skills(self, claude_skills_data: str = None) -> ExtractionResult:
        """
        Extract profile from Claude Skills conversation data
        
        Args:
            claude_skills_data: Raw conversation data from Claude Skills
                               If None, will prompt user for manual input
        """
        errors = []
        extraction_cost = 0.0
        
        if not claude_skills_data:
            print("\n🎯 Claude Skills Data Input Required")
            print("To extract your profile, please provide your Claude Skills conversation data.")
            print("You can either:")
            print("1. Copy-paste key conversations about your experience")
            print("2. Provide a summary of your skills and projects")
            print("3. Upload text files with your background")
            
            claude_skills_data = input("\nPlease paste your Claude Skills data or experience summary:\n")
            
            if not claude_skills_data.strip():
                return ExtractionResult(
                    success=False,
                    profile_data={},
                    confidence_score=0.0,
                    sources_used=[],
                    extraction_cost=0.0,
                    timestamp=datetime.now().isoformat(),
                    errors=["No Claude Skills data provided"]
                )
        
        # Design comprehensive extraction prompt
        extraction_prompt = self._build_extraction_prompt(claude_skills_data)
        
        # Call LLM for extraction
        response = call_llm(
            prompt=extraction_prompt,
            task_type="analysis",
            use_cache=False,  # Don't cache personal data
            max_tokens=4000
        )
        
        extraction_cost = response.cost_usd
        
        if not response.success:
            errors.append(f"LLM extraction failed: {response.error_message}")
            return ExtractionResult(
                success=False,
                profile_data={},
                confidence_score=0.0,
                sources_used=["claude_skills"],
                extraction_cost=extraction_cost,
                timestamp=datetime.now().isoformat(),
                errors=errors
            )
        
        # Parse extracted profile
        try:
            profile_data = json.loads(response.content.strip())
            confidence_score = profile_data.get('extraction_confidence', 0.8)
            
            # Add metadata
            profile_data['extraction_metadata'] = {
                'timestamp': datetime.now().isoformat(),
                'source': 'claude_skills',
                'extraction_cost_usd': extraction_cost,
                'llm_model': response.model,
                'tokens_used': response.tokens_used
            }
            
            return ExtractionResult(
                success=True,
                profile_data=profile_data,
                confidence_score=confidence_score,
                sources_used=["claude_skills"],
                extraction_cost=extraction_cost,
                timestamp=datetime.now().isoformat(),
                errors=[]
            )
            
        except json.JSONDecodeError as e:
            errors.append(f"Failed to parse extracted profile JSON: {e}")
            errors.append(f"Raw response: {response.content[:200]}...")
            
            return ExtractionResult(
                success=False,
                profile_data={},
                confidence_score=0.0,
                sources_used=["claude_skills"],
                extraction_cost=extraction_cost,
                timestamp=datetime.now().isoformat(),
                errors=errors
            )
    
    def _build_extraction_prompt(self, claude_skills_data: str) -> str:
        """Build comprehensive extraction prompt"""
        
        return f"""
You are an expert profile analyzer. Extract a comprehensive professional profile from the provided data.

CLAUDE SKILLS DATA:
{claude_skills_data}

Extract and structure the following information into a detailed JSON object:

{{
    "personal_info": {{
        "name": "Full name if mentioned",
        "current_title": "Current job title",
        "location": "Current location",
        "total_experience_years": "Number extracted from context",
        "pm_experience_years": "Product management specific years"
    }},
    "core_identity": {{
        "primary_expertise": "Main area of expertise (e.g., Product Management)",
        "specializations": ["List of specialized areas"],
        "industry_focus": ["Industries with experience"],
        "value_proposition": "One-sentence summary of unique value"
    }},
    "experience_domains": {{
        "fintech": {{
            "experience_level": "none/basic/intermediate/advanced/expert",
            "years_experience": 0,
            "specific_areas": ["payments", "banking", "compliance", "etc"],
            "key_achievements": ["Specific fintech achievements"],
            "technologies": ["Relevant fintech technologies"],
            "regulatory_knowledge": ["PSD2", "GDPR", "etc if mentioned"]
        }},
        "enterprise_saas": {{
            "experience_level": "none/basic/intermediate/advanced/expert", 
            "years_experience": 0,
            "specific_areas": ["b2b products", "enterprise integration", "etc"],
            "key_achievements": ["Specific enterprise achievements"],
            "technologies": ["Salesforce", "SAP", "enterprise tools"],
            "scale_handled": ["user counts, transaction volumes, etc"]
        }},
        "ai_automation": {{
            "experience_level": "none/basic/intermediate/advanced/expert",
            "years_experience": 0,
            "specific_areas": ["AI systems", "automation", "ML products"],
            "key_achievements": ["AI/ML specific achievements"],
            "technologies": ["AI/ML technologies used"],
            "project_types": ["Types of AI projects built"]
        }}
    }},
    "detailed_projects": [
        {{
            "title": "Project name",
            "context": "Business problem this solved",
            "role": "Your specific role and responsibilities", 
            "approach": "How you approached and solved it",
            "technologies": ["Technologies and tools used"],
            "team_size": "Number if mentioned",
            "duration": "Project length",
            "quantified_results": ["Specific metrics and outcomes"],
            "business_impact": "Revenue/cost/efficiency impact",
            "skills_demonstrated": ["Skills this project showcased"],
            "challenges_overcome": ["Key challenges faced"],
            "relevant_for_roles": ["fintech_pm", "enterprise_pm", "ai_pm"]
        }}
    ],
    "skills_detailed": {{
        "product_management": {{
            "proficiency": "beginner/intermediate/advanced/expert",
            "years_experience": 0,
            "specific_skills": ["product strategy", "roadmapping", "etc"],
            "tools_used": ["Jira", "Figma", "analytics tools"],
            "evidence": ["Projects or achievements demonstrating this"]
        }},
        "technical_skills": {{
            "proficiency": "beginner/intermediate/advanced/expert",
            "programming": ["Languages known"],
            "platforms": ["Salesforce", "SAP", "cloud platforms"], 
            "apis_integration": ["Types of API work done"],
            "databases": ["Database technologies"],
            "evidence": ["Technical projects or implementations"]
        }},
        "business_skills": {{
            "proficiency": "beginner/intermediate/advanced/expert", 
            "areas": ["strategy", "analytics", "stakeholder management"],
            "quantified_achievements": ["Revenue impact", "cost savings", "efficiency gains"],
            "leadership_experience": ["Team sizes led", "cross-functional work"],
            "evidence": ["Business outcomes achieved"]
        }}
    }},
    "achievements_quantified": [
        {{
            "achievement": "What was accomplished",
            "metric": "Specific number/percentage",
            "context": "Business context and significance",
            "timeframe": "When this was achieved", 
            "verification": "How this could be verified"
        }}
    ],
    "transferable_experiences": {{
        "leadership": ["Examples of leadership experience"],
        "problem_solving": ["Complex problems solved"],
        "stakeholder_management": ["Types of stakeholders managed"],
        "technical_translation": ["Examples of technical-business translation"],
        "process_improvement": ["Process improvements made"]
    }},
    "preferences": {{
        "role_types": ["ic", "team_lead", "management"],
        "company_stages": ["startup", "scaleup", "enterprise"],
        "industries_interested": ["fintech", "saas", "healthtech"],
        "industries_avoid": ["gambling", "crypto", "etc"],
        "work_style": ["remote", "hybrid", "office"],
        "location_constraints": ["geographic limitations"]
    }},
    "education_certifications": {{
        "degrees": [
            {{
                "level": "Bachelor's/Master's/PhD",
                "field": "Field of study", 
                "institution": "University name",
                "year": "Graduation year"
            }}
        ],
        "certifications": [
            {{
                "name": "Certification name",
                "issuer": "Issuing organization",
                "year": "Year obtained",
                "relevance": "How relevant to current goals"
            }}
        ]
    }},
    "extraction_confidence": 0.85,
    "gaps_to_fill": ["Areas where more information would be helpful"]
}}

INSTRUCTIONS:
1. Extract only factual information mentioned in the data
2. Do not invent or assume information not provided
3. For missing information, use "not_specified" or appropriate null values
4. Focus on quantifiable achievements and specific technologies
5. Classify experience levels accurately based on evidence
6. Identify transferable skills that apply across domains
7. Return ONLY the JSON object, no other text
8. Ensure all JSON is valid and properly formatted

CRITICAL: Be conservative with experience levels and claims. Only mark something as "expert" if there's clear evidence of deep expertise. When in doubt, use lower confidence levels.
"""
    
    def enhance_with_existing_data(self, extracted_profile: Dict) -> Dict:
        """Enhance extracted profile with existing data sources"""
        
        # Load existing profile if available
        existing_profile_path = Path(__file__).parent.parent / "data" / "user_profile.json"
        existing_config_path = Path(__file__).parent.parent / "config" / "user_profile.json"
        
        existing_data = {}
        
        # Try to load from existing sources
        for profile_path in [existing_profile_path, existing_config_path]:
            if profile_path.exists():
                try:
                    with open(profile_path, 'r') as f:
                        existing_data.update(json.load(f))
                    print(f"✅ Loaded existing data from {profile_path}")
                except Exception as e:
                    print(f"⚠️  Failed to load {profile_path}: {e}")
        
        # Merge data intelligently
        enhanced_profile = extracted_profile.copy()
        
        # Add any quantified achievements from existing data
        if 'key_achievements' in existing_data:
            if 'legacy_achievements' not in enhanced_profile:
                enhanced_profile['legacy_achievements'] = existing_data['key_achievements']
        
        # Preserve any manual customizations
        if 'manual_overrides' in existing_data:
            enhanced_profile['manual_overrides'] = existing_data['manual_overrides']
        
        # Add enhancement metadata
        enhanced_profile['enhancement_metadata'] = {
            'enhanced_at': datetime.now().isoformat(),
            'sources_merged': list(existing_data.keys()),
            'existing_data_found': bool(existing_data)
        }
        
        return enhanced_profile
    
    def save_profile(self, profile_data: Dict) -> bool:
        """Save comprehensive profile to local storage"""
        try:
            # Create backup of existing profile
            if self.profile_file.exists():
                backup_name = f"profile_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_path = self.backup_dir / backup_name
                
                with open(self.profile_file, 'r') as f:
                    existing = json.load(f)
                
                with open(backup_path, 'w') as f:
                    json.dump(existing, f, indent=2)
                
                print(f"✅ Backup created: {backup_path}")
            
            # Save new profile
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Profile saved: {self.profile_file}")
            print(f"📁 Profile size: {len(json.dumps(profile_data))} characters")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save profile: {e}")
            return False
    
    def load_profile(self) -> Optional[Dict]:
        """Load existing comprehensive profile"""
        if self.profile_file.exists():
            try:
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"❌ Failed to load profile: {e}")
        
        return None
    
    def extract_and_save(self, claude_skills_data: str = None) -> ExtractionResult:
        """Complete extraction and save workflow"""
        print("🚀 Starting Comprehensive Profile Extraction...")
        
        # Extract from Claude Skills
        extraction_result = self.extract_from_claude_skills(claude_skills_data)
        
        if not extraction_result.success:
            print("❌ Profile extraction failed:")
            for error in extraction_result.errors:
                print(f"   • {error}")
            return extraction_result
        
        print(f"✅ Profile extracted successfully (confidence: {extraction_result.confidence_score:.1%})")
        print(f"💰 Extraction cost: ${extraction_result.extraction_cost:.4f}")
        
        # Enhance with existing data
        enhanced_profile = self.enhance_with_existing_data(extraction_result.profile_data)
        
        # Save to local storage
        if self.save_profile(enhanced_profile):
            extraction_result.profile_data = enhanced_profile
            print("✅ Comprehensive profile saved successfully!")
        else:
            extraction_result.errors.append("Failed to save profile")
        
        return extraction_result
    
    def get_profile_summary(self) -> str:
        """Get a summary of the current profile"""
        profile = self.load_profile()
        
        if not profile:
            return "❌ No profile found. Run extraction first."
        
        summary = []
        summary.append(f"📊 Profile Summary:")
        summary.append(f"   Name: {profile.get('personal_info', {}).get('name', 'Not specified')}")
        summary.append(f"   Experience: {profile.get('personal_info', {}).get('total_experience_years', 'Not specified')} years")
        
        domains = profile.get('experience_domains', {})
        summary.append(f"   Domains: {len(domains)} areas mapped")
        
        projects = profile.get('detailed_projects', [])
        summary.append(f"   Projects: {len(projects)} detailed projects")
        
        achievements = profile.get('achievements_quantified', [])
        summary.append(f"   Achievements: {len(achievements)} quantified")
        
        extraction_meta = profile.get('extraction_metadata', {})
        if 'timestamp' in extraction_meta:
            summary.append(f"   Last updated: {extraction_meta['timestamp']}")
        
        return "\n".join(summary)