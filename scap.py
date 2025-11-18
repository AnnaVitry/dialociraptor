import pandas as pd
from trafilatura import fetch_url, extract, extract_metadata


# -----------------------------------------------------------
# 1) LISTE DES URLS À EXTRAIRE
# -----------------------------------------------------------
URLS = [

    # ----------------------------------------------------
    # 1. INSTITUTIONS OFFICIELLES
    # ----------------------------------------------------
    # HAS
    "https://www.has-sante.fr/jcms/c_2606780/fr/diabete",
    "https://www.has-sante.fr/recherche?text=diabete",

    # Santé Publique France
    "https://www.santepubliquefrance.fr/maladies-et-traumatismes/diabete",
    "https://www.santepubliquefrance.fr/dossiers/diabete",

    # Ameli
    "https://www.ameli.fr/assure/sante/themes/diabete",
    "https://www.ameli.fr/assure/sante/themes/diabete/comprendre-diabete",
    "https://www.ameli.fr/assure/sante/bons-gestes/diabete-et-prevention",

    # Ministère de la santé (général)
    "https://solidarites-sante.gouv.fr/",


    # ----------------------------------------------------
    # 2. RECHERCHE SCIENTIFIQUE (INSERM / CNRS / Pasteur)
    # ----------------------------------------------------
    # INSERM
    "https://www.inserm.fr/dossier/diabete/",
    "https://www.inserm.fr/recherche/actualites/",

    # Institut Pasteur
    "https://www.pasteur.fr/fr/recherche/diabete",

    # CNRS
    "https://www.cnrs.fr/fr/recherche?q=diabete",


    # ----------------------------------------------------
    # 3. SOCIÉTÉS SAVANTES & ASSOCIATIONS PATIENTS
    # ----------------------------------------------------
    # Société Francophone du Diabète
    "https://www.sfdiabete.org/",

    # Fédération Française des Diabétiques
    "https://www.federationdesdiabetiques.org/",

    # Diabète France
    "https://www.diabete-france.fr/",

    # Fondation du Diabète
    "https://www.fondation-diabete.org/",


    # ----------------------------------------------------
    # 4. CHU & HÔPITAUX (fiches pédagogiques)
    # ----------------------------------------------------
    "https://www.chu-lille.fr/?s=diabete",
    "https://www.chu-toulouse.fr/spip.php?page=recherche&recherche=diabete",
    "https://www.aphp.fr/search/node/diabete",


    # ----------------------------------------------------
    # 5. NUTRITION / PRÉVENTION
    # ----------------------------------------------------
    # PNNS — Manger Bouger
    "https://www.mangerbouger.fr/",

    # ANSES
    "https://www.anses.fr/fr",


    # ----------------------------------------------------
    # 6. DONNÉES & STATISTIQUES
    # ----------------------------------------------------
    # DREES
    "https://drees.solidarites-sante.gouv.fr/rechercher?search_api_fulltext=diab%C3%A8te",

    # INSEE
    "https://www.insee.fr/fr/statistiques?q=diabete",

]

# -----------------------------------------------------------
# 2) TÉLÉCHARGEMENT DES HTML BRUTS
# -----------------------------------------------------------

def download_pages(urls):
    print("Téléchargement des pages...")
    pages = []

    for url in urls:
        downloaded = fetch_url(url)
        if downloaded is None:
            print(f"[ERREUR] Impossible de télécharger : {url}")
            continue

        pages.append({
            "url": url,
            "html": downloaded
        })

    print(f"➜ {len(pages)} pages téléchargées.")
    return pages


# -----------------------------------------------------------
# 3) EXTRACTION TEXTE + MÉTADONNÉES (ROBUSTE)
# -----------------------------------------------------------

def extract_content(pages):
    print("Extraction du contenu...")

    data = []

    for item in pages:
        html = item["html"]
        url = item["url"]

        # 1. Texte principal Trafilatura
        texte = extract(html)

        # 2. Métadonnées (le type varie selon la page)
        meta = extract_metadata(html)

        # valeurs par défaut
        titre = None
        auteur = None
        date = None
        description = None

        # CAS 1 : meta = dict
        if isinstance(meta, dict):
            titre = meta.get("title")
            auteur = meta.get("author")
            date = meta.get("date")
            description = meta.get("description")

        # CAS 2 : meta = Document (objet interne)
        else:
            titre = getattr(meta, "title", None)
            auteur = getattr(meta, "author", None)
            date = getattr(meta, "date", None)
            description = getattr(meta, "description", None)

        data.append({
            "url": url,
            "texte": texte,
            "titre": titre,
            "auteur": auteur,
            "date": date,
            "description": description
        })

    print(f"➜ Extraction terminée pour {len(data)} pages.")
    return data


# -----------------------------------------------------------
# 4) NETTOYAGE AVEC PANDAS
# -----------------------------------------------------------

def clean_dataframe(data):
    print("Nettoyage du DataFrame...")

    df = pd.DataFrame(data)

    # supprimer lignes vides
    df = df[df["texte"].notnull()]

    # strip espaces / sauts de ligne
    df["texte"] = df["texte"].str.strip()

    # supprimer doublons
    df = df.drop_duplicates(subset="url")
    df = df.drop_duplicates(subset="texte")

    # longueur du texte
    df["longueur"] = df["texte"].apply(len)

    # filtrer texte trop court
    df = df[df["longueur"] > 300]

    print("➜ Nettoyage terminé.")
    return df


# -----------------------------------------------------------
# 5) MAIN
# -----------------------------------------------------------

def main():
    pages = download_pages(URLS)
    extracted = extract_content(pages)
    df = clean_dataframe(extracted)

    df.to_csv("./src/corpus_diabete_clean.csv", index=False)
    print("\n📁 Fichier sauvegardé : corpus_diabete_clean.csv")


# -----------------------------------------------------------
# POINT D’ENTRÉE
# -----------------------------------------------------------

if __name__ == "__main__":
    main()
