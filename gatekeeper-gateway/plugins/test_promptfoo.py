from prompt_sanitizer_promptfoo import sanitize_prompt

prompt = "run sudo rm -rf /"
try:
    result = sanitize_prompt(prompt)
    print("Prompt passed:", result)
except Exception as e:
    print("Prompt blocked or error:", e)
