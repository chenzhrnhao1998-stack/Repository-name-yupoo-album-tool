from dataclasses import dataclass, field
from pathlib import Path

IMAGE_EXT = {".jpg",".jpeg",".png",".webp",".gif",".bmp",".tif",".tiff"}
VIDEO_EXT = {".mp4",".mov",".m4v",".avi",".webm",".mkv"}

@dataclass
class Album:
    source: Path
    title: str
    description: str = ""
    files: list[Path] = field(default_factory=list)

    @property
    def images(self):
        return [p for p in self.files if p.suffix.lower() in IMAGE_EXT]

    @property
    def videos(self):
        return [p for p in self.files if p.suffix.lower() in VIDEO_EXT]

    @property
    def cover(self):
        for p in self.images:
            if "ZT" in p.stem.upper():
                return p
        return self.images[0] if self.images else None
