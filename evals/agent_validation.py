#!/usr/bin/env python3
"""
Agent Validation Framework
Tests and validates LLM agent performance with specific evaluation metrics.
"""

import json
import sys
import os
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import statistics

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from modules.llm_agents import SkillsAnalyzer, ContentOptimizer, CulturalToneAdapter, ContentRewriter, AgentOrchestrator

class AgentValidator:
    """Validates LLM agent performance with comprehensive testing"""
    
    def __init__(self):
        self.skills_analyzer = SkillsAnalyzer()
        self.content_optimizer = ContentOptimizer()
        self.cultural_adapter = CulturalToneAdapter()
        self.content_rewriter = ContentRewriter()
        self.orchestrator = AgentOrchestrator()
        
    def validate_skills_analyzer(self) -> Dict[str, Any]:
        """Validate SkillsAnalyzer agent performance"""
        
        test_cases = [
            {
                "name": "High_Match_AI_Role",
                "user_skills": [
                    "Product Management", "AI/ML", "RAG Architecture", "Salesforce", 
                    "Cross-functional Leadership", "System Integration"
                ],
                "jd_requirements": {
                    "required_skills": ["Product Management", "AI/ML", "Internal Tools", "Cross-functional Leadership"],
                    "preferred_skills": ["RAG", "System Integration", "SaaS"],
                    "focus_areas": ["AI automation", "internal operations"],
                    "company_context": "SaaS platform for global teams"
                },
                "expected_alignment": 85  # Expected alignment score
            },
            {
                "name": "Medium_Match_B2B_Role",
                "user_skills": [
                    "Product Management", "Salesforce", "B2B Strategy", "API Integration"
                ],
                "jd_requirements": {
                    "required_skills": ["Product Management", "B2B Experience", "CRM", "Enterprise"],
                    "preferred_skills": ["Salesforce", "API", "Analytics"],
                    "focus_areas": ["enterprise solutions", "customer success"],
                    "company_context": "B2B SaaS company"
                },
                "expected_alignment": 70
            },
            {
                "name": "Low_Match_Different_Focus",
                "user_skills": [
                    "Product Management", "AI/ML", "RAG", "Technical Architecture"
                ],
                "jd_requirements": {
                    "required_skills": ["Marketing", "Content Strategy", "Social Media", "Brand Management"],
                    "preferred_skills": ["Analytics", "Creative", "Communications"],
                    "focus_areas": ["brand awareness", "content creation"],
                    "company_context": "Digital marketing agency"
                },
                "expected_alignment": 30
            }
        ]
        
        results = {
            "agent": "SkillsAnalyzer",
            "test_results": [],
            "performance_metrics": {},
            "timestamp": datetime.now().isoformat()
        }
        
        print("🧪 Testing SkillsAnalyzer Agent")
        print("-" * 40)
        
        for test_case in test_cases:
            print(f"\\n📋 Test: {test_case['name']}")
            
            start_time = time.time()
            response = self.skills_analyzer.analyze_skills_alignment(
                test_case["user_skills"],
                test_case["jd_requirements"]
            )
            execution_time = time.time() - start_time
            
            if response.success:
                actual_alignment = response.data.get('alignment_score', 0)
                expected_alignment = test_case['expected_alignment']
                
                # Calculate accuracy (how close to expected score)
                accuracy = max(0, 100 - abs(actual_alignment - expected_alignment))
                
                test_result = {
                    "test_name": test_case['name'],
                    "success": True,
                    "expected_alignment": expected_alignment,
                    "actual_alignment": actual_alignment,
                    "accuracy": accuracy,
                    "execution_time": execution_time,
                    "confidence": response.confidence_score,
                    "priority_skills_count": len(response.data.get('priority_skills', [])),
                    "recommendations_count": len(response.data.get('recommendations', []))
                }
                
                print(f"  ✅ Alignment: {actual_alignment}% (expected: {expected_alignment}%)")
                print(f"  📊 Accuracy: {accuracy:.1f}%")
                print(f"  ⚡ Time: {execution_time:.2f}s")
                
            else:
                test_result = {
                    "test_name": test_case['name'],
                    "success": False,
                    "error": response.reasoning,
                    "execution_time": execution_time
                }
                print(f"  ❌ Failed: {response.reasoning}")
            
            results["test_results"].append(test_result)
        
        # Calculate performance metrics
        successful_tests = [t for t in results["test_results"] if t["success"]]
        if successful_tests:
            accuracies = [t["accuracy"] for t in successful_tests]
            execution_times = [t["execution_time"] for t in successful_tests]
            
            results["performance_metrics"] = {
                "success_rate": len(successful_tests) / len(test_cases) * 100,
                "average_accuracy": statistics.mean(accuracies),
                "average_execution_time": statistics.mean(execution_times),
                "min_accuracy": min(accuracies),
                "max_accuracy": max(accuracies)
            }
        
        return results
    
    def validate_content_optimizer(self) -> Dict[str, Any]:
        """Validate ContentOptimizer agent performance"""
        
        test_cases = [
            {
                "name": "High_Quality_Content",
                "content": "Built AI-powered RAG system achieving 94% accuracy serving 200+ users with 1,500+ weekly queries, reduced support tickets 75%, accelerated operations saving 50+ resource hours daily through intelligent automation and cross-functional collaboration.",
                "context": {
                    "role": "Product Manager",
                    "company": "SaaS Company",
                    "requirements": ["AI", "automation", "cross-functional", "metrics"]
                },
                "expected_score": 8.5
            },
            {
                "name": "Medium_Quality_Content",
                "content": "Managed product development and worked with teams to improve processes. Achieved good results and customer satisfaction.",
                "context": {
                    "role": "Product Manager",
                    "company": "Tech Startup",
                    "requirements": ["product management", "teamwork", "results"]
                },
                "expected_score": 5.5
            },
            {
                "name": "Low_Quality_Content",
                "content": "Did some work on products. Helped the team sometimes. Things went okay.",
                "context": {
                    "role": "Product Manager",
                    "company": "Company",
                    "requirements": ["management", "leadership"]
                },
                "expected_score": 3.0
            }
        ]
        
        results = {
            "agent": "ContentOptimizer",
            "test_results": [],
            "performance_metrics": {},
            "timestamp": datetime.now().isoformat()
        }
        
        print("\\n🧪 Testing ContentOptimizer Agent")
        print("-" * 40)
        
        for test_case in test_cases:
            print(f"\\n📋 Test: {test_case['name']}")
            
            start_time = time.time()
            response = self.content_optimizer.score_content_quality(
                test_case["content"],
                test_case["context"]
            )
            execution_time = time.time() - start_time
            
            if response.success:
                actual_score = response.data.get('overall_score', 0)
                expected_score = test_case['expected_score']
                
                # Calculate accuracy
                accuracy = max(0, 100 - abs((actual_score - expected_score) * 10))
                
                test_result = {
                    "test_name": test_case['name'],
                    "success": True,
                    "expected_score": expected_score,
                    "actual_score": actual_score,
                    "accuracy": accuracy,
                    "execution_time": execution_time,
                    "confidence": response.confidence_score,
                    "improvements_count": len(response.data.get('improvements', []))
                }
                
                print(f"  ✅ Score: {actual_score:.1f}/10 (expected: {expected_score}/10)")
                print(f"  📊 Accuracy: {accuracy:.1f}%")
                
            else:
                test_result = {
                    "test_name": test_case['name'],
                    "success": False,
                    "error": response.reasoning,
                    "execution_time": execution_time
                }
                print(f"  ❌ Failed: {response.reasoning}")
            
            results["test_results"].append(test_result)
        
        # Calculate performance metrics
        successful_tests = [t for t in results["test_results"] if t["success"]]
        if successful_tests:
            accuracies = [t["accuracy"] for t in successful_tests]
            execution_times = [t["execution_time"] for t in successful_tests]
            
            results["performance_metrics"] = {
                "success_rate": len(successful_tests) / len(test_cases) * 100,
                "average_accuracy": statistics.mean(accuracies),
                "average_execution_time": statistics.mean(execution_times)
            }
        
        return results
    
    def validate_cultural_adapter(self) -> Dict[str, Any]:
        """Validate CulturalToneAdapter agent performance"""
        
        test_cases = [
            {
                "name": "Netherlands_Direct_Adaptation",
                "content": "I believe I could potentially contribute to your team's success with my experience.",
                "country": "netherlands",
                "expected_adaptations": ["more direct", "remove hedging", "results-focused"]
            },
            {
                "name": "Sweden_Modest_Adaptation", 
                "content": "I am an exceptional leader who delivers outstanding results consistently.",
                "country": "sweden",
                "expected_adaptations": ["modest language", "collaborative", "avoid superlatives"]
            },
            {
                "name": "Ireland_Warm_Adaptation",
                "content": "Here are my qualifications and metrics for your consideration.",
                "country": "ireland", 
                "expected_adaptations": ["warmer tone", "personal", "relationship-focused"]
            }
        ]
        
        results = {
            "agent": "CulturalToneAdapter",
            "test_results": [],
            "performance_metrics": {},
            "timestamp": datetime.now().isoformat()
        }
        
        print("\\n🧪 Testing CulturalToneAdapter Agent")
        print("-" * 40)
        
        for test_case in test_cases:
            print(f"\\n📋 Test: {test_case['name']}")
            
            start_time = time.time()
            response = self.cultural_adapter.adapt_for_culture(
                test_case["content"],
                test_case["country"]
            )
            execution_time = time.time() - start_time
            
            if response.success:
                cultural_notes = response.data.get('cultural_notes', [])
                tone_adjustments = response.data.get('tone_adjustments', [])
                
                # Check if expected adaptations are mentioned
                adaptation_mentions = 0
                all_response_text = ' '.join(cultural_notes + tone_adjustments).lower()
                
                for expected_adaptation in test_case['expected_adaptations']:
                    if any(word in all_response_text for word in expected_adaptation.lower().split()):
                        adaptation_mentions += 1
                
                adaptation_accuracy = (adaptation_mentions / len(test_case['expected_adaptations'])) * 100
                
                test_result = {
                    "test_name": test_case['name'],
                    "success": True,
                    "adaptation_accuracy": adaptation_accuracy,
                    "cultural_notes_count": len(cultural_notes),
                    "adjustments_count": len(tone_adjustments),
                    "execution_time": execution_time,
                    "confidence": response.confidence_score
                }
                
                print(f"  ✅ Adaptation accuracy: {adaptation_accuracy:.1f}%")
                print(f"  🌍 Cultural notes: {len(cultural_notes)}")
                
            else:
                test_result = {
                    "test_name": test_case['name'],
                    "success": False,
                    "error": response.reasoning,
                    "execution_time": execution_time
                }
                print(f"  ❌ Failed: {response.reasoning}")
            
            results["test_results"].append(test_result)
        
        # Calculate performance metrics
        successful_tests = [t for t in results["test_results"] if t["success"]]
        if successful_tests:
            accuracies = [t["adaptation_accuracy"] for t in successful_tests]
            execution_times = [t["execution_time"] for t in successful_tests]
            
            results["performance_metrics"] = {
                "success_rate": len(successful_tests) / len(test_cases) * 100,
                "average_accuracy": statistics.mean(accuracies),
                "average_execution_time": statistics.mean(execution_times)
            }
        
        return results
    
    def validate_orchestrator(self) -> Dict[str, Any]:
        """Validate AgentOrchestrator integration"""
        
        test_case = {
            "content": "Built product features and managed development process. Worked with teams to deliver results.",
            "jd_data": {
                "job_title": "Product Manager",
                "company": "Deel",
                "country": "sweden", 
                "required_skills": ["Product Management", "Cross-functional Leadership", "SaaS"],
                "focus_areas": ["internal tools", "operations", "global teams"]
            },
            "user_profile": {
                "skills": ["Product Management", "AI/ML", "Salesforce", "Cross-functional Leadership"]
            }
        }
        
        print("\\n🧪 Testing AgentOrchestrator Integration")
        print("-" * 50)
        
        start_time = time.time()
        pipeline_result = self.orchestrator.optimize_content_pipeline(
            test_case["content"],
            test_case["jd_data"],
            test_case["user_profile"]
        )
        execution_time = time.time() - start_time
        
        # Validate pipeline results
        validation_results = {
            "agent": "AgentOrchestrator",
            "pipeline_success": "error" not in pipeline_result,
            "agents_executed": len(pipeline_result.get("agent_responses", {})),
            "optimization_steps": len(pipeline_result.get("optimization_steps", [])),
            "overall_confidence": pipeline_result.get("overall_confidence", 0),
            "execution_time": execution_time,
            "improvements_count": len(pipeline_result.get("improvements_summary", [])),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ Pipeline Success: {validation_results['pipeline_success']}")
        print(f"🤖 Agents Executed: {validation_results['agents_executed']}")
        print(f"📈 Overall Confidence: {validation_results['overall_confidence']:.2f}")
        print(f"⚡ Execution Time: {execution_time:.2f}s")
        
        return validation_results
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run validation on all agents"""
        
        print("🚀 Running Comprehensive Agent Validation")
        print("=" * 60)
        
        validation_results = {
            "validation_timestamp": datetime.now().isoformat(),
            "framework_version": "1.0.0",
            "agents_tested": [],
            "overall_summary": {}
        }
        
        # Test individual agents
        skills_results = self.validate_skills_analyzer()
        content_results = self.validate_content_optimizer()
        cultural_results = self.validate_cultural_adapter()
        orchestrator_results = self.validate_orchestrator()
        
        validation_results["agents_tested"] = [
            skills_results,
            content_results,
            cultural_results,
            orchestrator_results
        ]
        
        # Calculate overall summary
        individual_agents = [skills_results, content_results, cultural_results]
        success_rates = [agent.get("performance_metrics", {}).get("success_rate", 0) for agent in individual_agents]
        avg_accuracies = [agent.get("performance_metrics", {}).get("average_accuracy", 0) for agent in individual_agents]
        
        validation_results["overall_summary"] = {
            "total_agents_tested": len(individual_agents) + 1,  # +1 for orchestrator
            "average_success_rate": statistics.mean(success_rates) if success_rates else 0,
            "average_accuracy": statistics.mean(avg_accuracies) if avg_accuracies else 0,
            "orchestrator_success": orchestrator_results["pipeline_success"],
            "framework_ready": all(rate > 80 for rate in success_rates) and orchestrator_results["pipeline_success"]
        }
        
        print(f"\\n🏆 VALIDATION SUMMARY")
        print("=" * 30)
        print(f"Average Success Rate: {validation_results['overall_summary']['average_success_rate']:.1f}%")
        print(f"Average Accuracy: {validation_results['overall_summary']['average_accuracy']:.1f}%")
        print(f"Framework Ready: {validation_results['overall_summary']['framework_ready']}")
        
        return validation_results
    
    def save_validation_report(self, results: Dict[str, Any], output_file: str = None):
        """Save validation results to file"""
        
        if output_file is None:
            output_file = f"agent_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\\n📄 Validation report saved to: {output_file}")
        return output_file

if __name__ == "__main__":
    validator = AgentValidator()
    
    # Run comprehensive validation
    results = validator.run_comprehensive_validation()
    
    # Save results
    report_file = validator.save_validation_report(results)
    
    # Print final status
    if results["overall_summary"]["framework_ready"]:
        print("\\n🎉 LLM Agent Framework is ready for production use!")
    else:
        print("\\n⚠️ LLM Agent Framework needs improvement before production use.")