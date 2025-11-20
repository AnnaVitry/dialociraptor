# Ligne 1 : Importe la librairie Pandas pour manipuler les données
import pandas as pd

# Ligne 2 : Importe le modèle d'embedding (SentenceTransformer)
from sentence_transformers import SentenceTransformer

# Ligne 4 : Définissez le chemin vers votre fichier CSV consolidé
fichier_csv_maitre = "src\\info_diabete - Feuille 1.csv"

# Ligne 5 : Charge le CSV dans un DataFrame Pandas
df = pd.read_csv(fichier_csv_maitre)

# Ligne 6 : Choisissez et chargez un modèle d'embedding (l'un des plus rapides et efficaces)
# Ce modèle va générer vos vecteurs numériques.
model = SentenceTransformer('all-MiniLM-L6-v2')

# Ligne 7 : Affiche le nombre de lignes (chunks) à traiter (Vérification)
print(f"Nombre de chunks à vectoriser : {len(df)}")

# Ligne 8 : Extrait la colonne de contenu qui sera transformée en vecteurs
# ASSUREZ-VOUS que 'CHUNK_CONTENT' est le nom exact de votre colonne maîtresse !
corpus = df['Chunk_content'].tolist()

# Ligne 9 : Effectue l'opération d'embedding. 
# Cette ligne prend chaque texte du corpus et le transforme en un vecteur de nombres.
embeddings = model.encode(corpus, show_progress_bar=True)

# Ligne 10 : Affiche les dimensions du résultat (Vérification)
# Par exemple, si vous avez 1000 chunks, le résultat sera (1000, 384)
print(f"Taille du tableau d'embeddings : {embeddings.shape}")

# Ligne 11 : Importe NumPy, souvent utilisé pour sauvegarder les tableaux de vecteurs
import numpy as np

# Ligne 12 : Définit le nom du fichier de sortie
fichier_embeddings = 'embeddings_diabete.npy'

# Ligne 13 : Sauvegarde les embeddings dans un format binaire optimisé
np.save(fichier_embeddings, embeddings)