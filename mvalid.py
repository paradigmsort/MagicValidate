import ply.lex as lex
import ply.yacc as yacc

tokens = ('ID_LINE',
          'CREATURE_TYPE_LINE',
          'LAND_TYPE_LINE',
          'OTHER_TYPE_LINE',
          'COST_LINE',
          'PT_LINE',
          'TEXT_LINE',
          'OR_BLOCK',
          'BLANK_LINE')

# land creatures are not supported
noncreature_nonland_permanent = r"Artifact|Enchantment|Planeswalker"
creature = r"Creature"
land = r"Land"
nonpermanent = r"Instant|Sorcery"
tribal = r"Tribal"

# creatures always have subtypes
creature_type_line = r"((" + noncreature_nonland_permanent + r")\ )*Creature\ -\ .*\n"
land_type_line = r"((" + noncreature_nonland_permanent + r"|" + tribal + r")\ )*Land\n"
other_type = r"(" + noncreature_nonland_permanent + r"|" + tribal + r"|" + nonpermanent + r")"
other_type_line = other_type + r"(\ " + other_type + r")*(\ -\ .*)?\n"
mana = r"(W|U|B|R|G)"
rarity = r"(C|U|R|M|L)"


def lines(n, t):
    t.lexer.lineno += n


@lex.TOKEN(r"(" + mana + r"|C)" + rarity + r"\d+\n")
def t_ID_LINE(t):
    lines(1, t)
    return t


@lex.TOKEN(creature_type_line)
def t_CREATURE_TYPE_LINE(t):
    lines(1, t)
    return t


@lex.TOKEN(land_type_line)
def t_LAND_TYPE_LINE(t):
    lines(1, t)
    return t


@lex.TOKEN(other_type_line)
def t_OTHER_TYPE_LINE(t):
    lines(1, t)
    return t


@lex.TOKEN(r"(\d+" + mana + r"*|\d*" + mana + r"+)\n")
def t_COST_LINE(t):
    lines(1, t)
    return t


@lex.TOKEN(r"\d*/\d*\n")
def t_PT_LINE(t):
    lines(1, t)
    return t


@lex.TOKEN(r".+\n")
def t_TEXT_LINE(t):
    lines(1, t)
    return t


@lex.TOKEN(r"\nor\n\n")
def t_OR_BLOCK(t):
    lines(3, t)
    return t


@lex.TOKEN(r"\n")
def t_BLANK_LINE(t):
    lines(1, t)
    return t


def t_error(t):
    print("Can't make token with " + t.value + " (line " + str(t.lexer.lineno) + ")")

lex.lex()


def p_cardfile(p):
    'cardfile : cardblock cardfile_more'
    p[2].insert(0, p[1])
    p[0] = p[2]


def p_cardfile_more(p):
    'cardfile_more : BLANK_LINE cardfile'
    p[0] = p[2]


def p_cardfile_done(p):
    'cardfile_more : empty'
    p[0] = []


def p_cardblock(p):
    'cardblock : ID_LINE cards'
    p[0] = (p[1], p[2])


def p_cards(p):
    'cards : card cards_more'
    p[2].insert(0, p[1])
    p[0] = p[2]


def p_cards_more(p):
    'cards_more : OR_BLOCK cards'
    p[0] = p[2]


def p_cards_done(p):
    'cards_more : empty'
    p[0] = []


def p_card(p):
    '''card : creature
            | spell
            | land'''
    p[0] = p[1]


def p_creature(p):
    'creature : TEXT_LINE COST_LINE CREATURE_TYPE_LINE PT_LINE rules_text'
    p[0] = {'name': p[1], 'cost': p[2], 'types': p[3], 'pt': p[4], 'rules_text': p[5]}


def p_noncreature(p):
    'spell : TEXT_LINE COST_LINE OTHER_TYPE_LINE rules_text'
    p[0] = {'name': p[1], 'cost': p[2], 'types': p[3], 'rules_text': p[4]}


def p_land(p):
    'land : TEXT_LINE LAND_TYPE_LINE rules_text'
    p[0] = {'name': p[1], 'types': p[2], 'rules_text': p[3]}


def p_rules_text_more(p):
    'rules_text : TEXT_LINE rules_text'
    p[0] = p[1] + p[2]


def p_rules_text_done(p):
    'rules_text : empty'
    p[0] = ''


def p_empty(p):
    ' empty : '
    pass


def p_error(p):
    print("Error at " + str(p))
    # look for the blank line separating block
    while 1:
        tok = yacc.token()
        if not tok:
            break
        if tok.type == 'BLANK_LINE':
            yacc.restart()
            yacc.errok()
            return yacc.token()  # return the next line after the blank

yacc.yacc()


def unit_test():
    sample = (
'''WC01
Squire
1W1
Artifact Creature - Human Soldier
1/2

WC02
Squire
1W2
Artifact Creature - Human Soldier
1/2

WC03
Squire
1W
Artifact Creature - Human Soldier
1/2

or

Squire
1W
Artifact Creature - Human Soldier
1/2
''')
    mvalid(sample)


def mvalid(filestr):
    lex.input(filestr)
    yacc.parse(filestr, debug=0)

if __name__ == "__main__":
    unit_test()
