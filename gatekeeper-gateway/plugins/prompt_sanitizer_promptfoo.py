
from fastapi import HTTPException
from typing import Optional
from plugins.policy_engine_loader import load_policy_engine

policy_engine = load_policy_engine()

def sanitize_prompt(prompt: str, context: Optional[dict] = None) -> str:
    # Simulate Promptfoo logic
    injection = "disregard previous instructions" in prompt.lower()
    context = context or {}
    action = "sanitize"
    resource = "prompt_promptfoo"
    if injection:
        decision = policy_engine.evaluate(context, action, resource, prompt=prompt, injection=True)
        if not decision["allow"]:
            raise HTTPException(400, f"Blocked by policy: {decision['reason']}")
    return prompt
