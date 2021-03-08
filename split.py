
"""Splitting a given corpus into training, development, and testing sets."""


import argparse

import random

from typing import Iterator, List


def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
    # Just in case someone forgets to put a blank line at the end...
    if lines:
        yield lines


def write_tags(path: str, set: str):
    with open(path, "w") as sink:
        for line in set:
            print(line, file=sink)


def main(args: argparse.Namespace) -> None:
    corpus = list(read_tags(args.input))

    random.seed(args.seed)
    random.shuffle(corpus)

    length = len(corpus)

    eightyP = (8 * length) // 10    #eighty percent of corpus length
    tenP = length // 10             #ten percent of corpus length
    
    if tenP < 1:                    #for small corpuses
        tenP = 1

    train = corpus[: eightyP]

    dev = corpus[eightyP : eightyP + tenP]

    test = corpus[eightyP + tenP :]

    write_tags(args.train, train)
    write_tags(args.dev, dev)
    write_tags(args.test, test)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--seed", required=True, 
        help="seed for randomizing data"
        )

    parser.add_argument(
        "input", help="input corpus here"
        )

    parser.add_argument(
        "train", help="path for training set"
        )

    parser.add_argument(
        "dev", help="path for development set"
        )
        
    parser.add_argument(
        "test", help="path for testing set"
        )

    main(parser.parse_args())
