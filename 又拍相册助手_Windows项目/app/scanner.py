from pathlib import Path
from .models import Album, IMAGE_EXT, VIDEO_EXT

def scan_root(root: str):
    root = Path(root)
    albums = []
    for d in sorted([p for p in root.iterdir() if p.is_dir()], key=lambda x: x.name.lower()):
        files = [p for p in d.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXT | VIDEO_EXT]
        if files:
            desc = ""
            desc_file = d / "描述.txt"
            if desc_file.exists():
                try: desc = desc_file.read_text("utf-8")
                except Exception: pass
            albums.append(Album(d, d.name, desc, files))
    return albums
