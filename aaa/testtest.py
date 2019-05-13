import re
from collections import Counter
from operator import itemgetter


def make_stat(filename):
    """
    ������� ��������� ���������� �� ������ �� ������ ��� � ������ ����.
    """
    homeStat = dict()
    file = open(filename, 'r')
    textFile = file.read().splitlines()
    allStat = dict()
    for line in textFile:
        if re.findall('<h3>....</h3>', line):
            year = re.findall('<h3>....</h3>', line)[0][4:8]
            homeStat[year] = [dict(), dict(), allStat]
        if re.findall(r'/>(\w+\w+)', line):
            name = re.findall(r'/>\w+ (\w+)', line)[0]

            if (name[len(name) - 1] == '�' or name[len(name) - 1] == '�' or name == '������') and name != '������' and name != '˸��' and name != '����':
                if homeStat[year][1].setdefault(name) is None:
                    homeStat[year][1][name] = 0
                if homeStat[year][2].setdefault(name) is None:
                    homeStat[year][2][name] = 0
                homeStat[year][2][name] += 1
                homeStat[year][1][name] += 1
            else:
                if homeStat[year][0].setdefault(name) is None:
                    homeStat[year][0][name] = 0
                if homeStat[year][2].setdefault(name) is None:
                    homeStat[year][2][name] = 0
                homeStat[year][2][name] += 1
                homeStat[year][0][name] += 1

    return homeStat


def extract_years(stat):
    """
    ������� ��������� �� ���� ����������� ���������� � ����� ������ �����,
    ������������� �� �����������.
    """
    return sorted(stat.keys())


def extract_general(stat):
    """
    ������� ��������� �� ���� ����������� ���������� � ����� ������ tuple'��
    (���, ����������) ����� ���������� ��� ���� ���.
    ������ ������ ���� ������������ �� �������� ����������.
    """

    sortedStat = sorted(stat['2004'][2].items(), key=itemgetter(1), reverse=True)
    return sortedStat


def extract_general_male(stat):
    """
    ������� ��������� �� ���� ����������� ���������� � ����� ������ tuple'��
    (���, ����������) ����� ���������� ��� ��� ���������.
    ������ ������ ���� ������������ �� �������� ����������.
    """
    sortedStat = Counter()
    for year in stat:
        for name in stat[year][0]:
            sortedStat[name] += stat[year][0][name]
    return sorted(sortedStat.items(), key=itemgetter(1), reverse=True)


def extract_general_female(stat):
    """
    ������� ��������� �� ���� ����������� ���������� � ����� ������ tuple'��
    (���, ����������) ����� ���������� ��� ��� �������.
    ������ ������ ���� ������������ �� �������� ����������.
    """
    sortedStat = Counter()
    for year in stat:
        for name in stat[year][1]:
            sortedStat[name] += stat[year][1][name]
    return sorted(sortedStat.items(), key=itemgetter(1), reverse=True)


def extract_year(stat, year):
    """
    ������� ��������� �� ���� ����������� ���������� � ���.
    ��������� � ������ tuple'�� (���, ����������) ����� ���������� ��� ����
    ��� � ��������� ����.
    ������ ������ ���� ������������ �� �������� ����������.
    """

    sortedStat = Counter()
    for name in stat[year][0]:
        sortedStat[name] += stat[year][0][name]
    for name in stat[year][1]:
        sortedStat[name] += stat[year][1][name]
    return sorted(sortedStat.items(), key=itemgetter(1), reverse=True)


def extract_year_male(stat, year):
    """
    ������� ��������� �� ���� ����������� ���������� � ���.
    ��������� � ������ tuple'�� (���, ����������) ����� ���������� ��� ����
    ��� ��������� � ��������� ����.
    ������ ������ ���� ������������ �� �������� ����������.
    """
    sortedStat = Counter()

    for name in stat[year][0]:
        sortedStat[name] += stat[year][0][name]
    return sorted(sortedStat.items(), key=itemgetter(1), reverse=True)


def extract_year_female(stat, year):
    """
    ������� ��������� �� ���� ����������� ���������� � ���.
    ��������� � ������ tuple'�� (���, ����������) ����� ���������� ��� ����
    ��� ������� � ��������� ����.
    ������ ������ ���� ������������ �� �������� ����������.
    """
    sortedStat = Counter()

    for name in stat[year][1]:
        sortedStat[name] += stat[year][1][name]
    return sorted(sortedStat.items(), key=itemgetter(1), reverse=True)


if __name__ == '__main__':
    pass
