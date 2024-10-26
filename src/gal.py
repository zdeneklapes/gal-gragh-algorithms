import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file')
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)


if __name__ == '__main__':
    main()
