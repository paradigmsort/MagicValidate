import argparse
import mvalid
import magicplaytest

parser = argparse.ArgumentParser(description='Validate magic files')
parser.add_argument('filename', help='the file to validate')
parser.add_argument('-m', '--make-playtest', action='store_true')
parser.add_argument('-s', '--show', action='store_true')
parser.add_argument('-d', '--directory', action='store_true')

args = parser.parse_args()


def parse_file(filename):
    file = open(filename)
    cards = mvalid.mvalid(file.read())
    file.close()
    return cards

if args.directory:
    cards = []
    import os
    for (dirpath, dirnames, filenames) in os.walk(args.filename):
        for filename in filenames:
            cards.extend(parse_file(os.path.join(dirpath,filename)))
else:
    cards = parse_file(args.filename)

if args.show:
    print cards

if args.make_playtest:
    magicplaytest.make_playtest(cards)
