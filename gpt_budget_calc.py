#!/usr/bin/env python3
"""
GPT Budget Calculator for $5 Credit
"""

def calculate_gpt_budget():
    print("💰 Your $5 GPT Budget Analysis")
    print("=" * 40)
    
    gpt_cost_per_app = 0.0050  # 0.5¢ per application
    budget = 5.00
    
    max_applications = int(budget / gpt_cost_per_app)
    
    print(f"💸 Cost per application: ${gpt_cost_per_app:.4f} (~0.5¢)")
    print(f"🎯 Maximum applications with $5: {max_applications:,}")
    print()
    
    # Different scenarios
    scenarios = [100, 500, 1000]
    
    for apps in scenarios:
        total_cost = apps * gpt_cost_per_app
        remaining = budget - total_cost
        
        if remaining >= 0:
            print(f"✅ {apps:,} applications: ${total_cost:.2f} (${remaining:.2f} left)")
        else:
            print(f"❌ {apps:,} applications: ${total_cost:.2f} (${abs(remaining):.2f} over budget)")
    
    print(f"\n🚀 RECOMMENDATION:")
    print(f"   Your $5 budget is perfect for GPT-3.5!")
    print(f"   You can generate 1,000 applications and still have ${budget - (1000 * gpt_cost_per_app):.2f} left!")

if __name__ == "__main__":
    calculate_gpt_budget()