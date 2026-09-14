"""Tests for Multi-Language Translation Engine."""

import pytest
from fastapi.testclient import TestClient
from autobook.models import BookProject, ChapterContent, BookMetadata
from autobook.translation import BookTranslationEngine
from autobook.pipeline.master_pipeline import ContentPipeline
from autobook.server.main import app, PROJECTS

client = TestClient(app)


def test_translation_engine():
    engine = BookTranslationEngine()

    project = BookProject(
        id="test_trans_1",
        title="Original Book",
        topic_or_url="Philosophy",
        metadata=BookMetadata(title="Original Book", subtitle="A Study"),
        chapters=[
            ChapterContent(
                chapter_number=1,
                title="Chapter 1: Intro",
                raw_text="Hello world.",
                proofread_text="Hello world."
            )
        ]
    )

    translated = engine.translate_project(project, "es")

    assert translated.id == "test_trans_1_es"
    assert translated.metadata.language == "es"
    assert "[ES]" in translated.title
    assert "[ES]" in translated.chapters[0].title
    assert "[ES]" in translated.chapters[0].proofread_text


def test_unsupported_language():
    engine = BookTranslationEngine()
    project = BookProject(
        id="test_trans_2",
        title="Book",
        topic_or_url="Test",
        metadata=BookMetadata(title="Book")
    )

    with pytest.raises(ValueError):
        engine.translate_project(project, "klingon")


def test_translation_api_endpoint():
    pipeline = ContentPipeline()
    project = pipeline.run_pipeline("The History of Space Travel")
    PROJECTS[project.id] = project

    res = client.post(f"/api/projects/{project.id}/translate", json={"target_language": "fr"})
    assert res.status_code == 200
    data = res.json()

    assert data["original_project_id"] == project.id
    assert data["target_language"] == "fr"
    translated_id = data["translated_project_id"]
    assert translated_id in PROJECTS
    assert PROJECTS[translated_id].metadata.language == "fr"
