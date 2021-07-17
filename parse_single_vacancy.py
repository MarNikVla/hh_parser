"""
    Module contain functions for parsing single vacancy from hh.ru
"""

import unicodedata
from bs4 import BeautifulSoup
import requests
from codetiming import Timer

# establishing session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
})


# Take vacancy url, return dict with
# dict.keys = (title', 'key_skills', 'salary'. 'description'. 'link')
def parse_single_vacancy(url) -> dict:
    data = dict()
    text = session.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.find("h1", {'class': ['bloko-header-1'], 'data-qa': ['vacancy-title']}).text
    key_skills = ' '.join([x.get_text() for x in soup.find_all("div", {
        'class': ['skills-element', 'bloko-tag', 'bloko-tag_inline']})])
    salary = soup.find("p", {'class': ['vacancy-salary']}).text
    description = soup.find("div",
                            {'data-qa': ['vacancy-description']}).text or None

    data.update({
        'title': unicodedata.normalize("NFKD", title),
        'key_skills': unicodedata.normalize("NFKD", key_skills),
        'salary': unicodedata.normalize("NFKD", salary),
        'description': unicodedata.normalize("NFKD", description),
        'link': url,
    })
    return data


# if __name__ == '__main__':
#     t = Timer()
#     t.start()
#     parse_single_vacancy('https://hh.ru/vacancy/41892897')
#     t.stop()
