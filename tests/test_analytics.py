"""Tests for Analytics & Reading Time Analysis Engine."""

import os
import zipfile
import json
import pytest
from fastapi.testclient import TestClient
from autobook.models import BookProject, ChapterContent, BookMetadata
from autobook.analytics import BookAnalyticsEngine
from autobook.pipeline.master_pipeline import ContentPipeline
from autobook.server.main import app, PROJECTS
from autobook.exporter import BundleExporter


client = TestClient(app)


def test_analytics_engine_calculation():
    engine = BookAnalyticsEngine()

    project = BookProject(
        id="test_analytics_1",
        title="Test Book Analytics",
        topic_or_url="Analytics test",
        metadata=BookMetadata(title="Test Book Analytics"),
        chapters=[
            ChapterContent(
                chapter_number=1,
                title="Chapter 1: Intro",
                raw_text="This is a simple text to test reading ease and word count calculation.",
                proofread_text="This is a simple text to test reading ease and word count calculation."
            ),
            ChapterContent(
                chapter_number=2,
                title="Chapter 2: Deep Dive",
                raw_text="Quantum mechanics and algorithmic complexity require rigorous computational analysis.",
                proofread_text="Quantum mechanics and algorithmic complexity require rigorous computational analysis."
            )
        ]
    )

    analytics = engine.analyze_project(project)

    assert analytics["project_id"] == "test_analytics_1"
    assert analytics["total_chapters"] == 2
    assert analytics["total_word_count"] == 22
    assert "estimated_reading_time" in analytics
    assert analytics["estimated_reading_time"]["minutes"] >= 0.1
    assert len(analytics["chapters"]) == 2
    assert analytics["chapters"][0]["chapter_number"] == 1
    assert analytics["readability"]["flesch_reading_ease"] > 0


def test_analytics_api_endpoint():
    pipeline = ContentPipeline()
    project = pipeline.run_pipeline("Artificial Intelligence in Modern Medicine")
    PROJECTS[project.id] = project

    res = client.get(f"/api/projects/{project.id}/analytics")
    assert res.status_code == 200
    data = res.json()

    assert data["project_id"] == project.id
    assert data["total_chapters"] == 10
    assert data["total_word_count"] > 100
    assert "formatted" in data["estimated_reading_time"]


def test_analytics_in_exporter_bundle(tmp_path):
    pipeline = ContentPipeline()
    project = pipeline.run_pipeline("History of Renaissance Art")

    exporter = BundleExporter(output_dir=str(tmp_path))
    zip_path = exporter.build_bundle(project)

    assert os.path.exists(zip_path)

    # Check that analytics_report.json exists inside the zip archive
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        file_list = zipf.namelist()
        assert "analytics_report.json" in file_list

        analytics_file = zipf.open("analytics_report.json")
        data = json.loads(analytics_file.read().decode('utf-8'))
        assert data["title"] == project.title
        assert data["total_chapters"] == 10
