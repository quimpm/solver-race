#!/usr/bin/env python3
import sys
import fracaSAT


def main():
    if len(sys.argv) < 2:
        print("./fracasat-graph-col.py <output-file> [<cnf-file>]")
    output-file = sys.argv[1]
    if len(sys.argv) == 3:
        cnf-file = sys.argv[2]
        fracaSAT.get_formula(cnf-file)
    else:


if __name__ == "__main__":
    main()