# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI-based AI learning assistant based on the supplied project documentation.

## Modules

1. **Q&A** — asks Gemini a student question.
2. **Explanation** — explains a topic in simple language. The supplied documentation used `MBZUAI/LaMini-Flan-T5-783M`; this implementation supports that local model and also provides a Gemini provider for easier installation.
3. **Summarization** — summarizes pasted study text.
4. **Quiz Generation** — generates exactly 3 MCQs with 4 options each and validates the answer.
5. **Learning Recommendations** — creates a beginner/intermediate/advanced learning path.

## Structure

```text
EduGenie/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── gemini_client.py
│   └── services/
│       ├── qna.py
│       ├── explanation.py
│       ├── summary.py
│       ├── quiz.py
│       └── learning_path.py
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
├── scripts/
├── .env.example
├── requirements.txt
└── requirements-local.txt
```

## Windows + VS Code

Open the project folder in VS Code and create a PowerShell terminal.

### 1. Create the virtual environment

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the environment executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

### 2. Install packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=your_key_here
```

You can change `GEMINI_MODEL` if a different model is available to your API key.

### 4. Run

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000` — application
- `http://127.0.0.1:8000/docs` — Swagger API documentation
- `http://127.0.0.1:8000/health` — health check

### 5. Test

The automated tests mock AI calls, so they do not consume Gemini quota:

```powershell
pytest -q
```

Static Python/config validation:

```powershell
python scripts/check_project.py
```

## Optional local LaMini explanation model

The original supplied implementation uses `MBZUAI/LaMini-Flan-T5-783M`.

Install:

```powershell
pip install -r requirements-local.txt
```

Then set:

```text
EXPLANATION_PROVIDER=local
```

The model is lazy-loaded and downloaded from Hugging Face on first use. If it cannot load, EduGenie falls back to Gemini for that request.

For the simplest setup, leave:

```text
EXPLANATION_PROVIDER=gemini
```

## API contract

### Q&A

```text
GET /qa?question=Which%20is%20the%20largest%20ocean?
```

### Explanation

```http
POST /explain/
Content-Type: application/json

{"topic":"Binary Search Algorithm"}
```

### Summary

```http
POST /summarize/
Content-Type: application/json

{"text":"Your study paragraph..."}
```

### Quiz

```http
POST /quiz
Content-Type: application/json

{"text":"Your study passage..."}
```

Returns exactly 3 questions, each with 4 options.

### Learning recommendations

```text
GET /learn/recommendations?topic=SQL
```

## Troubleshooting

**`GEMINI_API_KEY is not configured`**  
Check `.env`, then restart Uvicorn.

**Model unavailable / quota / 503**  
Set `GEMINI_MODEL` to another model available to your account. The model is configurable rather than hard-coded.

**PowerShell activation error**

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**Port in use**

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

## Implementation note

The supplied documentation shows an earlier implementation using the legacy `google.generativeai` package and `gemini-1.5-pro`. This project preserves the documented user-facing modules and endpoint design while using the current `google-genai` SDK and Gemini Interactions API, structured output for quiz generation, Pydantic validation, lazy local-model loading, and testable service modules.
