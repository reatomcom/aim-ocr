from doctr.io import Document, DocumentFile
from doctr.models import ocr_predictor

from .utils import ScanData


class DocTR:
    def __init__(self):
        self.model = ocr_predictor(pretrained=True)

    def run(self, image_path: str) -> list[ScanData]:
        doc: Document = self.model(DocumentFile.from_images(image_path))

        output = []
        for page in doc.pages:
            ph, pw = page.dimensions
            for block in page.blocks:
                for line in block.lines:
                    for word in line.words:
                        (xmin, ymin), (xmax, ymax) = [
                            (round(x * pw), round(y * ph)) for x, y in word.geometry
                        ]

                        output.append(
                            ScanData(
                                word.value,
                                xmin,
                                ymin,
                                xmax - xmin,
                                ymax - ymin,
                                word.confidence * 100,
                            )
                        )

        return output
