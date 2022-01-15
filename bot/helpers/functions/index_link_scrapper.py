import time
from bs4 import BeautifulSoup
from bot.helpers.utils.chrome_driver import chrome_driver

async def fetch_index_links(link):
    driver = await chrome_driver()
    driver.get(link)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all('div', class_='list-group-item list-group-item-action')
    links_list = []
    links = []
    for div in divs:
        a = div.find_all('a')
        for link in a:
            links_list.append(link.get('href'))
    for link in links_list:
        if not link.startswith('/'):
            links.append(link)
    return links