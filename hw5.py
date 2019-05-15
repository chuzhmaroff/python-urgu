#!/usr/bin/env python3
import unittest
import urllib.request
import sys
import re
import datetime
import collections


def get_date(date_string):
    try:
        date = datetime.datetime.strptime(date_string, '%d/%b/%Y').date()
        return date
    except ValueError:
        return None


class ParsedLine:
    def __init__(self, page_speed, page_link, user, browser, date):
        self.page_speed = page_speed
        self.page_link = page_link
        self.user = user
        self.browser = browser
        self.date = date


class Statistic:
    def __init__(self):
        self.page_speed = SpeedPages()
        self.page_speed_average = {}
        self.popular_page = {}
        self.active_user = {}
        self.popular_browser = {}
        self.user_day_activity = {}

    def freq_stat(self, parsed_line):
        if parsed_line.page_link not in self.popular_page:
            self.popular_page[parsed_line.page_link] = 0
        self.popular_page[parsed_line.page_link] += 1

        if parsed_line.user not in self.active_user:
            self.active_user[parsed_line.user] = 0
        self.active_user[parsed_line.user] += 1

        if parsed_line.browser not in self.popular_browser:
            self.popular_browser[parsed_line.browser] = 0
        self.popular_browser[parsed_line.browser] += 1

    def page_speed_stat(self, parsed_line):
        if parsed_line.page_speed is None:
            return
        time = parsed_line.page_speed
        prev_page = self.page_speed
        current_page = (parsed_line.page_link, time)
        if time <= prev_page.fastest[1]:
            prev_page.fastest = current_page
        if time >= prev_page.slowest[1]:
            prev_page.slowest = current_page

        if current_page not in self.page_speed_average:
            self.page_speed_average[current_page[0]] = (time, 1)
        else:
            prev = self.page_speed_average[current_page[0]]
            self.page_speed_average[current_page[0]] = (
                prev[0] + time,
                prev[1] + 1)

    def activity_day_user(self, parsed_line):
        if parsed_line.date not in self.user_day_activity:
            self.user_day_activity[parsed_line.date] = collections.Counter()
        self.user_day_activity[parsed_line.date][parsed_line.user] += 1

    def add_line(self, line):
        parsed_line = lineParce(line)
        if parsed_line is None:
            return
        self.freq_stat(parsed_line)
        self.page_speed_stat(parsed_line)
        self.activity_day_user(parsed_line)

    def results(self):
        return FinalStat(self).__dict__


class FinalStat:
    def __init__(self, stat):
        if stat.active_user == {}:
            return
        self.FastestPage = stat.page_speed.fastest[0]
        self.MostActiveClient = sorted_most(stat.active_user)
        self.MostActiveClientByDay = {}
        sort_days = sorted(stat.user_day_activity.keys())
        for day in sort_days:
            self.MostActiveClientByDay[day] = sorted_most(
                stat.user_day_activity[day])
        self.MostPopularBrowser = sorted_most(stat.popular_browser)
        self.MostPopularPage = sorted_most(stat.popular_page)
        self.SlowestAveragePage = get_max_average(stat.page_speed_average)[0]
        self.SlowestPage = stat.page_speed.slowest[0]

    def print_result(self):
        print('FastestPage: ', self.FastestPage)
        print('MostActiveClient: ', self.MostActiveClient)
        print('MostActiveClientByDay: ')
        for day in self.MostActiveClientByDay:
            print(f"  {day}: {self.MostActiveClientByDay[day]}")
        print('\nMostPopularBrowser: ', self.MostPopularBrowser)
        print('MostPopularPage: ', self.MostPopularPage)
        print('SlowestAveragePage: ', self.SlowestAveragePage)
        print('SlowestPage: ', self.SlowestPage)


def sorted_most(dictionary):
    sorted_stat = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    first_item = sorted_stat[0]
    same_values = {x for x in sorted_stat if x[1] == first_item[1]}
    return sorted(same_values, key=lambda x: x[0], reverse=False)[0][0]


def get_max_average(dictionary):
    for page in dictionary:
        dictionary[page] = dictionary[page][0] / dictionary[page][1]
    maximum = ('temp', 0.0)
    for page in dictionary:
        if dictionary[page] >= maximum[1]:
            maximum = (page, dictionary[page])
    return maximum


class SpeedPages:
    def __init__(self):
        self.fastest = ('default', float('inf'))
        self.slowest = ('default', -1)


def lineParce(line):
    pattern = re.compile(
        r"""^((?:\d{1,3}\.){3}\d{1,3})
                \s-\s-\s
                \[(\d{1,2}/[A-Za-z]{1,3}/\d{4})
                :\d{2}:\d{2}:\d{2}\s[+\-]\d{4}\]
                \s"(?:GET|PUT|POST|HEAD|OPTIONS|DELETE)\s
                (/(?:/|\w|\*|'|\(|\)|;|:|@|&|=
                |\+|\$|,|\?|\#|\[|\]|-|_|\.|~
                |!|"|%|<|>|^|`|{|\}|\|)+?)
                \s(?:\w|\.|/){3,}?"\s\d+?\s\d+?\s".+?"\s
                "(.+?)"
                \s?(\d*)
                 """,
        re.VERBOSE)

    info = pattern.search(line)
    if info is None:
        return None

    time = int(info.group(5)) if info.group(5) is not '' \
        else None

    date = get_date(info.group(2))
    if date is None:
        return None

    for ip in info.group(1).split('.'):
        if int(ip) > 255:
            return None

    return ParsedLine(
        time,
        info.group(3),
        info.group(1),
        info.group(4),
        date)


def make_stat():
    return Statistic()


def main(source):
    for link in source:
        stat = make_stat()
        with urllib.request.urlopen(link) as file:
            for line in file:
                stat.add_line(line)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


class LogStatTests(unittest.TestCase):
    unittest.TestCase.maxDiff = None

    def test_empty_log(self):
        parser = ParseLog()
        parser.add_line('')
        result = parser.results()
        self.assertEqual(result, {'FastestPage': '',
                                  'MostActiveClient': '',
                                  'MostActiveClientByDay': {},
                                  'MostPopularBrowser': '',
                                  'MostPopularPage': '',
                                  'SlowestAveragePage': '',
                                  'SlowestPage': ''})

    def test_date_processing(self):
        date = '29/Jan/1997'
        self.assertEqual(datetime.date(1997, 1, 29), get_date(date))

    def test_wrong_date_processing(self):
        date = '29/Feb/2001'
        self.assertEqual(None, get_date(date))

    def test_parse_wrong_ip(self):
        line = '192.168.345.70 - - [15/Jan/2013:19:48:05 +0600] "GET ' \
               + '/tv/useUser HTTP/1.1" 200 431 "http://call" "Opera/9.80" 101'
        self.assertEqual(None, lineParce(line))

    def test_simple_speed_parse(self):
        self.assertEqual(10178, lineParce(self.line).page_speed)

    def test_simple_browser_parse(self):
        self.assertEqual("Opera/2.28", lineParce(self.line).browser)

    def test_get_max_average(self):
        stat = {"one": (25, 5), "two": (16, 4), "three": (36, 6)}
        self.assertEqual(("three", 6), get_max_average(stat))

    def test_simple_link_parse(self):
        self.assertEqual("/tv/useUser", lineParce(self.line).page_link)

    def test_incorrect_log(self):
        parser = ParseLog()
        parser.add_line('kukareku - Bajukov 9| teb9| lublu <3')
        self.assertEqual(parser.fastest_page[0], '')
        self.assertEqual(parser.most_active_clients[0], '')
        self.assertEqual(parser.most_popular_browser[0], '')
        self.assertEqual(parser.most_popular_pages[0], '')
        self.assertEqual(parser.slowest_page[0], '')
