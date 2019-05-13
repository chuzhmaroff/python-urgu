#!/usr/bin/env python3

from urllib.request import urlopen
from urllib.parse import quote, unquote
from urllib.error import URLError, HTTPError
import re


def get_content(name):
    try:
        with urlopen('http://ru.wikipedia.org/wiki/' + quote(name)) as page:
            content = page.read().decode('utf-8', errors='errors')
    except (URLError, HTTPError):
        return None
    return content


def extract_content(page):
    if page is None:
        return 0, 0
    if page is not None:
        body = page.find("<div id=\"bodyContent\"")
        vis = page.find("<div class=\"visualClear\"")
        return body, vis


def extract_links(page, begin, end):
    compile = re.compile(r'["\']/wiki/([\w%]+?)["\']', re.IGNORECASE)
    allLinks = re.finditer(compile, page[begin:end])
    result = []
    for link in allLinks:
        if not link.group(1) in result:
            result.append(unquote(link.group(1)))
    return result


def find_chain(start, finish):
    jump = []
    if start == finish:
        return [start]
    while finish not in jump:
        page = get_content(start)
        if page is None:
            return None
        else:
            jump.append(start)
        begin, end = extract_content(page)
        links = extract_links(page, begin, end)
        if finish in links:
            jump.append(finish)
            return jump
        else:
            for link in links:
                if link in jump:
                    continue
                else:
                    start = link
                    break


def main():
    pass


if __name__ == '__main__':
    main()
