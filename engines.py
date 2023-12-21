from dataclasses import dataclass
<<<<<<< HEAD
from pathlib import Path
=======
>>>>>>> main

import easyocr
import pytesseract

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

@dataclass
class BBox:
    left: int
    top: int
    width: int
    height: int


@dataclass
class ScanData:
    text: str
    bbox: BBox = None
    conf: float = 1

    def __post_init__(self):
        self.conf = round(self.conf, 5)


def run_pytesseract(image_path: str) -> list[ScanData]:
    output = pytesseract.image_to_data(
        image_path, lang="eng+lav", output_type=pytesseract.Output.DICT
    )

    return [
        ScanData(text, BBox(left, top, width, height), confidence / 100)
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


def run_easyocr(image_path: str) -> list[ScanData]:
    output = []
    for bbox, text, confidence in reader.readtext(image_path):
        if not text.strip():
            continue

        tl, br = zip(*[map(round, (min(cmp), max(cmp))) for cmp in zip(*bbox)])
        dims = [cmp_max - cmp_min for cmp_min, cmp_max in zip(tl, br)]
        output.append(ScanData(text, BBox(*tl, *dims), float(confidence)))

    return output
<<<<<<< HEAD


def run_doctr(image_path):
    image_path = Path(image_path)
    model = ocr_predictor(det_arch = 'db_resnet50', reco_arch = 'crnn_vgg16_bn', pretrained = True, detect_language = True)

    output = {}

    output[image_path.name] = []
    page = model(DocumentFile.from_images(image_path)).export()['pages'][0]
    pw, ph = reversed(page['dimensions'])
    for block in page['blocks']:
        for line in block['lines']:
            for word in line['words']:
                bbox = (ag := [[round(y*ph), round(x*pw)] for x, y in word['geometry']])[0] + [(y - x) for x, y in zip(*ag)]
                output[image_path.name].append({
                    'text': word['value'],
                    'top': bbox[0],
                    'left': bbox[1],
                    'width': bbox[2],
                    'height': bbox[3],
                    'conf': round(word['confidence']*100, 3)
                })
    return output[image_path.name]
=======
>>>>>>> main
