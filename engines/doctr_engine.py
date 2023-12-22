from doctr.models import ocr_predictor
from doctr.io import DocumentFile

from .utils import ScanData

class DocTR:
    def run(self, image_path: str) -> list[ScanData]:
        model = ocr_predictor(det_arch = 'db_resnet50', reco_arch = 'crnn_vgg16_bn', pretrained = True, detect_language = True)

        output = []

        page = model(DocumentFile.from_images(image_path)).export()['pages'][0]
        pw, ph = reversed(page['dimensions'])
        for block in page['blocks']:
            for line in block['lines']:
                for word in line['words']:
                    bbox = (ag := [[round(y*ph), round(x*pw)] for x, y in word['geometry']])[0] + [(y - x) for x, y in zip(*ag)]
                    text = word['value']
                    top = bbox[0]
                    left = bbox[1]
                    width = bbox[2]
                    height = bbox[3]
                    conf = round(word['confidence']*100, 3)
                    output.append(ScanData(text, top, left, width, height, conf))
        return output