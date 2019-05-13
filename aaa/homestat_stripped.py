#!/usr/bin/env python3

import re
from collections import Counter
from operator import itemgetter

def make_stat(filename):
    fileOpen = open(filename, 'r', encoding='cp1251')
    stats = dict()
    a = fileOpen.read().splitlines()
    fileOpen.close()
    direct = dict()
    exception1 = {'а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я'}
    exception2 = {'Илья', 'Никита', 'Лёва', 'Алехандро'}

    years = 0
    for i in range(0, len(a)):
        if re.findall(r'20\d{2}', a[i]):
            if years != 0:
                stats[years] = direct
            years = re.findall(r'20\d{2}', a[i])[0]
            direct = dict()
        if 'name' in a[i]:
            name = re.findall(r'/>\w+ (\w+)', a[i])
            clear = name[0][len(name[0])-1]
            male = -10 if clear in exception1 and name[0] not in exception2 or name[0] == 'Любовь' else -15
            if not direct.get(name[0]):
                direct[name[0]] = list({0, male})
            direct[name[0]][0] += 1
    stats[years] = direct
    return stats


def extract_years(stat):
    return sorted(stat.keys())


def extract_general(stat):
    sortedStat = sorted(stat['2004'][2].items(), key=itemgetter(1), reverse=True)
    return sortedStat


def extract_general_male(stat):
    stat = Counter()
    for year in stat:
        for name in stat[year][0]:
            stat[name] += stat[year][0][name]
    return sorted(stat.items(), key=itemgetter(1), reverse=True)


def extract_general_female(stat):
    stat = Counter()
    for year in stat:
        for name in stat[year][1]:
            stat[name] += stat[year][1][name]
    return sorted(stat.items(), key=itemgetter(1), reverse=True)


def extract_year(stat, year):
    stat = Counter()
    for name in stat[year][0]:
        stat[name] += stat[year][0][name]
    for name in stat[year][1]:
        stat[name] += stat[year][1][name]
    return sorted(stat.items(), key=itemgetter(1), reverse=True)


def extract_year_male(stat, year):
    stat = Counter()
    for name in stat[year][0]:
        stat[name] += stat[year][0][name]
    return sorted(stat.items(), key=itemgetter(1), reverse=True)


def extract_year_female(stat, year):
    stat = Counter()
    for name in stat[year][1]:
        stat[name] += stat[year][1][name]
    return sorted(stat.items(), key=itemgetter(1), reverse=True)


if __name__ == '__main__':
    pass
