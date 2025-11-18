from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Metadata

# Chargement avec nettoyage agressif
reader = SimpleDirectoryReader(
    input_dir="data/raw_pdfs",
    required_exts=[".pdf"],
    recursive=True,
    # Nettoyage Unstructured
    file_extractor={".pdf": lambda x: x},  # utilise Unstructured par défaut
    num_files_limit=None,
)

# Nettoyage supplémentaire : suppression headers/footers automatiques
documents = reader.load_data(
    show_progress=True,
    # Unstructured options pour PDFs français
    languages=["fra"],
    strategy="hi_res",  # meilleure OCR pour scans
    extract_images=False,
)

print(f"{len(documents)} documents chargés et nettoyés")