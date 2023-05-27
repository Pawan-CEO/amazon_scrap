import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'session-id=259-3361949-3805605; session-id-time=2082787201l; i18n-prefs=INR; ubid-acbin=258-8210134-5800138; session-token=SHi81P2FeZLy/Y8CGzWW4RCyS4p9vOTMnRGuaHyVC9w16WkbRF2RZlqoJfOQ8W2Vfl8Ylk4Jb8Ya5Yoy6/K/bi3ZTzuY+gKQ1gAhfq5oo/xuIn4q/D4t6wKJogA3mr+5ePDf//MgmCW9YKrd3TM4+pNnzy7ACOipk6azO93tArXXnbROvUiq26qrwhT6G3pwpGRsmNd67JS4D+RuqxBmp9GxPpP8I8kkYhI5uvOUQIo=; csm-hit=tb:HAXBHAE6M7PCX11JTZXF+s-6M1E2C2VRGTJXGYM41BP|1685100461896&t:1685100461897&adb:adblk_no',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
    "viewport-width": "675"
}

proxies = {'http': 'http://world.proxymesh.com:31280',
           'https': 'http://world.proxymesh.com:31280'}
dataframe_main = pd.DataFrame(columns=["prod_link", "description", "price", "rating", "rating_count"])
for i in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%252C283&ref=sr_pg_{i}'
    response = requests.get(url, headers=headers, verify=False)
    source = response.text
    soup = BeautifulSoup(source, 'html.parser')


    all = soup.findAll('div', attrs={
        "class": "sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16"})
    

    prod_link_main = []
    description_main = []
    price_main = []
    rating_main = []
    rating_count_main = []

    for i in all:
        description = ''
        price = ''

        prod_link = 'https://www.amazon.in' + i.find('a', attrs={
            'class': "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})['href']
        description = i.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'}).text
        price = i.find('span', attrs={'class': "a-price-whole"}).text
        try:
            rating = i.find('span', attrs={'class': 'a-icon-alt'}).text
            rating_count = i.find('span', attrs={'class': 'a-size-base s-underline-text'}).text
        except:
            rating = ''
            rating_count = ''
        print(prod_link, description, price, rating, rating_count)
        prod_link_main.append(prod_link)
        description_main.append(description)
        price_main.append(price)
        rating_main.append(rating)
        rating_count_main.append(rating_count)

    data_frame_temp = pd.DataFrame(
        {"prod_link": prod_link_main, "description": description, "price": price_main, "rating": rating_main,
         "rating_count": rating_count_main})
    dataframe_main = pd.concat([dataframe_main, data_frame_temp],axis=0)
    



dataframe_main['Description']=''
for p_link in dataframe_main['prod_link'].values:
    url = p_link
    response = requests.get(url, headers=headers, verify=False)
    source = response.text
    soup = BeautifulSoup(source, 'html.parser')
    Description_name = soup.find('span', class_='a-size-large product-title-word-break')
    description = Description_name.get_text(separator='|').strip('|').strip()
    dataframe_main.loc[dataframe_main['prod_link']==p_link,'Description']=description

    




dataframe_main.to_csv('download_data.csv')


