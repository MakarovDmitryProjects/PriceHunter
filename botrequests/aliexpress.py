import requests
from bs4 import BeautifulSoup


def request(url: str):
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.text, "lxml")

        title = soup.find('h1').text
        for item in soup.find_all('img'):
            if 'data-idx="1"' in str(item):
                img = item['src']
        temp_price = soup.find('div', class_='snow-price_SnowPrice__mainS__jlh6el').text
        temp_price_ws = temp_price.replace(' ', '')
        temp_price_float = temp_price_ws.replace(',', '.')
        temp_num = temp_price_float[:-1]
        current_price = float(temp_num)

        return title, img, current_price
    except:
        return False
