import pytesseract

from .utils import ScanData


class PyTesseract:
    def run(self, image_path: str) -> list[ScanData]:
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
