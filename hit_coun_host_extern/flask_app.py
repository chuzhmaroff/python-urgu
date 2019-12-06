import hashlib
import sqlite3
from datetime import datetime

import requests
from flask import Flask, render_template, make_response, request, send_file

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Server importthis.pythonanywhere.com'


@app.route('/upload', methods=['GET', 'POST'])
def main():
    res = send_file("1pic_stat.png", mimetype='image/gif')
    if not get_bool_unique_ip(get_ip_address()):
        count_unique_user_for_ip()
    if get_bool_its_none_cookies(str(request.cookies)):
        count_unique_user_for_cookie()
        new_cookie = create_unique_cookie_for_user(str(request.user_agent))
        res.set_cookie('chzmrff-id-image-cookie', new_cookie,
                       max_age=60 * 60 * 24 * 365 * 4)  # 4 years
        add_user_at_databases(get_ip_address(), new_cookie)
        return res
    else:  # у него уже есть куки от нашего сайта
        add_user_at_databases(get_ip_address(), str(request.cookies))
        return res


@app.route('/api', methods=['GET'])
def api():
    if request.method == "GET":
        return calculation_api(request.args.get("unique"),
                               request.args.get("non_unique_day"),
                               request.args.get("non_unique_all"))
    return "serverimportthis.com"


@app.route("/stat", methods=['GET', 'POST'])
def stat():
    kastil = cookie = do_read("count_unique_user_for_cookie.txt")
    adding_last_conn_to_txt()
    r = render_template("stat.html", date=str(datetime.now()),
                        count_user=get_count_non_unique_user(),
                        c_unique_ip=do_read("count_unique_user_for_ip.txt"),
                        c_unique_cookie=kastil,  # Я исправлю это, честно
                        ip_address=get_ip_address(),
                        cookies=request.cookies,
                        user_agent=request.user_agent,
                        accept_lang=request.accept_languages,
                        full_info_geo=get_info_on_ip(get_ip_address()),
                        lat=get_coordinates_ip(get_ip_address())[0],
                        lon=get_coordinates_ip(get_ip_address())[1])
    return r


def calculation_api(value_unique, value_non_unique_day, value_non_unique_all):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = ""
    if value_unique == "ip":
        return do_read("count_unique_user_for_ip.txt")
    if value_unique == "cookie":
        return do_read("count_unique_user_for_cookie.txt")
    if type(value_non_unique_day) == str and value_non_unique_day != "":
        for x in cursor.execute("SELECT count() FROM USER_INFO "
                                "WHERE DATE={}".format(value_non_unique_day)):
            result += str(x)
        return result
    if value_non_unique_all is "":
        for x in cursor.execute("SELECT count() FROM USER_INFO"):
            result += str(x)
        return result
    return make_response(render_template('help_api.html'))


def do_read(path):  # testing
    with open(path, "r") as f:
        res = f.read()
    return res


def get_bool_its_none_cookies(user_cookies):
    if len(user_cookies) == 2 or len(user_cookies) == 77 or \
            len(user_cookies) == 90 or len(user_cookies) == 38:
        return True
    else:
        return False


def get_count_non_unique_user():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    res = ""
    for x in cursor.execute("SELECT count() FROM USER_INFO"):
        res += str(x)
    return res[1:4]


def adding_last_conn_to_txt():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    res = ""
    for line in cursor.execute("SELECT * FROM user_info"):
        res += str(line) + " \n"

    with open('info_last_conn_07112019.txt', 'w') as f:
        result = str(res)
        f.write(result)


def get_info_on_ip(ip):
    info_or_ip = ""
    api = "http://ip-api.com/line/{}?fields=country,countryCode," \
          "region,regionName,city,query".format(ip)
    response = requests.get(api)
    for line in response:
        info_or_ip += str(line)
    return info_or_ip


def get_coordinates_ip(ip):
    api = "http://ip-api.com/line/{}?fields=lat,lon".format(ip)
    response = requests.get(api)
    a = ""
    for line in response:
        a += str(line)
    lat = float(a[2:9])
    lon = float(a[11:18])
    return lat, lon


def add_user_at_databases(ip_adress, cookie_for_user):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    ref_time = int(datetime.now().strftime('%y%m%d'))
    user_info = [(str(ip_adress), str(cookie_for_user), ref_time)]
    cursor.executemany("INSERT INTO user_info VALUES (?,?,?)", user_info)
    conn.commit()


def get_bool_unique_ip(ip_adress):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    a = ""
    for x in cursor.execute("SELECT IP_ADRESS FROM USER_INFO"):
        a += str(x)
    if ip_adress in a:
        return True
    else:
        return False


def create_unique_cookie_for_user(user_agent):
    date = str(datetime.now())
    uniq_cookies = str.join(date, user_agent)
    f = hashlib.md5(str(uniq_cookies).encode('utf-8'))
    enter_cookie = f.hexdigest()
    return enter_cookie


def count_unique_user_for_ip():
    with open("count_unique_user_for_ip.txt", "r+") as f:
        count = int(f.read()) + 1
        f.seek(0)
        f.truncate()
        result = str(count)
        f.write(result)


def count_unique_user_for_cookie():
    with open("count_unique_user_for_cookie.txt", "r+") as f:
        count = int(f.read()) + 1
        f.seek(0)
        f.truncate()
        result = str(count)
        f.write(result)


def get_ip_address():
    return str(request.headers.get('X-Real-IP'))


if __name__ == '__main__':
    app.debug = True
    app.run()
