#!/usr/bin/env python3
import matplotlib.pyplot as pl
from functools import reduce


def get_file_data(lines):
    name = lines[0].split('/')[-1][:-1]
    time = []
    for l in lines[1:]:
        l = l[:-1]
        if not l:
            return name, reduce(lambda x, y: x + y, time) / 25
        l = l.replace(',', '.')
        time.append(float(l))
    return name, reduce(lambda x, y: x + y, time) / 25


def read_file(file_name):
    file = open(file_name, "r")
    lines = file.readlines()[2:]
    while lines:
        name, mean = get_file_data(lines)
        lines = lines[7:]
        print(name, mean)


if __name__ == '__main__':
    ALL = "./all.txt"
    NORMAL = "./normal.txt"
    read_file(ALL)
