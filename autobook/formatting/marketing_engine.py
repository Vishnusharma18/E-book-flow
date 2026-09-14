"""Task 3.4: Marketing Banner & Quote Poster Canvas Auto-Generator.

Generates quote posters, social media banners, and launch bundle graphics.
"""

import os
from PIL import Image, ImageDraw, ImageFont
from autobook.models import BookProject


class MarketingEngine:
    """Generates promotional assets and quote banners."""

    def __init__(self):
        pass

    def generate_quote_poster(self, project: BookProject, quote_text: str, output_path: str) -> str:
        """Generates elegant 1080x1080 quote poster for Instagram / Twitter."""
        size = (1080, 1080)
        img = Image.new("RGB", size, color=(30, 35, 45))  # Deep navy background
        draw = ImageDraw.Draw(img)

        # Border frame
        draw.rectangle([40, 40, 1040, 1040], outline=(200, 160, 90), width=3)  # Gold frame

        font = ImageFont.load_default()

        # Quote body
        formatted_quote = f"“{quote_text}”"
        draw.text((540, 480), formatted_quote, fill=(245, 245, 240), font=font, anchor="mm")

        # Attribution
        draw.text((540, 680), f"— {project.title}", fill=(200, 160, 90), font=font, anchor="mm")
        draw.text((540, 960), "AVAILABLE NOW IN PRINT & DIGITAL", fill=(160, 160, 160), font=font, anchor="mm")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img.save(output_path)
        return output_path

    def generate_launch_banner(self, project: BookProject, output_path: str) -> str:
        """Generates 1200x630 web launch / Twitter header banner."""
        width, height = 1200, 630
        img = Image.new("RGB", (width, height), color=(245, 242, 235))
        draw = ImageDraw.Draw(img)

        # Gold bar accent
        draw.rectangle([0, 0, width, 12], fill=(180, 140, 80))

        font = ImageFont.load_default()

        draw.text((100, 180), "NEW BOOK RELEASE", fill=(180, 140, 80), font=font)
        draw.text((100, 240), project.title.upper(), fill=(30, 30, 30), font=font)
        draw.text((100, 320), project.metadata.subtitle or "", fill=(80, 80, 80), font=font)

        draw.text((100, 480), "Includes EPUB, Print PDF & Launch Bundle Kit", fill=(100, 100, 100), font=font)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img.save(output_path)
        return output_path
