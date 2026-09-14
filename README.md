# AutoBook Publisher Agent Platform

An automated AI publishing suite designed to transform book ideas into fully formatted PDFs, EPUBs, wraparound covers, 3D mockups, and marketing bundles.

## Repository Structure

```
autobook-publisher-agent/
├── README.md
├── autobook/
│   ├── analytics.py          # Analytics & Reading Time Analysis Engine
│   ├── translation.py        # Multi-Language Translation Engine
│   ├── exporter.py           # One-Click .zip Publishing Bundle Exporter
│   ├── models.py             # Core Data Models (BookProject, Metadata, etc.)
│   ├── formatting/           # PDF (WeasyPrint), EPUB, Cover & Marketing Canvas Engines
│   ├── pipeline/             # Research, Writer, Proofreader & Master Pipeline Agents
│   └── server/               # FastAPI Server & REST Endpoints
├── frontend/                 # Next.js 14 Dashboard & Landing Pages
└── tests/                    # Pytest Suite (100% Pass Rate)
```

## Core Module Guide
- `brain/system-prompts-and-agent-architecture.md`: Full agent system prompts & pipeline flow.
- `brain/product-vision-and-target-audience.md`: Product positioning, target demographics, and output deliverables.
- `brain/roadmap-and-task-tracker.md`: Dynamic task board with 🟩 (COMPLETED) and ⬜ (PENDING) statuses.
- `brain/tech-stack-and-system-architecture.md`: FastAPI + Next.js 14 + WeasyPrint architecture specs.

---

## Live Demo Example & Sample Outputs

Below is a live execution example generated using the AutoBook Publisher pipeline:

### Demo Configuration:
- **Topic**: *"The Future of Quantum Computing and AI"*
- **Generated Book Title**: *"The Journey of The Future Of Quantum Computing And Ai"*
- **Project ID**: `305fa717`

### Analytics Metrics:
- **Total Chapters**: 10 Chapters
- **Total Word Count**: 2,390 Words
- **Estimated Reading Time**: 11 Minutes
- **Flesch Reading Ease Score**: 38.03 (*Academic / Highly Complex*)

### Generated Deliverables (.zip Publishing Bundle):
```
305fa717_publishing_bundle.zip
├── 305fa717_print.pdf           # Print-ready PDF with dropcaps & headers
├── 305fa717_ebook.epub          # Validated EPUB 3.0 e-book
├── cover_front.png              # Front Cover Design
├── cover_wraparound.png         # KDP Wraparound Cover (Front + Spine + Back)
├── mockup_3d.png                # 3D Hardcover Book Mockup
├── marketing_poster.png         # Social Media Quote Poster
├── marketing_banner.png         # Promotional Banner
├── kdp_metadata.json            # KDP Metadata Export
└── analytics_report.json        # Analytics & Readability Report
```

---

## Quick Start

### Running Tests
```bash
python3 -m pytest
```

### Starting the API Server
```bash
python3 -m uvicorn autobook.server.main:app --reload
```
