from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ouvrir le navigateur
driver = webdriver.Firefox()
driver.get("https://www.linkedin.com")

# Attendre que l'utilisateur se connecte manuellement
input("Veuillez vous connecter à LinkedIn dans le navigateur, puis appuyez sur Entrée.")

# Récupérer le contenu de la page après la connexion
url = "https://www.linkedin.com/company/the-coca-cola-company/about/"
driver.get(url)

# Attendre quelques secondes pour permettre au contenu de se charger complètement
import time
time.sleep(5)

# Récupérer le contenu de la page après le chargement complet
html = driver.page_source

# Fermer le navigateur
driver.quit()

# Enregistrer le contenu dans un fichier
with open("recette.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Page enregistrée avec succès.")
