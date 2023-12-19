import easyocr
import pytesseract

OCRReturnType = list[tuple[str, tuple[int, int, int, int], float]]


def run_pytesseract(image_path: str) -> OCRReturnType:
    output = pytesseract.image_to_data(
        image_path, lang="eng+lav", output_type=pytesseract.Output.DICT
    )

    return [
        (
            text,
            (left, top, width, height),
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
    output = []
    for bbox, text, confidence in reader.readtext(image_path):
        if text.strip():
            continue

        tl, br = zip(*[(min(cmp), max(cmp)) for cmp in zip(*bbox)])
        dims = [cmp_max - cmp_min for cmp_min, cmp_max in zip(tl, br)]
        output.append((text, (*tl, *dims), confidence))

    return output
