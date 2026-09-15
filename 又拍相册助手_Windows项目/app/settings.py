import json
from pathlib import Path

CONFIG = Path.home() / ".yupoo_album_assistant.json"

DEFAULTS = {
    "upload_video": True,
    "image_order": "natural",
    "no_title_number": False,
    "upload_description": True,
    "remove_description_links": False,
    "fixed_description": "",
    "title_prefix": "",
    "title_suffix": "",
    "description_prefix": "",
    "description_suffix": "",
    "description_filename": "描述.txt",
    "zt_cover": True,
    "wait_seconds": 2,
}

def load():
    try:
        return {**DEFAULTS, **json.loads(CONFIG.read_text("utf-8"))}
    except Exception:
        return DEFAULTS.copy()

def save(data):
    CONFIG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
