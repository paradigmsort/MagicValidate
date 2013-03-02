import pyx


def marginalize(rect, margin):
    mrect = {}
    mrect["left"] = rect["left"] + margin
    mrect["bot"] = rect["bot"] + margin
    mrect["right"] = rect["right"] - margin
    mrect["top"] = rect["top"] - margin
    return mrect


class CardWriter:
    def __init__(self, canvas, rect):
        self.canvas = canvas
        margin = 0.1
        self.rect = marginalize(rect, margin)
        self.location = {'name': (self.rect["left"], self.rect["top"], [pyx.text.parbox(3), pyx.text.halign.left, pyx.text.valign.top]),
                         'cost': (self.rect["right"], self.rect["top"], [pyx.text.parbox(1.5), pyx.text.halign.right, pyx.text.valign.top]),
                         'pt': (self.rect["right"], self.rect["bot"], [pyx.text.parbox(1), pyx.text.halign.right, pyx.text.valign.bottom]),
                         'types': (self.rect["left"], self.rect["top"] - 2, [pyx.text.parbox(3), pyx.text.halign.left, pyx.text.valign.bottom]),
                         'rules_text': (self.rect["left"], self.rect["top"] - 3, [pyx.text.parbox(4.5), pyx.text.halign.left, pyx.text.valign.top]),
                         'slot': (self.rect["left"], self.rect["bot"], [pyx.text.parbox(3), pyx.text.halign.left, pyx.text.valign.bottom])}

    def write(self, item, text):
        self.canvas.text(self.location[item][0], self.location[item][1], text, self.location[item][2])


def drawcard(c, card, slot, rect):
    writer = CardWriter(c, rect)
    writer.write('name', "\Large " + card['name'])
    if 'cost' in card:
        writer.write('cost', "\Large " + card['cost'])
    if 'pt' in card:
        writer.write('pt', "\Large " + card['pt'])
    writer.write('types', card['types'])
    writer.write('rules_text', card['rules_text'].replace('\n', '\\break '))
    writer.write('slot', slot)
    c.stroke(pyx.path.rect(rect["left"], rect["bot"], rect["right"] - rect["left"], rect["top"] - rect["bot"]))


def unit_test():
    squire = {"name": "Squire", "cost": "1W", "pt": "1/2", "types": "Creature - Human Soldier"}

    baserect = {"left": 0, "bot": 0, "right": 4, "top": 6}
    tworect = {"left": 4, "bot": 0, "right": 8, "top": 6}

    c = pyx.canvas.canvas()

    drawcard(c, squire, baserect)
    drawcard(c, squire, tworect)

    c.writePDFfile()
    print("ok")


class RectPage:
    def __init__(self):
        x_size = 4.8
        y_size = 6.7
        self.canvas = pyx.canvas.canvas()
        self.page = pyx.document.page(self.canvas, paperformat=pyx.document.paperformat.Letter)
        self.rects = [{"left": x*x_size, "bot": y*y_size, "right": (x+1)*x_size, "top": (y+1)*y_size} for y in range(4) for x in [3, 2, 1, 0]]

    def full(self):
        if self.rects:
            return False
        else:
            return True

    def draw(self, card, slot):
        drawcard(self.canvas, card, slot, self.rects.pop())

    def getpage(self):
        return self.page


def make_playtest(cards, filename):
    pages = []
    page = RectPage()

    for (slot, slot_cards) in cards:
        for card in slot_cards:
            page.draw(card,slot)
            if page.full():
                pages.append(page.getpage())
                page = RectPage()

    pages.append(page.getpage())

    doc = pyx.document.document(pages)
    doc.writePDFfile(filename)


def unit_test_2():
    squire = {"name": "Squire", "cost": "1W", "pt": "1/2", "types": "Creature - Human Soldier", "rules_text":"Winning"}
    cards = [('WC01', [squire]), ('WC02', [squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire])]
    make_playtest(cards, None)

if __name__ == "__main__":
    unit_test_2()
