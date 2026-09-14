"""Tests for FastAPI Server & Bundle Exporter (Tasks 4.1 - 4.4)."""

import os
import pytest
from fastapi.testclient import TestClient
from autobook.server.main import app, PROJECTS
from autobook.pipeline.master_pipeline import ContentPipeline
from autobook.exporter import BundleExporter


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "AutoBook Publisher API"


def test_create_and_get_project():
    res = client.post("/api/projects", json={"topic_or_url": "Industrial Revolution Heroes"})
    assert res.status_code == 200
    data = res.json()
    assert "project_id" in data
    proj_id = data["project_id"]

    get_res = client.get(f"/api/projects/{proj_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == proj_id


def test_bundle_exporter(tmp_path):
    pipeline = ContentPipeline()
    project = pipeline.run_pipeline("History of Cartography")

    exporter = BundleExporter(output_dir=str(tmp_path))
    zip_path = exporter.build_bundle(project)

    assert os.path.exists(zip_path)
    assert zip_path.endswith(".zip")
    assert os.path.getsize(zip_path) > 0


def test_landing_page_endpoint():
    pipeline = ContentPipeline()
    project = pipeline.run_pipeline("Renaissance Painting Masters")
    PROJECTS[project.id] = project

    res = client.get(f"/api/projects/{project.id}/landing")
    assert res.status_code == 200
    assert "PLOUGH PRESS" in res.text
    assert project.title in res.text
