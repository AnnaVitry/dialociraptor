import chainlit as cl
from llama_index.core import StorageContext, load_index_from_storage, Settings
# On remplace l'import OpenAI par Groq pour éviter l'erreur de validation du nom du modèle
from llama_index.llms.groq import Groq 
from llama_index.embeddings.huggingface import HuggingFaceEmbedding 
import os
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

# --- CONFIGURATION CRITIQUE ---

# 1. EMBEDDING : IDENTIQUE à build_index.py (BAAI/bge-m3)
# Cela permet de lire correctement les vecteurs créés précédemment.
print("Chargement du modèle d'embedding...")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

# 2. LLM (Groq) : Utilisation du connecteur officiel Groq
# Cela contourne l'erreur "Unknown model" de la classe OpenAI standard.
Settings.llm = Groq(
    model="llama-3.1-8b-instant",              # Modèle Llama 3 sur Groq
    temperature=0.1,                     # Faible température pour la précision
    api_key=os.getenv("OPENAI_API_KEY")  # On récupère ta clé gsk_ ici
)

# Message de disclaimer obligatoire (Critère Interface)
DISCLAIMER = """
⚠️ **AVERTISSEMENT IMPORTANT** ⚠️
Ce chatbot est un prototype informatif destiné à un organisme public. 
**Il ne remplace en aucun cas un avis médical professionnel.**
En cas de doute sur votre état de santé, consultez immédiatement un médecin.
"""

@cl.on_chat_start
async def start():
    """Cette fonction s'exécute au démarrage d'une nouvelle session utilisateur."""
    try:
        # Chargement de l'index persistant créé par build_index.py
        storage_context = StorageContext.from_defaults(persist_dir="./index_storage")
        index = load_index_from_storage(storage_context)
        
        # Création du moteur de requête (Retriever + LLM)
        query_engine = index.as_query_engine(
            streaming=True, 
            similarity_top_k=3  # Récupère les 3 morceaux les plus pertinents
        )
        
        # On stocke le moteur dans la session pour le réutiliser à chaque message
        cl.user_session.set("query_engine", query_engine)

        # Envoi du message d'accueil avec le disclaimer
        await cl.Message(content=f"Bonjour ! Je suis votre assistant virtuel sur le diabète (Propulsé par Groq).\n{DISCLAIMER}").send()
        
    except Exception as e:
        error_msg = (
            f"Erreur critique au chargement : {e}. \n\n"
            "1. Avez-vous lancé 'pip install llama-index-llms-groq' ?\n"
            "2. Avez-vous bien lancé 'python build_index.py' avant ?"
        )
        await cl.Message(content=error_msg).send()

@cl.on_message
async def main(message: cl.Message):
    """Cette fonction s'exécute à chaque fois que l'utilisateur envoie un message."""
    
    query_engine = cl.user_session.get("query_engine")
    
    # Prompt système renforçant le rôle et la sécurité
    prompt_complet = (
        "Tu es un assistant expert en diabète pour un organisme public de santé. "
        "Tu dois répondre en français de manière claire et pédagogique. "
        "Utilise EXCLUSIVEMENT le contexte fourni ci-dessous pour répondre. "
        "Si la réponse ne se trouve pas dans le contexte, dis poliment que tu ne sais pas, n'invente rien. "
        "Reste empathique mais professionnel et factuel.\n\n"
        f"Question de l'utilisateur : {message.content}"
    )

    msg = cl.Message(content="")
    
    try:
        # Appel au moteur RAG
        response = query_engine.query(prompt_complet)

        # Diffusion de la réponse (Streaming) mot par mot
        for token in response.response_gen:
            await msg.stream_token(token)

        # --- GESTION DES SOURCES (Critère d'évaluation : Fidélité & Rigueur) ---
        if response.source_nodes:
            sources_text = "\n\n---Sources utilisées---"
            unique_sources = set()
            
            for node in response.source_nodes:
                # On récupère la métadonnée "source" définie dans build_index.py
                src = node.metadata.get('source', 'Source inconnue')
                topic = node.metadata.get('topic', 'Général')
                
                # On crée une chaine propre "Source (Sujet)"
                source_entry = f"{src} (Thème : {topic})"
                unique_sources.add(source_entry)
            
            for src in unique_sources:
                sources_text += f"\n📚 {src}"
            
            await msg.stream_token(sources_text)
        
        await msg.send()
        
    except Exception as e:
        await cl.Message(content=f"Une erreur est survenue lors de la génération de la réponse : {e}").send()