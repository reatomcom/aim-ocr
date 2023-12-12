import easyocr
import pytesseract

OCRReturnType = list[tuple[str, list[tuple[int, int]], float]]


def run_pytesseract(image_path: str) -> OCRReturnType:
    output = pytesseract.image_to_data(
        image_path, lang="eng+lav", output_type=pytesseract.Output.DICT
    )

    return [
        (
            text,
            [
                (left, top),
                (left + width, top),
                (left + width, top + height),
                (left, top + height),
            ],
            confidence / 100,
        )
        for text, left, top, width, height, confidence in zip(
            output["text"],
            output["left"],
            output["top"],
            output["width"],
            output["height"],
            output["conf"],
        )
        if text.strip()
    ]


reader = easyocr.Reader(["en", "lv"], gpu=False, verbose=False)


def run_easyocr(image_path: str) -> OCRReturnType:
    return [
        (text, [(int(x), int(y)) for x, y in bbox], confidence)
        for bbox, text, confidence in reader.readtext(image_path)
        if text.strip()
    ]
