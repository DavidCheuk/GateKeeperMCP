import subprocess
import tempfile
import json
import os
from fastapi import HTTPException

PROMPTFOO_SUITE_PATH = os.environ.get("PROMPTFOO_SUITE_PATH", "./plugins/promptfoo_safety_suite.yml")

def sanitize_prompt(prompt: str) -> str:
    # Write prompt to temp file
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False) as pf:
        pf.write(prompt)
        pf.flush()
        prompt_path = pf.name

    try:
        # Call promptfoo and capture JSON output only
        with tempfile.NamedTemporaryFile("r+", suffix=".json", delete=False) as outf:
            output_path = outf.name

        result = subprocess.run(
            [
                "promptfoo", "eval",
                "--prompts", prompt_path,
                "--config", PROMPTFOO_SUITE_PATH,
                "--output", output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        os.unlink(prompt_path)

        # Debug: Print raw promptfoo output and error
        print("----- promptfoo STDOUT -----")
        print(result.stdout.decode())
        print("----- promptfoo STDERR -----")
        print(result.stderr.decode())
        print("----- End promptfoo output -----")

        # Try reading the output file
        try:
            with open(output_path, "r") as f:
                content = f.read()
            os.unlink(output_path)
        except Exception as e:
            print("Could not read promptfoo output file:", e)
            raise HTTPException(400, f"promptfoo sanitizer error: Could not read output file: {e}")

        # Debug: Print raw content of output file
        print("----- promptfoo OUTPUT FILE CONTENT -----")
        print(content)
        print("----- End promptfoo output file -----")

        try:
            output_json = json.loads(content)
        except Exception as jsonerr:
            # Show the exact content that failed JSON parsing
            raise HTTPException(400, f"promptfoo sanitizer error: output not valid JSON:\n{content}\n\nJSON Error: {jsonerr}")

        # Walk through results and block on any failed assertion
        results = output_json.get("results", [])
        if not isinstance(results, list):
            raise HTTPException(400, f"promptfoo sanitizer error: output 'results' is not a list: {type(results)} {results}")

        for res in results:
            assertion_results = res.get("assertionResults") or res.get("results", [])
            for check in assertion_results:
                if not check.get("pass", True):
                    raise HTTPException(400, f"Prompt blocked by promptfoo: {check.get('error') or check.get('message') or check}")

        return prompt
    except Exception as e:
        # Show the last error, which should now include more info
        raise HTTPException(400, f"promptfoo sanitizer error: {str(e)}")
