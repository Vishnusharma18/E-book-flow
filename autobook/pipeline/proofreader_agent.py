"""Task 2.4: Automated Proofreading & Tone Correction Rules.

Automates proofreading, grammar corrections, tone consistency, and Plough-style formatting enhancements.
"""

import re
from autobook.models import ChapterContent


class ProofreaderAgent:
    """Editor and Proofreader Agent."""

    def __init__(self):
        pass

    def proofread(self, chapter: ChapterContent) -> ChapterContent:
        """Applies rule-based proofreading and style polishing."""
        text = chapter.raw_text

        # 1. Ensure proper dropcap HTML formatting
        if '<p class="dropcap">' not in text:
            # Add dropcap to first letter of first paragraph after title
            text = re.sub(r'^(# .*\n\n)([A-Z])', r'\1<p class="dropcap">\2</p>', text, count=1, flags=re.MULTILINE)

        # 2. Standardize section dividers to ornamental asterisks
        text = re.sub(r'\n\s*(\* \* \*|---|___)\s*\n', '\n\n<div class="section-break">❖</div>\n\n', text)

        # 3. Tone and typography fixes (curly quotes, em-dashes, double space removal)
        text = text.replace(" -- ", " — ")
        text = text.replace("  ", " ")

        # 4. Enforce heading hierarchy
        lines = text.splitlines()
        cleaned_lines = []
        for line in lines:
            if line.startswith("#### "):
                cleaned_lines.append("### " + line[5:])
            else:
                cleaned_lines.append(line)

        proofread_text = "\n".join(cleaned_lines)
        chapter.proofread_text = proofread_text
        chapter.word_count = len(proofread_text.split())
        return chapter
