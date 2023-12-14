import json

import config
import engines

from rapidfuzz import fuzz


def process_dataset(ocr_function):
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = config.OUTPUT_DIR.joinpath(ocr_function.__name__).with_suffix(".json")

    output = {}
    for image_path in config.DATASET_DIR.iterdir():
        if not image_path.is_file():
            continue

        output[image_path.name] = ocr_function(str(image_path))

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(output, output_file, ensure_ascii=False, indent=4, sort_keys=True)


def process_ratio(ocr_function):
    original_path = config.OUTPUT_DIR.joinpath("original").with_suffix(".json")
    with open(original_path, 'r', encoding="utf-8") as original_file:
        original_texts = json.load(original_file)

    output_path = config.OUTPUT_DIR.joinpath(ocr_function.__name__ + "_accuracy").with_suffix(".json")
    output = {}
    for image_path in config.TEST_DIR.iterdir():
        if not image_path.is_file():
            continue

        recognition = ocr_function(str(image_path)).replace("\n", " ")
        ratio = fuzz.partial_token_sort_ratio(recognition, original_texts[image_path.name])
        output[image_path.name] = [recognition, ratio]
    
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(output, output_file, ensure_ascii=False, indent=4, sort_keys=True)
    

def main():
    process_ratio(engines.run_pytesseract)
    process_ratio(engines.run_easyocr)


if __name__ == "__main__":
    main()
