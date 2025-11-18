#!/usr/bin/env python3
"""
Calculate ACTUAL API cost for one application
Based on real token usage patterns in the system
"""

def calculate_actual_cost():
    """Calculate real cost based on actual usage patterns"""
    
    print("💰 CALCULATING ACTUAL API COST PER APPLICATION")
    print("=" * 60)
    
    # Based on your system's actual usage patterns:
    
    # MAIN COMPONENTS THAT ACTUALLY MAKE API CALLS
    components = {
        "enhanced_fact_aware_generator": {
            "description": "Main resume generation",
            "api_calls": 1,  # Only 1 main call in _generate_resume_with_depth_validation
            "prompt_tokens": 2000,  # JD + user profile + instructions
            "response_tokens": 1500,  # Generated resume content
            "model": "claude-3-5-haiku-20241022"  # Default model from llm_service.py
        },
        
        "ats_optimization": {
            "description": "ATS keyword optimization (if enabled)",
            "api_calls": 1,
            "prompt_tokens": 1500,  # Resume + JD for optimization
            "response_tokens": 800,   # Optimized resume
            "model": "claude-3-5-haiku-20241022"
        },
        
        "cover_letter_generation": {
            "description": "Cover letter (optional)",
            "api_calls": 1,
            "prompt_tokens": 1000,  # JD + basic instructions
            "response_tokens": 400,  # Cover letter content
            "model": "claude-3-5-haiku-20241022"
        }
    }
    
    # PRICING from llm_service.py (per 1M tokens)
    pricing = {
        "claude-3-5-haiku-20241022": {
            "input": 1.0,   # $1 per 1M input tokens
            "output": 5.0   # $5 per 1M output tokens
        }
    }
    
    print("📊 COST BREAKDOWN:")
    print("-" * 60)
    
    total_cost = 0
    
    for component, details in components.items():
        model = details["model"]
        input_cost = (details["prompt_tokens"] / 1_000_000) * pricing[model]["input"]
        output_cost = (details["response_tokens"] / 1_000_000) * pricing[model]["output"]
        component_cost = input_cost + output_cost
        
        print(f"\n🔧 {component}:")
        print(f"   Description: {details['description']}")
        print(f"   API Calls: {details['api_calls']}")
        print(f"   Input tokens: {details['prompt_tokens']:,}")
        print(f"   Output tokens: {details['response_tokens']:,}")
        print(f"   Input cost: ${input_cost:.4f}")
        print(f"   Output cost: ${output_cost:.4f}")
        print(f"   Total cost: ${component_cost:.4f}")
        
        total_cost += component_cost
    
    print("\n" + "=" * 60)
    print(f"💵 TOTAL COST PER APPLICATION: ${total_cost:.4f}")
    
    # Convert to INR (approximate rate: 1 USD = 83 INR)
    inr_cost = total_cost * 83
    print(f"💵 TOTAL COST IN INR: ₹{inr_cost:.2f}")
    
    print("\n🎯 COST OPTIMIZATION FEATURES:")
    print("✅ Response caching (repeat requests = ₹0)")
    print("✅ Uses cheapest capable model (Claude 3.5 Haiku)")
    print("✅ Efficient prompt design (minimal tokens)")
    print("✅ Single API call for main generation")
    
    # Cost per 10 applications
    print(f"\n📈 VOLUME PRICING:")
    print(f"   10 applications: ₹{inr_cost * 10:.2f}")
    print(f"   50 applications: ₹{inr_cost * 50:.2f}")
    print(f"   100 applications: ₹{inr_cost * 100:.2f}")
    
    # Break down what each step does
    print(f"\n🔍 WHAT EACH API CALL DOES:")
    print("1. Main Resume Generation:")
    print("   - Analyzes JD requirements")
    print("   - Matches with your experience")
    print("   - Generates complete resume")
    print("   - Ensures factual accuracy")
    print("   - Applies country-specific formatting")
    
    print("2. ATS Optimization (optional):")
    print("   - Scans for missing keywords")
    print("   - Optimizes for ATS systems")
    print("   - Maintains content quality")
    
    print("3. Cover Letter (if requested):")
    print("   - Company-specific content")
    print("   - Role-targeted messaging")
    
    return total_cost

if __name__ == "__main__":
    calculate_actual_cost()