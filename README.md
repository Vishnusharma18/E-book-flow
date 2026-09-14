# AutoBook Publisher Agent Platform

An automated AI publishing suite designed to transform book ideas into fully formatted PDFs, EPUBs, wraparound covers, 3D mockups, and marketing bundles.

---

## 🚀 How To Use AutoBook Publisher

### 1. Prerequisites & Installation

Ensure you have Python 3.12+ installed. Install required dependencies:

```bash
pip install fastapi pydantic uvicorn Pillow ebooklib weasyprint pytest httpx
```

### 2. Running via Python Script / CLI

You can generate a complete book, covers, and publishing bundle programmatically:

```python
from autobook.pipeline.master_pipeline import ContentPipeline
from autobook.exporter import BundleExporter
from autobook.analytics import BookAnalyticsEngine

# Step 1: Run end-to-end generation pipeline on any topic
pipeline = ContentPipeline()
project = pipeline.run_pipeline("The Future of Quantum Computing and AI")

# Step 2: Analyze book metrics & reading time
analytics = BookAnalyticsEngine().analyze_project(project)
print("Total Words:", analytics["total_word_count"])
print("Reading Time:", analytics["estimated_reading_time"]["formatted"])

# Step 3: Export complete publishing bundle (.zip)
exporter = BundleExporter(output_dir="results")
zip_path = exporter.build_bundle(project)
print("Publishing bundle exported to:", zip_path)
```

### 3. Running via REST API Server

Start the FastAPI backend server:

```bash
python3 -m uvicorn autobook.server.main:app --reload
```

Interactive API documentation will be available at `http://localhost:8000/docs`.

#### Available API Endpoints:
- **`POST /api/projects`**: Create & generate a new book project (`{"topic_or_url": "Topic Name"}`)
- **`GET /api/projects/{project_id}`**: Check project generation status & progress
- **`GET /api/projects/{project_id}/analytics`**: Get word counts, reading time, and readability metrics
- **`POST /api/projects/{project_id}/translate`**: Translate project to Spanish (`es`), French (`fr`), German (`de`), Hindi (`hi`), etc.
- **`GET /api/projects/{project_id}/download`**: Download the final `.zip` publishing bundle
- **`GET /api/projects/{project_id}/landing`**: View auto-generated direct purchase landing page

---

## 📂 Repository Structure

```
autobook-publisher-agent/
├── README.md
├── results/                  # Generated Demo Outputs & Artifacts
│   ├── 168f4dce/             # Extracted deliverables (PDF, EPUB, Covers, Mockup, Analytics)
│   └── 168f4dce_publishing_bundle.zip
├── autobook/
│   ├── analytics.py          # Analytics & Reading Time Analysis Engine
│   ├── translation.py        # Multi-Language Translation Engine
│   ├── exporter.py           # One-Click .zip Publishing Bundle Exporter
│   ├── models.py             # Core Data Models
│   ├── formatting/           # PDF (WeasyPrint), EPUB, Cover & Marketing Canvas Engines
│   ├── pipeline/             # Research, Writer, Proofreader & Master Pipeline Agents
│   └── server/               # FastAPI Server & REST Endpoints
├── frontend/                 # Next.js 14 Dashboard & Landing Pages
└── tests/                    # Pytest Suite (100% Pass Rate)
```

---

## 📊 Results & Demo Output Example

A sample run on the topic *"The Future of Quantum Computing and AI"* has been generated and saved in the `results/` folder.

### Demo Run Summary:
- **Topic**: *"The Future of Quantum Computing and AI"*
- **Generated Title**: *"The Journey of The Future Of Quantum Computing And Ai"*
- **Project ID**: `168f4dce`
- **Total Chapters**: 10 Chapters
- **Total Word Count**: 2,390 Words
- **Estimated Reading Time**: 11 Minutes
- **Readability Score**: 38.03 (*Academic / Highly Complex*)

### Generated Deliverables Saved in `results/`:
All output files are available in `results/168f4dce/` and packaged inside `results/168f4dce_publishing_bundle.zip`:

| Deliverable | File Path | Description |
| :--- | :--- | :--- |
| **Print PDF** | `results/168f4dce/168f4dce_print.pdf` | Print-ready PDF with dropcaps, headers & page numbers |
| **EPUB E-Book** | `results/168f4dce/168f4dce_ebook.epub` | Validated EPUB 3.0 file for e-readers |
| **Front Cover** | `results/168f4dce/cover_front.png` | High-resolution front cover graphic |
| **Wraparound Cover** | `results/168f4dce/cover_wraparound.png` | Complete KDP paperback cover (Back + Spine + Front) |
| **3D Book Mockup** | `results/168f4dce/mockup_3d.png` | 3D Hardcover perspective mockup |
| **Marketing Poster** | `results/168f4dce/marketing_poster.png` | Social media quote poster |
| **Marketing Banner** | `results/168f4dce/marketing_banner.png` | Launch promotional banner |
| **Analytics Report** | `results/168f4dce/analytics_report.json` | JSON word count, reading time & readability report |
| **KDP Metadata** | `results/168f4dce/kdp_metadata.json` | Publishing metadata JSON |
| **Full Bundle ZIP** | `results/168f4dce_publishing_bundle.zip` | 1-Click ZIP bundle containing all deliverables |

---

## 🧪 Testing

To run the full test suite (18 unit tests):

```bash
python3 -m pytest
```
