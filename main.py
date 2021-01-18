import requests
from bs4 import BeautifulSoup

# establishing session
s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
})

def load_user_data(session, profession='программист',page=0,):
    url = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&text={profession}&page={page}'.format(page=page, profession=profession)
    r = session.get(url)
    # soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup)
    return r.text
#
# def read_file(filename):
#     with open(filename) as input_file:
#         text = input_file.read()
#     return text
#
# def parse_user_datafile_bs(filename):
#     results = []
#     text = read_file(filename)
#
#     soup = BeautifulSoup(text)
#
#     film_list = soup.find('div', {'class': 'profileFilmsList'})
#     items = film_list.find_all('div', {'class': ['item', 'item even']})
#     for item in items:
#         # getting movie_id
#         movie_link = item.find('div', {'class': 'nameRus'}).find('a').get('href')
#         movie_desc = item.find('div', {'class': 'nameRus'}).find('a').text
#         movie_id = re.findall('\d+', movie_link)[0]
#
#         # getting english name
#         name_eng = item.find('div', {'class': 'nameEng'}).text
#
#         #getting watch time
#         watch_datetime = item.find('div', {'class': 'date'}).text
#         date_watched, time_watched = re.match('(\d{2}\.\d{2}\.\d{4}), (\d{2}:\d{2})', watch_datetime).groups()
#
#         # getting user rating
#         user_rating = item.find('div', {'class': 'vote'}).text
#         if user_rating:
#             user_rating = int(user_rating)
#
#         results.append({
#                 'movie_id': movie_id,
#                 'name_eng': name_eng,
#                 'date_watched': date_watched,
#                 'time_watched': time_watched,
#                 'user_rating': user_rating,
#                 'movie_desc': movie_desc
#             })
#     return results



def start(text=None):

    while True:
        data = load_user_data(session=s, page=0, profession=text)
        with open('test.html', 'w', encoding='utf-8') as output_file:
            output_file.write(data)
        break


if __name__ == '__main__':
    start('программист')
