from SimpleCV import *


class BaseCard(object):
    def __init__(self):
        self.fields = {}
        self.card = None

    def get_text(self, card, label, x, y, w, h):
        field = card.crop(x=x, y=y, w=w, h=h)
        field = field.grayscale() * 1.2 # Convert to grayscale and increase brightness
        field_text = field.readText().strip().split("\n")[0] # Run tesseract OCR and cleanup result
        self.fields[label] = field_text

    def get_signature(self, card, x, y, w, h):
        field = card.crop(x=x, y=y, w=w, h=h)
        field = field.grayscale().binarize().invert()

    def get_photo(self, card, x, y, w, h):
        field = card.crop(x=x, y=y, w=w, h=h)
