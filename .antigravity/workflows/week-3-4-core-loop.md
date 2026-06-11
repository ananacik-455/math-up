# Workflow: Week 3-4 Core Loop Implementation

## Objective
Implement adaptive difficulty tracking, streak state management, a progress dashboard in the React TWA, and seed the full content library for arithmetic and algebra.

## Standard Operating Procedure (SOP)

1. **Backend: Adaptive Matchmaking API**
   - Implement the mathematical Elo equations defined in `roles/game-director.md` inside a FastAPI service layer.
   - Update `user_topic_mastery` after every submission in the `game_sessions` table.
   - Create a smart route `/api/questions/next` that serves a custom-tailored question based on the user's current Elo.

2. **Backend: Streak Worker**
   - Implement the calendar-day check logic to safely increment or reset user streaks upon daily interaction.

3. **Frontend: Progress Dashboard UI**
   - Design a student dashboard using the Telegram UI Kit.
   - Display: Total XP, Current Streak counter (with a flame icon), and a visual Skill Tree showing locked/unlocked topics based on curriculum constraints.

4. **Database Seeding**
   - Expand the PostgreSQL questions database with 60 additional questions spanning all topics across Arithmetic, Fractions, and initial Algebra concepts.