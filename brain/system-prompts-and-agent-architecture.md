# System Prompts & Agent Architecture

## System Overview
AutoBook Publisher Agent is an automated AI pipeline and web application designed to take a simple book concept, title, or reference URL and convert it into a fully published, beautifully formatted book bundle (Plough-style aesthetics).

## Agent Workflow Diagram
```
[User Input: Topic/URL]
       │
       ▼
[01. Research & Outline Agent] ──► Generates Table of Contents & Chapter Scaffolding
       │
       ▼
[02. Narrative Writer Agent]   ──► Drafts Chapter Content (Narrative Non-Fiction)
       │
       ▼
[03. Editor & Proofreader Agent]─► Fixes Grammar, Flow, Tone, & Style Consistency
       │
       ▼
[04. Layout & Design Agent]    ──► Generates Print-Ready PDF & Reflowable EPUB 3.0
       │
       ▼
[05. Cover & Asset Agent]     ──► Generates 3D Mockups, Front/Back Covers & Launch Banners
       │
       ▼
[06. Publishing & Store Agent] ──► Prepares KDP Metadata Kit & Direct Sales Web Store Landing Page
```

## Agent Definitions & System Prompts

### Agent 1: Research & Outline Specialist
- **Role:** Curation & Fact-Checking Specialist.
- **Task:** Structure a 10-chapter outline based on historical figures, memoirs, or compelling biographies.
- **Output:** JSON schema representing `Chapter` objects with title, core thesis, key anecdotes, and estimated word count.

### Agent 2: Narrative Writer
- **Role:** Literary Non-Fiction Biographer.
- **Task:** Write engaging, story-driven chapter prose adhering to Plough Publishing's thoughtful, human-centric tone.
- **Output:** Clean Markdown formatted chapters with drop-caps markers and section breaks.

### Agent 3: Layout & Formatting Engine
- **Role:** Automated Typesetting Engine.
- **Task:** Convert raw Markdown into WeasyPrint HTML/CSS (Print PDF) and EPUB 3.0 file structures.
- **Rules:** Use classic serif fonts (Garamond/Georgia), 18mm outer margins, and elegant chapter headers.

### Agent 4: Media & Cover Generator
- **Role:** Visual Design Automation Agent.
- **Task:** Create minimal aesthetic front/back covers, 3D book mockups, and social media launch banners using SVG/Canvas/AI image API integrations.
