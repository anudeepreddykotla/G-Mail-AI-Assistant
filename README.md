# Gmail AI Assistant

A full-stack Gmail client with built-in AI features for summarization, smart replies, action extraction, intent detection, reminders, and intelligent email organization.

This project combines Gmail operations with AI-powered productivity features in a clean, scalable, and modular architecture.

---

## Tech Stack

### Frontend

- Next.js 16
- TypeScript
- TailwindCSS
- React Query
- Zustand

### Backend

- FastAPI
- PostgreSQL
- SQLAlchemy
- Google OAuth 2.0 (PKCE)
- JWT Authentication

### AI

- Gemini 2.5 Flash

---

## Features

# Authentication

- Google OAuth 2.0 login
- PKCE-based secure authentication
- JWT session management
- Persistent user sessions

---

# Gmail Features

## Email Management

- View inbox
- View sent mails
- View starred mails
- View trash
- View drafts
- View individual emails
- Search emails

## Email Actions

- Mark as read / unread
- Star / unstar emails
- Archive / unarchive emails
- Move to trash
- Restore from trash

## Sending Emails

- Compose new emails
- Reply to emails
- Thread-based replies

## Drafts

- Create drafts
- Edit drafts
- Delete drafts
- Send drafts

## Threads

- Fetch email threads
- View full threaded conversations
- Thread-aware replies
- Thread-aware AI summaries

## Labels

- List labels
- Create labels
- Apply labels to emails
- Remove labels from emails

---

# AI Features

## Email Summarization

Generate structured summaries for individual emails:

- Short summary
- Key bullet points
- Action items

---

## Thread Summarization

Generate summaries for complete email conversations to preserve context.

Useful for:
- Long discussions
- Team updates
- Ongoing project threads

---

## Smart Reply

Generate context-aware reply suggestions:

- Formal
- Casual
- Concise

Supports:
- Single email replies
- Thread-aware replies

---

## Action Extraction

Extract actionable tasks from emails:

Example:
- Submit assignment before Friday
- Attend sync at 5 PM

---

## Priority Classification

Classify emails into:

- High
- Medium
- Low

Examples:
- Job invitations
- Contest invitations
- Hackathons
- Interview mails
- Deadlines

---

## Intent Detection

Detect semantic intent of emails.

Examples:

- Job Opportunity
- Internship
- Interview
- Hackathon
- Contest
- Meeting
- Project Update
- Academic
- Payment Due
- Invoice
- Promotion
- Newsletter

---

## AI Label Suggestions

Generate smart labels based on email intent.

Examples:

- Work
- Project
- Career
- Finance
- Academic
- Promotions

---

## Reminder Extraction

Extract reminder-worthy tasks with deadlines and urgency.

Example:

- Register for hackathon
- Submit application
- Attend project sync

---

# Frontend Optimizations

## React Query

Used for:

- API caching
- Background refetching
- Better loading states
- Reduced duplicate requests

---

## Infinite Pagination

Implemented token-based pagination for scalable email loading.

---

## Debounced Search

Used `lodash/debounce` to optimize search and reduce API calls.

---

## Virtualized Rendering

Used `react-window` to render only visible email rows for better performance.

---

## Memoization

Used:

- `React.memo`
- `useMemo`
- `useCallback`

To reduce unnecessary rerenders.

---

## Route Prefetching

Prefetches routes and email content for faster navigation.

---

## AI Frontend Integration

Integrated AI actions directly into the email view:

- Summarize email
- Summarize thread
- Generate smart replies
- Extract tasks
- Detect priority
- Detect intent
- Suggest labels
- Extract reminders

---

# Backend Architecture

Built using modular service-based architecture.

```bash
backend/app
├── ai
├── api
├── auth
├── core
├── db
├── gmail
├── models
└── security
```

---

## Service Layer

Separated Gmail logic into:

- `message_service`
- `send_service`
- `draft_service`
- `thread_service`
- `label_service`
- `search_service`
- `message_actions`

---

## Dependency Injection

Reusable dependencies:

- `get_current_user()`
- `get_current_gmail()`

This reduces duplicated authentication logic.

---

## Security

- Refresh tokens encrypted before storage
- Automatic access token refresh

---

# AI Architecture

Structured AI layer:

```bash
backend/app/ai
├── client.py
├── prompts.py
├── schemas.py
├── summarizer.py
├── smart_reply.py
├── extractor.py
├── classifier.py
├── intent_detector.py
├── label_suggester.py
├── reminder_extractor.py
├── resolver.py
├── cache_service.py
└── utils.py
```

---

## AI Pipeline

```text
Frontend
   ↓
Protected AI Route
   ↓
Auth Validation
   ↓
Gmail Content Resolver
   ↓
Email Cleaning
   ↓
Gemini Processing
   ↓
Schema Validation
   ↓
Structured Response
```

---

## AI Optimizations

- Reusable Gemini client
- Prompt centralization
- Typed schemas
- Summary caching
- Email preprocessing
- Deterministic label generation
- Modular AI services
- Thread-aware context handling

---

# Project Structure

```bash
gmail-ai-assistant
├── backend
├── frontend
├── docker
└── docs
```

---

# Setup

## Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# Environment Variables

## Backend `.env`

```env
DATABASE_URL=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
ENCRYPTION_KEY=
GEMINI_API_KEY=
```

---

## License

MIT License