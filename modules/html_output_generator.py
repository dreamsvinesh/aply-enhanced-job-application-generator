"""
HTML Output Generator
Creates formatted HTML output that preserves formatting when copy-pasted to documents.
"""

from typing import Dict, List, Any
import re
from datetime import datetime

class HTMLOutputGenerator:
    """Generates clean HTML output for easy copy-paste with preserved formatting"""
    
    def __init__(self):
        self.css_styles = self._get_css_styles()
    
    def _get_css_styles(self) -> str:
        """CSS styles for professional document formatting"""
        return """
        <style>
            body {
                font-family: 'Calibri', 'Arial', sans-serif;
                line-height: 1.4;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                font-size: 24px;
                font-weight: bold;
                margin: 0 0 5px 0;
                color: #2c3e50;
            }
            .title {
                font-size: 14px;
                color: #7f8c8d;
                margin: 0 0 15px 0;
                font-style: italic;
            }
            .contact-info {
                font-size: 12px;
                color: #5d6d7e;
                margin: 0 0 20px 0;
            }
            .section-header {
                font-size: 14px;
                font-weight: bold;
                text-transform: uppercase;
                color: #2c3e50;
                border-bottom: 1px solid #bdc3c7;
                margin: 20px 0 10px 0;
                padding-bottom: 2px;
            }
            .subsection-header {
                font-size: 13px;
                font-weight: bold;
                margin: 15px 0 5px 0;
                color: #34495e;
            }
            .company-info {
                font-size: 12px;
                color: #7f8c8d;
                margin: 0 0 8px 0;
            }
            .bullet-point {
                margin: 3px 0;
                padding-left: 0px;
            }
            .skills-list {
                font-size: 12px;
                line-height: 1.6;
            }
            .summary-text {
                font-size: 12px;
                line-height: 1.5;
                text-align: justify;
            }
            .cover-letter {
                font-size: 12px;
                line-height: 1.6;
            }
            .message-box {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
                margin: 10px 0;
            }
            .metadata {
                font-size: 11px;
                color: #95a5a6;
                font-style: italic;
            }
            .highlight {
                background-color: #fff3cd;
                padding: 1px 3px;
                border-radius: 2px;
            }
        </style>
        """
    
    def generate_html_application(self, content_dict: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate complete HTML application package"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{metadata.get('company', 'Job')} Application - {metadata.get('applicant_name', 'Applicant')}</title>
            {self.css_styles}
        </head>
        <body>
        """
        
        # Application header
        html_content += self._generate_application_header(metadata)
        
        # Resume section
        html_content += self._generate_resume_html(content_dict.get('resume', {}))
        
        # Cover letter section
        html_content += self._generate_cover_letter_html(content_dict.get('cover_letter', ''))
        
        # LinkedIn message section
        html_content += self._generate_linkedin_message_html(content_dict.get('linkedin_message', ''))
        
        # Email template section
        html_content += self._generate_email_template_html(content_dict.get('email_template', {}))
        
        # Analytics and metadata
        html_content += self._generate_analytics_section(metadata)
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content
    
    def _generate_application_header(self, metadata: Dict[str, Any]) -> str:
        """Generate application header with metadata"""
        
        company = metadata.get('company', 'Company')
        country = metadata.get('country', '').title()
        ats_score = metadata.get('ats_score', 0)
        generation_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        score_class = "highlight" if ats_score >= 80 else ""
        
        return f"""
        <div style="text-align: center; margin-bottom: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
            <h1 style="margin: 0; color: #2c3e50;">{company} - Product Manager Application Package</h1>
            <div class="metadata" style="margin: 10px 0;">
                <strong>Generated:</strong> {generation_date}<br>
                <strong>Country:</strong> {country}<br>
                <strong>ATS Match Score:</strong> <span class="{score_class}">{ats_score}% {'✅' if ats_score >= 80 else '⚠️'}</span>
            </div>
        </div>
        """
    
    def _generate_resume_html(self, resume_data: Dict[str, Any]) -> str:
        """Generate HTML resume section"""
        
        html = '<div class="section-header">RESUME</div>\n'
        
        # Personal info
        personal_info = resume_data.get('personal_info', {})
        html += f"""
        <h1>{personal_info.get('name', 'VINESH KUMAR')}</h1>
        <div class="title">{personal_info.get('title', 'Senior Product Manager')}</div>
        <div class="contact-info">
            {personal_info.get('phone', '')} | {personal_info.get('email', '')} | 
            {personal_info.get('linkedin', '')} | {personal_info.get('location', '')}
        </div>
        """
        
        # Summary
        summary = resume_data.get('summary', '')
        html += f"""
        <div class="section-header">SUMMARY</div>
        <div class="summary-text">{summary}</div>
        """
        
        # Skills
        skills = resume_data.get('skills', '')
        html += f"""
        <div class="section-header">SKILLS</div>
        <div class="skills-list">{skills}</div>
        """
        
        # Experience
        html += '<div class="section-header">EXPERIENCE</div>\n'
        
        for experience in resume_data.get('experience', []):
            html += f"""
            <div class="subsection-header">{experience.get('title', '')}</div>
            <div class="company-info">
                <strong>{experience.get('company', '')}</strong> | {experience.get('location', '')} | {experience.get('duration', '')}
            </div>
            """
            
            for highlight in experience.get('highlights', []):
                html += f'<div class="bullet-point">• {highlight}</div>\n'
            
            html += '<br>\n'
        
        # Education
        education = resume_data.get('education', {})
        html += f"""
        <div class="section-header">EDUCATION</div>
        <div><strong>{education.get('degree', '')}</strong> | {education.get('university', '')} | {education.get('duration', '')}</div>
        """
        
        return html
    
    def _generate_cover_letter_html(self, cover_letter_content: str) -> str:
        """Generate HTML cover letter section"""
        
        html = '<div class="section-header">COVER LETTER</div>\n'
        html += f'<div class="cover-letter">{self._format_paragraphs(cover_letter_content)}</div>\n'
        
        return html
    
    def _generate_linkedin_message_html(self, linkedin_content: str) -> str:
        """Generate HTML LinkedIn message section"""
        
        char_count = len(linkedin_content)
        char_status = "✅" if char_count <= 300 else "⚠️"
        
        html = f"""
        <div class="section-header">LINKEDIN MESSAGE</div>
        <div class="metadata"><strong>Length:</strong> {char_count} characters {char_status}</div>
        <div class="message-box">{self._format_paragraphs(linkedin_content)}</div>
        """
        
        return html
    
    def _generate_email_template_html(self, email_data: Dict[str, Any]) -> str:
        """Generate HTML email template section"""
        
        html = '<div class="section-header">EMAIL TEMPLATE</div>\n'
        
        subject = email_data.get('subject', 'Application: Product Manager Position')
        body = email_data.get('body', '')
        
        html += f"""
        <div class="subsection-header">Subject: {subject}</div>
        <div class="message-box">{self._format_paragraphs(body)}</div>
        """
        
        return html
    
    def _generate_analytics_section(self, metadata: Dict[str, Any]) -> str:
        """Generate analytics and improvements section"""
        
        html = '<div class="section-header">CHANGES MADE</div>\n'
        
        changes = metadata.get('changes_made', [])
        for i, change in enumerate(changes[:5], 1):  # Show top 5 changes
            html += f'<div class="bullet-point">{i}. {change}</div>\n'
        
        html += '<div class="section-header">SKILLS ANALYSIS</div>\n'
        
        matched_skills = metadata.get('matched_skills', [])
        missing_skills = metadata.get('missing_skills', [])
        
        html += f"""
        <div><strong>Matched Skills:</strong> {', '.join(matched_skills[:8])}</div>
        <div><strong>Missing Skills:</strong> {', '.join(missing_skills[:5])}</div>
        """
        
        # AI Analysis if available
        ai_analysis = metadata.get('ai_analysis', {})
        if ai_analysis:
            skills_alignment = ai_analysis.get('skills_alignment', {})
            quality_score = ai_analysis.get('quality_score', {})
            
            html += '<div class="section-header">AI ANALYSIS</div>\n'
            
            if skills_alignment:
                alignment_score = skills_alignment.get('alignment_score', 0)
                html += f'<div><strong>Skills Alignment:</strong> {alignment_score}% match</div>\n'
            
            if quality_score:
                overall_score = quality_score.get('overall_score', 0)
                html += f'<div><strong>Content Quality:</strong> {overall_score:.1f}/10</div>\n'
        
        html += f"""
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #bdc3c7; text-align: center;">
            <div class="metadata">Generated by Enhanced Job Application Generator with LLM Agents</div>
        </div>
        """
        
        return html
    
    def _format_paragraphs(self, content: str) -> str:
        """Format content with proper paragraph breaks"""
        if not content:
            return ""
        
        # Split by double newlines and create paragraphs
        paragraphs = content.split('\\n\\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Replace single newlines with line breaks
                formatted = paragraph.replace('\\n', '<br>')
                formatted_paragraphs.append(f'<p style="margin: 8px 0;">{formatted}</p>')
        
        return '\\n'.join(formatted_paragraphs)
    
    def parse_markdown_to_html_structure(self, markdown_content: str) -> Dict[str, Any]:
        """Parse markdown resume content into structured HTML data"""
        
        sections = {}
        current_section = None
        content_buffer = []
        
        lines = markdown_content.split('\\n')
        
        for line in lines:
            line = line.strip()
            
            # Main headers (##)
            if line.startswith('## '):
                # Save previous section
                if current_section and content_buffer:
                    sections[current_section] = '\\n'.join(content_buffer)
                
                current_section = line[3:].lower().replace(' ', '_')
                content_buffer = []
            
            # Content lines
            elif line and current_section:
                content_buffer.append(line)
        
        # Save last section
        if current_section and content_buffer:
            sections[current_section] = '\\n'.join(content_buffer)
        
        return sections

# Export the generator
__all__ = ['HTMLOutputGenerator']