import importlib.util
import glob
from fastapi import HTTPException

def run_prompt_sanitizer_chain(prompt: str, context: dict = None) -> str:
    plugins = sorted(glob.glob("./plugins/prompt_sanitizer_*.py"))
    for plugin_path in plugins:
        mod_name = plugin_path.split('/')[-1][:-3]
        spec = importlib.util.spec_from_file_location(mod_name, plugin_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "sanitize_prompt"):
            prompt = mod.sanitize_prompt(prompt, context=context)
    return prompt
