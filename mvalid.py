import ply.lex as lex

tokens = ('TYPE_LINE', 'COST_LINE', 'PT_LINE', 'TEXT_LINE', 'BLANK_LINE')

type = r"(Artifact|Creature|Enchantment|Instant|Land|Planeswalker|Sorcery|Tribal)"

t_TYPE_LINE = type + r"(\ " + type + r")*(\ -\ .*)?\n"
t_COST_LINE = r"\d*(W|U|B|R|G)\n"
t_PT_LINE = r"\d*/\d*\n"
t_TEXT_LINE = r".+\n"
t_BLANK_LINE = r"\n"

lex.lex()

sample = (
'''
Squire
1W
Artifact Creature - Human Soldier
1/2
''')

lex.input(sample)
for tok in iter(lex.token, None):
    print (repr(tok.type), repr(tok.value))


def p_cardfile_more(p):
    'cardfile : BLANK_LINE card cardfile'
    p[3].append(p[2])
    p[0] = p[3]


def p_cardfile_done(p):
    'cardfile : empty'
    p[0] = []


def p_card(p):
    '''card : creature
            | noncreature'''
    p[0] = p[1]


def p_creature(p):
    'creature : TEXT_LINE COST_LINE TYPE_LINE PT_LINE rules_text'
    p[0] = {'name': p[1], 'cost': p[2], 'types': p[3], 'pt': p[4], 'rules_text': p[5]}


def p_noncreature(p):
    'noncreature : TEXT_LINE COST_LINE TYPE_LINE rules_text'
    p[0] = {'name': p[1], 'cost': p[2], 'types': p[3], 'rules_text': p[4]}


def p_rules_text_more(p):
    'rules_text : TEXT_LINE rules_text'
    p[0] = p[1] + p[2]


def p_rules_text_done(p):
    'rules_text : empty'
    p[0] = ''


def p_empty(p):
    ' empty : '
    pass

import ply.yacc as yacc
yacc.yacc()

yacc.parse(sample)
