#!/usr/bin/env python3

import sys
import matplotlib.pyplot as pl
from functools import reduce


def read_file(f):
    lines = f.readlines()
    is_header = True
    header = None
    res = {}
    for i, line in enumerate(lines):
        if is_header:
            header = int(line[:-1])
            res[header] = []
            is_header = False
        else:
            try:
                word = '.'.join(line[:-1].split(','))
                res[header].append(float(word))
            except:
                is_header = True
    return res


def plot_data(data):
    res = {}
    for k in data:
        res[k] = reduce(lambda x, y: x + y, data[k]) / 100
    print(res)
    pl.figure(1)
    pl.plot(res.keys(), res.values(), 'o-', label='Works')
    pl.legend()
    pl.savefig(f'flips.png')


if __name__ == '__main__':
    file = sys.argv[1]
    with open(file) as f:
        data = read_file(f)
        plot_data(data)
