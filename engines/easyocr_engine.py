import easyocr

from .utils import ScanData


class EasyOCR:
    def __init__(self):
        self.reader = easyocr.Reader(["en", "lv"], gpu=False, verbose=False)

    def run(self, image_path: str) -> list[ScanData]:
        output = []
        for bbox, text, confidence in self.reader.readtext(image_path):
            tl, br = zip(*[map(round, (min(cmp), max(cmp))) for cmp in zip(*bbox)])
            dims = [cmp_max - cmp_min for cmp_min, cmp_max in zip(tl, br)]
            output.append(ScanData(text, *tl, *dims, float(confidence) * 100))

        return output
