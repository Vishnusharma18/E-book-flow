"""Task 4.4: One-Click Bundle Download (.zip exporter).

Assembles PDF, EPUB, covers, 3D mockups, marketing posters, metadata, and landing page into a clean .zip bundle.
"""

import os
import zipfile
import json
from autobook.models import BookProject
from autobook.formatting.pdf_engine import PDFEngine
from autobook.formatting.epub_engine import EPUBEngine
from autobook.formatting.cover_engine import CoverEngine
from autobook.formatting.marketing_engine import MarketingEngine


class BundleExporter:
    """Export Bundle Builder."""

    def __init__(self, output_dir: str = "/tmp/autobook_builds"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.pdf_engine = PDFEngine()
        self.epub_engine = EPUBEngine()
        self.cover_engine = CoverEngine()
        self.marketing_engine = MarketingEngine()

    def build_bundle(self, project: BookProject) -> str:
        """Generates all deliverables and packages them into a single .zip file."""
        proj_dir = os.path.join(self.output_dir, project.id)
        os.makedirs(proj_dir, exist_ok=True)

        # File paths inside bundle
        pdf_path = os.path.join(proj_dir, f"{project.id}_print.pdf")
        epub_path = os.path.join(proj_dir, f"{project.id}_ebook.epub")
        front_cover_path = os.path.join(proj_dir, "cover_front.png")
        wrap_cover_path = os.path.join(proj_dir, "cover_wraparound.png")
        mockup_path = os.path.join(proj_dir, "mockup_3d.png")
        poster_path = os.path.join(proj_dir, "marketing_poster.png")
        banner_path = os.path.join(proj_dir, "marketing_banner.png")
        metadata_path = os.path.join(proj_dir, "kdp_metadata.json")

        # Generate components
        self.pdf_engine.generate_pdf(project, pdf_path)
        self.epub_engine.generate_epub(project, epub_path)
        self.cover_engine.generate_front_cover(project, front_cover_path)
        self.cover_engine.generate_wraparound_cover(project, wrap_cover_path)
        self.cover_engine.generate_3d_mockup(front_cover_path, mockup_path)
        self.marketing_engine.generate_quote_poster(project, "A journey of transformation and courage.", poster_path)
        self.marketing_engine.generate_launch_banner(project, banner_path)

        # Write Metadata JSON
        with open(metadata_path, "w") as f:
            json.dump(project.metadata.model_dump(), f, indent=2)

        # Zip creation
        zip_filename = f"{project.id}_publishing_bundle.zip"
        zip_path = os.path.join(self.output_dir, zip_filename)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(proj_dir):
                for file in files:
                    file_full_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_full_path, proj_dir)
                    zipf.write(file_full_path, arcname)

        return zip_path
