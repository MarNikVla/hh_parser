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
    title = soup.find("h1", {'class': ['bloko-header-1'], 'data-qa':['vacancy-title']}).text
    key_skills = ' '.join([x.get_text() for x in
                    soup.find_all("div", {'class': ['skills-element', 'bloko-tag', 'bloko-tag_inline']})])
    salary = soup.find("p", {'class': ['vacancy-salary']}).text
    description = soup.find_all("div", {'class': ['vacancy-description', 'bloko-tag', 'bloko-tag_inline']})
    print(title)
    print(salary)

    print('sdf')

    # vacation_list = soup.find_all("p",
    #                               {'class': ['vacancy-salary']}).text
    data.append({
        # 'title': vacation_desc,
        # 'key_skills': vacation_link_strip_query,
        # 'salary': vacation_desc,
        # 'description': vacation_link_strip_query,
        # 'link': url,
    })
    return data


#
#
# def get_last_page(vacation) -> int:
#     first_page = get_html(vacation, page=0)
#     soup = BeautifulSoup(first_page, 'html.parser')
#     last_page = soup.find_all("a",
#                               {'class': ['bloko-button', 'HH-Pager-Control']})[-2].get_text()
#     return int(last_page)
#
#
# def list_of_vacation_to_csv(vacation, page=None):
#     csv_columns = ['vacation', 'vacation_link']
#     if page:
#         last_page = page
#     else:
#         last_page = get_last_page(vacation)
#
#     with open(f'test/{vacation}_sync.csv', 'w', newline='', encoding='utf-8') as output_file:
#         writer = csv.DictWriter(output_file, fieldnames=csv_columns)
#         for page in range(last_page):
#             data = parse_vacation(vacation, page)
#             for item in data:
#                 writer.writerow(item)
#
#     return print('Done')


if __name__ == '__main__':
    t = Timer()
    t.start()
    parse_single_vacation(url)
    t.stop()
