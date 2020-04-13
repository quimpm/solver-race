#!/usr/bin/env python3
import matplotlib.pyplot as pl
from functools import reduce
import re


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
    res = []
    while lines:
        name, mean = get_file_data(lines)
        lines = lines[27:]
        res.append([name, mean])
    return res


def get_diff_files(all_data):
    d50 = list(filter(lambda x: re.search('^exemple-50*',x[0]), all_data))
    d75 = list(filter(lambda x: re.search('^exemple-75*',x[0]), all_data))
    return d50, d75


def get_name(data):
    return list(map(lambda x: x[0].split('-')[2][:-4], data))

def get_comp(data, i):
    return list(map(lambda x: x[i], data))


def create_graphic(file1, file2, index):
    all_data = read_file(file1)
    normal_data = read_file(file2)
    da50, da75 = get_diff_files(all_data)
    dn50, dn75 = get_diff_files(normal_data)
    pl.figure(int(index) + 1)
    pl.plot(get_name(da50), get_comp(da50, 1), 'o-', label="Using all")
    pl.plot(get_name(dn50), get_comp(dn50, 1), 'o-', label="Using normal")
    pl.legend()
    pl.savefig(f'50-graphic-{index}.png')
    pl.figure(int(index) + 2)
    pl.plot(get_name(da75), get_comp(da75, 1), 'o-', label="Using all")
    pl.plot(get_name(dn75), get_comp(dn75, 1), 'o-', label="Using normal")
    pl.legend()
    pl.savefig(f'75-graphic-{index}.png')


if __name__ == '__main__':
    ALL = "./all.txt"
    NORMAL = "./normal.txt"
    create_graphic(ALL, NORMAL, "1")

