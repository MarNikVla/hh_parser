"""
    Module only for exercise, not used in main.py script
    but works for async writing ['vacancy', 'vacancy_link'] to csv file
"""

import asyncio
import csv
from pathlib import Path
from typing import TextIO, List

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from codetiming import Timer

TIMER = Timer()
HH_PATTERN_HTML = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2' \
                  '&clusters=true' \
                  '&enable_snippets=true&text={vacancy}&page={page}'


async def get_html(session: ClientSession, vacancy: str, page: int) -> str:
    url = HH_PATTERN_HTML.format(page=page, vacancy=vacancy)
    async with session.get(url, ssl=False) as res:
        return await res.text()

# Parse hh.ru html_page to list ['vacancy', 'vacancy_link']
def parse_vacancy_page(html_page: str) -> List:
    data = []
    soup = BeautifulSoup(html_page, 'html.parser')
    vacancy_list = soup.find_all("div",
                                  {'class': ['vacancy-serp-item', 'vacancy-serp-item_premium']})
    for item in vacancy_list:
        vacancy_link = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).get('href')
        vacancy_desc = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).text
        vacancy_link_strip_query = vacancy_link.partition('?query')[0]
        data.append({
            'vacancy': vacancy_desc,
            'vacancy_link': vacancy_link_strip_query,
        })
    return data


async def get_last_page(session: ClientSession, vacancy: str) -> int:
    first_page = await get_html(session, vacancy, page=0)
    soup = BeautifulSoup(first_page, 'html.parser')
    last_page = soup.find_all("a",
                              {'class': ['bloko-button', 'HH-Pager-Control']})[-2].get_text()
    return int(last_page)


def write_vacancy_to_csv(file: TextIO, data: List) -> None:
    csv_columns = ['vacancy', 'vacancy_link']
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    for item in data:
        writer.writerow(item)

# Main logic is here
async def main(vacancy: str, path_to_save: str = 'test', page: int = None) -> None:
    async with ClientSession() as session:
        if page:
            last_page = page
        else:
            last_page = await get_last_page(session, vacancy)

        path_dir = path_to_save
        file_name = f'{vacancy}_async.csv'
        Path(path_dir).mkdir(parents=True, exist_ok=True)
        path_to_write = Path(path_dir, file_name)

        with open(path_to_write, 'w', newline='', encoding='utf-8') as output_file:
            for future in asyncio.as_completed([get_html(session, vacancy, page) for page in
                                                range(last_page)]):
                parse_result = parse_vacancy_page(await future)
                write_vacancy_to_csv(output_file, parse_result)
        return print('Done')


# The example below works
TIMER.start()
loop = asyncio.get_event_loop()
loop.run_until_complete(main('программист',  page=3))
TIMER.stop()
