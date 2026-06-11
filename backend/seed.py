import asyncio
from database import AsyncSessionLocal, engine
import models
import uuid

async def seed_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
        
    async with AsyncSessionLocal() as db:
        # Create user
        user = models.User(
            telegram_id=123456789, 
            first_name="Test", 
            username="testuser", 
            total_xp=0, 
            grade_level=5
        )
        db.add(user)
        
        # Create topics
        topic1 = models.Topic(
            name="Arithmetic", 
            suggested_grade=4, 
            is_nmt_relevant=True, 
            prerequisite_topic_ids=[]
        )
        topic2 = models.Topic(
            name="Fractions", 
            suggested_grade=5, 
            is_nmt_relevant=True, 
            prerequisite_topic_ids=[]
        )
        db.add_all([topic1, topic2])
        await db.flush() # Flush to get UUIDs
        
        # Create user mastery
        mastery1 = models.UserTopicMastery(
            user_id=user.id, 
            topic_id=topic1.id, 
            status=models.MasteryStatus.UNLOCKED
        )
        mastery2 = models.UserTopicMastery(
            user_id=user.id, 
            topic_id=topic2.id, 
            status=models.MasteryStatus.LOCKED
        )
        db.add_all([mastery1, mastery2])
        
        # Create questions
        questions = [
            models.Question(
                topic_id=topic1.id, 
                game_type=models.GameType.MULTIPLE_CHOICE,
                baseline_elo=1000,
                content={"text": "What is 15 + 27?", "options": {"A": "42", "B": "32", "C": "45", "D": "52"}}, 
                validation_rules={"correct_option": "A"}
            ),
            models.Question(
                topic_id=topic1.id, 
                game_type=models.GameType.MULTIPLE_CHOICE,
                baseline_elo=1000,
                content={"text": "What is 8 x 7?", "options": {"A": "54", "B": "56", "C": "64", "D": "48"}}, 
                validation_rules={"correct_option": "B"}
            ),
            models.Question(
                topic_id=topic2.id, 
                game_type=models.GameType.MULTIPLE_CHOICE,
                baseline_elo=1100,
                content={"text": "What is 1/2 + 1/4?", "options": {"A": "3/4", "B": "2/6", "C": "2/4", "D": "1/8"}}, 
                validation_rules={"correct_option": "A"}
            ),
            models.Question(
                topic_id=topic2.id, 
                game_type=models.GameType.MULTIPLE_CHOICE,
                baseline_elo=1150,
                content={"text": "What is 3/4 - 1/4?", "options": {"A": "1/2", "B": "1/4", "C": "2/8", "D": "1/3"}}, 
                validation_rules={"correct_option": "A"}
            ),
            models.Question(
                topic_id=topic1.id, 
                game_type=models.GameType.MULTIPLE_CHOICE,
                baseline_elo=1050,
                content={"text": "What is 144 / 12?", "options": {"A": "10", "B": "11", "C": "12", "D": "14"}}, 
                validation_rules={"correct_option": "C"}
            ),
        ]
        db.add_all(questions)
        await db.commit()
        print("Database seeded with new schema structure!")

if __name__ == "__main__":
    asyncio.run(seed_db())
