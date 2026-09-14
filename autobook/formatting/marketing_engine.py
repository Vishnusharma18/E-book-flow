"""Task 3.4: Enhanced Marketing Banner & Quote Poster Canvas Generator.

Generates quote posters, social media banners, and launch bundle graphics with premium aesthetics.
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from autobook.models import BookProject


class MarketingEngine:
    """Generates high-aesthetic promotional assets and quote banners."""

    def __init__(self):
        pass

    def generate_quote_poster(self, project: BookProject, quote_text: str, output_path: str) -> str:
        """Generates elegant 1080x1080 quote poster with rich dark gradient and gold foil accents."""
        size = (1080, 1080)
        img = Image.new("RGB", size, color=(18, 22, 34))
        draw = ImageDraw.Draw(img)

        gold = (212, 175, 55)
        white = (250, 250, 250)

        # Elegant double border frame
        draw.rectangle([50, 50, 1030, 1030], outline=gold, width=4)
        draw.rectangle([65, 65, 1015, 1015], outline=(50, 60, 85), width=2)

        font_default = ImageFont.load_default()

        # Header branding
        draw.text((540, 140), "❖  PUBLISHING HIGHLIGHT  ❖", fill=gold, font=font_default, anchor="mm")

        # Formatted quote text
        wrapped_quote = textwrap.wrap(f'“{quote_text}”', width=32)
        y_q = 420 - (len(wrapped_quote) * 20)
        for line in wrapped_quote:
            draw.text((540, y_q), line, fill=white, font=font_default, anchor="mm")
            y_q += 50

        # Attribution & Footer
        draw.line([(340, y_q + 40), (740, y_q + 40)], fill=gold, width=2)
        draw.text((540, y_q + 80), f"— {project.title.upper()}", fill=gold, font=font_default, anchor="mm")
        draw.text((540, y_q + 130), project.metadata.author, fill=(180, 190, 205), font=font_default, anchor="mm")

        draw.text((540, 960), "NOW AVAILABLE WORLDWIDE IN PRINT & DIGITAL", fill=(140, 150, 170), font=font_default, anchor="mm")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img.save(output_path)
        return output_path

    def generate_launch_banner(self, project: BookProject, output_path: str) -> str:
        """Generates 1200x630 web launch / Twitter header banner with rich layout."""
        width, height = 1200, 630
        img = Image.new("RGB", (width, height), color=(245, 242, 235))
        draw = ImageDraw.Draw(img)

        gold = (180, 140, 60)
        dark = (25, 30, 42)

        # Gold bar accent top & bottom
        draw.rectangle([0, 0, width, 16], fill=gold)
        draw.rectangle([0, height - 16, width, height], fill=gold)

        font_default = ImageFont.load_default()

        # Side frame accent
        draw.rectangle([50, 50, width - 50, height - 50], outline=gold, width=2)

        draw.text((100, 130), "◆  NEW OFFICIAL RELEASE  ◆", fill=gold, font=font_default)

        # Wrapped title
        title_lines = textwrap.wrap(project.title.upper(), width=35)
        y_t = 190
        for t_line in title_lines[:2]:
            draw.text((100, y_t), t_line, fill=dark, font=font_default)
            y_t += 50

        if project.metadata.subtitle:
            draw.text((100, y_t + 10), project.metadata.subtitle, fill=(90, 95, 110), font=font_default)
            y_t += 40

        draw.line([(100, y_t + 20), (500, y_t + 20)], fill=gold, width=2)

        draw.text((100, y_t + 60), f"AUTHOR: {project.metadata.author.upper()}", fill=dark, font=font_default)
        draw.text((100, y_t + 100), "INCLUDES PRINT PDF + EPUB E-BOOK + MARKETING BUNDLE", fill=(120, 125, 135), font=font_default)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img.save(output_path)
        return output_path
