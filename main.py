import time
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd

class LinioScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.data = []

    def scraping(self, product_name):
        cleaned_name = product_name.replace(" ", "+").lower()
        urls = [self.base_url + cleaned_name]
        page_number = 2
        for i in range(1, 5):
            urls.append(f"{self.base_url}{cleaned_name}&page={page_number}")
            page_number += 1

        self.data = []
        for i, url in enumerate(urls, start=1):
            try:
                response = self.get_url_with_retries(url)
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
                    post_link = "https://www.linio.com.co" + post_link

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
            except RequestException as e:
                print(f"Error al realizar la solicitud a {url}: {e}")
                break

    def get_url_with_retries(self, url, retries=3, delay=5):
        for i in range(retries):
            try:
                return requests.get(url)
            except RequestException as e:
                print(f"Intento {i+1} fallido: {e}")
                if i < retries - 1:
                    print(f"Reintentando en {delay} segundos...")
                    time.sleep(delay)
                else:
                    raise

    def export_to_csv(self):
        df = pd.DataFrame(self.data)
        df.to_csv("linio_colombia_scraped_data.csv", sep=";", index=False)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--product', type=str, required=True, help="Producto a buscar")
    args = parser.parse_args()

    scraper = LinioScraper(base_url="https://www.linio.com.co/search?scroll=&q=")  # URL para Colombia
    scraper.scraping(args.product)
    scraper.export_to_csv()
