from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid

import models
from database import engine, get_db, AsyncSessionLocal
from auth import validate_telegram_data
from pydantic import BaseModel

app = FastAPI(title="MathUp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow local frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

class LoginRequest(BaseModel):
    initData: str

@app.post("/api/auth/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    user_data = validate_telegram_data(req.initData)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Telegram data")
    
    telegram_id = user_data["id"]
    stmt = select(models.User).where(models.User.telegram_id == telegram_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        user = models.User(telegram_id=telegram_id, first_name=user_data.get("first_name"), username=user_data.get("username"))
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    return {"token": "mock_jwt_token", "user": {"id": str(user.id), "telegram_id": user.telegram_id, "first_name": user.first_name, "xp": user.total_xp}}

class AnswerRequest(BaseModel):
    question_id: uuid.UUID
    selected_option: str

async def get_current_user(authorization: str = Header(None), db: AsyncSession = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    init_data = authorization.split("Bearer ")[1]
    user_data = validate_telegram_data(init_data)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Telegram data")
        
    telegram_id = user_data["id"]
    stmt = select(models.User).where(models.User.telegram_id == telegram_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

@app.get("/api/questions")
async def get_questions(db: AsyncSession = Depends(get_db)):
    # Returns random questions for MVP
    stmt = select(models.Question).limit(5)
    result = await db.execute(stmt)
    questions = result.scalars().all()
    # Serve JSON content
    return [{"id": str(q.id), "text": q.content.get("text", ""), "options": q.content.get("options", {})} for q in questions]

@app.post("/api/answer")
async def submit_answer(req: AnswerRequest, current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Validate answer
    stmt = select(models.Question).where(models.Question.id == req.question_id)
    result = await db.execute(stmt)
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    is_correct = (question.validation_rules.get("correct_option") == req.selected_option)
    
    awarded_xp = 10 if is_correct else 0
    if is_correct:
        current_user.total_xp += awarded_xp
        
    session_log = models.GameSession(
        user_id=current_user.id,
        question_id=question.id,
        is_correct=is_correct,
        awarded_xp=awarded_xp,
        time_taken_ms=0
    )
    db.add(session_log)
    
    await db.commit()
    await db.refresh(current_user)
        
    return {"correct": is_correct, "correct_option": question.validation_rules.get("correct_option"), "new_xp": current_user.total_xp}
