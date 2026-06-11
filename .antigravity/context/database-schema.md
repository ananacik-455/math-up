# MathUp MVP: Database Schema Contract

## Architecture Strategy
- **Database:** PostgreSQL
- **Pattern:** Hybrid Relational + Document (JSONB)
- **Primary Keys:** UUID v4
- **Timestamps:** All tables must include `created_at` and `updated_at`.

## Core Tables

### 1. `users`
Stores player identity and global progression. `grade_level` is ONLY a demographic label used for the initial placement test, not a boundary for their education plan.
* `id` (UUID, PK)
* `telegram_id` (BigInt, Unique)
* `grade_level` (Int) - Used to set initial assumptions.
* `total_xp` (Int, default 0)
* `current_streak` (Int, default 0)
* `last_active_date` (Date)
* `is_premium` (Boolean, default false)

### 2. `topics` (The Ordered Education Plan)
Forms the curriculum Skill Tree. Topics are unlocked sequentially based on prerequisite completion.
* `id` (UUID, PK)
* `name` (String) - e.g., "Fractions", "Linear Equations".
* `suggested_grade` (Int) - The curriculum standard (for UI mapping).
* `prerequisite_topic_ids` (Array of UUIDs, nullable) - Topics that must be mastered before this unlocks.
* `is_nmt_relevant` (Boolean) 

### 3. `questions` (Flexible Content)
Stores game data using JSONB to handle diverse formats (Multiple Choice, Anagrams, etc.).
* `id` (UUID, PK)
* `topic_id` (UUID, FK to topics.id)
* `game_type` (Enum: 'MULTIPLE_CHOICE', 'ANAGRAM', 'SPEED_MATCH')
* `baseline_elo` (Int) - Base difficulty of the question.
* `content` (JSONB) - UI and input data.
* `validation_rules` (JSONB) - Correct answer logic.

### 4. `user_topic_mastery` (The Actual Knowledge State)
The truth of what a student knows. Tracks unlocking and mastery independent of their age or start date.
* `user_id` (UUID, FK to users.id)
* `topic_id` (UUID, FK to topics.id)
* `status` (Enum: 'LOCKED', 'UNLOCKED', 'MASTERED') - Drives the education plan progression.
* `elo_rating` (Int, default 1000) 
* `accuracy_rate` (Float) 

### 5. `game_sessions` (Answer History)
Logs individual answers.
* `id` (UUID, PK)
* `user_id` (UUID, FK to users.id)
* `question_id` (UUID, FK to questions.id)
* `is_correct` (Boolean)
* `time_taken_ms` (Int)
* `awarded_xp` (Int)