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


def process_dataset(*ocr_funcs: Callable[[str], list[engines.ScanData]]):
    output = {}
    for image_path in sorted(config.DATASET_DIR.iterdir()):
        if not image_path.is_file():
            continue

        output[image_path.name] = {
            ocr_func.__name__: ocr_func(str(image_path)) for ocr_func in ocr_funcs
        }

    return output


def process_ratio(ocr_function):
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    original_path = config.OUTPUT_DIR.joinpath("original").with_suffix(".json")
    with open(original_path, 'r', encoding="utf-8") as original_file:
        original_texts = json.load(original_file)

    output_path = config.OUTPUT_DIR.joinpath(ocr_function.__name__ + "_accuracy").with_suffix(".json")
    output = {}
    for image_path in config.OUTPUT_DIR.iterdir():
        if not image_path.is_file():
            continue

        recognition = ocr_function(str(image_path))
        if isinstance(recognition, list):
            recognition = " ".join([item['text'] for item in recognition])
        else:
            recognition = recognition.replace("\n", " ")
        ratio = fuzz.partial_token_sort_ratio(recognition, original_texts[image_path.name])
        output[image_path.name] = [recognition, ratio]
    
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(output, output_file, ensure_ascii=False, indent=4, sort_keys=True)
    

def main():
    output = process_dataset(engines.run_pytesseract, engines.run_easyocr, engines.run_doctr)

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = config.OUTPUT_DIR.joinpath("output").with_suffix(".json")

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(output, output_file, ensure_ascii=False, cls=DataClassEncoder, indent=4)


if __name__ == "__main__":
    main()
