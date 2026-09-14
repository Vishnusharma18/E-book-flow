"""Task 3.3: Cover Design Template Engine & 3D Mockup Renderer.

Generates minimalist front covers, wraparound cover spreads, and 3D realistic book mockups using Pillow.
"""

import os
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from autobook.models import BookProject


class CoverEngine:
    """Renders book covers and 3D mockups."""

    def __init__(self):
        pass

    def generate_front_cover(self, project: BookProject, output_path: str, width: int = 1600, height: int = 2400) -> str:
        """Renders minimalist front cover image."""
        img = Image.new("RGB", (width, height), color=(248, 246, 240))  # Warm cream background
        draw = ImageDraw.Draw(img)

        # Decorative borders
        draw.rectangle([60, 60, width - 60, height - 60], outline=(40, 40, 40), width=4)
        draw.rectangle([75, 75, width - 75, height - 75], outline=(180, 140, 80), width=2)  # Gold accent line

        # Load standard default font
        font_title = ImageFont.load_default()
        font_author = ImageFont.load_default()

        title_text = project.title.upper()
        subtitle_text = project.metadata.subtitle or ""
        author_text = project.metadata.author.upper()

        # Draw Title
        draw.text((width // 2, height // 3), title_text, fill=(30, 30, 30), font=font_title, anchor="mm")
        if subtitle_text:
            draw.text((width // 2, height // 3 + 120), subtitle_text, fill=(80, 80, 80), font=font_author, anchor="mm")

        # Ornamental motif
        draw.text((width // 2, height // 2 + 100), "❖", fill=(180, 140, 80), font=font_title, anchor="mm")

        # Author Name
        draw.text((width // 2, height - 250), author_text, fill=(40, 40, 40), font=font_author, anchor="mm")
        draw.text((width // 2, height - 180), "PLOUGH LITERARY PRESS", fill=(120, 120, 120), font=font_author, anchor="mm")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img.save(output_path)
        return output_path

    def generate_wraparound_cover(self, project: BookProject, output_path: str) -> str:
        """Renders full print wraparound cover (Back + Spine + Front)."""
        front_path = output_path.replace(".png", "_front.png")
        self.generate_front_cover(project, front_path, width=1600, height=2400)
        front_img = Image.open(front_path)

        spine_width = 300
        total_width = 1600 * 2 + spine_width
        height = 2400

        wrap = Image.new("RGB", (total_width, height), color=(244, 240, 232))
        draw = ImageDraw.Draw(wrap)

        # Paste Front
        wrap.paste(front_img, (1600 + spine_width, 0))

        # Back Cover Text
        blurb = project.metadata.description or f"A timeless narrative exploration of {project.title}."
        draw.text((800, 800), project.title.upper(), fill=(30, 30, 30), anchor="mm")
        draw.text((800, 1000), blurb[:300], fill=(60, 60, 60), anchor="mm")
        draw.rectangle([100, 100, 1500, height - 100], outline=(180, 140, 80), width=2)

        # Spine
        draw.rectangle([1600, 0, 1600 + spine_width, height], fill=(235, 228, 215))
        draw.text((1600 + spine_width // 2, height // 2), project.title, fill=(30, 30, 30), anchor="mm")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        wrap.save(output_path)
        return output_path

    def generate_3d_mockup(self, front_cover_path: str, output_path: str) -> str:
        """Generates realistic 3D book mockup image with shadows and depth."""
        if not os.path.exists(front_cover_path):
            raise FileNotFoundError(f"Front cover image not found at {front_cover_path}")

        cover = Image.open(front_cover_path).resize((600, 900))

        # Create canvas for 3D mockup
        canvas_w, canvas_h = 900, 1100
        mockup = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))

        # Render simulated spine/pages shadow effect
        shadow = Image.new("RGBA", (620, 920), (0, 0, 0, 50))
        shadow = shadow.filter(ImageFilter.GaussianBlur(15))
        mockup.paste(shadow, (150, 110), shadow)

        # Paste main cover angled offset
        mockup.paste(cover, (140, 90))

        # Add book spine side effect (3D page edge)
        page_edge = Image.new("RGB", (30, 890), color=(230, 225, 215))
        draw_edge = ImageDraw.Draw(page_edge)
        for y in range(0, 890, 4):
            draw_edge.line([(0, y), (30, y)], fill=(210, 205, 195))
        mockup.paste(page_edge, (110, 95))

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        mockup.save(output_path)
        return output_path
