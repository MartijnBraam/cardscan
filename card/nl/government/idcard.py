from SimpleCV import *
from card.base import BaseCard
from time import strptime


class idcard(BaseCard):
    def __init__(self, debug):
        self.card_aspect = 0.6272189349112426
        self.feature_angle = 47.0
        self.name = 'Dutch personal identification card'
        self.data_directory = 'data/nl/government/idcard'
        self.dn = 'nl.government.idcard'
        super(idcard, self).__init__(debug)

    def match(self, input_image):
        template = Image(self.data_directory + "/template.png")
        res = input_image.findTemplate(template_image=template, threshold=4)
        if res:
            width = template.width
            height = template.width * self.card_aspect
            card = input_image.crop(x=res.x()[0], y=res.y()[0], w=width+10, h=height+10)
            card = card.resize(w=1000)

            card = self.fix_rotation_twofeatures(card, ('top_left.png', 4), 'bottom_right.png')
            return self.parse(card)
        else:
            return None

    def parse(self, card):
        self.get_text(card, "nationality", x=355, y=105, w=320, h=37)
        self.get_text(card, "document_no", x=690, y=105, w=275, h=37)
        self.get_text(card, "surname", x=355, y=160, w=600, h=37)
        self.get_text(card, "given_names", x=355, y=218, w=390, h=37)
        self.get_text(card, "gender", x=750, y=218, w=150, h=37)
        self.get_text(card, "date_of_birth", x=355, y=275, w=390, h=37)
        self.get_text(card, "height", x=750, y=275, w=150, h=37)
        self.get_text(card, "place_of_birth", x=355, y=328, w=600, h=37)
        self.get_text(card, "personal_no", x=355, y=385, w=600, h=37)
        self.get_text(card, "date_of_issue", x=355, y=439, w=300, h=37)
        self.get_text(card, "date_of_expiry", x=690, y=439, w=275, h=37)
        self.get_text(card, "authority", x=355, y=495, w=600, h=37)

        self.get_signature(card, x=30, y=500, w=320, h=120)
        self.get_photo(card, x=80, y=110, w=240, h=350)

        if self.debug:
            card.save("debug/" + self.dn + "_gettext.png")

        structure = {
            'card': {
                'type': 'nl.government.idcard',
                'class': 'personal-indentification'
            },
            'country': 'nl',
            'documentId': self.fields['document_no'],
            'person': {
                'personalId': self.fields['personal_no'],
                'surname': self.fields['surname'],
                'givenNames': self.fields['given_names'],
                'birth': {
                    'date': self.parse_date(self.fields['date_of_birth']),
                    'place': self.fields['place_of_birth']
                },
                'nationality': self.fields['nationality'],
                'gender': self.parse_gender(self.fields['gender']),
                'height': self.parse_height(self.fields['height'])
            },
            'validity': {
                'start': self.parse_date(self.fields['date_of_issue']),
                'end': self.parse_date(self.fields['date_of_expiry'])
            },
            'authority': self.fields['authority']
        }
        return structure

    def parse_height(self, heightstr):
        # heightstr: 1,92 m
        heightstr = heightstr.strip().replace(" ", "") # 1,92m
        heightstr = heightstr[:-1].replace(",", ".") # 1.92
        return float(heightstr)

    def parse_gender(self, genderstr):
        # genderstr: M/M or V/F
        firstchr = genderstr.strip()[0].lower()
        if firstchr == 'm':
            return 'male'
        else:
            return 'female'

    def parse_date(self, datestr):
        # datestr: 12 MAA/MAR 2014
        datestr = datestr.replace(" ", "")  # 12MAA/MAR2014
        year = datestr[9:13] # 2014
        month = datestr[6:9].lower()  # mar
        month = strptime(month, "%b").tm_mon  # 4
        day = datestr[0:2] # 12
        datestr = "{}-{}-{}".format(year, month, day)  # 2014-4-12
        return datestr

