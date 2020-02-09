import argparse
import re
from xml.etree import ElementTree
from pathlib import Path


def main():

    args = parse_args()

    tree = ElementTree.parse(args.xsd_path)
    root = tree.getroot()
    license_element = root[0][0]

    license_text = re.sub(r" +", " ", license_element.text).strip()
    args.output_path.write_text(license_text)


def parse_args() -> argparse.Namespace:
    description = "Find the license in thesesar specified Base.xsd file and " \
                  "write it to a specified file. Incredibly basic and naive."
    parser = argparse.ArgumentParser(description=description)
    # noinspection PyTypeChecker
    parser.add_argument('xsd_path', type=Path, metavar="xsd-path",
                        help="Path to Base.xsd containing license")
    # noinspection PyTypeChecker
    parser.add_argument('output_path', type=Path, metavar="output-path",
                        help="File to write license to")

    return parser.parse_args()


if __name__ == '__main__':
    main()
