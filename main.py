import argparse
from app import csv_reader

TAG_M = 'mm'
TAG_A = 'af'
TAG_P = 'pp'


def main(args):
    try:
        rt = csv_reader.csv_reader_factory('ro').set_csvpath(args.ros).readCSV()
        sp = csv_reader.csv_reader_factory('sp').set_csvpath(args.ss).readCSV()
        c = defaultdict(list)
        for k, v in sp:
            # only retrieve spend, view
            c[k].append(v.get_spend_and_view())
        printOut(c)

        display(sp, TAG_M)
        display(sp, TAG_A)
        display(sp, TAG_P)
    # TODO: Could implement exception class to handle different type of error
    except Exception, e:
        print str(e)
        return str(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to parse given\
            csv files and return output.")
    parser.add_argument("--ros", help="Ros csv path", type=str, required=True)
    parser.add_argument("--ss", help="Ss csv path", type=str, required=True)
    args = parser.parse_args()
    main(args)

