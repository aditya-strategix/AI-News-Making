# AI-Powered Scraping & Summarization Platform

This document outlines the implementation plan for a state-of-the-art web application that allows users to select specific apps or websites, scrapes data from them, generates AI-powered summaries, and delivers them directly via Email and WhatsApp. 

To ensure the product is fit for the "current AI market era", the plan incorporates modern design aesthetics, user authentication, robust AI processing, and a scalable architecture.

> [!TIP]
> **Added Functionalities for a Premium Experience:**
> - **User Authentication & Profiles:** Allows multiple users ("all person use") to register, save their preferred sources, and set up their personal delivery details (Email & WhatsApp).
> - **Customizable Summaries:** Users can choose the format (e.g., Bullet Points, Executive Brief, Tweet Thread) and tone of the summary.
> - **Multi-Lingual Translation:** Summaries can be automatically translated and formatted into the user's preferred language (e.g., Spanish, Hindi).
> - **Delivery Scheduling:** Users can choose *when* they want to receive their summaries (e.g., daily at 8 AM, weekly on Fridays).
> - **Dashboard & Interactive RAG Chat:** A beautiful web interface to view past summaries, manage active sources, and an interactive chat interface to ask questions directly to the accumulated news.

## User Review Required

> [!WARNING]
> This plan introduces a split architecture: A **Next.js Frontend** for a premium user experience and a **FastAPI Python Backend** to leverage the existing data/AI libraries. 

> [!IMPORTANT]
> To send automated messages to WhatsApp, you will need a business API provider like **Twilio** or the **Meta WhatsApp Cloud API**. For emails, you will need an SMTP service like **SendGrid** or **Resend**. 

## Open Questions

1. **Third-party APIs:** Do you already have accounts/keys for Twilio (WhatsApp) and SendGrid/Resend (Email), or should we start with a standard free SMTP provider for testing?
2. **Scraping Targets:** Are there specific, complex sites you want to target right away that might require bypassing bot protections (e.g., LinkedIn, Twitter)? If so, we may need to integrate advanced scraping tools like Playwright instead of just BeautifulSoup.
3. **Database Preference:** The existing `pyproject.toml` includes PostgreSQL. Shall we proceed with setting up a local or hosted PostgreSQL database for user management?

## Proposed Changes

We will restructure the project into a robust Client-Server architecture.

### 1. Frontend (Next.js Application)
We will create a new directory `frontend/` initialized with Next.js, React, and modern UI libraries.

#### [NEW] `frontend/` (Next.js App)
- **UI Framework:** Next.js (App Router) for SEO and performance.
- **Styling:** Premium aesthetic using Vanilla CSS (or Tailwind if authorized), focusing on Glassmorphism, Dark Mode, and smooth micro-animations.
- **Pages:**
  - `Landing Page`: A high-converting, visually stunning homepage explaining the product.
  - `Dashboard`: Where logged-in users view past summaries.
  - `Sources & Settings`: Interface for users to select target websites, enter their WhatsApp/Email, and choose their summary tone/schedule.

### 2. Backend API (Python / FastAPI)
We will convert the existing `ai-news-aggregator` skeleton into a fully functional FastAPI web server.

#### [MODIFY] `e:\AI NEWS MAKING\ai-news-aggregator\pyproject.toml`
- Add `fastapi`, `uvicorn`, `celery` (for robust background tasks), `twilio` (for WhatsApp integrations), `langchain` / `langchain-openai` (for advanced GenAI workflows), and `chromadb` (for vector storage and RAG).

#### [NEW] `e:\AI NEWS MAKING\ai-news-aggregator\app\main.py`
- Initialize the FastAPI application, routing, and CORS middleware to communicate with the frontend.

#### [NEW] `e:\AI NEWS MAKING\ai-news-aggregator\app\api\endpoints.py`
- Create REST API endpoints for user registration, saving user preferences, and manually triggering a scrape/summarize task.

#### [NEW] `e:\AI NEWS MAKING\ai-news-aggregator\app\services\scraper.py`
- **Factory/Strategy Pattern for Scrapers:** We will implement a `BaseScraper` class with specific implementations for different sources (e.g., `YoutubeScraper` using `youtube-transcript-api`, `OpenAIScraper` for their blog structure). 
- **Generic Fallback:** For websites without a predefined scraper, we will include a `GenericScraper` that uses a smart readability algorithm (via `beautifulsoup4`) to extract the main article text. This way, we handle complex sites perfectly while still supporting *any* URL a user throws at it.

#### [NEW] `e:\AI NEWS MAKING\ai-news-aggregator\app\services\ai_summarizer.py`
- **LangChain Integration:** Implement the GenAI logic using **LangChain** to build robust LLM pipelines. We will use LangChain's `MapReduceDocumentsChain` or `RefineDocumentsChain` for summarizing large articles that exceed standard token limits, and structured `PromptTemplates` to enforce specific output formats (e.g., bullet points, executive summaries) and **target languages** (Translation). This modern architectural pattern demonstrates strong, production-ready GenAI skills.

#### [NEW] `e:\AI NEWS MAKING\ai-news-aggregator\app\services\rag_chat.py`
- **Vector Database & RAG Pipeline:** We will index all scraped articles into a local **ChromaDB** vector store using OpenAI embeddings. This module will expose a conversational LangChain retrieval pipeline (RAG), allowing users to "chat with the news" directly from the web dashboard.

#### [NEW] `e:\AI NEWS MAKING\ai-news-aggregator\app\services\notifications.py`
- Implement the logic to format and send the finalized AI summary to the user's provided Email via SMTP and WhatsApp via Twilio.

#### [NEW] `e:\AI NEWS MAKING\ai-news-aggregator\app\scheduler.py`
- Configure `APScheduler` (or Celery) to periodically check the database for users whose scheduled delivery time has arrived, trigger the scraper -> AI -> notification pipeline.

### 3. Database Layer
#### [NEW] `e:\AI NEWS MAKING\ai-news-aggregator\app\db\models.py`
- Define SQLAlchemy models for `Users`, `Sources` (websites they want to scrape), and `Summaries` (history of past generated content).

## Verification Plan

### Automated Tests
- Run `pytest` on the Python backend to verify that the scraping engine correctly parses HTML.
- Test the AI prompt templates using mock scraped data to ensure the formatting matches expectations (e.g., bullet points vs paragraphs).

### Manual Verification
1. Start both the FastAPI backend and Next.js frontend servers locally.
2. Sign up as a new user via the web interface.
3. Add a test website (e.g., a news blog) and configure a test email and phone number.
4. Manually trigger the pipeline and verify:
   - The UI updates dynamically.
   - A summary is generated successfully.
   - The summary arrives in the designated Email inbox.
   - The summary arrives on the designated WhatsApp number.
