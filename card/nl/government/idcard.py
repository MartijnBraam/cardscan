from SimpleCV import *
from time import strptime
import math


class idcard(object):
    def __init__(self):
        self.card = None
        self.card_aspect = 0.6272189349112426
        self.feature_angle = 47.0
        self.fields = {}
        self.name = 'Dutch personal identification card'

    def match(self, inputImage):
        template = Image("data/nl/government/idcard/idcard_nl.png")
        res = inputImage.findTemplate(template_image=template, threshold=4)
        if res:
            width = template.width
            height = template.width * self.card_aspect
            card = inputImage.crop(x=res.x()[0], y=res.y()[0], w=width+10, h=height+10)
            card = card.resize(w=1000)

            card = self.fixRotation(card)
            return self.parse(card)
        else:
            return None

    def fixRotation(self, card):
        feature_top_left = Image("data/nl/government/idcard/idcard_nl_topleft.png")
        pos_top_left = card.findTemplate(template_image=feature_top_left, threshold=4)[0]
        box = pos_top_left.boundingBox()
        top_left_center = (box[0]+box[2]/2, box[1]+box[3]/2)

        feature_bottom_right = Image("data/nl/government/idcard/idcard_nl_bottomright.png")
        pos_bottom_right = card.findTemplate(template_image=feature_bottom_right, threshold=5)[0]
        box = pos_bottom_right.boundingBox()
        bottom_right_center = (box[0]+box[2]/2, box[1]+box[3]/2)

        dx,dy = bottom_right_center[0]-top_left_center[0],bottom_right_center[1]-top_left_center[1]
        rads = math.atan2(dx, dy)
        degs = math.degrees(rads)
        delta_angle = degs - self.feature_angle
        card = card.rotate(delta_angle)
        return card

    def parse(self, card):
        self.getText(card, "nationality", x=355, y=105, w=340, h=37)
        self.getText(card, "document_no", x=690, y=105, w=300, h=37)
        self.getText(card, "surname", x=355, y=160, w=700, h=37)
        self.getText(card, "given_names", x=355, y=218, w=400, h=37)
        self.getText(card, "gender", x=750, y=218, w=150, h=37)
        self.getText(card, "date_of_birth", x=355, y=275, w=410, h=37)
        self.getText(card, "height", x=750, y=275, w=150, h=37)
        self.getText(card, "place_of_birth", x=355, y=328, w=700, h=37)
        self.getText(card, "personal_no", x=355, y=385, w=700, h=37)
        self.getText(card, "date_of_issue", x=355, y=439, w=300, h=37)
        self.getText(card, "date_of_expiry", x=690, y=439, w=300, h=37)
        self.getText(card, "authority", x=355, y=495, w=700, h=37)

        self.getSignature(card, x=30, y=500, w=340, h=120)
        self.getPhoto(card, x=80, y=110, w=240, h=350)
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
                    'date': self.parseDate(self.fields['date_of_birth']),
                    'place': self.fields['place_of_birth']
                },
                'nationality': self.fields['nationality'],
                'gender': self.parseGender(self.fields['gender']),
                'height': self.parseHeight(self.fields['height'])
            },
            'validity': {
                'start': self.parseDate(self.fields['date_of_issue']),
                'end': self.parseDate(self.fields['date_of_expiry'])
            },
            'authority': self.fields['authority']
        }
        return structure

    def parseHeight(self, heightstr):
        # heightstr: 1,92 m
        heightstr = heightstr.strip().replace(" ", "") # 1,92m
        heightstr = heightstr[:-1].replace(",", ".") # 1.92
        return float(heightstr)

    def parseGender(self, genderstr):
        # genderstr: M/M or V/F
        firstchr = genderstr.strip()[0].lower()
        if firstchr == 'm':
            return 'male'
        else:
            return 'female'

    def parseDate(self, datestr):
        # datestr: 12 MAA/MAR 2014
        datestr = datestr.replace(" ", "") # 12MAA/MAR2014
        year = datestr[9:13] # 2014
        month = datestr[6:9].lower() # mar
        month = strptime(month, "%b").tm_mon # 4
        day = datestr[0:2] # 12
        datestr = "{}-{}-{}".format(year,month,day) # 2014-4-12
        return datestr

    def getText(self, card, label, x, y, w, h):
        field = card.crop(x=x, y=y, w=w, h=h)
        field = field.grayscale()
        field = field * 1.2
        field_text = field.readText().strip().split("\n")[0]
        self.fields[label] = field_text

    def getSignature(self, card, x, y, w, h):
        field = card.crop(x=x, y=y, w=w, h=h)
        field = field.grayscale().binarize().invert()

    def getPhoto(self, card, x, y, w, h):
        field = card.crop(x=x, y=y, w=w, h=h)
