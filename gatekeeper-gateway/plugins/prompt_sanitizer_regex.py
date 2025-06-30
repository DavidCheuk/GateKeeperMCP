import re
from fastapi import HTTPException

BLOCKLIST = [r"ignore previous", r"system prompt:", r"sudo", r"simulate", r"delete all"]

def sanitize_prompt(prompt: str) -> str:
    for pattern in BLOCKLIST:
        if re.search(pattern, prompt, re.IGNORECASE):
            raise HTTPException(400, f"Prompt blocked by regex blocklist: pattern '{pattern}' found")
    return prompt
