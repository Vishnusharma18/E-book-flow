# Technical Architecture & Technology Stack

## System Architecture Diagram
```
   ┌─────────────────────────────────────────────────────────┐
   │                   Next.js 14 Web App                    │
   │        (Dashboard, Live Preview, Progress Tracker)       │
   └───────────────────────────┬─────────────────────────────┘
                               │ REST / SSE API
   ┌───────────────────────────▼─────────────────────────────┐
   │                  FastAPI Backend Server                 │
   │    (Task Queue, Agent Orchestrator, State Engine)       │
   └───────┬───────────────────┬───────────────────┬─────────┘
           │                   │                   │
   ┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
   │ AI Agents Engine│ │ Render Engine │   │ Export Bundle │
   │ (OpenAI/Gemini) │ │ (WeasyPrint / │   │ (.epub, .pdf, │
   │               │ │  Pillow / SVG)│   │  .zip kit)    │
   └───────────────┘   └───────────────┘   └───────────────┘
```

## Recommended Technology Stack

| Layer | Technology Selected | Reason / Benefit |
| :--- | :--- | :--- |
| **Frontend Framework** | **Next.js 14 (App Router, Tailwind CSS)** | Fast, SEO-optimized, smooth progress visualization dashboard. |
| **Backend API Server** | **Python FastAPI** | Asynchronous execution, native integration with WeasyPrint & AI libraries. |
| **AI Orchestration** | **LangChain / LlamaIndex / Direct API** | Agentic workflows for drafting, editing, and fact-checking. |
| **Typesetting & PDF** | **WeasyPrint (HTML/CSS to PDF)** | Precise CSS Paged Media support for margins, headers, and print bleeding. |
| **EPUB Engine** | **EBookLib (Python)** | Industry-standard EPUB 3.0 file builder. |
| **Graphic Generation** | **Pillow / CairoSVG / Canvas** | Automated 3D mockups, cover wraps, and social media posters. |
| **Task Queue** | **Celery + Redis / Background Tasks** | Asynchronous background generation for long book pipelines. |
| **Database** | **PostgreSQL / SQLite** | Store user projects, chapter states, and task statuses. |
