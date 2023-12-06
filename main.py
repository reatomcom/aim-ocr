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
    output_file = config.OUTPUT_DIR.joinpath(ocr_function.__name__).with_suffix(".txt")

    with output_file.open("w", encoding="utf-8") as f:
        for image_path in config.DATASET_DIR.iterdir():
            if not image_path.is_file():
                continue

            file_name = image_path.name
            title = "{0}\n{1}\n{0}".format("-" * len(str(file_name)), file_name)
            f.write(f"{title}\n{ocr_function(str(image_path))}\n\n")

        f.truncate(f.tell() - 2)


def main():
    process_dataset(run_pytesseract)
    process_dataset(run_easyocr)


if __name__ == "__main__":
    main()
