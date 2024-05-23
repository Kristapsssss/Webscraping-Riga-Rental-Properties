import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_tr = soup.find_all('tr')
    listings = all_tr[5:-4]

    data = []
    for listing in listings:
        details = listing.find_all('td')
        if details:
            posting = {
                'Title': details[2].text.strip(),
                'Location': details[3].text.strip(),
                'Rooms': details[4].text.strip(),
                'Size': details[5].text.strip(),
                'Floor': details[6].text.strip(),
                'Series': details[7].text.strip(),
                'Price': details[8].text.strip()
            }
            data.append(posting)

    return data


def get_all_pages_data(url, page_number):
    all_data = []
    for page in range(1, page_number + 1):
        page_url = f"{url}/page{page}.html"
        print(f"Scraping page: {page}, the page url is: {page_url}")
        page_data = get_page_data(page_url)
        all_data += page_data
    return all_data


base_url = "https://www.ss.lv/lv/real-estate/flats/riga/all/hand_over/"
pages = 45

all_riga_listings = get_all_pages_data(base_url, pages)

df = pd.DataFrame(all_riga_listings)
print(df.shape)


df.to_csv('riga_listings.csv', index=False)
