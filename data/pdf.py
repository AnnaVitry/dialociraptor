import os
from pathlib import Path
import pymupdf4llm

def create_recap_from_pdfs():
    """
    Lit tous les fichiers PDF dans le répertoire du script,
    en extrait le contenu au format Markdown, et les combine
    dans un unique fichier de récapitulatif.
    """
    # Le script est dans le dossier 'data', nous cherchons donc les PDF ici.
    script_dir = Path(__file__).parent
    output_file = script_dir / "recapitulatif_pdfs.md"
    
    all_md_content = []
    
    print(f"🔍 Recherche de fichiers PDF dans : {script_dir}")

    # Parcourir tous les fichiers dans le dossier
    for file_path in script_dir.glob("*.pdf"):
        print(f"  -> Traitement du fichier : {file_path.name}")
        try:
            # Extraire le contenu du PDF en Markdown
            md_text = pymupdf4llm.to_markdown(str(file_path))
            
            # Ajouter un titre avec le nom du fichier
            all_md_content.append(f"# Fichier : {file_path.name}\n\n{md_text}")
            
        except Exception as e:
            print(f"    [ERREUR] Impossible de traiter le fichier {file_path.name}: {e}")

    if not all_md_content:
        print("❌ Aucun fichier PDF n'a pu être traité.")
        return

    # Écrire tout le contenu collecté dans le fichier de récapitulatif
    output_file.write_text("\n\n---\n\n".join(all_md_content), encoding="utf-8")
    print(f"\n✅ Récapitulatif créé avec succès : {output_file}")

if __name__ == "__main__":
    create_recap_from_pdfs()