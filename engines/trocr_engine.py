from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

from .utils import ScanData


class TrOCR:
    def __init__(self):
        hub_id = "microsoft/trocr-large-printed"
        self.processor = TrOCRProcessor.from_pretrained(hub_id)
        self.model = VisionEncoderDecoderModel.from_pretrained(hub_id)

    def run(self, image_path: str) -> list[ScanData]:
        # todo: TrOCR is a recognition model,
        # so a separate detection model needs to be used

        # cut, process and generate ids for each bbox
        # then concatenate and batch decode
        image = Image.open(image_path).convert("RGB")

        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
        ids = self.model.generate(pixel_values)
        text = self.processor.batch_decode(ids, skip_special_tokens=True)[0]

        return [ScanData(text, 0, 0, 0, 0, 100)]
