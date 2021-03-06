#coding: utf-8
import zipfile


class MseWriter:
    def __init__(self, filename):
        self.file = open("set", "w")
        self.zipfile = zipfile.ZipFile(filename, "w")
        self.indent_level = 0
        self.blockstack = []

    def indent(self):
        self.file.write(self.indent_level * "\t")

    def increase_indent(self):
        self.indent_level += 1

    def decrease_indent(self):
        self.indent_level -= 1

    def writeline(self, text):
        self.indent()
        self.file.write(text + "\n")

    def addfield(self, fieldname, fieldcontent):
        self.writeline(fieldname + ": " + fieldcontent)

    def startblock(self, blockname):
        self.writeline(blockname + ":")
        self.increase_indent()
        self.blockstack.append(blockname)

    def endblock(self, blockname):
        self.decrease_indent()
        if (blockname != self.blockstack.pop()):
            raise Exception("BlockCloseError")

    def writecard(self, card):
        self.startblock("card")
        self.addfield("name", card["name"])
        if "cost" in card:
            self.addfield("casting cost", card["cost"])
        if '-' in card["types"]:
            supertypes, subtypes = card["types"].split("-")
            self.addfield("sub type", subtypes.strip())
        else:
            supertypes = card["types"]
        self.addfield("super type", supertypes.strip())
        self.startblock("rule text")
        for line in card["rules_text"].split("\n"):
            self.writeline(line)
        self.endblock("rule text")
        if "pt" in card:
            power, toughness = card["pt"].split("/")
            self.addfield("power", power)
            self.addfield("toughness", toughness)
        self.endblock("card")

    def writeheader(self):
        self.addfield("mse version", "0.3.8")
        self.addfield("game", "magic")
        self.addfield("stylesheet", "new")
        self.startblock("set info")
        self.addfield("copyright", "™ & © 1993—2013 Wizards of the Coast LLC")
        self.addfield("automatic card numbers", "true")
        self.endblock("set info")

    def writeset(self, cards):
        self.writeheader()
        for (slot, slot_cards) in cards:
            for card in slot_cards:
                self.writecard(card)

    def finalize(self):
        self.file.close()
        self.zipfile.write("set")
        self.zipfile.close()

if __name__ == "__main__":
    squire = {"name": "Squire", "cost": "1W", "pt": "1/2", "types": "Creature - Human Soldier", "rules_text": "Winning\nTesting"}
    writer = MseWriter("set")
    writer.writeheader()
    writer.writecard(squire)
