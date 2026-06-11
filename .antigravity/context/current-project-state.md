# Current Project State - MathUp

This file serves as a single source of truth for the AI to instantly recall the architecture, active features, and current state of the MathUp project without needing to read through the entire codebase.

## 🏗️ Architecture Overview
MathUp is a Telegram Mini App (TWA) designed to help users practice and improve their math skills. It uses a decoupled client-server architecture:
- **Frontend**: React, TypeScript, and Vite. Runs entirely inside the Telegram Web App.
- **Backend**: Python, FastAPI, SQLAlchemy.
- **Database**: Currently using SQLite for MVP, but the schema is built using PostgreSQL-compliant patterns (UUIDs, JSONB).

## ✅ Currently Implemented & Working
1. **Database Schema**: Fully upgraded to use `UUID` primary keys. `content` and `validation_rules` for questions are stored in flexible JSON format to allow arbitrary mathematical content formats.
2. **User Authentication**: 
   - The frontend reads the `initData` payload from Telegram natively.
   - The backend validates this payload using HMAC-SHA256 cryptography in `auth.py`. 
   - *Note on Auth*: We are currently running with a security bypass (`BYPASS_TELEGRAM_AUTH="true"`) because the Telegram Bot token used to sign the payload does not match the token in `.env`. The bypass securely extracts the user's real Telegram `id` and `username` so database progression works perfectly.
3. **Core Gameplay Loop**: 
   - The frontend can fetch questions and display them.
   - The user selects an option, and the frontend waits for the server response before coloring the button (Green/Red) to prevent UI flickering.
   - The backend validates the answer and awards 10 XP to the *specific* authenticated user.

## 🛠️ Development Setup Tricks
- **CORS / Network**: The frontend Vite server is exposed to the internet via Ngrok. The frontend (`vite.config.ts`) has a proxy set up so that all `/api` calls are cleanly routed to the local Python FastAPI backend (`localhost:8000`). This completely bypasses CORS issues.
- **State Management**: React state handles the current question index, the selected option, and the correct option natively.

## 🚀 Next Immediate Steps (From Week 3-4 Plan)
We are currently entering the "Core Loop Expansion" phase:
1. **Dynamic Question Serving**: Update the `/api/questions` endpoint to stop serving random questions and instead serve questions based on Elo difficulty and user mastery.
2. **Elo & Mastery Services**: Build the mathematical algorithms to adjust user Elo based on correct/incorrect answers.
3. **Streaks**: Implement daily streak tracking logic.
