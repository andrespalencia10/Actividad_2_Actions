import requests
from bs4 import BeautifulSoup
import csv
import argparse

class LinioScraper:
    def __init__(self, country):
        self.base_url = "https://www.linio.com.co"
        self.country = country
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.product_data = []

    def scraping(self, product):
        # Construir la URL de búsqueda para el producto
        url = f"{self.base_url}/search?scroll=&q={product}"
        
        # Desactivar la verificación SSL (no recomendado en producción)
        response = requests.get(url, headers=self.headers, verify=False)

        if response.status_code == 200:
            print("Datos obtenidos correctamente.")
            self.parse_html(response.text)
        else:
            print(f"Error al obtener datos: {response.status_code}")

    def parse_html(self, html_content):
        # Parsear el contenido HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Ejemplo de cómo extraer los productos de la página
        products = soup.find_all("div", class_="product-card")

        for product in products:
            name = product.find("h3", class_="product-title").get_text(strip=True)
            price = product.find("span", class_="price").get_text(strip=True)
            self.product_data.append([name, price])

        # Guardar los datos en un archivo CSV
        self.save_data()

    def save_data(self):
        # Verificar si el archivo CSV ya existe
        file_name = "linio_scraped_data.csv"
        
        # Si el archivo no existe, crear uno con encabezados
        file_exists = False
        try:
            with open(file_name, 'r') as file:
                file_exists = True
        except FileNotFoundError:
            pass
        
        # Guardar los datos en CSV
        with open(file_name, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Product Name", "Price"])
            writer.writerows(self.product_data)

        print(f"Datos guardados en {file_name}")

def main():
    # Definir los argumentos de línea de comando
    parser = argparse.ArgumentParser(description="Scraper para Linio Colombia.")
    parser.add_argument("--product", type=str, required=True, help="Nombre del producto para buscar.")
    args = parser.parse_args()

    # Crear una instancia del scraper para Colombia (ID país: 4)
    scraper = LinioScraper(country=4)

    # Ejecutar el scraping con el producto proporcionado
    scraper.scraping(args.product)

if __name__ == "__main__":
    main()
