import itertools

from bs4 import BeautifulSoup
import requests
import csv
import pathlib
import asyncio
from codetiming import Timer

import aiohttp

HTML='https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2'\
                             '&clusters=true' \
                             '&enable_snippets=true&text={vacation}&page={page}'

async def get_html(session, vacation, page):
    print('start' + str(page) + vacation)
    url= HTML.format(page=page, vacation= vacation)
    async with session.get(url, ssl=False) as res:
        print('start' + str(page))
        return await res.text()

def parse_vacation(text):
    data = []
    # print(page)
    # text = load_vacancy_page(profession=profession, page=page)
    soup = BeautifulSoup(text, 'html.parser')
    vacation_list = soup.find_all("div",
                                  {'class': ['vacancy-serp-item', 'vacancy-serp-item_premium']})

    for item in vacation_list:
        vacation_link = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).get('href')
        vacation_desc = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).text
        #Обре
        vacation_link_strip_query = vacation_link.partition('?query')[0]
        data.append({
            'vacation': vacation_desc,
            'vacation_link': vacation_link_strip_query,
        })
    return data

async def get_last_page(session, vacation):
    first_page = await get_html(session, vacation, page=0)
    soup = BeautifulSoup(first_page, 'html.parser')
    last_page = soup.find_all("a",
                                  {'class': ['bloko-button', 'HH-Pager-Control']})[-2].get_text()
    print(type(first_page))
    return last_page


async def get_all_pages(vacation):
    async with aiohttp.ClientSession() as session:
        last_page = await get_last_page(session, vacation)
        # first_page = await get_html(session, vacation, page=0)

        print(last_page)
        # pages = [i for i in range(page)]
        # # print(pages)
        # # urls = [HTML.format(page=page, profession=vacation) for page in pages]
        #
        # res= await asyncio.gather(*map(get_html, itertools.repeat(session), itertools.repeat(vacation), pages))
        # return res


# async def main(page, profession):
#     async with aiohttp.ClientSession() as session:
#         pages = [i for i in range(page)]
#         # print(pages)
#
#
#         res= await asyncio.gather(*map(get_html, itertools.repeat(session), pages))
#         return res
        # result = []
        # for item in res:
        #     result.append(parse_vacation(item))
        #     print(len(parse_vacation(item)))


        # for item in enumerate(res):
        #     with open(f'test{item[0]}.html', 'w', encoding='utf-8') as output_file:
        #         output_file.write(item[1])

        # with open('test.csv', 'a', newline='', encoding='utf-8') as output_file:
        #     # data = parse_vacation(profession, page=page)
        #     writer = csv.DictWriter(output_file, fieldnames=csv_columns)
        #     # writer.writeheader()
        #     for item in data:
        #         writer.writerow(item)
        # return print(res[0])
# async def test(profession='программист', page=10):
#     res = await main(profession='программист', page=10)
#     for item in res:
#         # result.append(parse_vacation(item))
#         print(len(parse_vacation(item)))


loop = asyncio.get_event_loop()
t = Timer()
t.start()
loop.run_until_complete(get_all_pages('программист'))
t.stop()
