# Workflow: Week 1-2 Skeleton

## Objective
Build the initial Telegram bot + Mini App shell, authentication, core game loop for one game mode, and basic progression.

## Standard Operating Procedure (SOP)

1. **Telegram Bot & TWA Shell Setup**
   - Initialize the Telegram bot.
   - Set up the React + Vite frontend and configure it as a Telegram Web App (TWA).
   - Set up the Python + FastAPI backend.
   - Establish communication between the TWA and the backend.

2. **Authentication**
   - Implement Telegram native authentication.
   - Ensure no separate login is required and user data is securely passed from Telegram to the backend.

3. **Game Mode: Multiple Choice**
   - Build the UI for the multiple-choice game mode (thumb-friendly for mobile).
   - Implement the logic to serve questions and validate answers.

4. **Initial Content Integration**
   - Populate the database with 20 initial questions covering 2 topics (e.g., Arithmetic and Fractions).

5. **Progression System (XP Counter)**
   - Implement the logic to award XP for correct answers.
   - Build the UI to display the current XP and track progress.
