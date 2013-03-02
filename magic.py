import argparse
import mvalid
import magicplaytest

parser = argparse.ArgumentParser(description='Validate magic files')
parser.add_argument('filename', help='the file to validate')
parser.add_argument('-m', '--make-playtest', action='store_true')
parser.add_argument('-s', '--show', action='store_true')

args = parser.parse_args()
file = open(args.filename)
parsed_cards = mvalid.mvalid(file.read())

if args.show:
    print parsed_cards
 
if args.make_playtest:
    magicplaytest.make_playtest(parsed_cards)
