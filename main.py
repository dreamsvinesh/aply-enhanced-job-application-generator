#!/usr/bin/env python3
"""
Enhanced Job Application Generator
Generates tailored resumes, cover letters, and outreach messages based on job descriptions.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

from modules.jd_parser import JobDescriptionParser
from modules.resume_generator import ResumeGenerator
from modules.cover_letter_generator import CoverLetterGenerator
from modules.message_generator import MessageGenerator
from modules.country_config import CountryConfig
from modules.role_fit_analyzer import RoleFitAnalyzer

class JobApplicationGenerator:
    def __init__(self):
        self.jd_parser = JobDescriptionParser()
        self.resume_generator = ResumeGenerator()
        self.cover_letter_generator = CoverLetterGenerator()
        self.message_generator = MessageGenerator()
        self.country_config = CountryConfig()
        self.role_fit_analyzer = RoleFitAnalyzer()
        
    def generate_application_package(self, job_description: str, country: str, company_name: str = None) -> str:
        """
        Main workflow: Generate complete application package
        
        Args:
            job_description: Full job description text
            country: Target country (netherlands, finland, ireland, sweden, denmark, portugal)
            company_name: Company name (extracted from JD if not provided)
            
        Returns:
            Path to generated markdown file
        """
        print(f"🎯 Generating application package for {country.title()}...")
        
        # Step 1: Parse job description
        print("📋 Parsing job description...")
        jd_data = self.jd_parser.parse(job_description)
        
        if not company_name:
            company_name = jd_data.get('company', 'UnknownCompany')
        
        # Step 1.5: Analyze role fit
        print("🔍 Analyzing role fit...")
        fit_analysis = self.role_fit_analyzer.analyze_fit(jd_data)
        
        if not fit_analysis['should_apply']:
            print(f"⚠️  {fit_analysis['recommendation']}")
            print(f"📊 Fit Score: {fit_analysis['fit_score']:.0f}/100")
            
            if fit_analysis['critical_gaps']:
                print("\n❌ Critical gaps identified:")
                for gap in fit_analysis['critical_gaps']:
                    print(f"   • {gap}")
            
            proceed = input("\nDo you still want to generate the application? (y/N): ").lower()
            if proceed != 'y':
                print("❌ Application generation cancelled.")
                return None
        
        # Step 2: Generate resume based on JD requirements
        print("📄 Generating tailored resume...")
        resume_content, resume_changes = self.resume_generator.generate(jd_data, country)
        
        # Step 3: Generate cover letter
        print("📝 Generating cover letter...")
        cover_letter = self.cover_letter_generator.generate(jd_data, country, company_name)
        
        # Step 4: Generate LinkedIn and email messages
        print("💬 Generating outreach messages...")
        linkedin_msg = self.message_generator.generate_linkedin_message(jd_data, country)
        email_msg = self.message_generator.generate_email_message(jd_data, country, company_name)
        
        # Step 5: Compile into single HTML file
        print("📦 Compiling application package...")
        output_path = self._create_output_file(
            company_name, country, resume_content, cover_letter, 
            linkedin_msg, email_msg, resume_changes, jd_data, fit_analysis
        )
        
        print(f"✅ Application package generated: {output_path}")
        return output_path
    
    def _create_output_file(self, company_name: str, country: str, 
                           resume: str, cover_letter: str, linkedin_msg: str, 
                           email_msg: str, changes: List[str], jd_data: Dict, 
                           fit_analysis: Dict) -> str:
        """Create the final HTML output file"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"{company_name}_{country}_{timestamp}.html"
        output_path = Path("output") / filename
        
        # Get fit score
        fit_score = fit_analysis.get('fit_score', 0)
        
        # Create HTML content
        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name} - Application Package</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #3498db; }}
        .fit-analysis {{ background: {('#d4edda' if fit_score >= 60 else '#f8d7da')}; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 5px solid {('#28a745' if fit_score >= 60 else '#dc3545')}; }}
        .section {{ margin: 30px 0; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background: #fafafa; }}
        .section h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .resume {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .copy-btn {{ background: #3498db; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; float: right; margin-bottom: 10px; }}
        .copy-btn:hover {{ background: #2980b9; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat {{ text-align: center; padding: 15px; background: #ecf0f1; border-radius: 8px; }}
        .gap {{ color: #e74c3c; margin: 5px 0; }}
        .strength {{ color: #27ae60; margin: 5px 0; }}
        .warning {{ color: #f39c12; }}
        .success {{ color: #27ae60; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{company_name} - {jd_data.get('role_title', 'Product Manager')}</h1>
            <p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
            <p><strong>Country:</strong> {country.title()}</p>
        </div>
        
        <div class="fit-analysis">
            <h2>🎯 Role Fit Analysis</h2>
            <div class="stats">
                <div class="stat">
                    <h3>{fit_score:.0f}/100</h3>
                    <p>Fit Score</p>
                </div>
                <div class="stat">
                    <h3>{'✅' if fit_analysis['should_apply'] else '❌'}</h3>
                    <p>Recommended</p>
                </div>
                <div class="stat">
                    <h3>{fit_analysis['effort_required'].title()}</h3>
                    <p>Effort Required</p>
                </div>
            </div>
            <p><strong>Recommendation:</strong> {fit_analysis['recommendation']}</p>
            
            {('<div><h4>❌ Critical Gaps:</h4>' + ''.join(f'<div class="gap">• {gap}</div>' for gap in fit_analysis['critical_gaps']) + '</div>') if fit_analysis['critical_gaps'] else ''}
            
            {('<div><h4>✅ Strengths:</h4>' + ''.join(f'<div class="strength">• {strength}</div>' for strength in fit_analysis['strengths']) + '</div>') if fit_analysis['strengths'] else ''}
        </div>

        <div class="section">
            <h2>📄 Resume</h2>
            <button class="copy-btn" onclick="copyToClipboard('resume-content')">Copy Resume</button>
            <div class="resume" id="resume-content">
                {resume.replace(chr(10), '<br>').replace('**', '<strong>').replace('**', '</strong>')}
            </div>
        </div>

        <div class="section">
            <h2>📝 Cover Letter</h2>
            <button class="copy-btn" onclick="copyToClipboard('cover-content')">Copy Cover Letter</button>
            <div id="cover-content">
                {cover_letter.replace(chr(10), '<br>').replace('**', '<strong>').replace('**', '</strong>')}
            </div>
        </div>

        <div class="section">
            <h2>💬 LinkedIn Message</h2>
            <p><strong>Length:</strong> {len(linkedin_msg)} characters {'<span class="success">✅</span>' if len(linkedin_msg) <= 400 else '<span class="warning">⚠️</span>'}</p>
            <button class="copy-btn" onclick="copyToClipboard('linkedin-content')">Copy Message</button>
            <div id="linkedin-content">
                {linkedin_msg.replace(chr(10), '<br>')}
            </div>
        </div>

        <div class="section">
            <h2>📧 Email Template</h2>
            <p><strong>Subject:</strong> {email_msg.get('subject', 'N/A')}</p>
            <button class="copy-btn" onclick="copyToClipboard('email-content')">Copy Email</button>
            <div id="email-content">
                {email_msg.get('body', '').replace(chr(10), '<br>')}
            </div>
        </div>

        <div class="section">
            <h2>📊 Changes Made</h2>
            {self._format_changes_html(changes)}
        </div>

        <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
            <p><em>Generated by Enhanced Job Application Generator</em></p>
        </div>
    </div>

    <script>
        function copyToClipboard(elementId) {{
            const element = document.getElementById(elementId);
            const text = element.innerText || element.textContent;
            navigator.clipboard.writeText(text).then(function() {{
                const button = event.target;
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                button.style.background = '#27ae60';
                setTimeout(() => {{
                    button.textContent = originalText;
                    button.style.background = '#3498db';
                }}, 2000);
            }});
        }}
    </script>
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return str(output_path)
    
    def _format_changes(self, changes: List[str]) -> str:
        """Format the changes list for markdown output"""
        if not changes:
            return "No specific changes made to base resume."
        
        formatted = []
        for i, change in enumerate(changes, 1):
            formatted.append(f"{i}. {change}")
        
        return "\n".join(formatted)
    
    def _format_changes_html(self, changes: List[str]) -> str:
        """Format the changes list for HTML output"""
        if not changes:
            return "<p>No specific changes made to base resume.</p>"
        
        formatted = []
        for i, change in enumerate(changes, 1):
            formatted.append(f"<li>{change}</li>")
        
        return f"<ol>{''.join(formatted)}</ol>"

def main():
    """Interactive command line interface"""
    print("🚀 Enhanced Job Application Generator")
    print("=" * 50)
    
    generator = JobApplicationGenerator()
    
    # Get job description
    print("\n📋 Please paste the job description below (press Enter twice when done):")
    job_description_lines = []
    empty_lines = 0
    
    while empty_lines < 2:
        line = input()
        if line.strip() == "":
            empty_lines += 1
        else:
            empty_lines = 0
        job_description_lines.append(line)
    
    job_description = "\n".join(job_description_lines).strip()
    
    if not job_description:
        print("❌ Error: No job description provided.")
        return
    
    # Get country
    print("\n🌍 Select target country:")
    countries = ["netherlands", "finland", "ireland", "sweden", "denmark", "portugal"]
    for i, country in enumerate(countries, 1):
        print(f"  {i}. {country.title()}")
    
    while True:
        try:
            choice = int(input("\nEnter choice (1-6): "))
            if 1 <= choice <= 6:
                selected_country = countries[choice - 1]
                break
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Optional: Get company name
    company_name = input(f"\n🏢 Company name (optional, will extract from JD): ").strip()
    
    # Generate application package
    try:
        output_path = generator.generate_application_package(
            job_description, selected_country, company_name or None
        )
        
        print(f"\n🎉 Success! Application package saved to: {output_path}")
        print(f"\nOpen the HTML file in your browser to view and copy formatted content.")
        
    except Exception as e:
        print(f"\n❌ Error generating application package: {str(e)}")

if __name__ == "__main__":
    main()