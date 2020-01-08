from bs4 import BeautifulSoup
import requests
import scrape
import pandas as pd
import numpy as np

url = 'http://scores.nbcsports.com/epl/fixtures.asp?month='
months = [str(i) for i in range(8, 13)]

def scrape_urls(url, month):
    final_url = url + month
    response = requests.get(final_url)
    if response.status_code != 200:
        print(response.status_code)
        return 0
    #print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table', class_='shsTable shsBorderTable')
    table = table[0]
    table_rows_1 = table.find_all('tr', class_='shsRow1Row')
    table_rows_0 = table.find_all('tr', class_='shsRow0Row')
    urls_0 = []
    urls_1 = []
    for row in table_rows_0:
        a = row.find('a', href=True)
        if a['href'].find('gamecode') == -1:
            continue
        urls_0.append(a['href'])
    for row in table_rows_1:
        a = row.find('a', href=True)
        if a['href'].find('gamecode') == -1:
            continue
        urls_1.append(a['href'])
    list_of_urls = scrape.sort_arrays(urls_0, urls_1)
    list_of_urls = ['http://scores.nbcsports.com' + s for s in list_of_urls]
    return list_of_urls


if __name__ == '__main__':
    f = open('urls.txt', 'a')
    for month in months:
        urls = scrape_urls(url, month)
        for u in urls:
            f.write(u+'\n')
    f.close()
