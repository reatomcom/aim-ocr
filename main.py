import config


def run_pytesseract(image_path):
    import pytesseract

    return pytesseract.image_to_string(str(image_path))


def process_dataset(ocr_function):
    root = config.DATASET_DIR
    images = [x for x in root.iterdir() if x.is_file()]

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = config.OUTPUT_DIR.joinpath(ocr_function.__name__).with_suffix(".txt")

    with output_file.open("w", encoding="utf-8") as f:
        for image in images:
            f.write(f"{image}\n{ocr_function(root.joinpath(image))}\n\n")


def main():
    process_dataset(run_pytesseract)


if __name__ == "__main__":
    main()
