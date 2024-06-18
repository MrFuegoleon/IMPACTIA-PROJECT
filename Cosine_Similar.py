import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('english')



def text_preprocessing(column):
    # Convertir tout le texte en minuscules
    column = column.str.lower()
    # Supprimer les URLs, mentions (@) et autres ponctuations spécifiées
    column = column.str.replace(r'http\S+|www.\S+', '', regex=True)
    column = column.str.replace(r'[@%:,.]', '', regex=True)
    # Supprimer les espaces supplémentaires
    column = column.str.strip()
    # Diviser chaque phrase en mots pour appliquer les stopwords
    word_tokens = column.str.split()
    keywords = word_tokens.apply(lambda x: [item for item in x if item not in stop])
    # Assembler les mots de chaque phrase à nouveau
    keywords = keywords.apply(lambda x: ' '.join(x))
    return keywords


def NouvelleData(INFO_ENTR, DATA):
    # Nouvelle information nettoyée
    cleaned_INFO_ENTR = text_preprocessing(pd.Series([INFO_ENTR]))[0]

    # Créer un DataFrame temporaire pour la nouvelle information
    temp_df = pd.DataFrame({
        'name': ['new compagnies'],
        'followers': ['unknown'],
        'domain': ['Technologie'],
        'er': ['unknown'],
        'country': ['Maroc'],
        'overall_infos': [INFO_ENTR],
        'cleaned_infos': [cleaned_INFO_ENTR]
    })

    # Ajouter la nouvelle information au DataFrame existant
    NEW_DATA = pd.concat([DATA, temp_df], ignore_index=True)
    return NEW_DATA


