import timeit
import sys
import re
import datetime
import collections


def main():
    stat = {
        'page_speed': {
            'fastest': ('default', float("inf")),
            'slowest': ('default', -1)},
        'page_speed_average': {},
        'popular_page': collections.Counter(),
        'active_user': collections.Counter(),
        'popular_browser': collections.Counter(),
        'active_user_by_day': {}
    }
    for line in sys.stdin:
        element = parse(line)
        if element is not None:
            do_all(element, stat)
    find_average(stat['page_speed_average'])
    print_result(stat)


def parse(line):
    pattern = re.compile(
        r"""^((?:\d{1,3}\.){3}\d{1,3})#userID, group1
                \s-\s-\s
                \[(\d{1,2}/[A-Za-z]{1,3}/\d{4})  #date, group2
                :\d{2}:\d{2}:\d{2}\s[+\-]\d{4}\]
                \s"(?:GET|PUT|POST|HEAD|OPTIONS|DELETE)\s
                (/(?:/|\w|\*|'|\(|\)|;|:|@|&|=
                |\+|\$|,|\?|\#|\[|\]|-|_|\.|~
                |!|"|%|<|>|^|`|{|\}|\|)+?)      #page, group3
                \s(?:\w|\.|/){3,}?"\s\d+?\s\d+?\s".+?"\s
                "(.+?)"                          #browser, group4
                \s?(\d*)                         #time of processing, group5
                 """,
        re.VERBOSE)

    info = pattern.search(line)
    if info is None:
        return None
    time = int(info.group(5)) or -1

    try:
        date = get_date(info.group(2))
    except Exception:
        return None

    for ip in info.group(1).split('.'):
        if int(ip) > 255:
            return None

    return {
        'page_speed': (info.group(3), time),
        'popular_page': info.group(3),
        'active_user': info.group(1),
        'popular_browser': info.group(4),
        'active_user_by_day': (info.group(1), date)
    }


def print_result(stat):
    print("FastestPage: {0}".format(stat['page_speed']['fastest'][0]))
    print("MostActiveClient: {0}".format(
        stat['active_user'].most_common(1)[0][0]))
    print("MostActiveClientByDay:")
    for day in sort_keys(stat['active_user_by_day']):
        print("  {0}: {1}".format(
            day, stat['active_user_by_day'][day].most_common(1)[0][0]))
    print("\nMostPopularBrowser: {0}".format(
        stat['popular_browser'].most_common(1)[0][0]))
    print("MostPopularPage: {0}".format(
        stat['popular_page'].most_common(1)[0][0]))
    print("SlowestAveragePage: {0}".format(
        find_slowest_average(stat['page_speed_average'])[0]))
    print("SlowestPage: {0}".format(stat['page_speed']['slowest'][0]))


def get_date(date_string):
    date = datetime.datetime.strptime(date_string, '%d/%b/%Y')
    return date.strftime('%Y-%m-%d')


def do_all(parsed_line, stat):
    frequency_stat(parsed_line, stat)
    page_speed_stat(parsed_line, stat)
    active_user_by_day(parsed_line, stat)


def frequency_stat(parsed_line, stat):
    stat['popular_page'][parsed_line['popular_page']] += 1
    stat['active_user'][parsed_line['active_user']] += 1
    stat['popular_browser'][parsed_line['popular_browser']] += 1


def page_speed_stat(parsed_line, stat):
    if parsed_line['page_speed'][1] != -1:
        current_page = parsed_line['page_speed']
        current_time = current_page[1]
        previous_page = stat['page_speed']
        if current_time <= previous_page['fastest'][1]:
            previous_page['fastest'] = current_page
        if current_time >= previous_page['slowest'][1]:
            previous_page['slowest'] = current_page

        if current_page not in stat['page_speed_average']:
            stat['page_speed_average'][current_page[0]] = (current_time, 1)
        else:
            prev = stat['page_speed_average'][current_page[0]]
            stat['page_speed_average'][current_page[0]] = (
                prev[0] + current_time, prev[1] + 1)


def active_user_by_day(parsed_line, stat):
    user_ip, day = parsed_line['active_user_by_day']
    if day not in stat['active_user_by_day']:
        stat['active_user_by_day'][day] = collections.Counter()
    stat['active_user_by_day'][day][user_ip] += 1


def find_average(stat):
    for page in stat:
        stat[page] = stat[page][0] / stat[page][1]


def find_slowest_average(stat):
    maximum = ('default', -1)
    for page in stat:
        if stat[page] >= maximum[1]:
            maximum = (page, stat[page])
    return maximum


def sort_keys(dictionary):
    return sorted(dictionary.keys())


if __name__ == '__main__':
    main()
