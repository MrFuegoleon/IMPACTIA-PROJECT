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

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
datat = pd.read_csv('cleaned_final_data.csv')


labels = [] # Initialize labels list
for i in range(0, len(data), 100): # Iterate to the length of the dataframe
    label_name = f"label{i//100 + 1}"  # Nom du label, par exemple label1, label2, ...
    labels.append(data.iloc[i:i+100]['overall_infos'].tolist())  # Extraction du sous-groupe de domaines and convert to a list

# Dynamically unpack labels list
for i, label_group in enumerate(labels):
    # Process each label group as needed
    print(f"Processing label group {i+1}: {label_group}")


highest_score = float('-inf')  # Initialisez le score le plus élevé à une valeur très basse
domain_with_highest_score = None  # Initialisez le domaine correspondant au score le plus élevé

for i in range(len(labels)):
    candidate_labels = labels[i]

    A2 = classifier(sequence_to_classify, candidate_labels)

    # Obtenez les labels et les scores pour A2
    labels_A2 = A2['labels']
    scores_A2 = A2['scores']

    # Trouvez le label avec le score le plus élevé pour cette itération
    max_score_index = scores_A2.index(max(scores_A2))
    max_score_label = labels_A2[max_score_index]
    max_score = scores_A2[max_score_index]

    # Mettez à jour le score le plus élevé global si nécessaire
    if max_score > highest_score:
        highest_score = max_score
        domain_with_highest_score = max_score_label

# Affichez le domaine avec le score le plus élevé parmi tous les labels
print(f"Le domaine avec le score le plus élevé est '{domain_with_highest_score}' avec un score de {highest_score}.")