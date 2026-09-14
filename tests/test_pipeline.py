"""Tests for Content & Generation Pipeline (Tasks 2.2 - 2.4)."""

import pytest
from autobook.pipeline.research_agent import ResearchAgent
from autobook.pipeline.writer_agent import WriterAgent
from autobook.pipeline.proofreader_agent import ProofreaderAgent
from autobook.pipeline.master_pipeline import ContentPipeline


def test_research_agent():
    agent = ResearchAgent()
    outline = agent.generate_outline("Artificial Intelligence in Healthcare")
    assert outline.title is not None
    assert len(outline.chapters) == 10
    assert outline.chapters[0].chapter_number == 1

    metadata = agent.generate_metadata("Artificial Intelligence in Healthcare", outline)
    assert metadata.title == outline.title
    assert len(metadata.keywords) > 0


def test_writer_agent():
    research = ResearchAgent()
    outline = research.generate_outline("Quantum Computing")
    writer = WriterAgent()
    chapter = writer.draft_chapter(outline.chapters[0], outline.title)
    assert chapter.chapter_number == 1
    assert "Quantum Computing" in chapter.raw_text or outline.title in chapter.raw_text
    assert chapter.word_count > 50


def test_proofreader_agent():
    research = ResearchAgent()
    outline = research.generate_outline("Space Exploration")
    writer = WriterAgent()
    chapter = writer.draft_chapter(outline.chapters[0], outline.title)

    proofreader = ProofreaderAgent()
    edited_chapter = proofreader.proofread(chapter)
    assert len(edited_chapter.proofread_text) > 0
    assert "<p class=\"dropcap\">" in edited_chapter.proofread_text or "# " in edited_chapter.proofread_text


def test_master_pipeline():
    pipeline = ContentPipeline()
    progress_records = []

    def log_progress(msg, pct):
        progress_records.append((msg, pct))

    project = pipeline.run_pipeline("Renewable Energy Innovations", progress_callback=log_progress)

    assert project.status == "content_ready"
    assert len(project.chapters) == 10
    assert project.progress == 80.0
    assert len(progress_records) > 0
