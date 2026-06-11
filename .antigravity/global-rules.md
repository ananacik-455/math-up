# Global Rules

## Tech Stack
**Frontend:** React + Vite + Telegram UI Kit. Optimised for mobile — all interactions must be thumb-friendly.
**Backend:** Python + FastAPI + PostgreSQL (for user progress) + Redis (for leaderboard).

## Architectural Constraints
- The application MUST live entirely inside Telegram as a Web App (TWA).
- Use Telegram's native auth — no separate login needed.
- Payments via Telegram Stars or direct card.

## Credentials Management
- **Environment Variables**: Always use `.env` files for saving all credentials, tokens, and secret keys. Never hardcode secrets in the source code. Provide `.env.example` templates.
