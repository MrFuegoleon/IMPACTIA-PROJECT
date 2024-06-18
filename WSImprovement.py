import json
import re
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configurer la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paramètres configurables
URLS = [
        "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=1",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=2",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=3",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=4",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=5",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=6",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=7",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=8",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=9",
    "https://starngage.com/plus/en-us/influencer/ranking/tiktok/morocco?page=10",

]

LOGIN_URL = "https://starngage.com/plus/en-us/login"
JSON_DATA_FILE = "data_tiktok.json"

# Configurer WebDriver
options = Options()
options.headless = False  # Désactiver le mode headless pour permettre l'interaction manuelle
driver = webdriver.Firefox(options=options)

def wait_for_manual_login():
    try:
        input("Appuyez sur Enter après avoir complété l'identification manuelle...")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("Connexion manuelle réussie.")
    except Exception as e:
        logging.error(f"Erreur lors de la connexion manuelle : {e}")
        driver.quit()
        raise

def scrape_page(driver, url):
    results = []
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        table = soup.find("tbody")
        rows = table.find_all("tr")
        
        for row in rows:
            name = row.find("div", class_="mb-1 fw-bold").text.strip()
            name = re.sub(r'[^\x00-\x7F]+', '', name)
            cells = row.find_all("td")
            result = {
                "name": name,
                "number": cells[0].text.strip(),
                "@name": cells[1].text.strip(),
                "followers": cells[2].text.strip(),
                "er": cells[3].text.strip(),
                "country": cells[4].text.strip(),
                "domain": cells[5].text.strip(),
                
                "potential_reach": cells[6].text.strip()
            }
            results.append(result)
        logging.info(f"Scraping réussi pour {url}")
    except Exception as e:
        logging.error(f"Erreur lors du scraping de {url} : {e}")
    
    return results

def save_results_to_json(results, file_path):
    try:
        with open(file_path, "w") as json_file:
            json.dump(results, json_file, indent=4)
        logging.info(f"Résultats sauvegardés avec succès dans {file_path}")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde des résultats dans {file_path} : {e}")

def main():
    results_list = []
    
    driver.get(LOGIN_URL)
    wait_for_manual_login()
    
    for url in URLS:
        results = scrape_page(driver, url)
        results_list.extend(results)
    
    driver.quit()
    
    save_results_to_json(results_list, JSON_DATA_FILE)

if __name__ == "__main__":
    main()
