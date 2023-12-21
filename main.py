import json
import dataclasses
from collections.abc import Callable

import config
import engines


class DataClassEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        return super().default(o)


def process_dataset(*ocr_funcs: Callable[[str], list[engines.ScanData]]):
    image_paths = sorted(p for p in config.DATASET_DIR.iterdir() if p.is_file())
    output = {p.name: {} for p in image_paths}

    for ocr_func in ocr_funcs:
        for image_path in image_paths:
            output[image_path.name][ocr_func.__name__] = [
                sd for sd in ocr_func(str(image_path)) if sd.text
            ]

    return output


def main():
    output = process_dataset(engines.run_pytesseract, engines.run_easyocr)

    config.OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with config.OUTPUT_FILE.open("w", encoding="utf-8") as output_file:
        json.dump(output, output_file, ensure_ascii=False, cls=DataClassEncoder)


if __name__ == "__main__":
    main()
