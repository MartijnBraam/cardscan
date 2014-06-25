#!/usr/bin/env python2
from SimpleCV import *
import shutil

class CardScan:
    def __init__(self, args):
        self.args = args
        self.verbose = args.verbose
        self.card_parsers = []
        self.register_card("nl.government.idcard")
        self.register_card("nl.government.drivinglicence")

    def register_card(self, dn):
        dn = "card." + dn
        class_name = dn.split(".")[-1]
        mod = __import__(dn, fromlist=[class_name])
        card_class = getattr(mod, class_name)
        self.card_parsers.append(card_class(self.args))
        if self.verbose:
            print("Added detection class {}".format(dn))

    def parse(self, filename):
        input_image = Image(filename)

        # Create new empty debug directory if debug is enabled
        if self.args.debug:
            if os.path.isdir("debug"):
                shutil.rmtree("debug")
            os.mkdir("debug")
            input_image.save("debug/input.png")

        # Use blob detection to find all cards in the scanned document
        input_image_inverse = input_image.invert()
        cards = input_image_inverse.findBlobs(threshval=10, minsize=50)
        if self.verbose:
            print("Detected {} blobs".format(len(cards)))

        # Normalize card rotation
        normalized_cards = []
        for idx, card in enumerate(cards):
            card.rotate(card.angle())
            normalized = card.hullImage().invert()
            normalized_cards.append(normalized)
            if self.args.debug:
                normalized.save("debug/normalized_{}.png".format(idx))

        # Run all registered card classes against all detected blobs
        matches = []
        for ncard in normalized_cards:
            if self.verbose:
                print("Running testers for blob")
            for tester in self.card_parsers:
                if self.verbose:
                    print("  Running tester: {}".format(tester.name))
                match = tester.match(ncard)
                if match != None:
                    if self.verbose:
                        print("    Tester matched!")
                    matches.append(match)
                    break

        # Output results
        if self.verbose:
            print "Output format: {}".format(self.args.format)

        if self.args.format == "json":
            import json

            json_report = json.dumps(matches)
            print json_report

        if self.args.format == "yaml":
            import yaml

            print yaml.dump(matches)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Tool to extract json objects from scanned cards')
    parser.add_argument('filename', help="File to scan for cards. This tool currently expects it to be 300dpi")
    parser.add_argument('-v', '--verbose', action="store_true", help="Enable verbose output")
    parser.add_argument('-f', '--format', help="Output formatting", choices=['json', 'yaml'], default="yaml")
    parser.add_argument('-d', '--debug',
                        help="This creates a debug directory in the current directory with debug files from the card classes",
                        action="store_true")
    parser.add_argument('-e', '--export', help="Export extracted images like signature and photo", action="store_true")
    args = parser.parse_args()

    cardscan = CardScan(args)
    cardscan.parse(args.filename)