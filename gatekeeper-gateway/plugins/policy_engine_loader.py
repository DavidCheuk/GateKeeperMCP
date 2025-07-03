import sys
import os
import importlib.util

policy_engines_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'policy_engines'))
opa_plugin_path = os.path.join(policy_engines_dir, 'opa_plugin.py')

if not os.path.exists(opa_plugin_path):
    raise ImportError(f"opa_plugin.py not found at {opa_plugin_path}")

spec = importlib.util.spec_from_file_location("opa_plugin", opa_plugin_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load spec for opa_plugin.py at {opa_plugin_path}")

opa_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(opa_module)
OPAPlugin = opa_module.OPAPlugin

# This loader can be extended to support multiple backends in the future
def load_policy_engine():
    opa_url = os.getenv("OPA_URL", "http://opa:8181/v1/data/enterprise/policy")
    return OPAPlugin(opa_url)
