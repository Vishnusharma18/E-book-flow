"""Task 3.1: Enhanced HTML/CSS to WeasyPrint PDF Layout Template Engine."""

import os
import weasyprint
from autobook.models import BookProject


class PDFEngine:
    """Renders print-ready PDF files using WeasyPrint and custom CSS Paged Media."""

    def __init__(self):
        pass

    def build_html_content(self, project: BookProject) -> str:
        """Constructs HTML string styled with high-aesthetic typography for print."""
        chapters_html = ""
        for ch in project.chapters:
            text_content = ch.proofread_text or ch.raw_text or ""

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
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap');

        @page {{
            size: 6in 9in; /* Standard Paperback Trim */
            margin-top: 22mm;
            margin-bottom: 22mm;
            margin-inside: 24mm; /* Gutter margin */
            margin-outside: 20mm;
            @top-center {{
                content: "{project.title}";
                font-family: 'Cinzel', 'Georgia', serif;
                font-size: 7.5pt;
                letter-spacing: 1.5px;
                color: #777777;
                text-transform: uppercase;
            }}
            @bottom-center {{
                content: counter(page);
                font-family: 'EB Garamond', 'Georgia', serif;
                font-size: 10pt;
                color: #444444;
            }}
        }}

        @page :first {{
            @top-center {{ content: none; }}
            @bottom-center {{ content: none; }}
        }}

        body {{
            font-family: 'EB Garamond', 'Garamond', 'Georgia', serif;
            font-size: 11.5pt;
            line-height: 1.65;
            color: #1a1a1a;
            text-align: justify;
        }}

        .title-page {{
            page-break-after: always;
            text-align: center;
            padding-top: 2.5in;
        }}

        .book-title {{
            font-family: 'Cinzel', serif;
            font-size: 28pt;
            font-weight: 700;
            letter-spacing: 2px;
            color: #111827;
            margin-bottom: 15px;
            text-transform: uppercase;
        }}

        .book-subtitle {{
            font-family: 'EB Garamond', serif;
            font-size: 14pt;
            font-style: italic;
            color: #4b5563;
            margin-bottom: 50px;
        }}

        .ornament-divider {{
            font-size: 16pt;
            color: #d4af37;
            margin: 40px 0;
        }}

        .book-author {{
            font-family: 'Cinzel', serif;
            font-size: 11pt;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: #374151;
        }}

        .publisher-brand {{
            margin-top: 80px;
            font-family: 'Cinzel', serif;
            font-size: 9pt;
            letter-spacing: 2px;
            color: #9ca3af;
        }}

        .chapter-page {{
            page-break-before: always;
        }}

        .chapter-title {{
            font-family: 'Cinzel', serif;
            font-size: 20pt;
            font-weight: 500;
            text-align: center;
            margin-top: 1.2in;
            margin-bottom: 0.6in;
            letter-spacing: 1px;
            color: #1f2937;
        }}

        .section-title {{
            font-family: 'Cinzel', serif;
            font-size: 12pt;
            font-weight: 700;
            margin-top: 24px;
            margin-bottom: 12px;
            text-align: left;
            letter-spacing: 0.5px;
            color: #374151;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 0;
            text-indent: 1.6em;
        }}

        p.first-paragraph {{
            text-indent: 0;
        }}

        .dropcap {{
            float: left;
            font-size: 3.5em;
            line-height: 0.8;
            margin-right: 8px;
            margin-bottom: -4px;
            font-family: 'Cinzel', 'Georgia', serif;
            color: #d4af37;
        }}

        .section-break {{
            text-align: center;
            margin: 24px 0;
            font-size: 14pt;
            color: #d4af37;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1 class="book-title">{project.title}</h1>
        <div class="book-subtitle">{project.metadata.subtitle}</div>
        <div class="ornament-divider">❖  ◆  ❖</div>
        <div class="book-author">{project.metadata.author}</div>
        <div class="publisher-brand">PLOUGH LITERARY PRESS</div>
    </div>
    {chapters_html}
</body>
</html>
"""
        return full_html

    def generate_pdf(self, project: BookProject, output_path: str) -> str:
        """Generates print-ready PDF file using WeasyPrint."""
        html_str = self.build_html_content(project)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        weasyprint.HTML(string=html_str).write_pdf(output_path)
        return output_path
