from ragas import evaluate
from ragas.metrics import context_precision, answer_relevancy, faithfulness
from datasets import Dataset
from llama_index.core import StorageContext, load_index_from_storage
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Charger l'index
storage_context = StorageContext.from_defaults(persist_dir="./index_storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

# 2. Jeu de données de test (Ground Truth) - À compléter avec 5-8 questions réelles
test_questions = [
    "Quels sont les symptômes du diabète de type 2 ?",
    "Quelle est la valeur cible de l'HbA1c ?",
    "Le diabète de type 1 est-il héréditaire ?"
]

test_ground_truths = [
    ["Les symptômes incluent une soif excessive, des mictions fréquentes, la fatigue."],
    ["La cible est généralement inférieure à 7% pour la plupart des patients."],
    ["Il existe une prédisposition génétique, mais c'est une maladie auto-immune."]
]

print("Génération des réponses par le RAG...")

answers = []
contexts = []

# 3. Générer les réponses du RAG pour l'évaluation
for question in test_questions:
    response = query_engine.query(question)
    answers.append(response.response)
    # Ragas a besoin du texte des chunks récupérés (contexts)
    contexts.append([node.node.text for node in response.source_nodes])

# 4. Préparer le Dataset pour Ragas
data_dict = {
    "question": test_questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": test_ground_truths
}
dataset = Dataset.from_dict(data_dict)

# 5. Lancer l'évaluation
print("Calcul des métriques Ragas...")
results = evaluate(
    dataset=dataset,
    metrics=[
        context_precision, # Est-ce que le RAG a trouvé le bon document ?
        answer_relevancy,  # Est-ce que la réponse répond à la question ?
        faithfulness       # Est-ce que la réponse respecte le contexte (pas d'hallucination) ?
    ]
)

# 6. Afficher et sauvegarder les résultats
print(results)
df_results = results.to_pandas()
df_results.to_csv("resultats_evaluation_ragas.csv")
print("Résultats sauvegardés dans resultats_evaluation_ragas.csv")