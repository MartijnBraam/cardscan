from SimpleCV import *
from card.base import BaseCard
from time import strptime


class drivinglicence(BaseCard):
    def __init__(self, debug):
        self.card_aspect = 0.6272189349112426
        self.feature_angle = 93.1681203756
        self.name = 'Dutch driving licence'
        self.data_directory = 'data/nl/government/drivinglicence'
        self.dn = 'nl.government.drivinglicence'
        super(drivinglicence, self).__init__(debug)

    def match(self, input_image):
        template = Image(self.data_directory + "/template.png")
        res = input_image.findTemplate(template_image=template, threshold=3)
        if res:
            width = template.width
            height = template.width * self.card_aspect
            card = input_image.crop(x=res.x()[0], y=res.y()[0], w=width+10, h=height+10)
            card = card.resize(w=1000)

            card = self.fix_rotation_twofeatures(card, 'top_left.png', ('top_right.png', 1, 'CCORR_NORM'))
            return self.parse(card)
        else:
            return None

    def parse(self, card):
        self.get_text(card, "surname", x=320, y=100, w=600, h=37)
        self.get_text(card, "first_name", x=320, y=166, w=600, h=32)
        self.get_text(card, "birth_date", x=320, y=210, w=170, h=32)
        self.get_text(card, "birth_place", x=500, y=210, w=400, h=32)

        if self.debug:
            card.save("debug/" + self.dn + "_gettext.png")

        return {}
