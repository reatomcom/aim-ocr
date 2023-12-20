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
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = config.OUTPUT_DIR.joinpath("output").with_suffix(".json")

    output = {}
    for image_path in sorted(config.DATASET_DIR.iterdir()):
        if not image_path.is_file():
            continue

        output[image_path.name] = {
            ocr_func.__name__: ocr_func(str(image_path)) for ocr_func in ocr_funcs
        }

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(output, output_file, ensure_ascii=False, cls=DataClassEncoder)


def main():
    process_dataset(engines.run_pytesseract, engines.run_easyocr)


if __name__ == "__main__":
    main()
