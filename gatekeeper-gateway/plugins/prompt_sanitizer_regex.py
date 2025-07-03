
import re
from fastapi import HTTPException
from typing import Optional
from plugins.policy_engine_loader import load_policy_engine

policy_engine = load_policy_engine()

DANGEROUS_PATTERNS = [
    r"(?i)drop\s+table",
    r"(?i)disregard.*instructions"
]

def sanitize_prompt(prompt: str, context: Optional[dict] = None) -> str:
    context = context or {}
    action = "sanitize"
    resource = "prompt_regex"
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, prompt):
            decision = policy_engine.evaluate(context, action, resource, prompt=prompt, pattern=pattern)
            if not decision["allow"]:
                raise HTTPException(400, f"Blocked by policy: {decision['reason']}")
    return prompt
