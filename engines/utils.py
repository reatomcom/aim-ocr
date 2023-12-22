from typing import Protocol
from dataclasses import dataclass


@dataclass
class ScanData:
    text: str
    left: int
    top: int
    width: int
    height: int
    conf: float

    def __post_init__(self):
        self.text = self.text.strip()
        self.conf = round(self.conf, 3)


class OCREngine(Protocol):
    def run(self, image_path: str) -> list[ScanData]:
        ...
