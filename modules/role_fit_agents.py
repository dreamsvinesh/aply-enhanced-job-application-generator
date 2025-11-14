#!/usr/bin/env python3
"""
Specialized Role Fit Analysis Agents
Provides intelligent, domain-agnostic role fit analysis using specialized agents
"""

import json
import re
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
import time

@dataclass
class AgentResult:
    """Standardized result format for all role fit agents"""
    success: bool
    score: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    findings: List[str]
    recommendations: List[str]
    metadata: Dict[str, any]
    execution_time: float

class DomainMismatchAgent:
    """
    Detects domain conflicts between user preferences and job requirements
    Generic detection without hardcoded domains
    """
    
    def __init__(self):
        self.name = "domain_mismatch_agent"
    
    def analyze(self, user_profile: Dict, job_content: str) -> AgentResult:
        """Analyze domain mismatch using semantic content analysis"""
        start_time = time.time()
        
        try:
            # Get user's avoid domains from nested structure
            avoid_domains = user_profile.get('experience', {}).get('avoid_domains', [])
            preferred_domains = user_profile.get('experience', {}).get('domains', [])
            
            # Normalize job content for analysis
            job_text = job_content.lower()
            
            # Find domain conflicts using semantic keywords
            domain_conflicts = []
            confidence_scores = []
            
            for avoid_domain in avoid_domains:
                conflict_score, conflict_details = self._detect_domain_presence(
                    avoid_domain, job_text
                )
                
                if conflict_score > 0.3:  # Threshold for significant presence
                    domain_conflicts.append({
                        'domain': avoid_domain,
                        'score': conflict_score,
                        'evidence': conflict_details
                    })
                    confidence_scores.append(conflict_score)
            
            # Calculate overall domain alignment score
            if domain_conflicts:
                # Penalize based on worst conflict
                worst_conflict = max(conflict['score'] for conflict in domain_conflicts)
                domain_score = max(0.0, 1.0 - worst_conflict)
            else:
                # Check positive domain alignment
                domain_score = max(0.6, self._calculate_positive_alignment(
                    preferred_domains, job_text
                ))
            
            # Build findings and recommendations
            findings = []
            recommendations = []
            
            if domain_conflicts:
                for conflict in domain_conflicts:
                    findings.append(
                        f"Domain conflict detected: {conflict['domain']} "
                        f"(confidence: {conflict['score']:.1%})"
                    )
                    findings.extend([f"  Evidence: {evidence}" for evidence in conflict['evidence'][:2]])
                
                recommendations.append("Consider roles in preferred domains instead")
                recommendations.append("Review job description for domain-specific requirements")
            else:
                findings.append("No significant domain conflicts detected")
                if domain_score > 0.7:
                    findings.append(f"Good domain alignment (score: {domain_score:.1%})")
                    recommendations.append("Domain alignment supports application")
            
            confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.8
            
            return AgentResult(
                success=True,
                score=domain_score,
                confidence=confidence,
                findings=findings,
                recommendations=recommendations,
                metadata={
                    'conflicts': domain_conflicts,
                    'analyzed_domains': avoid_domains + preferred_domains
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                score=0.0,
                confidence=0.0,
                findings=[f"Domain analysis failed: {str(e)}"],
                recommendations=[],
                metadata={},
                execution_time=time.time() - start_time
            )
    
    def _detect_domain_presence(self, domain: str, job_text: str) -> Tuple[float, List[str]]:
        """Detect presence of a domain in job text using semantic keywords"""
        
        # Domain-specific keyword mapping
        domain_keywords = {
            'crypto': [
                'crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'blockchain', 
                'defi', 'web3', 'nft', 'hodl', 'altcoin', 'mining', 'wallet',
                'exchange', 'trading', 'tokenize', 'smart contract', 'metaverse',
                'kraken', 'coinbase', 'binance'
            ],
            'gambling': [
                'gambling', 'casino', 'poker', 'betting', 'wagering', 'lottery',
                'sportsbook', 'slots', 'jackpot', 'odds', 'bookmaker', 'gaming',
                'blackjack', 'roulette', 'bingo'
            ],
            'adult_content': [
                'adult', 'mature', 'explicit', 'nsfw', 'dating', 'escort',
                'adult entertainment', 'xxx', 'webcam', 'strip'
            ],
            'tobacco': [
                'tobacco', 'cigarette', 'smoking', 'vaping', 'nicotine',
                'cigar', 'e-cigarette', 'marlboro', 'philip morris'
            ],
            'alcohol': [
                'alcohol', 'beer', 'wine', 'spirits', 'liquor', 'brewery',
                'distillery', 'vodka', 'whiskey', 'cocktail'
            ]
        }
        
        # Get relevant keywords for this domain
        keywords = domain_keywords.get(domain.lower(), [domain.lower()])
        
        # Count keyword matches and gather evidence
        matches = []
        total_score = 0.0
        
        for keyword in keywords:
            if keyword in job_text:
                # Calculate frequency score
                count = job_text.count(keyword)
                frequency_score = min(count * 0.2, 1.0)  # Cap at 1.0
                total_score += frequency_score
                
                matches.append(f"'{keyword}' mentioned {count} time(s)")
        
        # Normalize score
        final_score = min(total_score / len(keywords), 1.0)
        
        return final_score, matches
    
    def _calculate_positive_alignment(self, preferred_domains: List[str], job_text: str) -> float:
        """Calculate positive alignment with preferred domains"""
        
        if not preferred_domains:
            return 0.6  # Neutral score
        
        total_alignment = 0.0
        
        for domain in preferred_domains:
            alignment_score = self._detect_domain_presence(domain, job_text)[0]
            total_alignment += alignment_score
        
        return min(total_alignment / len(preferred_domains), 1.0)

class SkillsGapAgent:
    """
    Analyzes skills alignment using semantic matching and transferable skills
    """
    
    def __init__(self):
        self.name = "skills_gap_agent"
        self.skill_synonyms = self._load_skill_synonyms()
    
    def analyze(self, user_profile: Dict, job_requirements: Dict) -> AgentResult:
        """Analyze skills gap using semantic matching"""
        start_time = time.time()
        
        try:
            user_skills = [s.lower() for s in user_profile.get('skills', {}).get('core_skills', [])]
            required_skills = [s.lower() for s in job_requirements.get('required_skills', [])]
            preferred_skills = [s.lower() for s in job_requirements.get('preferred_skills', [])]
            
            # Analyze required skills
            required_analysis = self._analyze_skill_set(user_skills, required_skills, "required")
            
            # Analyze preferred skills  
            preferred_analysis = self._analyze_skill_set(user_skills, preferred_skills, "preferred")
            
            # Calculate overall skills score
            required_weight = 0.8
            preferred_weight = 0.2
            
            overall_score = (
                required_analysis['score'] * required_weight + 
                preferred_analysis['score'] * preferred_weight
            )
            
            # Combine findings and recommendations
            findings = []
            findings.extend(required_analysis['findings'])
            findings.extend(preferred_analysis['findings'])
            
            recommendations = []
            recommendations.extend(required_analysis['recommendations'])
            recommendations.extend(preferred_analysis['recommendations'])
            
            # Add transferable skills analysis
            transferable = self._identify_transferable_skills(
                user_skills, required_skills + preferred_skills
            )
            
            if transferable:
                findings.append(f"Identified {len(transferable)} transferable skills")
                recommendations.append("Emphasize transferable skills in application")
            
            confidence = (required_analysis['confidence'] + preferred_analysis['confidence']) / 2
            
            return AgentResult(
                success=True,
                score=overall_score,
                confidence=confidence,
                findings=findings,
                recommendations=recommendations,
                metadata={
                    'required_analysis': required_analysis,
                    'preferred_analysis': preferred_analysis,
                    'transferable_skills': transferable,
                    'skill_gaps': required_analysis['gaps'] + preferred_analysis['gaps']
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                score=0.0,
                confidence=0.0,
                findings=[f"Skills analysis failed: {str(e)}"],
                recommendations=[],
                metadata={},
                execution_time=time.time() - start_time
            )
    
    def _analyze_skill_set(self, user_skills: List[str], target_skills: List[str], skill_type: str) -> Dict:
        """Analyze alignment for a specific set of skills"""
        
        if not target_skills:
            return {
                'score': 1.0,
                'findings': [f"No {skill_type} skills specified"],
                'recommendations': [],
                'confidence': 1.0,
                'gaps': []
            }
        
        matched_skills = []
        gap_skills = []
        transferable_matches = []
        
        for target_skill in target_skills:
            match_type, user_skill = self._find_skill_match(user_skills, target_skill)
            
            if match_type == 'exact':
                matched_skills.append((target_skill, user_skill, 'exact'))
            elif match_type == 'semantic':
                matched_skills.append((target_skill, user_skill, 'semantic'))
            elif match_type == 'transferable':
                transferable_matches.append((target_skill, user_skill, 'transferable'))
            else:
                gap_skills.append(target_skill)
        
        # Calculate score
        exact_matches = sum(1 for _, _, match_type in matched_skills if match_type == 'exact')
        semantic_matches = sum(1 for _, _, match_type in matched_skills if match_type == 'semantic')
        transferable_count = len(transferable_matches)
        
        score = (
            exact_matches * 1.0 + 
            semantic_matches * 0.8 + 
            transferable_count * 0.5
        ) / len(target_skills)
        
        score = min(score, 1.0)
        
        # Build findings
        findings = []
        if matched_skills:
            findings.append(f"Matched {len(matched_skills)}/{len(target_skills)} {skill_type} skills")
        if transferable_matches:
            findings.append(f"Found {len(transferable_matches)} transferable skills")
        if gap_skills:
            findings.append(f"Missing {len(gap_skills)} {skill_type} skills: {', '.join(gap_skills[:3])}")
        
        # Build recommendations
        recommendations = []
        if score >= 0.8:
            recommendations.append(f"Strong {skill_type} skills alignment - emphasize in application")
        elif score >= 0.6:
            recommendations.append(f"Good {skill_type} skills match - highlight transferable skills")
        else:
            recommendations.append(f"Significant {skill_type} skills gaps - consider skill development")
        
        return {
            'score': score,
            'findings': findings,
            'recommendations': recommendations,
            'confidence': 0.85,
            'gaps': gap_skills,
            'matches': matched_skills,
            'transferable': transferable_matches
        }
    
    def _find_skill_match(self, user_skills: List[str], target_skill: str) -> Tuple[str, Optional[str]]:
        """Find the best match for a target skill in user skills"""
        
        # Exact match
        if target_skill in user_skills:
            return 'exact', target_skill
        
        # Semantic match using synonyms
        target_synonyms = self.skill_synonyms.get(target_skill, [target_skill])
        
        for user_skill in user_skills:
            user_synonyms = self.skill_synonyms.get(user_skill, [user_skill])
            
            # Check if any synonyms match
            if any(syn in target_synonyms for syn in user_synonyms):
                return 'semantic', user_skill
            
            # Check substring matches
            if target_skill in user_skill or user_skill in target_skill:
                return 'semantic', user_skill
        
        # Check for transferable skills
        transferable_skill = self._check_transferable_skill(user_skills, target_skill)
        if transferable_skill:
            return 'transferable', transferable_skill
        
        return 'none', None
    
    def _check_transferable_skill(self, user_skills: List[str], target_skill: str) -> Optional[str]:
        """Check if user has transferable skills for the target skill"""
        
        transferable_mappings = {
            'product management': ['project management', 'program management', 'business analysis'],
            'stakeholder management': ['client management', 'relationship management', 'account management'],
            'data analysis': ['business intelligence', 'analytics', 'reporting', 'sql'],
            'user research': ['market research', 'customer research', 'user experience'],
            'agile methodologies': ['scrum', 'kanban', 'lean', 'project management'],
            'cross-functional leadership': ['team leadership', 'project leadership', 'team management']
        }
        
        target_transferables = transferable_mappings.get(target_skill, [])
        
        for user_skill in user_skills:
            if user_skill in target_transferables:
                return user_skill
        
        return None
    
    def _identify_transferable_skills(self, user_skills: List[str], target_skills: List[str]) -> List[Dict]:
        """Identify all transferable skills between user and target"""
        
        transferable = []
        
        for target_skill in target_skills:
            transferable_skill = self._check_transferable_skill(user_skills, target_skill)
            if transferable_skill:
                transferable.append({
                    'target_skill': target_skill,
                    'user_skill': transferable_skill,
                    'transferability': 'medium'
                })
        
        return transferable
    
    def _load_skill_synonyms(self) -> Dict[str, List[str]]:
        """Load skill synonym mappings for better matching"""
        
        return {
            'product management': ['product strategy', 'product planning', 'product development'],
            'project management': ['program management', 'project coordination', 'project planning'],
            'data analysis': ['data analytics', 'business intelligence', 'data science'],
            'user experience': ['ux design', 'user research', 'usability testing'],
            'stakeholder management': ['client relations', 'customer success', 'account management'],
            'agile': ['scrum', 'kanban', 'lean methodology', 'agile development'],
            'sql': ['database queries', 'data querying', 'database management'],
            'api': ['rest api', 'api development', 'api integration', 'web services'],
            'javascript': ['js', 'frontend development', 'web development'],
            'python': ['data science', 'automation', 'scripting'],
            'machine learning': ['ml', 'ai', 'artificial intelligence', 'predictive modeling']
        }

class ExperienceMatchingAgent:
    """
    Analyzes experience level and type alignment with job requirements
    """
    
    def __init__(self):
        self.name = "experience_matching_agent"
    
    def analyze(self, user_profile: Dict, job_requirements: Dict) -> AgentResult:
        """Analyze experience level and type matching"""
        start_time = time.time()
        
        try:
            # Extract experience data from nested structure
            user_years = user_profile.get('basic_info', {}).get('experience_years', 0)
            required_years = job_requirements.get('experience_years', 0)
            
            user_level = user_profile.get('basic_info', {}).get('experience_level', 'mid')
            required_level = job_requirements.get('seniority_level', 'mid')
            
            user_industries = user_profile.get('experience', {}).get('industries', [])
            target_industry = job_requirements.get('industry', '').lower()
            
            # Analyze years of experience
            years_analysis = self._analyze_years_requirement(user_years, required_years)
            
            # Analyze seniority level
            level_analysis = self._analyze_seniority_level(user_level, required_level)
            
            # Analyze industry experience
            industry_analysis = self._analyze_industry_experience(user_industries, target_industry)
            
            # Calculate overall experience score
            experience_score = (
                years_analysis['score'] * 0.4 +
                level_analysis['score'] * 0.3 +
                industry_analysis['score'] * 0.3
            )
            
            # Combine findings
            findings = []
            findings.extend(years_analysis['findings'])
            findings.extend(level_analysis['findings'])
            findings.extend(industry_analysis['findings'])
            
            # Combine recommendations
            recommendations = []
            recommendations.extend(years_analysis['recommendations'])
            recommendations.extend(level_analysis['recommendations'])
            recommendations.extend(industry_analysis['recommendations'])
            
            confidence = min(years_analysis['confidence'], level_analysis['confidence'], industry_analysis['confidence'])
            
            return AgentResult(
                success=True,
                score=experience_score,
                confidence=confidence,
                findings=findings,
                recommendations=recommendations,
                metadata={
                    'years_analysis': years_analysis,
                    'level_analysis': level_analysis,
                    'industry_analysis': industry_analysis
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                score=0.0,
                confidence=0.0,
                findings=[f"Experience analysis failed: {str(e)}"],
                recommendations=[],
                metadata={},
                execution_time=time.time() - start_time
            )
    
    def _analyze_years_requirement(self, user_years: int, required_years: int) -> Dict:
        """Analyze years of experience requirement"""
        
        if required_years == 0:
            return {
                'score': 1.0,
                'findings': ['No specific experience requirement mentioned'],
                'recommendations': ['Emphasize relevant experience quality over quantity'],
                'confidence': 1.0
            }
        
        ratio = user_years / required_years if required_years > 0 else 1.0
        
        if ratio >= 1.0:
            score = 1.0
            finding = f"Experience exceeds requirement ({user_years} vs {required_years} years)"
            recommendation = "Strong experience match - emphasize experience breadth"
        elif ratio >= 0.8:
            score = 0.9
            finding = f"Experience meets requirement ({user_years} vs {required_years} years)"
            recommendation = "Good experience match - highlight relevant experience"
        elif ratio >= 0.6:
            score = 0.7
            finding = f"Experience slightly below requirement ({user_years} vs {required_years} years)"
            recommendation = "Emphasize quality and relevance of experience"
        else:
            score = 0.4
            finding = f"Experience significantly below requirement ({user_years} vs {required_years} years)"
            recommendation = "Consider roles requiring less experience or highlight transferable skills"
        
        return {
            'score': score,
            'findings': [finding],
            'recommendations': [recommendation],
            'confidence': 0.9
        }
    
    def _analyze_seniority_level(self, user_level: str, required_level: str) -> Dict:
        """Analyze seniority level alignment"""
        
        level_hierarchy = {
            'entry': 1,
            'junior': 2,
            'mid': 3,
            'senior': 4,
            'staff': 5,
            'principal': 6,
            'director': 7,
            'vp': 8,
            'executive': 9
        }
        
        user_rank = level_hierarchy.get(user_level.lower(), 3)
        required_rank = level_hierarchy.get(required_level.lower(), 3)
        
        if user_rank >= required_rank:
            score = 1.0
            finding = f"Seniority level matches or exceeds requirement ({user_level} >= {required_level})"
            recommendation = "Strong seniority match - emphasize leadership experience"
        elif user_rank >= required_rank - 1:
            score = 0.8
            finding = f"Seniority level close to requirement ({user_level} vs {required_level})"
            recommendation = "Good seniority match - highlight growth trajectory"
        else:
            score = 0.5
            finding = f"Seniority level below requirement ({user_level} vs {required_level})"
            recommendation = "Consider more junior roles or emphasize rapid growth potential"
        
        return {
            'score': score,
            'findings': [finding],
            'recommendations': [recommendation],
            'confidence': 0.85
        }
    
    def _analyze_industry_experience(self, user_industries: List[str], target_industry: str) -> Dict:
        """Analyze industry experience alignment"""
        
        if not target_industry:
            return {
                'score': 0.8,
                'findings': ['No specific industry requirement identified'],
                'recommendations': ['Emphasize transferable skills across industries'],
                'confidence': 0.7
            }
        
        user_industries_lower = [ind.lower() for ind in user_industries]
        
        if target_industry in user_industries_lower:
            score = 1.0
            finding = f"Direct industry experience match ({target_industry})"
            recommendation = "Strong industry match - emphasize domain expertise"
        elif any(ind in target_industry or target_industry in ind for ind in user_industries_lower):
            score = 0.8
            finding = f"Related industry experience ({', '.join(user_industries_lower[:2])})"
            recommendation = "Good industry alignment - highlight transferable domain knowledge"
        else:
            # Check for adjacent industries
            adjacent_score = self._calculate_industry_adjacency(user_industries_lower, target_industry)
            score = adjacent_score
            
            if score >= 0.6:
                finding = f"Adjacent industry experience with transferable skills"
                recommendation = "Emphasize transferable skills and industry transition capability"
            else:
                finding = f"Different industry background ({', '.join(user_industries_lower[:2])} vs {target_industry})"
                recommendation = "Consider industry transition challenges and emphasize universal skills"
        
        return {
            'score': score,
            'findings': [finding],
            'recommendations': [recommendation],
            'confidence': 0.8
        }
    
    def _calculate_industry_adjacency(self, user_industries: List[str], target_industry: str) -> float:
        """Calculate how adjacent user industries are to target industry"""
        
        industry_clusters = {
            'fintech': ['finance', 'banking', 'payments', 'insurance', 'investment'],
            'saas': ['software', 'technology', 'cloud', 'enterprise'],
            'ecommerce': ['retail', 'marketplace', 'commerce', 'shopping'],
            'healthtech': ['healthcare', 'medical', 'pharmaceutical', 'biotech'],
            'edtech': ['education', 'learning', 'training', 'academia']
        }
        
        # Find which cluster target industry belongs to
        target_cluster = None
        for cluster, industries in industry_clusters.items():
            if target_industry in industries or any(ind in target_industry for ind in industries):
                target_cluster = industries
                break
        
        if not target_cluster:
            return 0.4  # Default for unknown industry
        
        # Check if user has experience in the same cluster
        for user_industry in user_industries:
            if any(cluster_ind in user_industry for cluster_ind in target_cluster):
                return 0.7  # Adjacent industry experience
        
        return 0.4  # Different industry cluster

class IndustryAlignmentAgent:
    """
    Analyzes industry transition feasibility and cultural fit
    """
    
    def __init__(self):
        self.name = "industry_alignment_agent"
    
    def analyze(self, user_profile: Dict, job_requirements: Dict) -> AgentResult:
        """Analyze industry alignment and transition feasibility"""
        start_time = time.time()
        
        try:
            user_industries = [ind.lower() for ind in user_profile.get('experience', {}).get('industries', [])]
            target_industry = job_requirements.get('industry', '').lower()
            company_stage = job_requirements.get('company_stage', 'unknown').lower()
            company_size = job_requirements.get('company_size', 'unknown').lower()
            
            # Analyze industry transition
            transition_analysis = self._analyze_industry_transition(user_industries, target_industry)
            
            # Analyze company stage fit
            stage_analysis = self._analyze_company_stage_fit(user_profile, company_stage)
            
            # Analyze company size fit
            size_analysis = self._analyze_company_size_fit(user_profile, company_size)
            
            # Calculate overall industry alignment score
            alignment_score = (
                transition_analysis['score'] * 0.5 +
                stage_analysis['score'] * 0.25 +
                size_analysis['score'] * 0.25
            )
            
            # Combine findings and recommendations
            findings = []
            findings.extend(transition_analysis['findings'])
            findings.extend(stage_analysis['findings'])
            findings.extend(size_analysis['findings'])
            
            recommendations = []
            recommendations.extend(transition_analysis['recommendations'])
            recommendations.extend(stage_analysis['recommendations'])
            recommendations.extend(size_analysis['recommendations'])
            
            confidence = min(
                transition_analysis['confidence'],
                stage_analysis['confidence'],
                size_analysis['confidence']
            )
            
            return AgentResult(
                success=True,
                score=alignment_score,
                confidence=confidence,
                findings=findings,
                recommendations=recommendations,
                metadata={
                    'transition_analysis': transition_analysis,
                    'stage_analysis': stage_analysis,
                    'size_analysis': size_analysis,
                    'transition_difficulty': self._assess_transition_difficulty(alignment_score)
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                score=0.0,
                confidence=0.0,
                findings=[f"Industry analysis failed: {str(e)}"],
                recommendations=[],
                metadata={},
                execution_time=time.time() - start_time
            )
    
    def _analyze_industry_transition(self, user_industries: List[str], target_industry: str) -> Dict:
        """Analyze feasibility of industry transition"""
        
        if not target_industry:
            return {
                'score': 0.8,
                'findings': ['Industry not clearly specified'],
                'recommendations': ['Research target industry requirements'],
                'confidence': 0.6
            }
        
        # Check for direct match
        if target_industry in user_industries:
            return {
                'score': 1.0,
                'findings': [f'Direct industry match: {target_industry}'],
                'recommendations': ['Emphasize deep industry knowledge'],
                'confidence': 1.0
            }
        
        # Calculate transition difficulty
        transition_score = self._calculate_transition_score(user_industries, target_industry)
        
        if transition_score >= 0.8:
            finding = 'Easy industry transition - adjacent industries'
            recommendation = 'Highlight transferable industry knowledge'
        elif transition_score >= 0.6:
            finding = 'Moderate industry transition - some overlap'
            recommendation = 'Emphasize universal skills and quick learning ability'
        elif transition_score >= 0.4:
            finding = 'Challenging industry transition - limited overlap'
            recommendation = 'Focus on core skills and demonstrate adaptability'
        else:
            finding = 'Difficult industry transition - significant differences'
            recommendation = 'Consider if industry change aligns with career goals'
        
        return {
            'score': transition_score,
            'findings': [finding],
            'recommendations': [recommendation],
            'confidence': 0.8
        }
    
    def _calculate_transition_score(self, user_industries: List[str], target_industry: str) -> float:
        """Calculate industry transition difficulty score"""
        
        # Industry transition matrix (simplified)
        transitions = {
            'fintech': {'finance': 1.0, 'banking': 1.0, 'saas': 0.8, 'technology': 0.8},
            'saas': {'technology': 1.0, 'software': 1.0, 'fintech': 0.8, 'ecommerce': 0.7},
            'ecommerce': {'retail': 1.0, 'saas': 0.7, 'technology': 0.7, 'marketplace': 1.0},
            'healthcare': {'medtech': 1.0, 'pharmaceutical': 0.9, 'saas': 0.6},
            'finance': {'fintech': 1.0, 'banking': 1.0, 'insurance': 0.9, 'saas': 0.6}
        }
        
        max_score = 0.0
        
        for user_industry in user_industries:
            # Direct lookup
            if user_industry in transitions.get(target_industry, {}):
                max_score = max(max_score, transitions[target_industry][user_industry])
            elif target_industry in transitions.get(user_industry, {}):
                max_score = max(max_score, transitions[user_industry][target_industry])
            else:
                # Generic similarity check
                similarity = self._calculate_industry_similarity(user_industry, target_industry)
                max_score = max(max_score, similarity)
        
        return min(max_score, 1.0)
    
    def _calculate_industry_similarity(self, industry1: str, industry2: str) -> float:
        """Calculate similarity between two industries"""
        
        # B2B vs B2C
        b2b_industries = ['saas', 'enterprise', 'fintech', 'consulting']
        b2c_industries = ['ecommerce', 'retail', 'consumer', 'gaming']
        
        industry1_b2b = any(b2b in industry1 for b2b in b2b_industries)
        industry2_b2b = any(b2b in industry2 for b2b in b2b_industries)
        
        if industry1_b2b == industry2_b2b:
            return 0.6  # Same business model
        
        return 0.4  # Different business models
    
    def _analyze_company_stage_fit(self, user_profile: Dict, company_stage: str) -> Dict:
        """Analyze fit with company stage (startup, scaleup, enterprise)"""
        
        user_preferences = user_profile.get('company_stage_preference', [])
        
        if company_stage == 'unknown':
            return {
                'score': 0.8,
                'findings': ['Company stage not clearly identified'],
                'recommendations': ['Research company stage and culture'],
                'confidence': 0.6
            }
        
        if company_stage in user_preferences or not user_preferences:
            return {
                'score': 1.0,
                'findings': [f'Good company stage fit: {company_stage}'],
                'recommendations': [f'Emphasize {company_stage} experience'],
                'confidence': 0.9
            }
        
        # Analyze stage transition
        stage_scores = {
            'startup': 0.8,    # High energy, fast pace
            'scaleup': 0.9,    # Good balance
            'enterprise': 0.7   # More structured
        }
        
        score = stage_scores.get(company_stage, 0.7)
        
        return {
            'score': score,
            'findings': [f'Company stage: {company_stage} - consider cultural fit'],
            'recommendations': [f'Research {company_stage} company culture and expectations'],
            'confidence': 0.7
        }
    
    def _analyze_company_size_fit(self, user_profile: Dict, company_size: str) -> Dict:
        """Analyze fit with company size"""
        
        if company_size == 'unknown':
            return {
                'score': 0.8,
                'findings': ['Company size not specified'],
                'recommendations': ['Research company size and structure'],
                'confidence': 0.6
            }
        
        # Most product managers can adapt to different company sizes
        return {
            'score': 0.9,
            'findings': [f'Company size: {company_size}'],
            'recommendations': ['Adapt experience examples to company size context'],
            'confidence': 0.8
        }
    
    def _assess_transition_difficulty(self, alignment_score: float) -> str:
        """Assess overall transition difficulty"""
        
        if alignment_score >= 0.8:
            return 'low'
        elif alignment_score >= 0.6:
            return 'medium'
        elif alignment_score >= 0.4:
            return 'high'
        else:
            return 'very_high'

# Export all agents
__all__ = [
    'DomainMismatchAgent',
    'SkillsGapAgent', 
    'ExperienceMatchingAgent',
    'IndustryAlignmentAgent',
    'AgentResult'
]