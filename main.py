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
    output = {}
    for ocr_func in ocr_funcs:
        for image_path in sorted(config.DATASET_DIR.iterdir()):
            if not image_path.is_file():
                continue

            if image_path.name not in output:
                output[image_path.name] = {}

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
