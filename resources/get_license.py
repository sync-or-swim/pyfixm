import argparse
import re
from xml.etree import ElementTree
from pathlib import Path


def main():

    args = parse_args()

    tree = ElementTree.parse(args.xsd_path)
    root = tree.getroot()

    # This happens to be where the license is located. Shouldn't change w/o a
    # version bump
    license_element = root[0][0]

    # Replace sequences of two or more spaces with a single space
    license_text = re.sub(r" +", " ", license_element.text).strip()

    # Write to file
    args.output_path.write_text(license_text)


def parse_args() -> argparse.Namespace:
    description = "Extract the license from the specified Base.xsd file and " \
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
