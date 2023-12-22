import json
import dataclasses
from collections.abc import Callable

import config
import engines

from rapidfuzz import fuzz

class DataClassEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        return super().default(o)


def process_dataset(*ocr_types: type[engines.OCREngine]):
    image_paths = sorted(p for p in config.DATASET_DIR.iterdir() if p.is_file())
    output = {p.name: {} for p in image_paths}

    for ocr_type in ocr_types:
        ocr_instance = ocr_type()
        ocr_name = ocr_type.__name__.lower()

        for image_path in image_paths:
            output[image_path.name][ocr_name] = {
                "accuracy": None,
                "runtime": None,
                "bboxes": [sd for sd in ocr_instance.run(str(image_path)) if sd.text],
            }

    return output


def main():
    output = process_dataset(engines.PyTesseract, engines.EasyOCR)

    config.OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with config.OUTPUT_FILE.open("w", encoding="utf-8") as output_file:
        json.dump(output, output_file, ensure_ascii=False, cls=DataClassEncoder)


if __name__ == "__main__":
    main()
