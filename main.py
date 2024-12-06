import requests
from bs4 import BeautifulSoup
import csv
import argparse

class LinioScraper:
    def __init__(self):
        self.base_url = "https://www.linio.com.co/search?scroll=&q="  
        self.data = []

    def scraping(self, product_name):
        cleaned_name = product_name.replace(" ", "+").lower()
        urls = [self.base_url + cleaned_name]
        page_number = 2
        for i in range(1, 5):
            urls.append(f"{self.base_url}{cleaned_name}&page={page_number}")
            page_number += 1

        self.data = []
        c = 1

        for i, url in enumerate(urls, start=1):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find_all('div', class_='catalogue-product')

            if not content:
                print(f"\nNo hay más contenido en la página {i}. URL: {url}")
                continue

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
                c += 1

        # Verifica si la lista de datos está vacía
        if not self.data:
            print("\nNo se encontraron productos para el término de búsqueda.")
        else:
            print(f"\nSe encontraron {len(self.data)} productos.")
        
        self.export_to_csv()

    def export_to_csv(self):
        try:
            with open("linio_scraped_data.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "price", "post link", "image link"])
                writer.writeheader()
                writer.writerows(self.data)
            print("\nDatos exportados correctamente a 'linio_scraped_data.csv'")
        except Exception as e:
            print(f"\nError al guardar el archivo CSV: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', required=True, help='Producto a buscar')
    args = parser.parse_args()

    scraper = LinioScraper()
    scraper.scraping(args.product)

if __name__ == "__main__":
    main()
