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
# Fonction pour découper le texte en segments de longueur maximale
def chunk_text(text, max_length=1024):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def clean_text(text):
    # Convertir le texte en minuscules
    text = text.lower()
    
    # Supprimer les caractères spéciaux, les nombres et les ponctuations
    text = re.sub(r'[^a-zÀ-ÿ\s]', '', text)
    
    # Supprimer les accents et normaliser le texte en Unicode
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    
    # Supprimer les espaces supplémentaires
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
