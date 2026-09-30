from __future__ import annotations
from functools import lru_cache
from ..config import get_settings
from ..gemini_client import generate_text

@lru_cache
def _local_pipeline():
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    import torch
    settings = get_settings()
    tokenizer = AutoTokenizer.from_pretrained(settings.explanation_model)
    model = AutoModelForSeq2SeqLM.from_pretrained(settings.explanation_model)
    return tokenizer, model, torch

def _explain_with_local_model(topic: str) -> str:
    settings = get_settings()
    tokenizer, model, torch = _local_pipeline()
    input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
    inputs = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            **inputs, max_new_tokens=settings.local_max_new_tokens,
            temperature=settings.local_temperature, top_k=settings.local_top_k,
            top_p=settings.local_top_p, do_sample=True,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

def explain_topic(topic: str) -> str:
    settings = get_settings()
    if settings.explanation_provider.lower() == "local":
        try:
            return _explain_with_local_model(topic)
        except Exception:
            return generate_text(
                f"Explain the concept of '{topic}' in a simple and clear way for a school student.",
                system_instruction="You are EduGenie. Give a beginner-friendly explanation with one simple example.",
                temperature=0.4, max_output_tokens=900,
            )
    return generate_text(
        f"Explain the concept of '{topic}' in a simple and clear way for a school student.",
        system_instruction=(
            "You are EduGenie. Explain from first principles using simple language, "
            "short sections, and one example when helpful."
        ),
        temperature=0.4, max_output_tokens=900,
    )
