import weaviate
from weaviate.auth import AuthApiKey
from pypdf import PdfReader
from transformers import AutoTokenizer

# Ausfüllbare Config
WEAVIATE_URL = "URL"  # Weavitate URL 
WEAVIATE_API_KEY = "KEY"  # Weaviate API Key 
PDF_PATH = "pdf.pdf"  # Pfad zur einzulesenden PDF
CLASS_NAME = "ChunkBeispiel"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" # Modell für Tokenizer und Embedding 
CHUNK_SIZE = 500  # Maximale Anzahl von Tokens pro Chunk
CHUNK_OVERLAP = 50  # Anzahl der überlappenden Tokens zwischen den Chunks

# Weaviate Client initialisieren
try:
    client = weaviate.Client(
        url=WEAVIATE_URL,
        auth_client_secret=AuthApiKey(WEAVIATE_API_KEY) if WEAVIATE_API_KEY else None,
        additional_headers={
            "X-OpenAI-Api-Key": "KEY"
        }
    )
    client.is_ready()
    print("Verbindung zu Weaviate erfolgreich hergestellt!")
except Exception as e:
    print(f"Fehler bei Verbindung zu Weaviate: {e}")
    exit()

# Definition vom Schema
def create_weaviate_schema():
    schema = {
        "classes": [
            {
                "class": CLASS_NAME,
                "description": "Ein Chunk aus einem Dokument",
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "Der Textinhalt des Chunks",
                    },
                    {
                        "name": "pageNumber",
                        "dataType": ["int"],
                        "description": "Die Seitenzahl des Chunks im Originaldokument",
                    },
                    {
                        "name": "sourceFile",
                        "dataType": ["text"],
                        "description": "Der Name der Quelldatei",
                    }
                ],
                "vectorizer": "text2vec-transformers", 
                "moduleConfig": {
                    "text2vec-transformers": { 
                        "vectorizeClassName": False,
                        "model": MODEL_NAME
                    }
                }
            }
        ]
    }
    if not client.schema.contains(schema):
        client.schema.create(schema)
        print(f"Schema für Klasse '{CLASS_NAME}' wurde erstellt.")
    else:
        print(f"Schema für Klasse '{CLASS_NAME}' ist bereits vorhanden.")

# PDF lesen und chunken
def get_pdf_chunks(pdf_path, chunk_size, chunk_overlap):
    reader = PdfReader(pdf_path)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    chunks = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue

        tokens = tokenizer.encode(text, add_special_tokens=False)
        
        start_index = 0
        while start_index < len(tokens):
            end_index = min(start_index + chunk_size, len(tokens))
            chunk_tokens = tokens[start_index:end_index]
            chunk_text = tokenizer.decode(chunk_tokens)
            
            chunks.append({
                "content": chunk_text,
                "pageNumber": i + 1,
                "sourceFile": pdf_path.split("/")[-1] 
            })
            
            if end_index == len(tokens):
                break
            
            start_index += chunk_size - chunk_overlap
            
    return chunks

# Chunks in Weaviate DB speicher
def import_chunks_to_weaviate(chunks):
    print(f"Starte Import von {len(chunks)} Chunks nach Weaviate...")
    with client.batch as batch:
        batch.batch_size = 100 
        for i, chunk in enumerate(chunks):
            properties = {
                "content": chunk["content"],
                "pageNumber": chunk["pageNumber"],
                "sourceFile": chunk["sourceFile"]
            }
            try:
                batch.add_data_object(
                    data_object=properties,
                    class_name=CLASS_NAME
                )
                if (i + 1) % batch.batch_size == 0:
                    print(f"  {i+1}/{len(chunks)} Chunks hinzugefügt...")
            except Exception as e:
                print(f"Fehler beim Hinzufügen von Chunk {i}: {e}")
    print(f"Import abgeschlossen. {len(chunks)} Chunks verarbeitet.")

# Main
if __name__ == "__main__":
    create_weaviate_schema()
    
    print(f"Lese PDF: {PDF_PATH} und chuke den Text...")
    document_chunks = get_pdf_chunks(PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Insgesamt {len(document_chunks)} Chunks erstellt.")
    
    if document_chunks:
        import_chunks_to_weaviate(document_chunks)
    else:
        print("Keine Chunks zum Importieren gefunden.")