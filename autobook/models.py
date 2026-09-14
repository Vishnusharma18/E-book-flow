"""Data models for AutoBook Publisher Platform."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChapterOutline(BaseModel):
    chapter_number: int
    title: str
    core_thesis: str
    key_anecdotes: List[str] = Field(default_factory=list)
    estimated_word_count: int = 2000
    summary: str = ""


class BookOutline(BaseModel):
    title: str
    subtitle: str
    target_audience: str
    core_theme: str
    chapters: List[ChapterOutline] = Field(default_factory=list)


class ChapterContent(BaseModel):
    chapter_number: int
    title: str
    raw_text: str
    proofread_text: str = ""
    word_count: int = 0


class BookMetadata(BaseModel):
    title: str
    subtitle: str = ""
    author: str = "AutoBook Publisher"
    publisher: str = "Plough Aesthetic Press"
    description: str = ""
    keywords: List[str] = Field(default_factory=list)
    bisac_categories: List[str] = Field(default_factory=list)
    language: str = "en"


class BookProject(BaseModel):
    id: str
    title: str
    topic_or_url: str
    metadata: BookMetadata
    outline: Optional[BookOutline] = None
    chapters: List[ChapterContent] = Field(default_factory=list)
    status: str = "created"  # created, researching, writing, proofreading, rendering, completed, failed
    progress: float = 0.0  # 0 to 100
    current_step: str = "Initialized"
    created_at: str = ""
