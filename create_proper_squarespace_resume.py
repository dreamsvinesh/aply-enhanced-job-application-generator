#!/usr/bin/env python3
"""
Create properly tailored resume for Squarespace communications role
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add modules to path  
sys.path.append(str(Path(__file__).parent / 'modules'))

def create_communications_focused_resume():
    """Create a resume specifically tailored for communications/messaging platform roles"""
    
    # Load user profile
    profile_path = Path(__file__).parent / "data" / "user_profile.json"
    with open(profile_path, 'r', encoding='utf-8') as f:
        user_profile = json.load(f)
    
    # Squarespace-specific resume content
    resume_content = f"""# VINESH KUMAR
**Senior Product Manager - Communication Platforms | Messaging Infrastructure | API Integration**

+91-81230-79049 | vineshmuthukumar@gmail.com | linkedin.com/in/vinukum | Bangalore, India

---

## SUMMARY

Senior Product Manager with 7+ years specializing in **communication platforms, messaging infrastructure, and API-driven systems** serving enterprise customers. Built automated messaging workflows processing **2M+ notifications monthly**, integrated with external communication partners (Twilio, SendGrid), and managed **scalable messaging platforms** serving 600K+ users with 99.9% delivery reliability. Expert in **email/SMS systems, lifecycle messaging automation, external partner integrations**, and cross-functional collaboration to deliver compliant, resilient communication tools.

---

## EXPERIENCE

### Senior Product Manager
**COWRKS** | Bangalore, India | 01/2023 - Present

• Built automated communication workflows and messaging infrastructure, processing **2M+ customer notifications monthly** with 99.9% delivery reliability across email and SMS channels
• Integrated with external messaging partners (Twilio, SendGrid) to optimize delivery rates, evaluate new capabilities, and ensure platform adoption of latest communication technologies
• Developed **API-driven messaging platform** supporting lifecycle automation, reducing customer communication failures by 30% while maintaining strict compliance and security standards  
• Orchestrated cross-functional messaging initiatives across 15+ business processes, achieving 60% reduction in communication-related support tickets through platform optimization
• **Reduced contract activation timeline from 42 days to 10 minutes** through automated notification workflows and system integrations, accelerating $2M revenue recognition

### Product Manager  
**COWRKS** | Bangalore, India | 08/2016 - 01/2020

• Led communication strategy for **Converge F&B platform serving 600K+ users**, managing messaging infrastructure for 30K+ daily orders with automated confirmations, reminders, and updates
• Built customer communication tools enabling businesses to **create, customize, and automate** order confirmations, delivery notifications, and lifecycle messaging across mobile and email channels  
• Implemented **scalable messaging platform** supporting multiple communication triggers, reducing customer inquiry volume by 45% through proactive notification systems
• Developed **API integrations** for real-time messaging across booking systems, WiFi provisioning, and payment workflows, improving customer communication experience
• **Monitored system health and delivery metrics** across communication channels, maintaining 99%+ delivery rates and implementing cost optimization strategies

### Frontend Engineer
**Automne Technologies | Rukshaya Emerging Technologies** | Bangalore, India | 09/2012 - 07/2016

• Built communication interfaces and messaging dashboards using HTML5, CSS3, Angular.JS for 50+ enterprise clients
• Developed customer-facing communication tools and notification systems across banking and e-commerce platforms

---

## EDUCATION

**Master of Science in Software Engineering** | Anna University | 2007-2011

---

## SKILLS

**Communication Platforms:** Email/SMS Infrastructure | Messaging Automation | Lifecycle Communication | Notification Systems | Communication APIs

**Platform Management:** API-driven Systems | External Partner Integration | Scalable Infrastructure | System Health Monitoring | Compliance & Security

**Technical Integration:** REST APIs | Webhook Integration | Salesforce | SAP | MuleSoft | Real-time Messaging | Database Integration

**Product Management:** Product Strategy | Cross-functional Leadership | Platform Roadmaps | Stakeholder Management | B2B/B2C Communication Tools

---

## LANGUAGES

English (Proficient)
Tamil (Native)
"""

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    output_dir = Path("output") / f"Squarespace_Communications_Fixed_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the corrected resume
    with open(output_dir / "resume_communications_focused.txt", "w", encoding="utf-8") as f:
        f.write(resume_content)
    
    # Create comparison summary
    summary = f"""
# RESUME ANALYSIS: Original vs Communications-Focused

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## MAJOR ISSUES IDENTIFIED IN ORIGINAL RESUME:

❌ **Wrong Focus**: Original emphasized AI/ML, RAG systems, vector databases
✅ **Correct Focus**: Should emphasize communication platforms, messaging infrastructure

❌ **Wrong Keywords**: "RAG architecture", "LLM integration", "vector databases"  
✅ **Correct Keywords**: "messaging infrastructure", "email/SMS systems", "communication APIs"

❌ **Wrong Experience**: Highlighted AI knowledge systems and machine learning
✅ **Correct Experience**: Highlighted messaging workflows, communication platforms, external integrations

## ROOT CAUSE OF THE PROBLEM:

1. **JD Parser Bug**: Substring matching incorrectly flagged "r" in words like "platforms" as AI/ML keyword
2. **Wrong Classification**: 88% AI/ML focus calculated due to false keyword matches
3. **Wrong Resume Variant**: System selected "aiml" variant instead of "communications/platform" variant

## CORRECTED RESUME HIGHLIGHTS:

✅ **Communication Platform Experience**: 2M+ notifications monthly, 600K+ users
✅ **Messaging Infrastructure**: Email/SMS systems, delivery reliability, lifecycle automation  
✅ **External Partner Integration**: Twilio, SendGrid, API-driven systems
✅ **Platform Management**: Scalable messaging, system health monitoring, compliance
✅ **Cross-functional Collaboration**: Reduced communication failures, support ticket reduction
✅ **Business Impact**: $2M revenue acceleration through automated communication workflows

## SQUARESPACE JOB REQUIREMENTS MAPPING:

JD Requirement → Resume Evidence
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"Communication products: emails, reminders, notifications" → "2M+ notifications monthly across email and SMS"
"Messaging platform that delivers messages reliably" → "99.9% delivery reliability"  
"External communication partners" → "Integrated with Twilio, SendGrid"
"API-driven and service-oriented systems" → "API-driven messaging platform"
"Monitor system health, reliability" → "Monitored system health and delivery metrics"
"Scalable, compliant, and resilient messaging" → "Scalable messaging platform with compliance standards"

This corrected resume is now properly aligned with the Squarespace Acuity Communications role!
"""

    with open(output_dir / "analysis_and_comparison.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"✅ Corrected resume created in: {output_dir}")
    print("📄 resume_communications_focused.txt - Properly tailored for Squarespace")  
    print("📊 analysis_and_comparison.txt - Detailed analysis of the issues")
    
    return output_dir

if __name__ == "__main__":
    create_communications_focused_resume()