from typing import List, Dict, Any

from bs4 import BeautifulSoup
import requests

# establishing session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
})

HH_PATTERN_HTML = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2' \
                  '&clusters=true' \
                  '&enable_snippets=true&text={vacation}&page={page}'


def get_html(vacancy: str, page: int = 0) -> str:
    url = HH_PATTERN_HTML.format(
        page=page, vacation=vacancy)
    html = session.get(url).text
    return html


def parse_vacancy(vacancy: str, page: int = None) -> List[Dict[str, Any]]:
    data = []
    # print(page)
    text = get_html(vacancy=vacancy, page=page)
    soup = BeautifulSoup(text, 'html.parser')
    vacancies_list = soup.find_all("div",
                                  {'class': ['vacancy-serp-item', 'vacancy-serp-item_premium']})

    for item in vacancies_list:
        vacancy_link = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).get('href')
        vacancy_desc = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).text
        vacancy_link_strip_query = vacancy_link.partition('?query')[0]
        data.append({
            'vacancy': vacancy_desc,
            'vacancy_link': vacancy_link_strip_query,
        })
    return data


def get_last_page(vacancy) -> int:
    first_page = get_html(vacancy)
    soup = BeautifulSoup(first_page, 'html.parser')
    last_page = soup.find_all("a",
                              {'class': ['bloko-button', 'HH-Pager-Control']})[-2].get_text()
    return int(last_page)


def url_of_vacancies_to_list(vacancy: str, amount_pages: int = 3) -> List[str]:
    csv_columns = ['vacancy', 'vacancy_link']
    if amount_pages:
        last_page = amount_pages
    else:
        last_page = get_last_page(vacancy)

    list_of_urls = list()
    for page in range(last_page):
        data = parse_vacancy(vacancy, page)
        # print(data)
        for item in data:
            list_of_urls.append(item['vacancy_link'])
        # for item in data:
        #     writer.writerow(item)

    return list_of_urls


if __name__ == '__main__':
    pass
    # t = Timer()
    # t.start()
    # print(url_of_vacancies_to_list('программист', amount_pages=2))
    # t.stop()
