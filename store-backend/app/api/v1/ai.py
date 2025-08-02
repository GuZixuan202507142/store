from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from app.core.config import settings

router = APIRouter()

class AIChatRequest(BaseModel):
    prompt: str

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@router.post("/chat")
async def chat_with_ai(request: AIChatRequest):
    try:
        response = model.generate_content(request.prompt)
        return {"message": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
