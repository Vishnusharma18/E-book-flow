"""Analytics & Reading Time Analysis Engine for AutoBook Publisher Platform."""

import re
from typing import Dict, Any, List
from autobook.models import BookProject, ChapterContent


class BookAnalyticsEngine:
    """Engine for analyzing book content metrics, reading times, and complexity."""

    AVERAGE_WPM = 200  # Average reading speed in words per minute

    @staticmethod
    def calculate_flesch_reading_ease(text: str) -> float:
        """Calculates Flesch Reading Ease score for text."""
        words = re.findall(r'\b\w+\b', text)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]

        num_words = len(words)
        num_sentences = len(sentences) if len(sentences) > 0 else 1

        if num_words == 0:
            return 100.0

        # Count syllables (approximation)
        def count_syllables(word: str) -> int:
            word = word.lower()
            if len(word) <= 3:
                return 1
            word = re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$', '', word)
            word = re.sub(r'^y', '', word)
            syllables = len(re.findall(r'[aeiouy]{1,2}', word))
            return max(1, syllables)

        num_syllables = sum(count_syllables(w) for w in words)

        # Flesch formula: 206.835 - 1.015 * (total words / total sentences) - 84.6 * (total syllables / total words)
        score = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)
        return round(max(0.0, min(100.0, score)), 2)

    def analyze_project(self, project: BookProject) -> Dict[str, Any]:
        """Generates comprehensive analytics for a book project."""
        chapter_analytics = []
        total_words = 0
        total_chars = 0
        all_text = []

        for ch in project.chapters:
            content = ch.proofread_text or ch.raw_text or ""
            words = len(re.findall(r'\b\w+\b', content))
            chars = len(content)
            reading_time_mins = round(words / self.AVERAGE_WPM, 1) if words > 0 else 0.0
            flesch_score = self.calculate_flesch_reading_ease(content)

            total_words += words
            total_chars += chars
            all_text.append(content)

            chapter_analytics.append({
                "chapter_number": ch.chapter_number,
                "title": ch.title,
                "word_count": words,
                "character_count": chars,
                "estimated_reading_time_minutes": reading_time_mins,
                "flesch_reading_ease": flesch_score
            })

        full_text = " ".join(all_text)
        overall_reading_time_mins = round(total_words / self.AVERAGE_WPM, 1) if total_words > 0 else 0.0
        overall_reading_time_hours = round(overall_reading_time_mins / 60.0, 2)
        overall_flesch_score = self.calculate_flesch_reading_ease(full_text)

        # Interpret readability score
        if overall_flesch_score >= 80:
            readability_level = "Easy (6th Grade)"
        elif overall_flesch_score >= 60:
            readability_level = "Standard (8th-9th Grade)"
        elif overall_flesch_score >= 40:
            readability_level = "Challenging (High School / College)"
        else:
            readability_level = "Academic / Highly Complex"

        return {
            "project_id": project.id,
            "title": project.title,
            "total_chapters": len(project.chapters),
            "total_word_count": total_words,
            "total_character_count": total_chars,
            "estimated_reading_time": {
                "minutes": overall_reading_time_mins,
                "hours": overall_reading_time_hours,
                "formatted": f"{int(overall_reading_time_hours)}h {int(overall_reading_time_mins % 60)}m" if overall_reading_time_hours >= 1 else f"{int(overall_reading_time_mins)} mins"
            },
            "readability": {
                "flesch_reading_ease": overall_flesch_score,
                "level": readability_level
            },
            "chapters": chapter_analytics
        }
