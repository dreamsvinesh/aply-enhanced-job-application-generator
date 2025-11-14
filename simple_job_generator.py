#!/usr/bin/env python3
"""
Simple Job Application Generator
No complex agents, no multiple files - just ONE working script
"""

import os
import json
from pathlib import Path
from datetime import datetime

def load_env():
    """Load API key from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def call_openai_simple(prompt, max_tokens=2000):
    """Simple OpenAI call without complex wrappers"""
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        return response.choices[0].message.content, True
        
    except Exception as e:
        return f"Error: {e}", False

def analyze_job(job_description):
    """Simple job analysis"""
    prompt = f"""
Analyze this job and return ONLY a JSON object:

{job_description}

Return exactly this format:
{{
  "company": "Company name",
  "role": "Job title", 
  "domain": "fintech/ai/enterprise/saas",
  "skills": ["skill1", "skill2", "skill3"]
}}
"""
    
    result, success = call_openai_simple(prompt, 500)
    if success:
        try:
            return json.loads(result)
        except:
            return {"company": "Unknown", "role": "Unknown", "domain": "unknown", "skills": []}
    return {"company": "Unknown", "role": "Unknown", "domain": "unknown", "skills": []}

def generate_resume(job_analysis):
    """Generate simple, complete resume"""
    prompt = f"""
Generate a complete resume for this job:
Company: {job_analysis['company']}
Role: {job_analysis['role']}
Domain: {job_analysis['domain']}

Use this profile:
- Vinesh Kumar
- 7+ years Product Manager
- Fintech experience: Payment processing, contract automation ($2M revenue impact)
- Enterprise experience: 600K+ users, ₹180 crores GMV
- AI/ML experience: RAG systems, 94% accuracy

Create a COMPLETE resume focused on {job_analysis['domain']} domain.
NO placeholders, NO "[Your Name]" - use real content.
Format: Clean text, ready to use.
"""
    
    resume, success = call_openai_simple(prompt, 2000)
    return resume if success else "Resume generation failed"

def generate_cover_letter(job_analysis):
    """Generate simple, complete cover letter"""
    prompt = f"""
Generate a complete cover letter for:
Company: {job_analysis['company']}
Role: {job_analysis['role']}

Requirements:
- Address to {job_analysis['company']} hiring team
- Focus on {job_analysis['domain']} experience
- Use real achievements: $2M revenue automation, 94% AI accuracy, ₹180 crores GMV
- 3-4 paragraphs maximum
- Ready to send (NO placeholders)
- Professional but concise

Start with actual content, not "[Your Name]"
"""
    
    letter, success = call_openai_simple(prompt, 1500)
    return letter if success else "Cover letter generation failed"

def save_application(company, resume, cover_letter):
    """Save application to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("output") / f"{company}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save resume
    with open(output_dir / "resume.txt", 'w') as f:
        f.write(resume)
    
    # Save cover letter  
    with open(output_dir / "cover_letter.txt", 'w') as f:
        f.write(cover_letter)
    
    # Save summary
    with open(output_dir / "summary.txt", 'w') as f:
        f.write(f"Application for {company}\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Files: resume.txt, cover_letter.txt\n")
    
    return str(output_dir)

def main():
    """Simple main function"""
    load_env()
    
    print("🚀 SIMPLE Job Application Generator")
    print("No complex agents - just working generation")
    print("=" * 50)
    
    # Get job description
    print("\nPaste job description (press Enter twice when done):")
    lines = []
    empty_count = 0
    
    while True:
        line = input()
        if line.strip() == "":
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
            lines.append(line)
    
    job_description = "\n".join(lines)
    
    if not job_description.strip():
        print("❌ No job description provided")
        return
    
    print("\n🔍 Analyzing job...")
    job_analysis = analyze_job(job_description)
    
    print(f"   Company: {job_analysis['company']}")
    print(f"   Role: {job_analysis['role']}")
    print(f"   Domain: {job_analysis['domain']}")
    
    print("\n📝 Generating resume...")
    resume = generate_resume(job_analysis)
    
    print("📋 Generating cover letter...")
    cover_letter = generate_cover_letter(job_analysis)
    
    print("💾 Saving files...")
    output_dir = save_application(job_analysis['company'], resume, cover_letter)
    
    print(f"\n✅ DONE!")
    print(f"📁 Files saved to: {output_dir}")
    print(f"📄 resume.txt")
    print(f"📋 cover_letter.txt")
    print(f"📊 summary.txt")
    
    # Show preview
    print(f"\n👀 Resume preview (first 200 chars):")
    print(resume[:200] + "...")
    
    print(f"\n👀 Cover letter preview (first 200 chars):")
    print(cover_letter[:200] + "...")

if __name__ == "__main__":
    main()