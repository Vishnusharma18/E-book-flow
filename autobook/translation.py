"""Multi-Language Translation Engine for AutoBook Publisher Platform."""

from typing import Dict, Any, List, Optional
from autobook.models import BookProject, ChapterContent, BookMetadata


class BookTranslationEngine:
    """Engine for translating book projects into multiple languages."""

    SUPPORTED_LANGUAGES = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "hi": "Hindi",
        "it": "Italian",
        "pt": "Portuguese"
    }

    # Mock translation dictionary for demonstration / offline capability
    MOCK_PREFIXES = {
        "es": "[ES] ",
        "fr": "[FR] ",
        "de": "[DE] ",
        "hi": "[HI] ",
        "it": "[IT] ",
        "pt": "[PT] "
    }

    def translate_project(self, project: BookProject, target_language: str) -> BookProject:
        """Translates a BookProject into the target language."""
        lang_code = target_language.lower().strip()
        if lang_code not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language code '{target_language}'. Supported: {list(self.SUPPORTED_LANGUAGES.keys())}")

        prefix = self.MOCK_PREFIXES.get(lang_code, f"[{lang_code.upper()}] ")

        # Create translated copy of metadata
        translated_metadata = BookMetadata(
            title=f"{prefix}{project.metadata.title}",
            subtitle=f"{prefix}{project.metadata.subtitle}" if project.metadata.subtitle else "",
            author=project.metadata.author,
            publisher=project.metadata.publisher,
            description=f"{prefix}{project.metadata.description}" if project.metadata.description else "",
            keywords=project.metadata.keywords,
            bisac_categories=project.metadata.bisac_categories,
            language=lang_code
        )

        # Create translated chapters
        translated_chapters = []
        for ch in project.chapters:
            raw = ch.raw_text or ""
            proofread = ch.proofread_text or ""
            translated_chapters.append(ChapterContent(
                chapter_number=ch.chapter_number,
                title=f"{prefix}{ch.title}",
                raw_text=f"{prefix}{raw}" if raw else "",
                proofread_text=f"{prefix}{proofread}" if proofread else "",
                word_count=ch.word_count
            ))

        translated_project = BookProject(
            id=f"{project.id}_{lang_code}",
            title=f"{prefix}{project.title}",
            topic_or_url=project.topic_or_url,
            metadata=translated_metadata,
            outline=project.outline,
            chapters=translated_chapters,
            status=project.status,
            progress=project.progress,
            current_step=f"Translated to {self.SUPPORTED_LANGUAGES[lang_code]}",
            created_at=project.created_at
        )

        return translated_project
