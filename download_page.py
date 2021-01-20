import requests

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

def start(text=None):
    while True:
        data = load_vacancy_page(session=session, page=0, profession=text)
        with open('test.html', 'w', encoding='utf-8') as output_file:
            output_file.write(data)
        break


if __name__ == '__main__':
    start('программист')
