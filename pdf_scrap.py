# pdf_scrap.py
# Extraction texte + métadonnées (Version Compatible Standard)

import os
from pathlib import Path
import pandas as pd

from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader

# --- CONSTANTE : CHEMIN ABSOLU ---
ABSOLUTE_INPUT_DIR = "C:/Users/Apprenant/Desktop/Simplon/Dev IA/learning/dialociraptor/data"
# ---------------------------------

def load_pdfs_robust(input_dir: str = ABSOLUTE_INPUT_DIR):
    """
    Charge tous les PDFs du dossier.
    Note: Utilise le lecteur standard (pypdf).
    """
    print("⬇️ Chargement et extraction des PDFs en cours...")

    # CORRECTION ICI : Le PDFReader standard ne prend pas d'arguments complexes
    pdf_reader = PDFReader()

    reader = SimpleDirectoryReader(
        input_dir=input_dir,
        required_exts=[".pdf"],
        recursive=True,
        file_extractor={".pdf": pdf_reader},
        # num_files_limit=10, # Décommentez pour tester sur peu de fichiers si ça plante
    )

    docs = reader.load_data(show_progress=True)
    print(f"✅ {len(docs)} documents chargés.")
    return docs


def docs_to_dataframe(docs):
    """
    Convertit la liste de Document LlamaIndex en DataFrame propre.
    """
    print("Conversion en DataFrame et nettoyage...")

    data = []
    for doc in docs:
        meta = doc.metadata
        texte = doc.text

        data.append({
            "file_name": meta.get("file_name", ""),
            "file_path": meta.get("file_path", ""),
            "page_label": meta.get("page_label", ""),
            "texte": texte,
            # Gestion robuste du titre
            "titre": meta.get("title") or meta.get("subject") or meta.get("file_name", "").replace(".pdf", ""),
            "auteur": meta.get("author"),
            "date": meta.get("creation_date") or meta.get("mod_date"),
            "description": meta.get("keywords") or meta.get("subject"),
            "nb_pages_total": meta.get("total_pages"),
        })

    df = pd.DataFrame(data)

    # Si le DataFrame est vide, on arrête là
    if df.empty:
        print("⚠️ Aucun document valide extrait.")
        return df

    # Nettoyage
    df = df[df["texte"].notnull()]
    df["texte"] = df["texte"].str.strip()
    # Réduit les sauts de ligne excessifs
    df["texte"] = df["texte"].str.replace(r"\n{3,}", "\n\n", regex=True)
    
    # On garde une ligne par page ou par fichier selon le découpage
    # Ici on dédoublonne par texte exact pour éviter les pages identiques
    df = df.drop_duplicates(subset=["texte"])
    
    df["longueur"] = df["texte"].apply(len)
    # Filtre les pages trop vides (moins de 50 caractères pour être sûr de garder le contenu)
    df = df[df["longueur"] > 50]

    df = df.reset_index(drop=True)

    print(f"🧹 Nettoyage terminé → {len(df)} pages/documents conservés.")
    return df


def main():
    input_dir = Path(ABSOLUTE_INPUT_DIR)
    
    # Chemin de sortie relatif au script actuel
    project_root = Path(__file__).parent
    # On sauvegarde directement à côté du script pour éviter les erreurs de dossier 'src' s'il n'existe pas
    output_path = project_root / "corpus_pdfs_clean.csv"

    if not input_dir.exists():
        print(f"❌ Dossier {input_dir} introuvable.")
        return

    docs = load_pdfs_robust(str(input_dir))
    
    if not docs:
        print("❌ Aucune donnée extraite. Vérifiez que les PDFs contiennent du texte sélectionnable (pas des images scanner).")
        return

    df = docs_to_dataframe(docs)

    if not df.empty:
        df.to_csv(output_path, index=False)
        print(f"\n📁 Fichier sauvegardé : {output_path}")
    else:
        print("\n⚠️ Le fichier CSV n'a pas été créé car le DataFrame est vide.")


if __name__ == "__main__":
    main()