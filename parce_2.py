import sys
import re


def slowesrtPG(page, _TIME_):
    if _STATS_["SlowestPage"][1] <= _TIME_:
        _STATS_["SlowestPage"] = (page, _TIME_)


def fastest_page(page, _TIME_):
    if _STATS_["FastestPage"][0] is None:
        _STATS_["FastestPage"] = (page, _TIME_)
    else:
        if _STATS_["FastestPage"][1] >= _TIME_:
            _STATS_["FastestPage"] = (page, _TIME_)


def get_day_miser(day):
    max_value = 0
    _ANSWER_ = ""
    for key in _STATS_["MostActiveClientByDay"][day]:
        value = _STATS_["MostActiveClientByDay"][day][key]
        if value >= max_value:
            if value > max_value:
                max_value = value
                _ANSWER_ = key
            else:
                if key < _ANSWER_:
                    _ANSWER_ = key
    return _ANSWER_


def date_converter(_DATE_):
    pars = _DATE_.split("/")
    return '-'.join([pars[2], _MONTHS_[pars[1]], pars[0]])


def slowesrtPG_average(page, _TIME_):
    time_res, count = _STATS_["SlowestAveragePage"].get(page, (0, 0))
    time_res = (time_res * count + _TIME_) / (count + 1)
    _STATS_["SlowestAveragePage"][page] = (time_res, count + 1)


def get_slowesrtPG_avg():
    max_value = 0
    _ANSWER_ = ""
    for key in _STATS_["SlowestAveragePage"]:
        if _STATS_["SlowestAveragePage"][key][0] > max_value:
            max_value = _STATS_["SlowestAveragePage"][key][0]
            _ANSWER_ = key
    return _ANSWER_


def most_popular(stat, page):
    _STATS_[stat][page] = \
        _STATS_[stat].get(page, 0) + 1


def get_mp(stat):
    max_value = 0
    _ANSWER_ = ""
    for key in _STATS_[stat]:
        value = _STATS_[stat][key]
        if value >= max_value:
            if value > max_value:
                max_value = value
                _ANSWER_ = key
            else:
                if key < _ANSWER_:
                    _ANSWER_ = key
    return _ANSWER_


def active_most_day(day, user):
    if day not in _STATS_["MostActiveClientByDay"]:
        _STATS_["MostActiveClientByDay"][day] = {}
    count = _STATS_["MostActiveClientByDay"][day].get(user, 0)
    _STATS_["MostActiveClientByDay"][day][user] = count + 1


def goprint():
    date_s = []
    new_date_s = []
    for key in _STATS_["MostActiveClientByDay"]:
        date_s.append((key, get_day_miser(key)))
    for key, value in sorted(date_s, key=lambda x: x[0]):
        new_date_s.append(str.format("{0}: {1}", key, value))

    print(str.format(
        """FastestPage: {0}
    MostActiveClient: {1}
    MostActiveClientByDay: {2}
    MostPopular_BROWSER_: {3}
    MostPopularPage: {4}
    SlowestAveragePage: {5}
    SlowestPage: {6}""",
        _STATS_["FastestPage"][0],
        get_mp("MostActiveClient"),
        '\n  '.join(new_date_s),
        get_mp("MostPopular_BROWSER_"),
        get_mp("MostPopularPage"),
        get_slowesrtPG_avg(),
        _STATS_["SlowestPage"][0]
    ))


def main():
    _STATS_["FastestPage"] = (None, 0)
    _STATS_["SlowestPage"] = (None, 0)
    _STATS_["MostActiveClient"] = {}
    _STATS_["MostActiveClientByDay"] = {}
    _STATS_["MostPopular_BROWSER_"] = {}
    _STATS_["MostPopularPage"] = {}
    _STATS_["SlowestAveragePage"] = {}

    for _LINE_ in sys.stdin:
        pars = re.search(_LINE_, _LINE_)
        if pars is None:
            continue
        _IP_adress = pars.group(1)
        _DATE_ = pars.group(2).split(':')[0]
        _QUERY_ = pars.group(3).split(' ')
        if _QUERY_[0] not in _REAL_QUERIES_:
            continue
        _BROWSER_ = pars.group(7)
        if pars.group(8) is not None:
            _TIME_ = int(pars.group(8)[1:])
            slowesrtPG(_QUERY_[1], _TIME_)
            fastest_page(_QUERY_[1], _TIME_)
            slowesrtPG_average(_QUERY_[1], _TIME_)
        most_popular("MostPopularPage", _QUERY_[1])
        most_popular("MostActiveClient", _IP_adress)
        most_popular("MostPopular_BROWSER_", _BROWSER_)
        active_most_day(date_converter(_DATE_), _IP_adress)

    goprint()


if __name__ == '__main__':
    main()

_IP_ = r'(\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}) - - '
_DATE_ = r'\[(\d{2}\/\w{3}\/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] '
_QUERY_ = r'"([A-Z]{3,7} [^"]*") '
_ANSWER_ = r'(\d{3}) '
_BYTES_ = r'(\d*) '
_REFERRER_ = r'"([^"]*)" '
_BROWSER_ = r'"([^"]*)"'
_TIME_ = r'( \d*)?'
_LINE_ = re.compile(_IP_ + _DATE_ + _QUERY_ +
                    _ANSWER_ + _BYTES_ + _REFERRER_ + _BROWSER_ + _TIME_)
_REAL_QUERIES_ = ["GET", "PUT", "POST", "HEAD", "OPTIONS", "DELETE"]
_MONTHS_ = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
            'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10',
            'Nov': '11', 'Dec': "12"}
_STATS_ = {}
