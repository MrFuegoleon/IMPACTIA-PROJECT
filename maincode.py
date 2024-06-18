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
import TextHtml
import SummarClean
import Cosine_Similar
import re
import unicodedata
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
datat = pd.read_csv('cleaned_final_data.csv')

data=pd.read_csv('dataf.csv')

data.isnull().sum()

data= data.dropna(subset='name', axis = 0)
data['domain'] = data['domain'].fillna("Unknown")
data = data.reset_index( drop=True)

DATA=data.drop(columns=['@name','number'],axis=1)

overall_infos = []
for i in range(0, DATA.shape[0]):
    overall_infos.append(DATA['country'][i]+' '+DATA['domain'][i])
DATA['overall_infos'] = overall_infos

#Stopwords help us to get rid of unwanted words like: a, an, are, is, ...
stop = stopwords.words('english')


# Configuration du navigateur
options = Options()
options.headless = True  # Utiliser un navigateur en mode headless (sans interface graphique)
driver = webdriver.Firefox(options=options)


# Query de recherche
query = "Bollore"
results_list = []

# Recherche en ligne et récupération des deux premiers résultats
top_results = TextHtml.search_and_get_top_results(query)

for url_to_scrape in top_results:
    driver.get(url_to_scrape)
    
    # Attendre que la page se charge complètement
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Récupérer le contenu de la page après le chargement complet
    html2 = driver.page_source
    
    # Utiliser BeautifulSoup pour extraire le contenu de la page
    soup = BeautifulSoup(html2, "html.parser")
    
    # Ajouter l'URL et le contenu à la liste des résultats
    text = soup.get_text()
    truncated_text = TextHtml.truncate_text(text, 1020)
    results_list.append((url_to_scrape, truncated_text))

# Fermer le navigateur
driver.quit()

# Concatenation des résultats en un seul bloc de texte
final_text = ""
for result in results_list:
    final_text += result[1] + "\n"

# Afficher les résultats concaténés
# print(final_text)

# Sauvegarder le texte concaténé dans un fichier pour une analyse ultérieure
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(final_text)


# Modèle de résumé
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Découper le texte en segments
text_chunks =SummarClean.chunk_text(final_text)

# Résumer chaque segment
summaries = []
for chunk in text_chunks:
    summary = summarizer(chunk, max_length=40, min_length=10, do_sample=False)
    summaries.append(summary[0]['summary_text'])

# Combiner les résumés
final_summary = ' '.join(summaries)

sequence_to_classify=SummarClean.clean_text(final_summary)
# Afficher le résumé final
print(sequence_to_classify)



candidate_labels=['news', 'celebrity', 'lifestyle', 'advertising', 'cooking', 'unknown', 'education', 'services', 'bikini', 'fitness', 'magazines', 'accessories', 'crafts', 'society', 'choreographer', 'garden', 'gaming', 'careers', 'styling', 'acting', 'celebrities', 'personal', 'entertainment', 'music', 'marketing', 'motorcycles', 'singer', 'chef', 'finance', 'modeling', 'showcase', 'producers', 'topic', 'beauty', 'hair', 'politics', 'events', 'auto', 'home', 'actors', 'drama', 'activity', 'training', 'life', 'art', 'journalists', 'vehicles', 'photography', 'photographer', 'portraits', 'creator', 'kids', 'travel', 'wedding', 'family', 'dance', 'parenting', 'cars', 'product', 'funny', 'soccer', 'animals', 'television', 'sports', 'songwriting', 'blogger', 'health', 'personality', 'basketball', 'cosplay', 'gym', 'fashion', 'upskilling', 'design', 'dogs', 'animation', 'automotive', 'business', 'moms', 'digital', 'outdoor', 'food', 'founder', 'humor', 'entrepreneur', 'hacks', 'creators', 'pets', 'blog', 'nature', 'arts', 'band', 'interior', 'video', 'diy', 'romance', 'care', 'coaching', 'self', 'medical', 'games', 'shopping', 'technology', 'drink']

A2 = classifier(sequence_to_classify, candidate_labels)

# Obtenez les labels et les scores pour A2
labels_A2 = A2['labels']
scores_A2 = A2['scores']

# Trier les labels et les scores par ordre décroissant selon les scores
sorted_indices_A2 = sorted(range(len(scores_A2)), key=lambda i: scores_A2[i], reverse=True)

# Sélectionner les trois premiers labels et leurs scores
top_3_labels = [labels_A2[i] for i in sorted_indices_A2[:3]]
top_3_scores = [scores_A2[i] for i in sorted_indices_A2[:3]]

# Sauvegarder les trois premiers labels dans un vecteur
INFO_ENTR = top_3_labels[0]+' '+top_3_labels[1]+' '+top_3_labels[2]


# Affichage des résultats
print("Top 3 labels with highest scores:")
for label, score in zip(top_3_labels, top_3_scores):
    print(f"Label: {label}, Score: {score}")

# Vecteur des catégories sélectionnées
print("INFO_ENTR:", INFO_ENTR)




NEW_DATA= Cosine_Similar.NouvelleData(INFO_ENTR, DATA)


FINAL_DATA=NEW_DATA['cleaned_infos'] = Cosine_Similar.text_preprocessing(NEW_DATA['overall_infos'])

# Transformation du texte en vecteurs de comptage
CV = CountVectorizer()
converted_matrix = CV.fit_transform(FINAL_DATA)

# Calcul de la similarité cosinus
cosine_similarities = cosine_similarity(converted_matrix)

# Obtenir les similarités de la nouvelle information avec toutes les autres
new_info_similarities = cosine_similarities[-1][:-1]

# Afficher les similarités avec les entrées existantes
similarity_scores = list(enumerate(new_info_similarities))
similarity_scores.sort(key=lambda x: x[1], reverse=True)

# Afficher les 3 entrées les plus similaires
N = 3
print(f"Les {N} entrées les plus similaires à '{INFO_ENTR}' sont :\n")

for idx, score in similarity_scores[:N]:
    print(f"Indice : {idx}, Similarité : {score:.2f}")
    print("Détails de l'entrée :")
    print("---------------------")
    print(f"Nom de l'influenceur : {NEW_DATA.iloc[idx]['name']}")
    print(f"Followers : {NEW_DATA.iloc[idx]['followers']}")
    print(f"Taux d'engagement (ER) : {NEW_DATA.iloc[idx]['er']}")
    print(f"Pays : {NEW_DATA.iloc[idx]['country']}")
    print(f"Domaine : {NEW_DATA.iloc[idx]['domain']}")
    print(f"Portée potentielle : {NEW_DATA.iloc[idx]['potential_reach']}")
    print(f"Informations globales : {NEW_DATA.iloc[idx]['overall_infos']}")
    print(f"Informations nettoyées : {NEW_DATA.iloc[idx]['cleaned_infos']}")
    print("\n" + "-"*30 + "\n")
