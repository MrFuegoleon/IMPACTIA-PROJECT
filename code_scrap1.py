from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


email = "doumbiaablo000@gmail.com"
password = "ALLAHOUAKBAR00"

# URL de la page LinkedIn de connexion
login_url = "https://www.linkedin.com/login"

# URL de la page à scraper après la connexion
url_1="https://starngage.com/plus/en-us/influencer/ranking/instagram/morocco"
url_to_scrape = url_1

# Configuration du navigateur
options = Options()
options.headless = True  # Utiliser un navigateur en mode headless (sans interface graphique)
driver = webdriver.Firefox(options=options)

# Ouvrir la page de login LinkedIn
driver.get(login_url)


# Remplir les champs de connexion
email_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")


email_field.send_keys(email)
password_field.send_keys(password)

# Soumettre le formulaire de connexion
password_field.send_keys(Keys.RETURN)

# Attendre que la page se charge après la connexion
time.sleep(5)  # Attendre quelques secondes pour le chargement

# Ouvrir l'URL à scraper
driver.get(url_to_scrape)

# Attendre que la page se charge complètement
time.sleep(5)

# Récupérer le contenu de la page après la connexion
html = driver.page_source

# Fermer le navigateur
driver.quit()

# Utiliser Beautiful Soup pour extraire le contenu de la page
soup = BeautifulSoup(html, "html5lib")


div_caract= soup.find("div",class_= "org-grid__content-height-enforcer")

# Description
description = div_caract.find("p", class_="break-words white-space-pre-wrap t-black--light text-body-medium").text.strip()
print("Presentation:", description)


# Informations supplémentaires
informations_supplementaire = div_caract.find("dl", class_="overflow-hidden")
informations_supplementaires = informations_supplementaire.find_all("dd", class_="mb4 t-black--light text-body-medium")
for info in informations_supplementaires:
    terme = info.find("dt", class_="mb1 text-heading-medium")
    valeur= info.text.strip()
    print(valeur)

# Enregistrer le contenu dans un fichier
with open("contenu.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Page enregistrée avec succès.")

# Fermer le navigateur
driver.quit()
