import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd

class LinioScraper:
    def __init__(self):
        self.base_url = None
        self.data = []

    def set_country(self, country_code):
        urls = {
            1: 'https://www.linio.com.ar/search?scroll=&q=',
            2: 'https://www.linio.cl/search?scroll=&q=',
            3: 'https://www.linio.com.co/search?scroll=&q=',
            4: 'https://www.linio.com.mx/search?scroll=&q=',
        }
        self.base_url = urls[country_code]

    def scraping(self, product_name):
        cleaned_name = product_name.replace(" ", "+").lower()
        urls = [self.base_url + cleaned_name]
        page_number = 2
        for i in range(1, 5):
            urls.append(f"{self.base_url}{cleaned_name}&page={page_number}")
            page_number += 1

        self.data = []

        for i, url in enumerate(urls, start=1):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find_all('div', class_='catalogue-product')

            if not content:
                print("\nNo hay más contenido para scrapear.")
                break

            print(f"\nScrapeando página número {i}. {url}")

            for post in content:
                title = post.find('a', class_='title-section').text.strip()
                price = post.find('span', class_='price-main-md').text.strip()
                post_link = post.find("a", class_='title-section')["href"]
                post_link = "https://www.linio.com" + post_link

                try:
                    img_link = post.find("img")["data-lazy"]
                except:
                    img_link = post.find("img")["src"]

                post_data = {
                    "title": title,
                    "price": price,
                    "post link": post_link,
                    "image link": img_link
                }

                self.data.append(post_data)

    def export_to_csv(self):
        df = pd.DataFrame(self.data)
        df.to_csv("linio_scraped_data.csv", sep=";")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linio Scraper")
    parser.add_argument("--country", type=int, required=True, help="Número del país (1: Argentina, 2: Chile, 3: Colombia, 4: México)")
    parser.add_argument("--product", type=str, required=True, help="Nombre del producto a buscar")
    args = parser.parse_args()

    scraper = LinioScraper()
    scraper.set_country(args.country)
    scraper.scraping(args.product)
    scraper.export_to_csv()
