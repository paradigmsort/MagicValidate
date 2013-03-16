class MseWriter:
    def __init__(self, filename):
        self.file = open(filename, "w")
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


def writecard(writer, card):
    writer.startblock("card")
    writer.addfield("name", card["name"])
    writer.addfield("casting cost", card["cost"])
    #super type
    #subtype
    writer.startblock("rule text")
    for line in card["rules_text"].split("\n"):
        writer.writeline(card["rules_text"])
    writer.endblock("rule text")
    if "pt" in card:
        power, toughness = card["pt"].split("/")
        writer.addfield("power", power)
        writer.addfield("toughness", toughness)

if __name__ == "__main__":
    squire = {"name": "Squire", "cost": "1W", "pt": "1/2", "types": "Creature - Human Soldier", "rules_text": "Winning"}
    writecard(MseWriter("test_set"), squire)
