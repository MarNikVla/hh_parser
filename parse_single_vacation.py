import unicodedata

from bs4 import BeautifulSoup
import requests
import csv
from codetiming import Timer

# establishing session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
})

url = 'https://hh.ru/vacancy/41892897'


def get_html(url):
    print('fdf')
    html = session.get(url).text
    return html


def parse_single_vacation(url):
    data = []
    # print(page)'
    text = get_html(url=url)
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.find("h1", {'class': ['bloko-header-1'], 'data-qa': ['vacancy-title']}).text
    key_skills = ' '.join([x.get_text() for x in
                           soup.find_all("div", {
                               'class': ['skills-element', 'bloko-tag', 'bloko-tag_inline']})])
    salary_raw = soup.find("p", {'class': ['vacancy-salary']}).text
    salary = unicodedata.normalize("NFKD", salary_raw)
    description = soup.find("div", {
        'class': ['g-user-content'], 'data-qa':['vacancy-description']}).text

    print('sdf')

    data.append({
        'title': title,
        'key_skills': key_skills,
        'salary': salary,
        'description': description,
        'link': url,
    })
    print(data)
    return data


if __name__ == '__main__':
    t = Timer()
    t.start()
    parse_single_vacation(url)
    t.stop()
