"""Task 3.3: Enhanced Cover Design Template Engine & 3D Mockup Renderer.

Generates elegant front covers, wraparound cover spreads, and 3D realistic book mockups using Pillow.
"""

import os
import textwrap
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from autobook.models import BookProject


class CoverEngine:
    """Renders high-aesthetic book covers and 3D mockups."""

    def __init__(self):
        pass

    def _create_gradient_background(self, width: int, height: int, start_color: Tuple[int, int, int], end_color: Tuple[int, int, int]) -> Image.Image:
        """Creates a smooth linear vertical gradient background image."""
        base = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(base)
        for y in range(height):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (y / height))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (y / height))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        return base

    def generate_front_cover(self, project: BookProject, output_path: str, width: int = 1600, height: int = 2400) -> str:
        """Renders high-aesthetic, rich front cover image with elegant borders and typography."""
        # Deep royal midnight blue to obsidian gradient
        img = self._create_gradient_background(width, height, (20, 28, 45), (10, 14, 25))
        draw = ImageDraw.Draw(img)

        # Outer & Inner Gold Accent Frames
        gold_primary = (212, 175, 55)
        gold_secondary = (180, 140, 60)
        slate_silver = (200, 210, 225)

        draw.rectangle([70, 70, width - 70, height - 70], outline=gold_primary, width=6)
        draw.rectangle([90, 90, width - 90, height - 90], outline=gold_secondary, width=2)
        draw.rectangle([110, 110, width - 110, height - 110], outline=(40, 55, 80), width=1)

        font_default = ImageFont.load_default()

        # Wrap Title text
        title_lines = textwrap.wrap(project.title.upper(), width=22)

        # Draw Decorative Top Emblem
        draw.text((width // 2, 220), "❖  PLOUGH CLASSIC EDITIONS  ❖", fill=gold_primary, font=font_default, anchor="mm")

        # Draw Title with drop shadow effect
        y_title = height // 3 - (len(title_lines) * 30)
        for line in title_lines:
            # Shadow
            draw.text((width // 2 + 3, y_title + 3), line, fill=(0, 0, 0), font=font_default, anchor="mm")
            # Main Text
            draw.text((width // 2, y_title), line, fill=(255, 255, 250), font=font_default, anchor="mm")
            y_title += 60

        # Subtitle
        if project.metadata.subtitle:
            sub_lines = textwrap.wrap(project.metadata.subtitle, width=35)
            y_sub = y_title + 40
            for s_line in sub_lines:
                draw.text((width // 2, y_sub), s_line, fill=slate_silver, font=font_default, anchor="mm")
                y_sub += 40

        # Center Ornamental Icon
        center_y = height // 2 + 100
        draw.ellipse([width // 2 - 40, center_y - 40, width // 2 + 40, center_y + 40], outline=gold_primary, width=2)
        draw.text((width // 2, center_y), "◆", fill=gold_primary, font=font_default, anchor="mm")

        # Author Name & Publisher Brand at bottom
        draw.text((width // 2, height - 320), "A WORK BY", fill=gold_secondary, font=font_default, anchor="mm")
        author_name = project.metadata.author.upper()
        draw.text((width // 2, height - 260), author_name, fill=(255, 255, 255), font=font_default, anchor="mm")

        draw.line([(width // 2 - 150, height - 200), (width // 2 + 150, height - 200)], fill=gold_primary, width=2)
        draw.text((width // 2, height - 160), "PLOUGH LITERARY PRESS", fill=gold_primary, font=font_default, anchor="mm")

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

        wrap = self._create_gradient_background(total_width, height, (18, 24, 38), (10, 14, 25))
        draw = ImageDraw.Draw(wrap)

        gold_primary = (212, 175, 55)

        # Paste Front Cover
        wrap.paste(front_img, (1600 + spine_width, 0))

        # Back Cover Frame & Contents
        draw.rectangle([80, 80, 1520, height - 80], outline=gold_primary, width=4)
        draw.rectangle([100, 100, 1500, height - 100], outline=(40, 55, 80), width=2)

        font_default = ImageFont.load_default()

        draw.text((800, 300), "ABOUT THIS EDITION", fill=gold_primary, font=font_default, anchor="mm")

        blurb = project.metadata.description or f"A comprehensive exploration of {project.title}."
        blurb_lines = textwrap.wrap(blurb, width=50)
        y_b = 450
        for b_line in blurb_lines[:15]:
            draw.text((800, y_b), b_line, fill=(220, 225, 235), font=font_default, anchor="mm")
            y_b += 45

        # Spine
        draw.rectangle([1600, 0, 1600 + spine_width, height], fill=(12, 16, 28))
        draw.rectangle([1600 + 10, 20, 1600 + spine_width - 10, height - 20], outline=gold_primary, width=2)

        draw.text((1600 + spine_width // 2, 200), "❖", fill=gold_primary, font=font_default, anchor="mm")
        draw.text((1600 + spine_width // 2, height // 2), project.title.upper(), fill=(255, 255, 255), font=font_default, anchor="mm")
        draw.text((1600 + spine_width // 2, height - 200), "PLOUGH PRESS", fill=gold_primary, font=font_default, anchor="mm")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        wrap.save(output_path)
        return output_path

    def generate_3d_mockup(self, front_cover_path: str, output_path: str) -> str:
        """Generates realistic 3D book mockup image with realistic shadows, page texture, and depth."""
        if not os.path.exists(front_cover_path):
            raise FileNotFoundError(f"Front cover image not found at {front_cover_path}")

        cover = Image.open(front_cover_path).resize((600, 900))

        canvas_w, canvas_h = 1000, 1200
        mockup = Image.new("RGBA", (canvas_w, canvas_h), (250, 250, 252, 255))

        # Soft realistic drop shadow
        shadow = Image.new("RGBA", (630, 930), (0, 0, 0, 90))
        shadow = shadow.filter(ImageFilter.GaussianBlur(25))
        mockup.paste(shadow, (210, 150), shadow)

        # 3D Page edge block (simulating book pages)
        page_edge = Image.new("RGB", (45, 890), color=(240, 236, 225))
        draw_edge = ImageDraw.Draw(page_edge)
        for y in range(0, 890, 3):
            draw_edge.line([(0, y), (45, y)], fill=(215, 210, 198))
        mockup.paste(page_edge, (155, 135))

        # Spine highlight line
        spine_line = Image.new("RGB", (8, 900), color=(212, 175, 55))
        mockup.paste(spine_line, (198, 130))

        # Paste Front Cover
        mockup.paste(cover, (206, 130))

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        mockup.save(output_path)
        return output_path
