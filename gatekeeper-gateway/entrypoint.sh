#!/bin/bash
echo "DEBUG: PATH at runtime is $PATH"
echo "DEBUG: promptfoo version:"
which promptfoo
promptfoo --version
exec uvicorn main:app --host 0.0.0.0 --port 8080
