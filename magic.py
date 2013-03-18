import argparse
import mvalid
import magicplaytest
import msewriter

parser = argparse.ArgumentParser(description='Validate magic files')
parser.add_argument('filename', help='the file to validate')
parser.add_argument('-m', '--make-playtest', action='store_true')
parser.add_argument('-e', '--make-mse-set', action='store_true')
parser.add_argument('-s', '--show', action='store_true')
parser.add_argument('-d', '--directory', action='store_true')
parser.add_argument('-o', '--out-file')

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
            if filename.endswith(".txt"):
                cards.extend(parse_file(os.path.join(dirpath, filename)))
else:
    cards = parse_file(args.filename)

if args.show:
    print cards

if args.make_playtest:
    if hasattr(args, 'outfile'):
        outfile = args.outfile
    else:
        outfile = args.filename + ".pdf"
    magicplaytest.make_playtest(cards, outfile)

if args.make_mse_set:
    if hasattr(args, 'outfile'):
        outfile = args.outfile
    else:
        outfile = args.filename + ".mse-set"
    set_writer = msewriter.MseWriter(outfile)
    set_writer.writeset(cards)
    set_writer.finalize()
