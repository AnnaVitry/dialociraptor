# 🦖 DialoRaptor

Un chatbot conversationnel intelligent basé sur la RAG (Retrieval-Augmented Generation) pour fournir des informations fiables sur le diabète.

## 📋 Table des matières

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Architecture technique](#architecture-technique)
- [Évaluation](#évaluation)
- [Données](#données)

---

## 📖 Description

**DialoRaptor** est un système de chatbot informatif destiné à un organisme public, utilisant une approche RAG (Retrieval-Augmented Generation) pour répondre à des questions sur le diabète avec précision et pertinence. Le système combine :

- 🔍 **Retrieval** : Recherche vectorielle sur une base de connaissances structurée
- 🤖 **Augmented Generation** : Génération de réponses contextualisées via LLM
- 💬 **Interface conversationnelle** : Chat interactif avec Chainlit

### ⚠️ Avertissement Important
Ce chatbot est un **prototype informatif** et ne remplace en aucun cas un avis médical professionnel. En cas de doute sur votre santé, consultez un médecin.

---

## ✨ Fonctionnalités

- ✅ Questions-réponses sur le diabète basées sur une base de connaissance
- ✅ Recherche sémantique avec embeddings HuggingFace
- ✅ Interface chat en temps réel avec streaming
- ✅ Persistance des résultats pour une performance optimisée
- ✅ Métadonnées de traçabilité (source, sujet)
- ✅ Évaluation des réponses avec RAGAS

---

## 🗂️ Structure du projet

```
dialociraptor/
├── app.py                              # Application principale Chainlit
├── build_index.py                      # Construction de l'index vectoriel
├── Embedding.py                        # Gestion des embeddings
├── evaluate_ragas.py                   # Évaluation des réponses
├── chainlit.md                         # Configuration Chainlit
├── requirements.txt                    # Dépendances Python
├── .env                                # Variables d'environnement (à créer)
├── README.md                           # Ce fichier
│
├── src/                                # Données source
│   ├── corpus_diabete_clean.csv        # Corpus nettoyé sur le diabète
│   ├── corpus_pdfs_clean.csv           # Corpus des PDFs
│   ├── info_diabete - Feuille 1.csv    # Dataset de Q&A
│   └── recapitulatif_pdfs.md           # Résumé des sources
│
├── data/                               # Données brutes (si nécessaire)
│
├── index_storage/                      # Index persistant
│   ├── default__vector_store.json      # Store vectoriel
│   ├── docstore.json                   # Documents
│   ├── graph_store.json                # Graphe de connaissances
│   ├── image__vector_store.json        # Images vectorisées
│   └── index_store.json                # Index
│
└── __pycache__/                        # Cache Python
```

---

## 🚀 Installation

### Prérequis
- Python 3.10+
- pip ou conda
- Une clé API 

### Étapes

#### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd dialociraptor
```

#### 2. Créer un environnement virtuel
```bash
# Avec venv
python -m venv .venv

# Activation (Windows)
.venv\Scripts\activate

# Activation (Linux/Mac)
source .venv/bin/activate
```

#### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4. Configurer les variables d'environnement
Créer un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=gsk_xxxxxxxxxxxxx  
```

---

## ⚙️ Configuration

### Modèles utilisés

| Composant | Modèle | Provider |
|-----------|--------|----------|
| **Embeddings** | BAAI/bge-m3 | HuggingFace (local) |
| **LLM** | Llama 3.1 8B | Groq |
| **Interface** | - | Chainlit |

### Paramètres ajustables

**Dans `app.py` :**
```python
Settings.llm = Groq(
    model="llama-3.1-8b-instant",
    temperature=0.1,              # ↓ pour plus de précision, ↑ pour plus de créativité
    api_key=os.getenv("OPENAI_API_KEY")
)

query_engine = index.as_query_engine(
    streaming=True,
    similarity_top_k=3             # Nombre de documents à récupérer
)
```

---

## 💬 Utilisation

### Lancer l'application

```bash
# Assurez-vous que l'environnement virtuel est activé
chainlit run app.py -w
```

L'interface s'ouvre à `http://localhost:8000`

### Workflow typique

1. **Première utilisation** : Exécuter `build_index.py` pour créer l'index
   ```bash
   python build_index.py
   ```

2. **Lancer le chatbot**
   ```bash
   chainlit run app.py -w
   ```

3. **Poser des questions** sur le diabète via l'interface

4. **Évaluer les résultats** avec RAGAS
   ```bash
   python evaluate_ragas.py
   ```

---

## 🏗️ Architecture technique

### Pipeline RAG

```
User Query
    ↓
[Embedding Layer - BAAI/bge-m3]
    ↓
[Vector Search - VectorStore]
    ↓
[Top-K Retrieval (k=3)]
    ↓
[Context + Prompt Augmentation]
    ↓
[LLM Generation - Groq/Llama 3.1]
    ↓
[Streaming Response via Chainlit]
    ↓
User Display
```

### Composants clés

**`build_index.py`**
- Charge les données CSV
- Crée des objets Document avec métadonnées
- Construit l'index vectoriel
- Persiste les données dans `./index_storage`

**`app.py`**
- Point d'entrée Chainlit
- Charge l'index persistant
- Gère les sessions utilisateur
- Exécute les requêtes en streaming

**`Embedding.py`**
- Utilitaires pour les embeddings
- Gestion des vecteurs

**`evaluate_ragas.py`**
- Évaluation des réponses via le framework RAGAS
- Métriques de qualité

---

## 📊 Évaluation

Le projet utilise **RAGAS** (Retrieval-Augmented Generation Assessment) pour évaluer :

- **Faithfulness** : Fidélité de la réponse au contexte
- **Answer Relevance** : Pertinence de la réponse
- **Context Precision** : Qualité du contexte récupéré

### Lancer l'évaluation
```bash
python evaluate_ragas.py
```

---

## 📁 Données

### Sources de données
- `corpus_diabete_clean.csv` : Corpus nettoyé sur le diabète
- `info_diabete - Feuille 1.csv` : Dataset de Q&A structuré
  - Colonnes : `Question`, `Chunk_content`, `Source_ref`, `Topic`

### Format des métadonnées
Chaque document contient :
- **source** : Source de référence (PDF, article, etc.)
- **topic** : Catégorie (symptômes, traitement, prévention, etc.)

---

## 🔧 Dépannage

### L'index n'est pas trouvé
```bash
python build_index.py  # Reconstruire l'index
```

### Erreur de clé API
- Vérifier que le fichier `.env` existe
- Vérifier que la clé API est correcte
- Redémarrer l'application

### Réponses de mauvaise qualité
- Augmenter `similarity_top_k` dans `app.py`
- Baisser la `temperature` pour plus de précision
- Vérifier la qualité des données source

---

## 📝 Licence

[À remplir selon votre projet]

## 👥 Auteurs

- Anna Vitry (Development)

---

## 📚 Ressources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Chainlit Documentation](https://docs.chainlit.io/)
- [Groq API](https://groq.com/docs/)
- [HuggingFace Embeddings](https://huggingface.co/)
- [RAGAS Framework](https://github.com/explodinggradients/ragas)
