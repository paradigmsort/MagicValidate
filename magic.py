import argparse
import mvalid

parser = argparse.ArgumentParser(description='Validate magic files')
parser.add_argument('filename', help='the file to validate')

args = parser.parse_args()
file = open(args.filename)
mvalid.mvalid(file.read())
