import json

import easyocr
import pytesseract

import config


def run_pytesseract(image_path):
    return pytesseract.image_to_string(image_path, lang="eng+lav")


reader = easyocr.Reader(["en", "lv"], gpu=False, verbose=False)


def run_easyocr(image_path):
    return "\n".join(reader.readtext(image_path, detail=0))


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


def main():
    process_dataset(run_pytesseract)
    process_dataset(run_easyocr)


if __name__ == "__main__":
    main()
