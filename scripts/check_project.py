from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
for path in ROOT.rglob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"))
    print("OK", path.relative_to(ROOT))

required = [
    "app/main.py","app/config.py","app/schemas.py","app/gemini_client.py",
    "app/services/qna.py","app/services/explanation.py","app/services/summary.py",
    "app/services/quiz.py","app/services/learning_path.py",
    "templates/index.html","static/app.js","static/style.css",
    "requirements.txt",".env.example"
]
for item in required:
    assert (ROOT/item).exists(), item
print("All required files exist.")
