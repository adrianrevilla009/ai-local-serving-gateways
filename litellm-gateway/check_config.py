"""Validate config.yaml offline: aliases, fallbacks, cache and that no real key is committed. Needs PyYAML."""
import pathlib
import sys

import yaml

cfg = yaml.safe_load(pathlib.Path(__file__).with_name("config.yaml").read_text())
errors = []

aliases = {}
for m in cfg["model_list"]:
    aliases.setdefault(m["model_name"], []).append(m["litellm_params"])
    if "api_base" not in m["litellm_params"]:
        errors.append(f"{m['model_name']}: backend without api_base")

if len(aliases.get("chat", [])) < 2:
    errors.append("alias 'chat' needs at least two backends to load-balance")

for rule in cfg["router_settings"].get("fallbacks", []):
    for src, targets in rule.items():
        for name in [src, *targets]:
            if name not in aliases:
                errors.append(f"fallback references unknown alias {name}")
        if src in targets:
            errors.append(f"{src} falls back to itself")

if not cfg["litellm_settings"].get("cache"):
    errors.append("cache disabled")

for m in cfg["model_list"]:
    key = str(m["litellm_params"].get("api_key", ""))
    if key and key != "none" and not key.startswith("os.environ/"):
        errors.append("api_key must be 'none' or os.environ/<VAR>")

if errors:
    sys.exit("FAIL: " + "; ".join(errors))
print(f"ok: {len(aliases)} aliases, {len(cfg['model_list'])} backends, fallback and cache configured")
