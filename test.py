from bs4 import BeautifulSoup
import requests
import csv
import pathlib
from codetiming import Timer

# establishing session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
})


def load_vacancy_page(profession=None, page=0):
    url = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true' \
          '&enable_snippets=true&text={profession}&page={page}'.format(
        page=page, profession=profession)
    html = session.get(url).text
    return html


def parse_vacation(profession=None, page=0):
    data = []
    print(page)
    text = load_vacancy_page(profession=profession, page=page)
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

def contain_vacation_data(data):
    print(data != [])
    return data != []

def list_of_vacation_to_csv(profession, page):
    csv_columns = ['vacation', 'vacation_link']
    while True:
        data = parse_vacation(profession, page=page)
        # print(data == [])
        if contain_vacation_data(data):
            with open('test.csv', 'a', newline='', encoding='utf-8') as output_file:
                # data = parse_vacation(profession, page=page)
                writer = csv.DictWriter(output_file, fieldnames=csv_columns)
                # writer.writeheader()
                for item in data:
                    writer.writerow(item)
                page+=1
        else:
            break
    return print('Done')


if __name__ == '__main__':
    try:
        file = pathlib.Path("test.csv")
        file.unlink()
    except:
        pass
    t = Timer()
    t.start()
    list_of_vacation_to_csv(profession='программист', page=20)
    t.stop()
