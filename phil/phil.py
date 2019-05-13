from urllib.request import urlopen
from urllib.parse import quote, unquote
from urllib.error import URLError, HTTPError
import re


def get_content(name):
    try:
        with urlopen('http://ru.wikipedia.org/wiki/' + quote(name)) as page:
            content = page.read().decode('utf-8', errors='ignore')
    except (URLError, HTTPError):
        return None
    return content


def extract_content(page):
    if page is None:
        return (0, 0)
    beggining = re.search(r'<div id="mw-content-text"', page).start()
    end = re.search(r'<div id="mw-navigation">', page).start()
    return (beggining, end - 1)


def extract_links(page, begin, end):
    text = re.compile(r'["\']/wiki/([\w%]+?)["\']', re.IGNORECASE)
    allLinks = re.finditer(text, page[begin:end])
    result = []
    for link in allLinks:
        if not link.group(1) in result:
            result.append(unquote(link.group(1)))
    return result


def find_chain(start, finish):
    steps = []
    if start == finish:
        return [start]
    while finish not in steps:
        page = get_content(start)
        if page is None:
            return None
        else:
            steps.append(start)
        begin, end = extract_content(page)
        links = extract_links(page, begin, end)
        if finish in links:
            steps.append(finish)
            return steps
        else:
            for link in links:
                if link in steps:
                    continue
                else:
                    start = link
                    break


if __name__ == '__main__':
    pass
