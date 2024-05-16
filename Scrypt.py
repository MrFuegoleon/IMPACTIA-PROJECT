from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import re

email = "doumbiaablo03@gmail.com"
password = "blablacar"

# URL de la page StarNgage de connexion
login_url = "https://starngage.com/plus/en-us/login"

# URL de la page à scraper après la connexion
url_1="https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco?page=1"
url_to_scrape = url_1


# Configuration du navigateur
options = Options()
options.headless = True  # Utiliser un navigateur en mode headless (sans interface graphique)
driver = webdriver.Firefox(options=options)

# 2 - Stcockage des données

results_list = []

""""
driver.get(login_url)

# Remplir les champs de connexion
email_field = driver.find_element(By.ID, "email")
password_field = driver.find_element(By.ID, "password")


email_field.send_keys(email)
password_field.send_keys(password)

# Soumettre le formulaire de connexion
password_field.send_keys(Keys.RETURN)


# Attendre que la page se charge après la connexion
time.sleep(5)  # Attendre quelques secondes pour le chargement
"""
# Ouvrir l'URL à scraper
driver.get(url_to_scrape)

# Attendre que la page se charge complètement
time.sleep(5)

# Récupérer le contenu de la page après la connexion
html = driver.page_source

# Fermer le navigateur
driver.quit()

# Utiliser Beautiful Soup pour extraire le contenu de la page
soup = BeautifulSoup(html, "html.parser")

# Enregistrer le contenu dans un fichier
with open("lol.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Page enregistrée avec succès.")

TABLE = soup.find("tbody")
BIGTR = TABLE.find_all("tr")

for TR in BIGTR:
    NAME = TR.find("div", class_="mb-1 fw-bold").text.strip()
    NAME = re.sub(r'[^\x00-\x7F]+', '', NAME)
    ALL_TD = TR.find_all("td")
    NUMBER = ALL_TD[0].text.strip()
    FOLLOWERS = ALL_TD[2].text.strip()
    ER = ALL_TD[3].text.strip()
    COUNTRY = ALL_TD[4].text.strip()
    DOMAIN = ALL_TD[5].text.strip().replace("\n", ", ")

    POTENTIAL_REACH = ALL_TD[6].text.strip()

    # Vérification des valeurs récupérées
    print("N*", NUMBER)
    print("Name:", NAME)
    print("Followers:", FOLLOWERS)
    print("ER:", ER)
    print("Country:", COUNTRY)
    print("Domain:", DOMAIN)
    print("Potential Reach:", POTENTIAL_REACH)


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

# Chemin du fichier JSON de sortie
JSON_DATA_FILE = "data.json"

# Écriture des résultats au format JSON dans un fichier
with open(JSON_DATA_FILE, "w") as json_file:
    json.dump(results_list, json_file, indent=4)

print("Résultats enregistrés avec succès sous forme de fichier JSON.")


