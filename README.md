# Gmail AI Assistant

A full-stack Gmail client with built-in AI features for summarization, smart replies, action extraction, and priority classification.

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

- Create draft
- Fetch drafts
- Edit drafts
- Delete drafts

## Threads

- Fetch email threads
- View complete thread conversations

## Labels

- List labels
- Create labels
- Add labels to emails
- Remove labels from emails

---

# AI Features

## Email Summarization

Generate structured summaries for emails:

- Short summary
- Key bullet points
- Action items

## Smart Reply

Generate three reply options:

- Formal
- Casual
- Concise

## Action Extraction

Extract actionable tasks from emails with deadlines.

Example:

- Submit assignment before Friday
- Attend meeting at 5 PM

## Priority Classification

Classify emails into:

- High
- Medium
- Low

Examples:

- Job invitations
- Contest invitations
- Hackathons
- Interviews
- Deadlines

---

# Frontend Optimizations

## React Query

Used for:

- API caching
- Background refetching
- Better loading states
- Reduced duplicate requests

## Infinite Pagination

Implemented token-based pagination for scalable email loading.

## Debounced Search

Used `lodash/debounce` to optimize search and reduce API calls.

## Virtualized Rendering

Used `react-window` to render only visible email rows for better performance.

## Memoization

Used:

- `React.memo`
- `useMemo`
- `useCallback`

To reduce unnecessary rerenders.

## Route Prefetching

Prefetches routes and email content for faster navigation.

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

## Service Layer

Separated Gmail logic into:

- `message_service`
- `send_service`
- `draft_service`
- `thread_service`
- `label_service`
- `search_service`
- `message_actions`

## Dependency Injection

Reusable dependencies:

- `get_current_user()`
- `get_current_gmail()`

This reduces duplicated authentication logic.

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
├── resolver.py
├── cache_service.py
└── utils.py
```

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

## AI Optimizations

- Reusable Gemini client
- Prompt centralization
- Typed schemas
- Summary caching
- Email preprocessing
- Modular AI services

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

## Future Improvements

- AI-powered email categorization
- Calendar event extraction
- Meeting summarization
- Attachment summarization
- Spam detection with AI
- Voice-based email actions

---

## License

MIT License
