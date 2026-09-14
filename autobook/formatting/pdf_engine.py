"""Task 3.1: HTML/CSS to WeasyPrint PDF Layout Template Engine."""

import os
from typing import Optional
import weasyprint
from autobook.models import BookProject


class PDFEngine:
    """Renders print-ready PDF files using WeasyPrint and custom CSS Paged Media."""

    def __init__(self):
        pass

    def build_html_content(self, project: BookProject) -> str:
        """Constructs HTML string styled with Plough-inspired typography for print."""
        chapters_html = ""
        for ch in project.chapters:
            # Clean markdown headings or paragraph markers for HTML rendering
            text_content = ch.proofread_text or ch.raw_text

            # Simple markdown to HTML transformations for chapter body
            html_body = []
            for block in text_content.split("\n\n"):
                block = block.strip()
                if not block:
                    continue
                if block.startswith("# "):
                    html_body.append(f'<h1 class="chapter-title">{block[2:]}</h1>')
                elif block.startswith("### "):
                    html_body.append(f'<h2 class="section-title">{block[4:]}</h2>')
                elif block.startswith("<p class=\"dropcap\">"):
                    html_body.append(f'<p class="first-paragraph">{block}</p>')
                elif block == '<div class="section-break">❖</div>':
                    html_body.append('<div class="section-break">❖</div>')
                else:
                    html_body.append(f'<p>{block}</p>')

            chapters_html += f"""
            <section class="chapter-page">
                {"".join(html_body)}
            </section>
            """

        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{project.title}</title>
    <style>
        @page {{
            size: 6in 9in; /* Standard Paperback Trim */
            margin-top: 20mm;
            margin-bottom: 20mm;
            margin-inside: 22mm; /* Gutter margin */
            margin-outside: 18mm;
            @bottom-center {{
                content: counter(page);
                font-family: 'Garamond', 'Georgia', serif;
                font-size: 9pt;
                color: #555555;
            }}
        }}

        body {{
            font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #222222;
            text-align: justify;
        }}

        .title-page {{
            page-break-after: always;
            text-align: center;
            padding-top: 3in;
        }}

        .book-title {{
            font-size: 26pt;
            font-weight: normal;
            letter-spacing: 1px;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}

        .book-subtitle {{
            font-size: 13pt;
            font-style: italic;
            color: #444;
            margin-bottom: 40px;
        }}

        .book-author {{
            font-size: 11pt;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #666;
        }}

        .chapter-page {{
            page-break-before: always;
        }}

        .chapter-title {{
            font-size: 20pt;
            font-weight: normal;
            text-align: center;
            margin-top: 1in;
            margin-bottom: 0.5in;
            letter-spacing: 0.5px;
        }}

        .section-title {{
            font-size: 13pt;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: left;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 0;
            text-indent: 1.5em;
        }}

        p.first-paragraph {{
            text-indent: 0;
        }}

        .dropcap {{
            float: left;
            font-size: 3.2em;
            line-height: 0.8;
            margin-right: 6px;
            margin-bottom: -2px;
            font-family: 'Georgia', serif;
            color: #111;
        }}

        .section-break {{
            text-align: center;
            margin: 20px 0;
            font-size: 12pt;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1 class="book-title">{project.title}</h1>
        <div class="book-subtitle">{project.metadata.subtitle}</div>
        <div class="book-author">{project.metadata.author}</div>
    </div>
    {chapters_html}
</body>
</html>
"""
        return full_html

    def generate_pdf(self, project: BookProject, output_path: str) -> str:
        """Generates PDF file using WeasyPrint."""
        html_str = self.build_html_content(project)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        weasyprint.HTML(string=html_str).write_pdf(output_path)
        return output_path
