from dataclasses import dataclass

import easyocr
import pytesseract


@dataclass
class ScanData:
    text: str
    left: int
    top: int
    width: int
    height: int
    conf: float

    def __post_init__(self):
        self.text = self.text.strip()
        self.conf = round(self.conf, 3)


def run_pytesseract(image_path: str) -> list[ScanData]:
    output = pytesseract.image_to_data(
        image_path, lang="eng+lav", output_type=pytesseract.Output.DICT
    )

    return [
        ScanData(*data)
        for data in zip(
            output["text"],
            output["left"],
            output["top"],
            output["width"],
            output["height"],
            output["conf"],
        )
    ]


reader = easyocr.Reader(["en", "lv"], gpu=False, verbose=False)


def run_easyocr(image_path: str) -> list[ScanData]:
    output = []
    for bbox, text, confidence in reader.readtext(image_path):
        tl, br = zip(*[map(round, (min(cmp), max(cmp))) for cmp in zip(*bbox)])
        dims = [cmp_max - cmp_min for cmp_min, cmp_max in zip(tl, br)]
        output.append(ScanData(text, *tl, *dims, float(confidence) * 100))

    return output
