import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from transformers import pipeline
import numpy as np
import pandas as pd
import re
import unicodedata




# Configuration du navigateur
options = Options()
options.headless = True  # Utiliser un navigateur en mode headless (sans interface graphique)
driver = webdriver.Firefox(options=Options())

def search_and_get_top_results(query,lang='en'):
    search_url = f"https://www.google.com/search?q={query}"
    driver.get(search_url)
    time.sleep(5)  # Attendre quelques secondes pour le chargement
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    search_results = soup.find_all('a', jsname='UWckNb', href=True)
    top_results = [link['href'] for link in search_results if link['href'].startswith('http')]
    return top_results[:2]


def truncate_text(text, max_length=1020):
    words = text.split()
    return ' '.join(words[:max_length])

