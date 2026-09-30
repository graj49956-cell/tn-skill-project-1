from fastapi.testclient import TestClient
from app.main import app
from app.services import qna, summary, explanation, quiz, learning_path
import app.main as main

client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_qna(monkeypatch):
    monkeypatch.setattr(main, "answer_question_with_gemini", lambda q: "Test answer")
    response = client.get("/qa", params={"question": "What is AI?"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Test answer"}

def test_explain(monkeypatch):
    monkeypatch.setattr(main, "explain_topic", lambda topic: "Simple explanation")
    response = client.post("/explain/", json={"topic": "Photosynthesis"})
    assert response.status_code == 200
    assert response.json()["topic"] == "Photosynthesis"

def test_summary(monkeypatch):
    monkeypatch.setattr(main, "summarize_text", lambda text: "Short summary")
    response = client.post("/summarize/", json={"text": "Long text"})
    assert response.status_code == 200
    assert response.json() == {"summary": "Short summary"}

def test_quiz(monkeypatch):
    monkeypatch.setattr(main, "generate_quiz", lambda text: [
        {"question":"Q1","options":["A","B","C","D"],"answer":"A"},
        {"question":"Q2","options":["A","B","C","D"],"answer":"B"},
        {"question":"Q3","options":["A","B","C","D"],"answer":"C"},
    ])
    response = client.post("/quiz", json={"text": "Study passage"})
    assert response.status_code == 200
    assert len(response.json()["quiz"]) == 3

def test_recommendations(monkeypatch):
    monkeypatch.setattr(main, "get_learning_recommendations", lambda topic: "Learning path")
    response = client.get("/learn/recommendations", params={"topic": "SQL"})
    assert response.status_code == 200
    assert response.json()["topic"] == "SQL"
