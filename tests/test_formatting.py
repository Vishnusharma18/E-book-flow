"""Tests for Formatting & Design Engine (Tasks 3.1 - 3.4)."""

import os
import pytest
from autobook.pipeline.master_pipeline import ContentPipeline
from autobook.formatting.pdf_engine import PDFEngine
from autobook.formatting.epub_engine import EPUBEngine
from autobook.formatting.cover_engine import CoverEngine
from autobook.formatting.marketing_engine import MarketingEngine


@pytest.fixture
def sample_project():
    pipeline = ContentPipeline()
    return pipeline.run_pipeline("Philosophy of Modern Architecture")


def test_pdf_engine(sample_project, tmp_path):
    pdf_engine = PDFEngine()
    out_pdf = str(tmp_path / "book.pdf")
    res = pdf_engine.generate_pdf(sample_project, out_pdf)
    assert os.path.exists(res)
    assert os.path.getsize(res) > 0


def test_epub_engine(sample_project, tmp_path):
    epub_engine = EPUBEngine()
    out_epub = str(tmp_path / "book.epub")
    res = epub_engine.generate_epub(sample_project, out_epub)
    assert os.path.exists(res)
    assert os.path.getsize(res) > 0


def test_cover_engine(sample_project, tmp_path):
    cover_engine = CoverEngine()
    out_front = str(tmp_path / "front.png")
    out_wrap = str(tmp_path / "wrap.png")
    out_mockup = str(tmp_path / "mockup.png")

    cover_engine.generate_front_cover(sample_project, out_front)
    assert os.path.exists(out_front)

    cover_engine.generate_wraparound_cover(sample_project, out_wrap)
    assert os.path.exists(out_wrap)

    cover_engine.generate_3d_mockup(out_front, out_mockup)
    assert os.path.exists(out_mockup)


def test_marketing_engine(sample_project, tmp_path):
    marketing_engine = MarketingEngine()
    out_poster = str(tmp_path / "poster.png")
    out_banner = str(tmp_path / "banner.png")

    marketing_engine.generate_quote_poster(sample_project, "Architecture is frozen music.", out_poster)
    assert os.path.exists(out_poster)

    marketing_engine.generate_launch_banner(sample_project, out_banner)
    assert os.path.exists(out_banner)
