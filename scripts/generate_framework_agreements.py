"""

Usage:
    scripts/generate_framework_agreements.py <supplier_lots_file> <supplier_declaration_file>

Example:
    ./generate_framework_agreements.py lots.csv declarations.csv
"""
import sys
from lib.generate_framework_agreements import check_lots_csv, read_csv
from docopt import docopt


if __name__ == '__main__':

    arguments = docopt(__doc__)

    supplier_lots_file = read_csv(arguments['<supplier_lots_file>'])
    supplier_declaration_file = read_csv(arguments['<supplier_declaration_file>'])

    if not check_lots_csv(supplier_lots_file):
        sys.exit("Lots CSV is invalid")

    sys.exit("Success")
