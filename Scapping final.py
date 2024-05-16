import json
import unicodedata
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

# Liste d'URLs à scraper
URLS = [
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=1",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=2",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=3",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=4",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=5",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=6",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=7",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=8",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=9",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=10",

    
]


URLc = [
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=2",
    ]

# Configuration du navigateur
options = Options()
options.headless = True  # Utiliser un navigateur en mode headless (sans interface graphique)
driver = webdriver.Firefox(options=options)

# Liste pour stocker les résultats
results_list = []

for url_to_scrape in URLc:
    
    email = "doumbiaablo03@gmail.com"
    password = "blablacar"

    # URL de la page LinkedIn de connexion
    login_url = "https://starngage.com/plus/en-us/login"

    # Ouvrir la page de login LinkedIn
    driver.get(login_url)
    time.sleep(5)  # Attendre quelques secondes pour le chargement

    # Remplir les champs de connexion
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")


    email_field.send_keys(email)
    password_field.send_keys(password)

    # Soumettre le formulaire de connexion
    password_field.send_keys(Keys.RETURN)

    # Attendre que la page se charge après la connexion
    time.sleep(5)  # Attendre quelques secondes pour le chargement

    driver.get(url_to_scrape)

    # Attendre que la page se charge complètement
    time.sleep(5)

    # Récupérer le contenu de la page après la connexion
    html = driver.page_source

    # Utiliser Beautiful Soup pour extraire le contenu de la page
    soup = BeautifulSoup(html, "html.parser")

    TABLE = soup.find("tbody")
    BIGTR = TABLE.find_all("tr")

    for TR in BIGTR:
        NAME = TR.find("div", class_="mb-1 fw-bold").text.strip()
        NAME = re.sub(r'[^\x00-\x7F]+', '', NAME)
        ALL_TD = TR.find_all("td")
        NUMBER = ALL_TD[0].text.strip()
        FOLLOWERS = ALL_TD[1].text.strip()
        ER = ALL_TD[2].text.strip()
        COUNTRY = ALL_TD[3].text.strip()
        DOMAIN = ALL_TD[4].text.strip().replace("\n", ", ")
        POTENTIAL_REACH = ALL_TD[5].text.strip()

        # Création d'un dictionnaire pour stocker les résultats de chaque ligne
        result_dict = {
            "name": NAME,
            "number": NUMBER,
            "followers": FOLLOWERS,
            "er": ER,
            "country": COUNTRY,
            "domain": DOMAIN,
            "potential_reach": POTENTIAL_REACH
        }

        # Ajout du dictionnaire à la liste des résultats
        results_list.append(result_dict)

# Fermer le navigateur
driver.quit()

# Chemin du fichier JSON de sortie
JSON_DATA_FILE = "data.json"

# Écriture des résultats au format JSON dans un fichier
with open(JSON_DATA_FILE, "w") as json_file:
    json.dump(results_list, json_file, indent=4)

print("Résultats enregistrés avec succès sous forme de fichier JSON.")
