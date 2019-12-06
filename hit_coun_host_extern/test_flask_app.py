import sqlite3
import unittest

import flask_app as app


def read_db_n_unique_day(value_non_unique_day):
    result = ""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for x in cursor.execute("SELECT count() FROM USER_INFO "
                            "WHERE DATE = {}".format(value_non_unique_day)):
        result += str(x)
    return result


def read_db_non_unique_all():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = ""
    for x in cursor.execute("SELECT count() FROM USER_INFO"):
        result += str(x)
    return result


class TestMethodApp(unittest.TestCase):
    def test_count_user_for_cookie(self):
        with open("count_unique_user_for_cookie.txt", "r") as f:
            count_do = int(f.read())
        app.count_unique_user_for_cookie()
        with open("count_unique_user_for_cookie.txt", "r") as f:
            count_od = int(f.read())
        self.assertNotEqual(count_do, count_od)
        self.assertTrue(type(count_do) == int)
        self.assertTrue(type(count_od) == int)

    def test_count_user_for_ip(self):
        with open("count_unique_user_for_ip.txt", "r") as f:
            count_do = int(f.read())
        app.count_unique_user_for_ip()
        with open("count_unique_user_for_ip.txt", "r") as f:
            count_od = int(f.read())
        self.assertNotEqual(count_do, count_od)
        self.assertTrue(type(count_do) == int)
        self.assertTrue(type(count_od) == int)

    def test_hello_world(self):
        txt = "Server importthis.pythonanywhere.com"
        self.assertIsNotNone(app.hello_world())
        self.assertTrue(isinstance(app.hello_world(), str))
        self.assertTrue(len(app.hello_world()) == len(txt))
        self.assertTrue(app.hello_world() == txt)

    def test_get_bool_its_none_cookies(self):
        user_agent = "Google Chrome"
        user_cookies_true = "{}"
        user_cookies = app.create_unique_cookie_for_user(user_agent)
        self.assertFalse(app.get_bool_its_none_cookies(user_cookies))
        self.assertTrue(app.get_bool_its_none_cookies(user_cookies_true))

    """def test_get_ip_address(self):
        a = app.get_ip_address()
        self.assertIsNotNone(a)"""

    def test_get_unique_cookies(self):
        user_agent = "Google Chrome"
        self.assertIsNotNone(app.create_unique_cookie_for_user(user_agent))
        self.assertTrue(
            type(app.create_unique_cookie_for_user(user_agent)) == str)

    def test_get_count_non_unique_user(self):
        self.assertTrue(type(app.get_count_non_unique_user()) == str)
        self.assertIsNotNone(app.get_count_non_unique_user())

    def test_get_info_on_ip(self):
        ip_address = "212.193.78.236"
        self.assertIsNotNone(app.get_info_on_ip(ip_address))
        self.assertTrue(type(app.get_info_on_ip(ip_address)) == str)

    def test_adding_last_conn_to_txt(self):
        with open('info_last_conn_07112019.txt', 'r') as f:
            text_before = f.read()

        cookies = app.create_unique_cookie_for_user("Google")
        ip_address = "212.193.78.236"

        app.add_user_at_databases(ip_address, cookies)
        app.adding_last_conn_to_txt()
        with open('info_last_conn_07112019.txt', 'r') as f:
            text_after = f.read()
        self.assertNotEqual(text_after, text_before)

    def test_get_coordinates_ip(self):
        ip_address = "212.193.78.236"
        lat = app.get_coordinates_ip(ip_address)[0]
        lon = app.get_coordinates_ip(ip_address)[1]
        self.assertNotEqual(lat, lon)
        self.assertTrue(type(lat) == float)
        self.assertTrue(type(lon) == float)

    def test_do_read(self):
        path = "text_file_for_test.txt"
        res = app.do_read(path)
        self.assertEqual(type(res), str)

    def test_get_bool_unique_ip(self):
        ip_address = "212.193.78.234"  # ip address urfu Turgeneva 4
        result = app.get_bool_unique_ip(ip_address)
        self.assertEqual(result, False)
        # self.assertTrue(result == bool)

    def test_create_unique_cookie_for_user(self):
        user_agent = "Google Chrome_v1"
        user_agent2 = "Google Chrome_v2"
        user_agent3 = "Yandex Browser"
        hash1 = app.create_unique_cookie_for_user(user_agent)
        hash2 = app.create_unique_cookie_for_user(user_agent2)
        hash3 = app.create_unique_cookie_for_user(user_agent3)
        self.assertIsNotNone(hash1)
        self.assertIsNotNone(hash2)
        self.assertIsNotNone(hash3)
        self.assertNotEqual(hash1, hash2)
        self.assertNotEqual(hash2, hash3)
        self.assertNotEqual(hash1, hash2, hash3)

    def test_calculate_api(self):
        path_c_unique_ip = "count_unique_user_for_ip.txt"
        path_c_unique_cookie = "count_unique_user_for_cookie.txt"
        _count_unique_user_for_ip = app.do_read(path_c_unique_ip)
        _count_unique_cookie = app.do_read(path_c_unique_cookie)
        _value_non_unique_day = "191107"  # 15
        self.assertTrue(
            app.calculation_api("ip", "", "") == _count_unique_user_for_ip)
        self.assertTrue(
            app.calculation_api("cookie", "", "") == _count_unique_cookie)
        self.assertTrue(app.calculation_api("", _value_non_unique_day, "") ==
                        read_db_n_unique_day(_value_non_unique_day))
        self.assertTrue(app.calculation_api("", None, "") ==
                        read_db_non_unique_all())
