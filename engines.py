import easyocr
import pytesseract


def run_pytesseract(image_path):
    return pytesseract.image_to_string(image_path, lang="eng+lav")


reader = easyocr.Reader(["en", "lv"], gpu=False, verbose=False)


def run_easyocr(image_path):
    return "\n".join(reader.readtext(image_path, detail=0))


