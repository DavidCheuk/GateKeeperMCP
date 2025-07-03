
from presidio_analyzer import AnalyzerEngine
from fastapi import HTTPException
from plugins.policy_engine_loader import load_policy_engine

analyzer = AnalyzerEngine()
policy_engine = load_policy_engine()

def sanitize_prompt(prompt: str, context: dict = None) -> str:
    results = analyzer.analyze(text=prompt, language="en")
    context = context or {}
    action = "sanitize"
    resource = "prompt_pii"
    if results:
        decision = policy_engine.evaluate(context, action, resource, prompt=prompt, pii_results=str(results))
        if not decision["allow"]:
            raise HTTPException(400, f"Blocked by policy: {decision['reason']}")
    return prompt
