"""Task 1.4 & FastAPI Server Implementation for AutoBook Platform."""

import os
from typing import Dict, Optional, List, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from autobook.models import BookProject
from autobook.pipeline.master_pipeline import ContentPipeline
from autobook.exporter import BundleExporter
from autobook.analytics import BookAnalyticsEngine

app = FastAPI(
    title="AutoBook Publisher Platform API",
    description="Automated AI publishing suite API for generating books, EPUBs, PDFs, covers, and marketing bundles.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database of projects
PROJECTS: Dict[str, BookProject] = {}
PROJECT_ZIP_PATHS: Dict[str, str] = {}

exporter = BundleExporter()
analytics_engine = BookAnalyticsEngine()


class CreateBookRequest(BaseModel):
    topic_or_url: str
    title: Optional[str] = None


def generate_book_task(project_id: str, topic_or_url: str, title: Optional[str]):
    pipeline = ContentPipeline()

    def progress_cb(msg: str, percent: float):
        if project_id in PROJECTS:
            PROJECTS[project_id].current_step = msg
            PROJECTS[project_id].progress = percent

    try:
        project = pipeline.run_pipeline(topic_or_url, custom_title=title, progress_callback=progress_cb)
        project.id = project_id
        project.status = "rendering"
        project.current_step = "Building PDF, EPUB, Cover Mockups, and Marketing Bundle..."
        project.progress = 85.0
        PROJECTS[project_id] = project

        zip_path = exporter.build_bundle(project)
        PROJECT_ZIP_PATHS[project_id] = zip_path

        project.status = "completed"
        project.progress = 100.0
        project.current_step = "Publication Bundle Ready"
        PROJECTS[project_id] = project
    except Exception as e:
        if project_id in PROJECTS:
            PROJECTS[project_id].status = "failed"
            PROJECTS[project_id].current_step = f"Error: {str(e)}"


@app.get("/")
def root():
    return {"status": "ok", "service": "AutoBook Publisher API", "docs": "/docs"}


@app.post("/api/projects", response_model=Dict[str, Any])
def create_project(req: CreateBookRequest, background_tasks: BackgroundTasks):
    import uuid
    project_id = str(uuid.uuid4())[:8]

    initial_project = BookProject(
        id=project_id,
        title=req.title or f"Book on {req.topic_or_url.title()}",
        topic_or_url=req.topic_or_url,
        metadata={
            "title": req.title or f"Book on {req.topic_or_url.title()}",
            "subtitle": "An Automated Narrative Journey",
            "author": "AutoBook Publisher",
            "publisher": "Plough Aesthetic Press"
        },
        status="researching",
        progress=5.0,
        current_step="Initializing Research Agent",
        created_at=""
    )
    PROJECTS[project_id] = initial_project

    background_tasks.add_task(generate_book_task, project_id, req.topic_or_url, req.title)

    return {"project_id": project_id, "message": "Book creation process initiated."}


@app.get("/api/projects")
def list_projects():
    return list(PROJECTS.values())


@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")
    return PROJECTS[project_id]


@app.get("/api/projects/{project_id}/analytics")
def get_project_analytics(project_id: str):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")
    project = PROJECTS[project_id]
    return analytics_engine.analyze_project(project)


@app.get("/api/projects/{project_id}/download")
def download_bundle(project_id: str):
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    zip_path = PROJECT_ZIP_PATHS.get(project_id)
    if not zip_path or not os.path.exists(zip_path):
        raise HTTPException(status_code=400, detail="Bundle not ready yet")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{project_id}_publishing_bundle.zip"
    )


@app.get("/api/projects/{project_id}/landing", response_class=HTMLResponse)
def get_landing_page(project_id: str):
    """Task 4.3: Direct Purchase Landing Page Template."""
    if project_id not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")

    project = PROJECTS[project_id]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project.title} - Official Book Release</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-amber-50/30 text-stone-800 font-serif antialiased">
    <nav class="max-w-6xl mx-auto px-6 py-6 flex justify-between items-center border-b border-amber-200">
        <div class="text-xl font-bold tracking-wider text-stone-900">PLOUGH PRESS</div>
        <a href="#buy" class="bg-stone-900 text-amber-50 px-5 py-2 rounded text-sm hover:bg-stone-800 transition">Get The Book</a>
    </nav>

    <main class="max-w-5xl mx-auto px-6 py-16 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <div>
            <span class="inline-block bg-amber-100 text-amber-900 text-xs px-3 py-1 rounded-full uppercase tracking-widest font-sans font-medium mb-4">Official Release</span>
            <h1 class="text-4xl md:text-5xl font-normal leading-tight text-stone-900 mb-4">{project.title}</h1>
            <p class="text-lg text-stone-600 italic mb-6">{project.metadata.subtitle}</p>
            <p class="text-stone-700 leading-relaxed mb-8 font-sans">{project.metadata.description}</p>

            <div id="buy" class="p-6 bg-white rounded-xl border border-stone-200 shadow-sm space-y-4">
                <div class="flex items-baseline justify-between">
                    <div>
                        <div class="text-2xl font-bold text-stone-900 font-sans">$19.99</div>
                        <div class="text-xs text-stone-500 font-sans">Includes EPUB, Print PDF & Launch Bundle</div>
                    </div>
                    <span class="text-xs font-sans text-emerald-700 bg-emerald-50 px-2 py-1 rounded border border-emerald-200">Instant Download</span>
                </div>
                <a href="/api/projects/{project.id}/download" class="block w-full text-center bg-stone-900 hover:bg-stone-800 text-white font-sans font-medium py-3 rounded-lg transition shadow">
                    Buy Now & Download Bundle
                </a>
            </div>
        </div>

        <div class="flex justify-center">
            <div class="w-80 bg-stone-100 p-8 rounded-2xl border border-stone-200 shadow-xl text-center space-y-4">
                <div class="text-2xl font-serif text-stone-900">{project.title}</div>
                <div class="text-xs text-stone-500 uppercase tracking-widest font-sans">{project.metadata.author}</div>
                <div class="my-8 py-12 border-y border-amber-300 text-amber-700 font-serif italic">❖</div>
                <div class="text-xs text-stone-400 font-sans">PLOUGH LITERARY PRESS</div>
            </div>
        </div>
    </main>

    <footer class="text-center py-8 text-xs text-stone-400 font-sans border-t border-amber-200 mt-16">
        © 2025 Plough Literary Press. All rights reserved. Powered by AutoBook Publisher Engine.
    </footer>
</body>
</html>"""
    return html
