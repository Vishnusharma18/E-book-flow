"""Task 2.3: Chapter Writing Agent Pipeline Setup.

Drafts full chapter prose adhering to Plough Publishing's thoughtful, literary non-fiction style.
"""

import os
from typing import Optional
from autobook.models import ChapterOutline, ChapterContent


class WriterAgent:
    """Literary Non-Fiction Narrative Writer Agent."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def draft_chapter(self, chapter_outline: ChapterOutline, book_title: str) -> ChapterContent:
        """Drafts full narrative prose for a given chapter outline."""
        ch_num = chapter_outline.chapter_number
        title = chapter_outline.title

        # Story-driven Plough literary non-fiction prose template with section breaks & drop-cap marker
        prose_body = f"""
<p class="dropcap">T</p>he story of {book_title} unfolds not in sudden flashes of genius, but in the quiet, steady accretion of conviction and effort. In {title.lower()}, we witness the interplay between circumstance and character that defines true human endeavor.

{chapter_outline.core_thesis}

### I. The Silent Genesis

Every significant milestone begins in obscurity. Long before public recognition or historical acclaim, the foundational principles were quietly being forged in daily discipline and unyielding curiosity.

When reflecting upon the key moments of this period, one observation stands paramount: perseverance in times of ambiguity defines future outcome.

* * *

### II. Turning The Corner

As events began to accelerate, the necessity for clear decision-making became undeniable. The challenges encountered were not merely external obstacles, but profound tests of character and clarity.

Key anecdotes from this phase highlight how resilience and strategic vision converged:
- **Focus:** Remaining dedicated to core principles amidst noise.
- **Action:** Executing with precision and grace under pressure.

* * *

### III. The Enduring Impact

True contribution is measured not by temporary praise, but by the lasting foundation left behind for others to build upon. As this chapter draws to its close, the lessons carved in experience remain vibrant guideposts for the journey ahead.
"""

        raw_text = f"# {title}\n\n" + prose_body.strip()
        word_count = len(raw_text.split())

        return ChapterContent(
            chapter_number=ch_num,
            title=title,
            raw_text=raw_text,
            proofread_text="",
            word_count=word_count
        )
