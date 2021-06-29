from bs4 import BeautifulSoup
import requests
import csv
from codetiming import Timer
from pathlib import Path

# establishing session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
})

HH_PATTERN_HTML = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2' \
                  '&clusters=true' \
                  '&enable_snippets=true&text={vacation}&page={page}'


def get_html(vacation, page=0):
    url = HH_PATTERN_HTML.format(
        page=page, vacation=vacation)
    html = session.get(url).text
    return html


def parse_vacation(vacation, page=None):
    data = []
    # print(page)
    text = get_html(vacation=vacation, page=page)
    soup = BeautifulSoup(text, 'html.parser')
    vacation_list = soup.find_all("div",
                                  {'class': ['vacancy-serp-item', 'vacancy-serp-item_premium']})

    for item in vacation_list:
        vacation_link = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).get('href')
        vacation_desc = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).text
        vacation_link_strip_query = vacation_link.partition('?query')[0]
        data.append({
            'vacation': vacation_desc,
            'vacation_link': vacation_link_strip_query,
        })
    return data


def get_last_page(vacation) -> int:
    first_page = get_html(vacation, page=0)
    soup = BeautifulSoup(first_page, 'html.parser')
    last_page = soup.find_all("a",
                              {'class': ['bloko-button', 'HH-Pager-Control']})[-2].get_text()
    return int(last_page)


def list_of_vacation_to_csv(vacation, path_to_save:str = 'test',  page=None):
    csv_columns = ['vacation', 'vacation_link']
    if page:
        last_page = page
    else:
        last_page = get_last_page(vacation)

    path_dir = path_to_save
    file_name = f'{vacation}_sync.csv'
    Path(path_dir).mkdir(parents=True, exist_ok=True)
    path_to_write = Path(path_dir, file_name)

    with open(path_to_write, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=csv_columns)
        for page in range(last_page):
            data = parse_vacation(vacation, page)
            for item in data:
                writer.writerow(item)

    return print('Done')


if __name__ == '__main__':
    t = Timer()
    t.start()
    list_of_vacation_to_csv('программист', page=6)
    t.stop()
