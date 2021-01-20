from bs4 import BeautifulSoup
import requests
import csv

# establishing session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
})


def load_vacancy_page(session, profession=None, page=0):
    url = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true' \
          '&enable_snippets=true&text={profession}&page={page}'.format(
        page=page, profession=profession)
    data = session.get(url)
    return data.text


def parse_vacation(profession=None, page=0):
    results = []
    text = load_vacancy_page(session, profession=profession, page=page)
    soup = BeautifulSoup(text, 'html.parser')
    vacation_list = soup.find_all("div",
                                  {'class': ['vacancy-serp-item', 'vacancy-serp-item_premium']})
    # print(vacation_list)

    for item in vacation_list:
        vacation_link = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).get('href')
        vacation_desc = item.find('a', {'class': ['bloko-link', 'HH-LinkModifier']}).text

        results.append({
            'vacation': vacation_desc,
            'vacation_link': vacation_link,
        })
    with open('test.csv', 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        for item in results:
            print(type(item.items()))
            # writer.writerow(','.join(item.items()))

    return print('Done')


if __name__ == '__main__':
    parse_vacation(profession='программист', page=0)
