from pathlib import Path

import easyocr
import pytesseract

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

def run_pytesseract(image_path):
    return pytesseract.image_to_string(image_path, lang="eng+lav")


reader = easyocr.Reader(["en", "lv"], gpu=False, verbose=False)


def run_easyocr(image_path):
    return "\n".join(reader.readtext(image_path, detail=0))


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
