#!/usr/bin/env python3
"""
Brutal Workflow Validation Agent
Uncompromising validation of each step in the resume generation workflow.
Retries failed steps once, then reports failures with detailed analysis.
"""

import time
import json
import traceback
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class ValidationStep:
    """Individual validation step"""
    step_id: str
    step_name: str
    input_data: Any
    expected_output_type: str
    validation_function: Callable
    retry_count: int = 0
    max_retries: int = 1
    status: str = "PENDING"  # PENDING, RUNNING, PASSED, FAILED, RETRYING
    output_data: Any = None
    error_message: str = ""
    execution_time: float = 0.0
    validation_details: Dict = None

@dataclass 
class WorkflowValidationResult:
    """Complete workflow validation result"""
    workflow_name: str
    total_steps: int
    passed_steps: int
    failed_steps: int
    overall_status: str
    execution_time: float
    validation_steps: List[ValidationStep]
    critical_failures: List[str]
    warnings: List[str]
    recommendations: List[str]

class BrutalWorkflowValidator:
    """
    Brutal validation agent that:
    1. Validates every single step input/output
    2. Retries failed steps ONCE
    3. Provides uncompromising detailed analysis
    4. Forces completion or reports exact failures
    """
    
    def __init__(self):
        self.current_workflow: Optional[str] = None
        self.validation_steps: List[ValidationStep] = []
        self.start_time: float = 0
        self.brutal_mode = True  # No tolerance for failures
        
    def start_workflow_validation(self, workflow_name: str) -> None:
        """Start validating a complete workflow"""
        self.current_workflow = workflow_name
        self.validation_steps = []
        self.start_time = time.time()
        
        print(f"🔥 BRUTAL WORKFLOW VALIDATION STARTED: {workflow_name}")
        print(f"⚡ Mode: UNCOMPROMISING - Every step will be validated")
        print(f"🔄 Retry Policy: 1 retry per failed step, then FAILURE")
        print("=" * 80)
    
    def add_validation_step(self, 
                          step_id: str, 
                          step_name: str, 
                          input_data: Any,
                          expected_output_type: str,
                          validation_function: Callable) -> ValidationStep:
        """Add a step to be validated"""
        step = ValidationStep(
            step_id=step_id,
            step_name=step_name,
            input_data=input_data,
            expected_output_type=expected_output_type,
            validation_function=validation_function
        )
        self.validation_steps.append(step)
        return step
    
    def execute_and_validate_step(self, step: ValidationStep, operation: Callable) -> bool:
        """Execute operation and brutally validate the step"""
        
        print(f"\n🔍 VALIDATING STEP: {step.step_name} (ID: {step.step_id})")
        print(f"📥 Input Type: {type(step.input_data).__name__}")
        print(f"🎯 Expected Output: {step.expected_output_type}")
        
        step.status = "RUNNING"
        step_start_time = time.time()
        
        try:
            # Execute the operation
            print("⚡ EXECUTING...")
            step.output_data = operation(step.input_data)
            step.execution_time = time.time() - step_start_time
            
            # Brutal validation of output
            validation_result = self._brutal_validate_output(step)
            
            if validation_result["is_valid"]:
                step.status = "PASSED"
                step.validation_details = validation_result
                print(f"✅ STEP PASSED: {step.step_name}")
                print(f"⏱️  Execution Time: {step.execution_time:.2f}s")
                return True
            else:
                step.status = "FAILED"
                step.error_message = validation_result["error"]
                step.validation_details = validation_result
                print(f"❌ STEP FAILED: {step.step_name}")
                print(f"💥 Error: {step.error_message}")
                
                # BRUTAL RETRY LOGIC
                if step.retry_count < step.max_retries:
                    return self._retry_step(step, operation)
                else:
                    print(f"🚫 STEP PERMANENTLY FAILED: {step.step_name}")
                    return False
                    
        except Exception as e:
            step.execution_time = time.time() - step_start_time
            step.status = "FAILED"
            step.error_message = f"Exception: {str(e)}"
            step.validation_details = {"exception": traceback.format_exc()}
            
            print(f"💀 STEP CRASHED: {step.step_name}")
            print(f"🔥 Exception: {str(e)}")
            
            # BRUTAL RETRY LOGIC
            if step.retry_count < step.max_retries:
                return self._retry_step(step, operation)
            else:
                print(f"☠️  STEP PERMANENTLY FAILED: {step.step_name}")
                return False
    
    def _retry_step(self, step: ValidationStep, operation: Callable) -> bool:
        """Retry a failed step ONCE"""
        step.retry_count += 1
        step.status = "RETRYING"
        
        print(f"🔄 RETRYING STEP: {step.step_name} (Attempt {step.retry_count + 1})")
        print("⚠️  This is the ONLY retry - failure means permanent failure")
        
        time.sleep(1)  # Brief pause before retry
        
        return self.execute_and_validate_step(step, operation)
    
    def _brutal_validate_output(self, step: ValidationStep) -> Dict[str, Any]:
        """Brutally validate step output - no mercy for incomplete results"""
        
        validation_result = {
            "is_valid": False,
            "error": "",
            "details": {},
            "brutal_checks": []
        }
        
        # Check 1: Output exists
        if step.output_data is None:
            validation_result["error"] = "Output is None - UNACCEPTABLE"
            validation_result["brutal_checks"].append("❌ Output existence: FAILED")
            return validation_result
        
        validation_result["brutal_checks"].append("✅ Output existence: PASSED")
        
        # Check 2: Output type validation
        expected_type = step.expected_output_type.lower()
        output_type = type(step.output_data).__name__.lower()
        
        if expected_type == "dict" and not isinstance(step.output_data, dict):
            validation_result["error"] = f"Expected dict, got {output_type}"
            validation_result["brutal_checks"].append(f"❌ Type validation: FAILED ({output_type} != dict)")
            return validation_result
        elif expected_type == "str" and not isinstance(step.output_data, str):
            validation_result["error"] = f"Expected string, got {output_type}"
            validation_result["brutal_checks"].append(f"❌ Type validation: FAILED ({output_type} != str)")
            return validation_result
        elif expected_type == "list" and not isinstance(step.output_data, list):
            validation_result["error"] = f"Expected list, got {output_type}"
            validation_result["brutal_checks"].append(f"❌ Type validation: FAILED ({output_type} != list)")
            return validation_result
        
        validation_result["brutal_checks"].append(f"✅ Type validation: PASSED ({output_type})")
        
        # Check 3: Content validation using provided validation function
        try:
            custom_validation = step.validation_function(step.input_data, step.output_data)
            if not custom_validation["is_valid"]:
                validation_result["error"] = f"Custom validation failed: {custom_validation['error']}"
                validation_result["brutal_checks"].append("❌ Custom validation: FAILED")
                validation_result["details"].update(custom_validation)
                return validation_result
            
            validation_result["brutal_checks"].append("✅ Custom validation: PASSED")
            validation_result["details"].update(custom_validation)
            
        except Exception as e:
            validation_result["error"] = f"Validation function crashed: {str(e)}"
            validation_result["brutal_checks"].append("💀 Custom validation: CRASHED")
            return validation_result
        
        # Check 4: Size/length validation for collections
        if isinstance(step.output_data, (list, dict, str)):
            if len(step.output_data) == 0:
                validation_result["error"] = "Output is empty - UNACCEPTABLE"
                validation_result["brutal_checks"].append("❌ Content size: FAILED (empty)")
                return validation_result
            
            validation_result["brutal_checks"].append(f"✅ Content size: PASSED ({len(step.output_data)} items)")
        
        # All brutal checks passed
        validation_result["is_valid"] = True
        validation_result["details"]["output_size"] = len(step.output_data) if hasattr(step.output_data, '__len__') else "N/A"
        validation_result["details"]["output_type"] = type(step.output_data).__name__
        
        return validation_result
    
    def finish_workflow_validation(self) -> WorkflowValidationResult:
        """Complete workflow validation and generate brutal analysis"""
        
        total_time = time.time() - self.start_time
        passed_steps = len([s for s in self.validation_steps if s.status == "PASSED"])
        failed_steps = len([s for s in self.validation_steps if s.status == "FAILED"])
        
        # Determine overall status
        if failed_steps == 0:
            overall_status = "PASSED"
        elif failed_steps < len(self.validation_steps) / 2:
            overall_status = "PARTIAL_FAILURE" 
        else:
            overall_status = "FAILED"
        
        # Generate brutal analysis
        critical_failures = []
        warnings = []
        recommendations = []
        
        for step in self.validation_steps:
            if step.status == "FAILED":
                critical_failures.append(f"Step {step.step_id} ({step.step_name}): {step.error_message}")
                recommendations.append(f"Fix {step.step_name}: Review input data and implementation logic")
            
            if step.execution_time > 10:  # Slow steps
                warnings.append(f"Step {step.step_name} is slow: {step.execution_time:.2f}s")
                recommendations.append(f"Optimize {step.step_name}: Performance is below acceptable threshold")
        
        result = WorkflowValidationResult(
            workflow_name=self.current_workflow,
            total_steps=len(self.validation_steps),
            passed_steps=passed_steps,
            failed_steps=failed_steps,
            overall_status=overall_status,
            execution_time=total_time,
            validation_steps=self.validation_steps,
            critical_failures=critical_failures,
            warnings=warnings,
            recommendations=recommendations
        )
        
        self._print_brutal_summary(result)
        return result
    
    def _print_brutal_summary(self, result: WorkflowValidationResult) -> None:
        """Print uncompromising summary of validation results"""
        
        print("\n" + "=" * 80)
        print("🔥 BRUTAL WORKFLOW VALIDATION COMPLETE")
        print("=" * 80)
        
        print(f"📊 WORKFLOW: {result.workflow_name}")
        print(f"⏱️  TOTAL TIME: {result.execution_time:.2f}s")
        print(f"📈 SUCCESS RATE: {result.passed_steps}/{result.total_steps} ({(result.passed_steps/result.total_steps*100):.1f}%)")
        
        # Overall status with brutal honesty
        if result.overall_status == "PASSED":
            print("🎉 OVERALL STATUS: ✅ PASSED - All steps executed successfully")
        elif result.overall_status == "PARTIAL_FAILURE":
            print("⚠️  OVERALL STATUS: 🟡 PARTIAL FAILURE - Some steps failed")
        else:
            print("💀 OVERALL STATUS: ❌ FAILED - Workflow has critical failures")
        
        # Critical failures (brutal reporting)
        if result.critical_failures:
            print(f"\n💥 CRITICAL FAILURES ({len(result.critical_failures)}):")
            for i, failure in enumerate(result.critical_failures, 1):
                print(f"  {i}. {failure}")
        
        # Warnings
        if result.warnings:
            print(f"\n⚠️  WARNINGS ({len(result.warnings)}):")
            for i, warning in enumerate(result.warnings, 1):
                print(f"  {i}. {warning}")
        
        # Brutal recommendations
        if result.recommendations:
            print(f"\n🔧 BRUTAL RECOMMENDATIONS ({len(result.recommendations)}):")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"  {i}. {rec}")
        
        # Step-by-step breakdown
        print(f"\n📋 DETAILED STEP BREAKDOWN:")
        print("-" * 60)
        
        for step in result.validation_steps:
            status_emoji = {"PASSED": "✅", "FAILED": "❌", "RETRYING": "🔄"}
            emoji = status_emoji.get(step.status, "❓")
            
            print(f"{emoji} {step.step_id}: {step.step_name}")
            print(f"   Status: {step.status}")
            print(f"   Time: {step.execution_time:.2f}s")
            
            if step.retry_count > 0:
                print(f"   Retries: {step.retry_count}")
            
            if step.error_message:
                print(f"   Error: {step.error_message}")
            
            if step.validation_details and step.validation_details.get("brutal_checks"):
                print("   Validation Checks:")
                for check in step.validation_details["brutal_checks"]:
                    print(f"     {check}")
            
            print()
        
        print("=" * 80)
    
    def save_validation_report(self, result: WorkflowValidationResult, output_dir: str) -> str:
        """Save detailed validation report to file"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Convert dataclass to dict for JSON serialization
        report_data = asdict(result)
        
        # Add timestamp and additional metadata
        report_data["generated_at"] = datetime.now().isoformat()
        report_data["validator_version"] = "1.0.0"
        report_data["brutal_mode"] = True
        
        # Save detailed JSON report
        json_report_file = output_path / f"brutal_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_report_file, "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        
        # Save human-readable summary
        summary_file = output_path / f"validation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(summary_file, "w") as f:
            f.write(f"BRUTAL WORKFLOW VALIDATION REPORT\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(f"Workflow: {result.workflow_name}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Time: {result.execution_time:.2f}s\n")
            f.write(f"Success Rate: {result.passed_steps}/{result.total_steps} ({(result.passed_steps/result.total_steps*100):.1f}%)\n")
            f.write(f"Overall Status: {result.overall_status}\n\n")
            
            if result.critical_failures:
                f.write(f"CRITICAL FAILURES:\n")
                for i, failure in enumerate(result.critical_failures, 1):
                    f.write(f"{i}. {failure}\n")
                f.write("\n")
            
            if result.warnings:
                f.write(f"WARNINGS:\n") 
                for i, warning in enumerate(result.warnings, 1):
                    f.write(f"{i}. {warning}\n")
                f.write("\n")
            
            f.write(f"STEP DETAILS:\n")
            for step in result.validation_steps:
                f.write(f"- {step.step_id}: {step.step_name} -> {step.status}\n")
                if step.error_message:
                    f.write(f"  Error: {step.error_message}\n")
        
        print(f"📊 Validation reports saved:")
        print(f"  • JSON Report: {json_report_file}")
        print(f"  • Summary: {summary_file}")
        
        return str(json_report_file)

# Validation functions for specific steps
def validate_data_extraction(input_data: Any, output_data: Any) -> Dict[str, Any]:
    """Validate data extraction step"""
    if not isinstance(output_data, dict):
        return {"is_valid": False, "error": "Output must be dict"}
    
    required_keys = ["personal_info", "work_experience", "education"]
    missing_keys = [key for key in required_keys if key not in output_data]
    
    if missing_keys:
        return {"is_valid": False, "error": f"Missing required keys: {missing_keys}"}
    
    # Validate work experience has content
    work_exp = output_data.get("work_experience", [])
    if len(work_exp) == 0:
        return {"is_valid": False, "error": "No work experience extracted"}
    
    # Check for Senior PM role with sufficient content
    senior_pm_roles = [exp for exp in work_exp if "senior" in exp.get("role", "").lower()]
    if senior_pm_roles:
        for role in senior_pm_roles:
            achievements = role.get("exact_achievements", [])
            if len(achievements) < 5:
                return {"is_valid": False, "error": f"Senior PM role has only {len(achievements)} achievements (minimum 5 required)"}
    
    return {"is_valid": True, "extracted_roles": len(work_exp), "has_senior_pm": len(senior_pm_roles) > 0}

def validate_resume_generation(input_data: Any, output_data: Any) -> Dict[str, Any]:
    """Validate resume generation step"""
    if not isinstance(output_data, dict):
        return {"is_valid": False, "error": "Output must be dict"}
    
    if "content" not in output_data:
        return {"is_valid": False, "error": "Missing 'content' field"}
    
    content = output_data["content"]
    if not isinstance(content, str) or len(content.strip()) == 0:
        return {"is_valid": False, "error": "Content is empty or invalid"}
    
    # Check for required sections (flexible matching)
    required_sections = {
        "experience": ["EXPERIENCE", "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE"],
        "education": ["EDUCATION"],
        "summary": ["SUMMARY", "PROFESSIONAL SUMMARY", "PROFILE"]
    }
    
    content_upper = content.upper()
    missing_sections = []
    
    for section_type, possible_names in required_sections.items():
        if not any(name in content_upper for name in possible_names):
            missing_sections.append(section_type)
    
    if missing_sections:
        return {"is_valid": False, "error": f"Missing sections: {missing_sections}"}
    
    # Check for factual preservation
    if "COWRKS" not in content:
        return {"is_valid": False, "error": "Real company COWRKS not found in content"}
    
    # Check content depth (accept both • and - bullet formats)
    lines = content.split('\n')
    experience_lines = [line for line in lines if line.strip().startswith('•') or line.strip().startswith('-')]
    
    if len(experience_lines) < 8:  # Minimum expected for senior roles
        return {"is_valid": False, "error": f"Insufficient content depth: only {len(experience_lines)} bullet points"}
    
    return {"is_valid": True, "content_length": len(content), "bullet_points": len(experience_lines)}

def validate_ats_scoring(input_data: Any, output_data: Any) -> Dict[str, Any]:
    """Validate ATS scoring step"""
    if not isinstance(output_data, dict):
        return {"is_valid": False, "error": "Output must be dict"}
    
    required_keys = ["overall_ats_score", "grade", "category_scores"]
    missing_keys = [key for key in required_keys if key not in output_data]
    
    if missing_keys:
        return {"is_valid": False, "error": f"Missing required keys: {missing_keys}"}
    
    score = output_data.get("overall_ats_score")
    if not isinstance(score, (int, float)) or score < 0 or score > 100:
        return {"is_valid": False, "error": f"Invalid ATS score: {score}"}
    
    grade = output_data.get("grade")
    if grade not in ["A", "B", "C", "D", "F"]:
        return {"is_valid": False, "error": f"Invalid grade: {grade}"}
    
    return {"is_valid": True, "ats_score": score, "grade": grade}

def validate_optimization(input_data: Any, output_data: Any) -> Dict[str, Any]:
    """Validate optimization step"""
    if not isinstance(output_data, dict):
        return {"is_valid": False, "error": "Output must be dict"}
    
    if "optimized_resume" not in output_data:
        return {"is_valid": False, "error": "Missing 'optimized_resume' field"}
    
    optimized_content = output_data["optimized_resume"]
    if not isinstance(optimized_content, str) or len(optimized_content.strip()) == 0:
        return {"is_valid": False, "error": "Optimized content is empty or invalid"}
    
    # Check for improvement
    if "final_ats_score" in output_data:
        final_score = output_data["final_ats_score"]
        if isinstance(final_score, dict) and "overall_ats_score" in final_score:
            final_ats_score = final_score["overall_ats_score"]
            if not isinstance(final_ats_score, (int, float)):
                return {"is_valid": False, "error": "Invalid final ATS score type"}
    
    return {"is_valid": True, "optimization_completed": True}

def main():
    """Demo of brutal workflow validation"""
    print("🔥 BRUTAL WORKFLOW VALIDATOR DEMO")
    print("=" * 60)
    
    validator = BrutalWorkflowValidator()
    validator.start_workflow_validation("Demo Resume Generation Workflow")
    
    # Demo validation steps
    def mock_data_extraction(input_data):
        return {
            "personal_info": {"name": "Test User"},
            "work_experience": [{"role": "Senior PM", "exact_achievements": ["Achievement 1", "Achievement 2", "Achievement 3", "Achievement 4", "Achievement 5"]}],
            "education": [{"degree": "Test Degree"}]
        }
    
    def mock_resume_generation(input_data):
        return {
            "content": "EXPERIENCE\nSenior PM at COWRKS\n• Achievement 1\n• Achievement 2\n• Achievement 3\n• Achievement 4\n• Achievement 5\n• Achievement 6\n• Achievement 7\n• Achievement 8\nEDUCATION\nTest Degree\nSUMMARY\nTest summary",
            "preserves_facts": True
        }
    
    def mock_ats_scoring(input_data):
        return {
            "overall_ats_score": 85.5,
            "grade": "B",
            "category_scores": {"hard_skills": {"score": 90}}
        }
    
    # Add and execute validation steps
    step1 = validator.add_validation_step("001", "Data Extraction", {}, "dict", validate_data_extraction)
    result1 = validator.execute_and_validate_step(step1, mock_data_extraction)
    
    step2 = validator.add_validation_step("002", "Resume Generation", step1.output_data, "dict", validate_resume_generation)
    result2 = validator.execute_and_validate_step(step2, mock_resume_generation)
    
    step3 = validator.add_validation_step("003", "ATS Scoring", step2.output_data, "dict", validate_ats_scoring)
    result3 = validator.execute_and_validate_step(step3, mock_ats_scoring)
    
    # Finish validation
    final_result = validator.finish_workflow_validation()
    
    # Save report
    report_file = validator.save_validation_report(final_result, "output/validation_reports")
    print(f"\n📊 Demo validation complete! Report: {report_file}")

if __name__ == "__main__":
    main()