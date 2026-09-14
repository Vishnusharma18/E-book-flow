"""Master Pipeline orchestrator for AutoBook Content Generation."""

import uuid
from datetime import datetime, timezone
from typing import Callable, Optional
from autobook.models import BookProject
from autobook.pipeline.research_agent import ResearchAgent
from autobook.pipeline.writer_agent import WriterAgent
from autobook.pipeline.proofreader_agent import ProofreaderAgent


class ContentPipeline:
    """Orchestrates the creation and processing of a book project."""

    def __init__(self, api_key: Optional[str] = None):
        self.research_agent = ResearchAgent(api_key=api_key)
        self.writer_agent = WriterAgent(api_key=api_key)
        self.proofreader_agent = ProofreaderAgent()

    def run_pipeline(
        self,
        topic_or_url: str,
        custom_title: Optional[str] = None,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> BookProject:
        """Executes full research, writing, and proofreading pipeline."""
        project_id = str(uuid.uuid4())[:8]

        def update_progress(msg: str, percent: float):
            if progress_callback:
                progress_callback(msg, percent)

        # Step 1: Research & Outline
        update_progress("Analyzing topic and structuring 10-chapter outline...", 10.0)
        outline = self.research_agent.generate_outline(topic_or_url, custom_title=custom_title)
        metadata = self.research_agent.generate_metadata(topic_or_url, outline)

        project = BookProject(
            id=project_id,
            title=outline.title,
            topic_or_url=topic_or_url,
            metadata=metadata,
            outline=outline,
            chapters=[],
            status="writing",
            progress=20.0,
            current_step="Drafting Chapter Content",
            created_at=datetime.now(timezone.utc).isoformat()
        )

        # Step 2 & 3: Draft and Proofread Chapters
        total_chapters = len(outline.chapters)
        for idx, ch_outline in enumerate(outline.chapters, start=1):
            progress_pct = 20.0 + (idx / total_chapters) * 60.0
            update_progress(f"Writing & editing Chapter {idx}/{total_chapters}: {ch_outline.title}", progress_pct)

            raw_ch = self.writer_agent.draft_chapter(ch_outline, project.title)
            proofread_ch = self.proofreader_agent.proofread(raw_ch)
            project.chapters.append(proofread_ch)

        project.status = "content_ready"
        project.progress = 80.0
        project.current_step = "Content Generation Complete"
        update_progress("Content generation and proofreading complete!", 80.0)

        return project
