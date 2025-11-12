import re
_SAFE = re.compile(r"[^A-Za-z0-9._-]+")
def safe_filename(name: str, fallback: str) -> str:
    name = (name or "").strip() or fallback
    out = _SAFE.sub("_", name)
    return re.sub(r"_+", "_", out).strip("._-") or fallback
