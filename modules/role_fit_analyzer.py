#!/usr/bin/env python3
"""
Role Fit Analyzer - Orchestrator for Specialized Role Fit Agents
Coordinates multiple specialized agents for comprehensive role fit analysis
"""

from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path
import time

from .role_fit_agents import (
    DomainMismatchAgent, 
    SkillsGapAgent, 
    ExperienceMatchingAgent, 
    IndustryAlignmentAgent,
    AgentResult
)

class RoleFitAnalyzer:
    def __init__(self):
        self.profile_data = self._load_profile()
        
        # Initialize specialized agents
        self.domain_agent = DomainMismatchAgent()
        self.skills_agent = SkillsGapAgent()
        self.experience_agent = ExperienceMatchingAgent()
        self.industry_agent = IndustryAlignmentAgent()
        
    def _load_profile(self) -> Dict:
        """Load user profile from config"""
        profile_path = Path("config/user_profile.json")
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                return json.load(f)
        return self._get_default_profile()
    
    def _get_default_profile(self) -> Dict:
        """Default profile structure"""
        return {
            "basic_info": {
                "experience_years": 7,
                "experience_level": "senior",
                "education": "mba"
            },
            "skills": {
                "core_skills": [
                    "product strategy", "roadmap planning", "stakeholder management",
                    "agile methodologies", "user research", "data analysis",
                    "api integration", "cross-functional leadership"
                ]
            },
            "experience": {
                "domains": ["product_management", "fintech", "saas"],
                "industries": ["fintech", "saas", "technology", "financial_services"],
                "avoid_domains": ["crypto", "gambling", "adult_content"]
            }
        }
    
    def analyze_fit(self, jd_data: Dict, timeout: float = 15.0) -> Dict:
        """
        Orchestrate comprehensive role fit analysis using specialized agents
        
        Returns:
            Dict with fit_score, recommendations, and detailed analysis
        """
        start_time = time.time()
        
        # Initialize analysis structure
        analysis = {
            "fit_score": 0,
            "recommendation": "",
            "critical_gaps": [],
            "minor_gaps": [],
            "strengths": [],
            "effort_required": "high",
            "should_apply": False,
            "detailed_analysis": {},
            "agent_results": {},
            "execution_time": 0
        }
        
        try:
            # Extract job content for domain analysis
            job_content = str(jd_data)
            
            # Run domain mismatch analysis
            if time.time() - start_time < timeout:
                domain_result = self.domain_agent.analyze(self.profile_data, job_content)
                analysis["agent_results"]["domain"] = domain_result
            
            # Run skills gap analysis
            if time.time() - start_time < timeout:
                skills_result = self.skills_agent.analyze(self.profile_data, jd_data)
                analysis["agent_results"]["skills"] = skills_result
            
            # Run experience matching analysis
            if time.time() - start_time < timeout:
                experience_result = self.experience_agent.analyze(self.profile_data, jd_data)
                analysis["agent_results"]["experience"] = experience_result
            
            # Run industry alignment analysis
            if time.time() - start_time < timeout:
                industry_result = self.industry_agent.analyze(self.profile_data, jd_data)
                analysis["agent_results"]["industry"] = industry_result
            
            # Aggregate agent results
            analysis = self._aggregate_agent_results(analysis)
            
        except Exception as e:
            # Fallback to basic analysis if agents fail
            analysis["recommendation"] = f"ANALYSIS ERROR - {str(e)}"
            analysis["should_apply"] = False
            analysis["critical_gaps"] = [f"Analysis failed: {str(e)}"]
        
        analysis["execution_time"] = time.time() - start_time
        return analysis
    
    def _aggregate_agent_results(self, analysis: Dict) -> Dict:
        """Aggregate results from all specialized agents"""
        
        agent_results = analysis["agent_results"]
        
        # Collect successful agent scores and findings
        scores = {}
        all_findings = []
        all_recommendations = []
        critical_gaps = []
        strengths = []
        
        weights = {
            "domain": 0.3,      # Critical for filtering unsuitable roles
            "skills": 0.35,     # Most important for job performance
            "experience": 0.2,  # Important but can be developed
            "industry": 0.15    # Least critical for experienced PMs
        }
        
        total_weight = 0.0
        weighted_score = 0.0
        
        for agent_type, result in agent_results.items():
            if result.success:
                # Collect scores with weights
                scores[agent_type] = result.score
                weighted_score += result.score * weights.get(agent_type, 0.25)
                total_weight += weights.get(agent_type, 0.25)
                
                # Collect findings
                all_findings.extend([f"[{agent_type.title()}] {finding}" for finding in result.findings])
                all_recommendations.extend(result.recommendations)
                
                # Identify critical issues and strengths based on agent type and score
                if result.score < 0.4:
                    critical_gaps.append(f"{agent_type.title()}: {result.findings[0] if result.findings else 'Low compatibility'}")
                elif result.score > 0.8:
                    strengths.append(f"{agent_type.title()}: {result.findings[0] if result.findings else 'Strong alignment'}")
        
        # Calculate final fit score
        if total_weight > 0:
            analysis["fit_score"] = (weighted_score / total_weight) * 100
        else:
            analysis["fit_score"] = 0
        
        # Determine if domain conflicts are critical blockers
        domain_result = agent_results.get("domain")
        has_domain_conflict = (domain_result and domain_result.success and 
                             domain_result.score < 0.3 and 
                             any('conflict' in finding.lower() for finding in domain_result.findings))
        
        # Generate recommendation based on aggregated analysis
        if has_domain_conflict:
            analysis["recommendation"] = "POOR FIT - Domain conflicts with profile preferences"
            analysis["effort_required"] = "very_high"
            analysis["should_apply"] = False
        elif analysis["fit_score"] >= 80:
            analysis["recommendation"] = "STRONG FIT - Apply with confidence"
            analysis["effort_required"] = "low"
            analysis["should_apply"] = True
        elif analysis["fit_score"] >= 65:
            analysis["recommendation"] = "GOOD FIT - Apply with targeted customization"
            analysis["effort_required"] = "medium"
            analysis["should_apply"] = True
        elif analysis["fit_score"] >= 50:
            analysis["recommendation"] = "MODERATE FIT - Consider with significant preparation"
            analysis["effort_required"] = "high"
            analysis["should_apply"] = False
        else:
            analysis["recommendation"] = "POOR FIT - Not recommended"
            analysis["effort_required"] = "very_high"
            analysis["should_apply"] = False
        
        # Update analysis with aggregated data
        analysis["critical_gaps"] = critical_gaps
        analysis["strengths"] = strengths
        analysis["detailed_analysis"] = scores
        
        # Remove duplicates and limit recommendations
        analysis["minor_gaps"] = list(set(all_recommendations))[:5]
        
        return analysis
    
    def generate_fit_report(self, jd_data: Dict) -> str:
        """Generate a formatted fit analysis report"""
        analysis = self.analyze_fit(jd_data)
        
        report = f"""
## ROLE FIT ANALYSIS

**Overall Fit Score:** {analysis['fit_score']:.0f}/100

**Recommendation:** {analysis['recommendation']}

**Effort Required:** {analysis['effort_required'].title()}

**Should Apply:** {'✅ Yes' if analysis['should_apply'] else '❌ No'}

### Strengths
{chr(10).join(f'• {strength}' for strength in analysis['strengths'])}

### Critical Gaps
{chr(10).join(f'• {gap}' for gap in analysis['critical_gaps']) if analysis['critical_gaps'] else 'None identified'}

### Minor Gaps
{chr(10).join(f'• {gap}' for gap in analysis['minor_gaps']) if analysis['minor_gaps'] else 'None identified'}

### Score Breakdown
• Experience: {analysis['detailed_analysis']['experience']}/100
• Skills: {analysis['detailed_analysis']['skills']}/100  
• Industry: {analysis['detailed_analysis']['industry']}/100
• Domain: {analysis['detailed_analysis']['domain']}/100
"""
        
        return report