"""
Professional HTML Generator - Matches Professional Resume Standards
Creates properly formatted HTML that exactly matches professional resume formatting
"""

from typing import Dict, List, Any
import re
from datetime import datetime

class ProfessionalHTMLGenerator:
    """Generates professionally formatted HTML that matches resume standards exactly"""
    
    def __init__(self):
        self.base_font_size = "11pt"  # Standard resume font size
        self.css_styles = self._get_professional_css()
    
    def _get_professional_css(self) -> str:
        """Professional CSS that matches standard resume formatting"""
        return """
        <style>
            body {
                font-family: 'Calibri', 'Arial', sans-serif;
                font-size: 11pt;
                line-height: 1.1;
                color: #000000;
                max-width: 8.5in;
                margin: 0 auto;
                padding: 0.5in;
                background-color: white;
            }
            
            /* Header Section */
            .resume-header {
                text-align: left;
                margin-bottom: 15pt;
            }
            
            .name {
                font-size: 18pt;
                font-weight: bold;
                color: #000000;
                margin: 0;
                text-transform: uppercase;
                letter-spacing: 1pt;
            }
            
            .title {
                font-size: 11pt;
                color: #4472C4;
                font-weight: normal;
                margin: 2pt 0 8pt 0;
            }
            
            .contact-info {
                font-size: 11pt;
                color: #000000;
                margin: 0;
                line-height: 1.2;
            }
            
            /* Section Headers */
            .section-header {
                font-size: 11pt;
                font-weight: bold;
                text-transform: uppercase;
                color: #000000;
                margin: 15pt 0 8pt 0;
                padding: 0;
                border-bottom: none;
                letter-spacing: 0.5pt;
            }
            
            /* Experience Section */
            .job-title {
                font-size: 11pt;
                font-weight: bold;
                color: #000000;
                margin: 8pt 0 2pt 0;
            }
            
            .company-info {
                font-size: 11pt;
                color: #4472C4;
                margin: 0 0 6pt 0;
                font-weight: normal;
            }
            
            .job-description {
                font-size: 11pt;
                color: #000000;
                margin: 0 0 4pt 0;
                line-height: 1.15;
                text-align: justify;
            }
            
            /* Bullet Points */
            .bullet-point {
                font-size: 11pt;
                color: #000000;
                margin: 2pt 0 2pt 15pt;
                line-height: 1.15;
                text-indent: -15pt;
                padding-left: 15pt;
                text-align: justify;
            }
            
            .bullet-point:before {
                content: "• ";
                font-weight: bold;
            }
            
            /* Skills Section */
            .skills-container {
                display: flex;
                flex-wrap: wrap;
                gap: 15pt;
                margin: 6pt 0;
            }
            
            .skills-column {
                flex: 1;
                min-width: 150pt;
            }
            
            .skills-category {
                font-size: 11pt;
                font-weight: bold;
                color: #000000;
                margin: 0 0 4pt 0;
            }
            
            .skills-list {
                font-size: 11pt;
                color: #000000;
                margin: 0 0 8pt 0;
                line-height: 1.2;
            }
            
            /* Summary Text */
            .summary-text {
                font-size: 11pt;
                color: #000000;
                line-height: 1.15;
                text-align: justify;
                margin: 6pt 0 0 0;
            }
            
            /* Education */
            .education-item {
                font-size: 11pt;
                color: #000000;
                margin: 4pt 0;
            }
            
            .education-degree {
                font-weight: bold;
            }
            
            .education-school {
                color: #4472C4;
            }
            
            /* Cover Letter */
            .cover-letter {
                font-size: 11pt;
                line-height: 1.4;
                color: #000000;
                margin: 10pt 0;
                text-align: left;
            }
            
            .cover-letter p {
                margin: 8pt 0;
                text-align: left;
            }
            
            /* Messages */
            .message-box {
                background-color: #f8f9fa;
                border: 1pt solid #dee2e6;
                border-radius: 4pt;
                padding: 10pt;
                margin: 8pt 0;
                font-size: 11pt;
            }
            
            .message-box ul {
                margin: 4pt 0;
                padding-left: 15pt;
            }
            
            .message-box li {
                margin: 2pt 0;
                line-height: 1.3;
            }
            
            /* Metadata */
            .metadata {
                font-size: 10pt;
                color: #666666;
                font-style: italic;
            }
            
            /* Core Competencies Box */
            .competencies-box {
                border: 1pt solid #4472C4;
                padding: 8pt;
                margin: 10pt 0;
                background-color: #f8f9fb;
            }
            
            .competency-title {
                font-size: 11pt;
                font-weight: bold;
                color: #4472C4;
                margin: 0 0 4pt 0;
            }
            
            .competency-desc {
                font-size: 10pt;
                color: #000000;
                line-height: 1.2;
                margin: 0;
            }
            
            /* Print Optimization */
            @media print {
                body {
                    margin: 0;
                    padding: 0.5in;
                }
                .message-box {
                    border: 1pt solid #000;
                    background-color: #f5f5f5;
                }
            }
            
            /* No page breaks within content blocks */
            .job-section {
                page-break-inside: avoid;
                margin-bottom: 10pt;
            }
        </style>
        """
    
    def generate_professional_application(self, content_dict: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate professionally formatted HTML application"""
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{metadata.get('company', 'Job')} Application - {metadata.get('applicant_name', 'Applicant')}</title>
    {self.css_styles}
</head>
<body>
"""
        
        # Application header (for digital viewing)
        html_content += self._generate_application_header(metadata)
        
        # Resume section
        html_content += self._generate_professional_resume(content_dict.get('resume', {}))
        
        # Page break before cover letter
        html_content += '<div style="page-break-before: always;"></div>'
        
        # Cover letter section
        html_content += self._generate_professional_cover_letter(content_dict.get('cover_letter', ''))
        
        # Page break before messages
        html_content += '<div style="page-break-before: always;"></div>'
        
        # Messages section
        html_content += self._generate_professional_messages(
            content_dict.get('linkedin_message', ''),
            content_dict.get('email_template', {})
        )
        
        html_content += """
</body>
</html>
"""
        
        return html_content
    
    def _generate_application_header(self, metadata: Dict[str, Any]) -> str:
        """Generate application header for digital viewing"""
        
        company = metadata.get('company', 'Company')
        country = metadata.get('country', '').title()
        ats_score = metadata.get('ats_score', 0)
        generation_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        return f"""
<div style="text-align: center; margin-bottom: 20pt; padding: 15pt; background-color: #f8f9fa; border: 1pt solid #dee2e6; border-radius: 4pt; page-break-after: always;">
    <div style="font-size: 14pt; font-weight: bold; color: #2c3e50; margin: 0;">{company} - Product Manager Application Package</div>
    <div class="metadata" style="margin: 8pt 0 0 0;">
        <strong>Generated:</strong> {generation_date} | 
        <strong>Country:</strong> {country} | 
        <strong>ATS Score:</strong> {ats_score}% {'✅' if ats_score >= 80 else '⚠️'}
    </div>
</div>
"""
    
    def _generate_professional_resume(self, resume_data: Dict[str, Any]) -> str:
        """Generate professionally formatted resume matching the PDF standard"""
        
        html = ""
        
        # Header section
        personal_info = resume_data.get('personal_info', {})
        html += f"""
<div class="resume-header">
    <div class="name">{personal_info.get('name', 'VINESH KUMAR')}</div>
    <div class="title">{personal_info.get('title', 'Senior Product Manager - AI | Enterprise Automation | RAG & Multi-Agent Systems')}</div>
    <div class="contact-info">
        {personal_info.get('phone', '')} {personal_info.get('email', '')} {personal_info.get('linkedin', '')} {personal_info.get('location', '')}<br>
        Open to visa sponsorship
    </div>
</div>
"""
        
        # Summary section
        summary = resume_data.get('summary', '')
        # Clean the summary - remove any \n--- artifacts
        summary = re.sub(r'\\n---.*$', '', summary)
        summary = re.sub(r'\n---.*$', '', summary)
        
        html += f"""
<div class="section-header">SUMMARY</div>
<div class="summary-text">{summary}</div>
"""
        
        # Experience section - with full content preserved
        html += '<div class="section-header">EXPERIENCE</div>'
        
        for experience in resume_data.get('experience', []):
            html += '<div class="job-section">'
            html += f'<div class="job-title">{experience.get("title", "")}</div>'
            html += f'<div class="company-info"><strong>{experience.get("company", "")}</strong></div>'
            html += f'<div class="company-info">{experience.get("duration", "")} {experience.get("location", "")}</div>'
            
            # Add full detailed bullet points
            for highlight in experience.get('highlights', []):
                # Ensure bullet points are properly formatted and full-length
                html += f'<div class="bullet-point">{highlight}</div>'
            
            html += '</div>'
        
        # Skills section - organized like the PDF
        html += self._generate_skills_section(resume_data.get('skills', ''))
        
        # Core competencies (like in the PDF)
        html += self._generate_core_competencies()
        
        # Education section
        education = resume_data.get('education', {})
        html += f"""
<div class="section-header">EDUCATION</div>
<div class="education-item">
    <span class="education-degree">{education.get('degree', '')}</span><br>
    <span class="education-school">{education.get('university', '')}</span><br>
    {education.get('duration', '')}
</div>
"""
        
        return html
    
    def _generate_skills_section(self, skills_raw: str) -> str:
        """Generate properly formatted skills section like the PDF"""
        
        # Clean skills and organize them properly
        if isinstance(skills_raw, str):
            skills_list = [skill.strip() for skill in skills_raw.replace('\\n---', '').split('|')]
        else:
            skills_list = []
        
        # Organize skills into categories like the PDF
        product_skills = []
        technical_skills = []
        
        for skill in skills_list:
            skill = skill.strip()
            if any(term in skill.lower() for term in ['product', 'roadmap', 'vision', 'strategy', 'stakeholder', 'agile', 'discovery']):
                product_skills.append(skill)
            else:
                technical_skills.append(skill)
        
        html = '<div class="section-header">SKILLS</div>'
        html += '<div class="skills-container">'
        
        # Left column
        html += '<div class="skills-column">'
        html += '<div class="skills-category">Vision & Roadmap</div><div class="skills-list">Roadmap Planning</div>'
        html += '<div class="skills-category">PRDs & User Stories</div><div class="skills-list">Prioritization</div>'
        html += '<div class="skills-category">Cross-Functional Teams</div>'
        html += '<div class="skills-category">Stakeholder Management</div><div class="skills-list">Agile/SAFe</div>'
        html += '<div class="skills-category">Product Discovery</div><div class="skills-list">Design Thinking</div>'
        html += '<div class="skills-category">User Research</div><div class="skills-list">Process Optimization</div>'
        html += '</div>'
        
        # Right column
        html += '<div class="skills-column">'
        html += '<div class="skills-category">RAG Architecture</div><div class="skills-list">Multi-Agent Systems</div>'
        html += '<div class="skills-category">Prompt Engineering</div><div class="skills-list">Vector DBs (pgvector)</div>'
        html += '<div class="skills-category">LLM Integration</div><div class="skills-list">Salesforce</div>'
        html += '</div>'
        
        html += '</div>'
        
        return html
    
    def _generate_core_competencies(self) -> str:
        """Generate core competencies section like the PDF"""
        
        return """
<div class="section-header">CORE COMPETENCIES</div>
<div class="competencies-box">
    <div class="competency-title">🔧 Business Transformation</div>
    <div class="competency-desc">Identifying and executing high-ROI automation opportunities that dramatically improve operational efficiency</div>
</div>
<div class="competencies-box">
    <div class="competency-title">💎 Technical Translation</div>
    <div class="competency-desc">Bridging business needs and technical implementation to deliver solutions that solve real problems</div>
</div>
<div class="competencies-box">
    <div class="competency-title">💎 User-Centered Design</div>
    <div class="competency-desc">Creating intuitive user experiences that drive adoption and enhance customer satisfaction</div>
</div>
"""
    
    def _generate_professional_cover_letter(self, cover_letter_content: str) -> str:
        """Generate professionally formatted cover letter"""
        
        html = '<div class="section-header">COVER LETTER</div>'
        
        # Format paragraphs properly
        paragraphs = cover_letter_content.split('\n\n')
        formatted_content = ""
        
        for paragraph in paragraphs:
            if paragraph.strip():
                formatted_content += f'<p>{paragraph.strip()}</p>'
        
        html += f'<div class="cover-letter">{formatted_content}</div>'
        
        return html
    
    def _generate_professional_messages(self, linkedin_message: str, email_template: Dict[str, Any]) -> str:
        """Generate professionally formatted messages section"""
        
        html = '<div class="section-header">OUTREACH MESSAGES</div>'
        
        # LinkedIn message
        char_count = len(linkedin_message)
        html += f"""
<div style="margin: 15pt 0;">
    <div style="font-weight: bold; margin-bottom: 5pt;">LinkedIn Message</div>
    <div class="metadata">Length: {char_count} characters {'✅' if char_count <= 300 else '⚠️'}</div>
    <div class="message-box">{linkedin_message}</div>
</div>
"""
        
        # Email template
        if isinstance(email_template, dict):
            subject = email_template.get('subject', 'Application: Product Manager Position')
            body = email_template.get('body', '')
        else:
            subject = "Application: Product Manager Position"
            body = str(email_template)
        
        # Format email body with proper bullet points
        if '•' in body:
            # Split into parts and format bullets properly
            parts = body.split('My background includes:')
            if len(parts) > 1:
                intro = parts[0].strip()
                rest = parts[1]
                
                # Extract bullet points
                bullet_part = ""
                conclusion = ""
                
                if 'I believe my technical skills' in rest:
                    bullet_section, conclusion = rest.split('I believe my technical skills', 1)
                    conclusion = 'I believe my technical skills' + conclusion
                else:
                    bullet_section = rest
                
                # Format bullets as proper HTML list
                bullets = [line.strip()[1:].strip() for line in bullet_section.split('\n') if line.strip().startswith('•')]
                
                formatted_body = f"""<p>{intro}</p>
<p>My background includes:</p>
<ul>
{''.join(f'<li>{bullet}</li>' for bullet in bullets)}
</ul>
<p>{conclusion.strip()}</p>"""
            else:
                formatted_body = f"<p>{body}</p>"
        else:
            formatted_body = f"<p>{body}</p>"
        
        html += f"""
<div style="margin: 15pt 0;">
    <div style="font-weight: bold; margin-bottom: 5pt;">Email Template</div>
    <div style="font-weight: bold; font-size: 11pt; margin-bottom: 5pt;">Subject: {subject}</div>
    <div class="message-box">{formatted_body}</div>
</div>
"""
        
        return html

# Export the professional generator
__all__ = ['ProfessionalHTMLGenerator']