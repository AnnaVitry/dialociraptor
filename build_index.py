import pandas as pd
from llama_index.embeddings.huggingface import HuggingFaceEmbedding 
from llama_index.core import Document, VectorStoreIndex, Settings
import os
from dotenv import load_dotenv

load_dotenv()

print("Chargement du modèle d'embedding local (cela peut prendre un moment la première fois)...")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

def construire_index():
    print("Chargement du CSV...")
    df = pd.read_csv("src\\info_diabete - Feuille 1.csv")
    
    # Conversion du DataFrame en objets Document LlamaIndex
    documents = []
    for index, row in df.iterrows():
        # On combine la question et le contenu pour l'embedding
        text_content = f"Question: {row['Question']}\nRéponse: {row['Chunk_content']}"
        
        # On ajoute les métadonnées (CRUCIAL pour les critères d'évaluation)
        metadata = {
            "source": row['Source_ref'],
            "topic": row['Topic']
        }
        
        doc = Document(text=text_content, metadata=metadata)
        documents.append(doc)

    print(f"{len(documents)} documents préparés. Création de l'index...")
    
    # Création de l'index vectoriel
    index = VectorStoreIndex.from_documents(documents)
    
    # Sauvegarde sur le disque (pour ne pas payer l'embedding à chaque lancement)
    index.storage_context.persist(persist_dir="./index_storage")
    print("Index sauvegardé dans ./index_storage")

if __name__ == "__main__":
    construire_index()