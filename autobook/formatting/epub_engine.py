"""Task 3.2: EPUB 3.0 Generation Pipeline Integration.

Creates industry-standard EPUB 3.0 ebooks compatible with Kindle, Apple Books, and Kobo.
"""

import os
import ebooklib
from ebooklib import epub
from autobook.models import BookProject


class EPUBEngine:
    """EPUB 3.0 Generator Engine."""

    def __init__(self):
        pass

    def generate_epub(self, project: BookProject, output_path: str) -> str:
        """Generates reflowable EPUB 3.0 file."""
        book = epub.EpubBook()

        # Set Metadata
        book.set_identifier(project.id)
        book.set_title(project.title)
        book.set_language(project.metadata.language)
        book.add_author(project.metadata.author)

        # Basic CSS
        style = """
        @namespace epub "http://www.idpf.org/2007/ops";
        body {
            font-family: Georgia, serif;
            line-height: 1.6;
            padding: 5%;
        }
        h1 {
            text-align: center;
            font-size: 1.8em;
            margin-bottom: 1em;
        }
        p {
            text-indent: 1.5em;
            margin: 0;
        }
        p.first {
            text-indent: 0;
        }
        .dropcap {
            float: left;
            font-size: 3em;
            line-height: 0.8em;
            margin-right: 0.1em;
        }
        .break {
            text-align: center;
            margin: 1.5em 0;
        }
        """
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style
        )
        book.add_item(nav_css)

        epub_chapters = []
        toc_items = []

        for idx, ch in enumerate(project.chapters, start=1):
            file_name = f"chap_{idx:02d}.xhtml"
            c = epub.EpubHtml(title=ch.title, file_name=file_name, lang="en")

            # Simple conversion of chapter body for EPUB XHTML
            text_content = ch.proofread_text or ch.raw_text
            html_body = []
            for block in text_content.split("\n\n"):
                block = block.strip()
                if not block:
                    continue
                if block.startswith("# "):
                    html_body.append(f"<h1>{block[2:]}</h1>")
                elif block.startswith("### "):
                    html_body.append(f"<h2>{block[4:]}</h2>")
                elif block == '<div class="section-break">❖</div>':
                    html_body.append('<div class="break">❖</div>')
                else:
                    html_body.append(f"<p>{block}</p>")

            c.content = f"<html><head></head><body>{''.join(html_body)}</body></html>"
            c.add_item(nav_css)
            book.add_item(c)
            epub_chapters.append(c)
            toc_items.append(c)

        # Spine and Table of Contents
        book.toc = tuple(toc_items)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine = ["nav"] + epub_chapters

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        epub.write_epub(output_path, book, {})
        return output_path
