from presidio_analyzer import AnalyzerEngine
from fastapi import HTTPException

analyzer = AnalyzerEngine()

def sanitize_prompt(prompt: str) -> str:
    results = analyzer.analyze(text=prompt, language="en")
    if results:
        raise HTTPException(400, f"Prompt blocked by PII detection: {results}")
    return prompt
