import os
from datetime import datetime
from typing import Dict
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, Color
import tempfile

class ExportUtils:
    """Utilities for exporting stories in various formats."""
    
    @staticmethod
    def create_story_text(story_data: Dict) -> str:
        """Create formatted text version of the story."""
        lines = []
        
        # Header
        lines.append("NARRAVOX STORY")
        lines.append("=" * 50)
        lines.append(f"Session ID: {story_data.get('session_id', 'Unknown')}")
        lines.append(f"Created: {story_data.get('export_timestamp', 'Unknown')}")
        lines.append(f"Turns: {story_data.get('turn_count', 0)}")
        lines.append("")
        
        # Cultural context if available
        if story_data.get('cultural_context'):
            lines.append("CULTURAL CONTEXT:")
            lines.append("-" * 20)
            lines.append(story_data['cultural_context'])
            lines.append("")
        
        # Story content
        lines.append("STORY:")
        lines.append("-" * 20)
        lines.append("")
        
        # Add story entries
        for entry in story_data.get('story_history', []):
            if entry['type'] in ['user', 'ai']:
                speaker = "YOU" if entry['type'] == 'user' else "AI"
                lines.append(f"[{speaker}]")
                lines.append(entry['content'])
                lines.append("")
        
        # Cultural explanations if available
        if story_data.get('cultural_explanations'):
            lines.append("CULTURAL INSIGHTS:")
            lines.append("-" * 20)
            for key, explanation in story_data['cultural_explanations'].items():
                lines.append(f"{key}: {explanation}")
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def create_story_pdf(story_data: Dict) -> str:
        """Create PDF version of the story and return file path."""
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
            
            # Define styles following Swiss Design principles
            styles = getSampleStyleSheet()
            
            # Custom styles for Swiss Design
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=black,
                fontName='Helvetica-Bold',
                alignment=0  # Left align
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=12,
                spaceBefore=20,
                textColor=black,
                fontName='Helvetica-Bold',
                alignment=0
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=10,
                textColor=black,
                fontName='Helvetica',
                alignment=0,
                leftIndent=0,
                rightIndent=0
            )
            
            meta_style = ParagraphStyle(
                'CustomMeta',
                parent=styles['Normal'],
                fontSize=9,
                spaceAfter=8,
                textColor=Color(0.4, 0.4, 0.4),  # Gray
                fontName='Helvetica',
                alignment=0
            )
            
            # Build PDF content
            story = []
            
            # Title
            story.append(Paragraph("NARRAVOX STORY", title_style))
            story.append(Spacer(1, 12))
            
            # Metadata
            story.append(Paragraph(f"Session ID: {story_data.get('session_id', 'Unknown')}", meta_style))
            story.append(Paragraph(f"Created: {story_data.get('export_timestamp', 'Unknown')}", meta_style))
            story.append(Paragraph(f"Turns: {story_data.get('turn_count', 0)}", meta_style))
            story.append(Spacer(1, 20))
            
            # Cultural context
            if story_data.get('cultural_context'):
                story.append(Paragraph("CULTURAL CONTEXT", heading_style))
                story.append(Paragraph(story_data['cultural_context'], body_style))
                story.append(Spacer(1, 15))
            
            # Story content
            story.append(Paragraph("STORY", heading_style))
            story.append(Spacer(1, 10))
            
            for entry in story_data.get('story_history', []):
                if entry['type'] in ['user', 'ai']:
                    speaker = "YOU" if entry['type'] == 'user' else "AI"
                    
                    # Speaker label
                    speaker_style = ParagraphStyle(
                        'Speaker',
                        parent=body_style,
                        fontSize=10,
                        fontName='Helvetica-Bold',
                        spaceAfter=5,
                        textColor=Color(0.3, 0.3, 0.3)
                    )
                    
                    story.append(Paragraph(f"[{speaker}]", speaker_style))
                    story.append(Paragraph(entry['content'], body_style))
                    story.append(Spacer(1, 15))
            
            # Cultural explanations
            if story_data.get('cultural_explanations'):
                story.append(Spacer(1, 20))
                story.append(Paragraph("CULTURAL INSIGHTS", heading_style))
                
                for key, explanation in story_data['cultural_explanations'].items():
                    story.append(Paragraph(f"<b>{key}:</b> {explanation}", body_style))
                    story.append(Spacer(1, 8))
            
            # Build PDF
            doc.build(story)
            
            return temp_file.name
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            raise Exception(f"PDF creation failed: {str(e)}")
    
    @staticmethod
    def create_shareable_link(session_id: str) -> str:
        """Create a shareable link for the story session."""
        # In a real implementation, this would create a permanent link
        # For now, return a placeholder that shows the concept
        base_url = "https://narravox.onrender.com"  # Will be actual deployment URL
        return f"{base_url}/story/{session_id}"
    
    @staticmethod
    def format_for_social_sharing(story_data: Dict) -> str:
        """Format story excerpt for social media sharing."""
        story_text = ""
        
        # Get first AI response as excerpt
        for entry in story_data.get('story_history', []):
            if entry['type'] == 'ai':
                story_text = entry['content']
                break
        
        # Truncate if needed
        if len(story_text) > 200:
            story_text = story_text[:197] + "..."
        
        return f'I created a story with Narravox: "{story_text}" Check it out!'
    
    @staticmethod
    def cleanup_temp_file(file_path: str):
        """Clean up temporary files."""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception:
            pass  # Ignore cleanup errors 