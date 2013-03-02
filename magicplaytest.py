import pyx


def marginalize(rect, margin):
    mrect = {}
    mrect["left"] = rect["left"] + margin
    mrect["bot"] = rect["bot"] + margin
    mrect["right"] = rect["right"] - margin
    mrect["top"] = rect["top"] - margin
    return mrect


def drawcard(c, card, slot, rect):
    margin = 0.1
    mrect = marginalize(rect, margin)
    c.text(mrect["left"], mrect["top"], card["name"], [pyx.text.parbox(3), pyx.text.halign.left, pyx.text.valign.top])
    if "cost" in card:
        c.text(mrect["right"], mrect["top"], card["cost"], [pyx.text.parbox(1), pyx.text.halign.right, pyx.text.valign.top])
    if "pt" in card:
        c.text(mrect["right"], mrect["bot"], card["pt"], [pyx.text.parbox(1), pyx.text.halign.right, pyx.text.valign.bottom])
    c.text(mrect["left"], mrect["top"] - 2, card["types"], [pyx.text.parbox(3), pyx.text.halign.left, pyx.text.valign.bottom])
    c.text(mrect["left"], mrect["top"] - 3, card["rules_text"], [pyx.text.parbox(4.5), pyx.text.halign.left, pyx.text.valign.top])
    c.text(mrect["left"], mrect["bot"], slot, [pyx.text.parbox(3), pyx.text.halign.left, pyx.text.valign.bottom])
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


def make_playtest(cards):
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
    doc.writePDFfile()


def unit_test_2():
    squire = {"name": "Squire", "cost": "1W", "pt": "1/2", "types": "Creature - Human Soldier", "rules_text":"Winning"}
    cards = [('WC01', [squire]), ('WC02', [squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire, squire])]
    make_playtest(cards)

if __name__ == "__main__":
    unit_test_2()
