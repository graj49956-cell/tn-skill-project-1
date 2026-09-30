from pathlib import Path
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from .gemini_client import GeminiServiceError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import get_settings
from .schemas import (
    AnswerResponse, ExplanationResponse, QuizResponse,
    RecommendationResponse, SummaryResponse, TextRequest, TopicRequest,
)
from .services.explanation import explain_topic
from .services.learning_path import get_learning_recommendations
from .services.qna import answer_question_with_gemini
from .services.quiz import generate_quiz
from .services.summary import summarize_text

BASE_DIR = Path(__file__).resolve().parent.parent
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.exception_handler(GeminiServiceError)
async def gemini_error_handler(request: Request, exc: GeminiServiceError):
    return JSONResponse(status_code=503, content={"error": str(exc)})


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"app_name": settings.app_name}
    )

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "explanation_provider": settings.explanation_provider,
    }

@app.get("/qa", response_model=AnswerResponse)
def answer_question(question: str = Query(..., min_length=1, max_length=5000)):
    return {"answer": answer_question_with_gemini(question.strip())}

@app.post("/explain/", response_model=ExplanationResponse)
def explain_api(payload: TopicRequest):
    return {"topic": payload.topic, "explanation": explain_topic(payload.topic)}

@app.post("/summarize/", response_model=SummaryResponse)
def summarize_api(payload: TextRequest):
    return {"summary": summarize_text(payload.text)}

@app.post("/quiz", response_model=QuizResponse)
def quiz_api(payload: TextRequest):
    return {"quiz": generate_quiz(payload.text)}

@app.get("/learn/recommendations", response_model=RecommendationResponse)
def learning_recommendation_api(
    topic: str = Query(..., min_length=1, max_length=500),
):
    return {
        "topic": topic.strip(),
        "recommendation": get_learning_recommendations(topic.strip()),
    }
