import json
from collections.abc import Callable

import config
import engines


def process_dataset(ocr_function: Callable[[str], engines.OCRReturnType]):
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = config.OUTPUT_DIR.joinpath(ocr_function.__name__).with_suffix(".json")

    output = {}
    for image_path in sorted(config.DATASET_DIR.iterdir()):
        if not image_path.is_file():
            continue

        output[image_path.name] = ocr_function(str(image_path))

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(output, output_file, ensure_ascii=False)


def main():
    process_dataset(engines.run_pytesseract)
    process_dataset(engines.run_easyocr)


if __name__ == "__main__":
    main()
