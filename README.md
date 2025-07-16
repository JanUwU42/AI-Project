# AI-Project
This project sets up a local Retrieval-Augmented Generation (RAG) system using a Docker container with Ollama and OpenWebUI. You can pull pre-trained models, add a custom knowledge base (e.g., university resources), and use it to ask questions and support your studies. Everything runs locally, so your data stays private and you don’t rely on big tech providers.

## Setup
Open-WebUI & Ollama Docker Container

```
docker run -d -p 3000:8080 -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama
```
Gewünschtes LLM pullen
```
sudo docker exec -it open-webui ollama pull mistral:7b-instruct-v0.3-q4_K_M
```
### Knowledge Base erstellen
In open-webui:
Workspace -> Knowledge -> + -> Daten angeben und Dateien hochladen
### Neues Modell erstellen
Workspace -> Models -> + -> Name Angeben, gewünschtes Modell auswählen, gewünschte Knowledge Base auswählen -> speichern
### Neuer Chat
Erstelltes Modell auswählen und chatten

## Used Tools
### Open Web UI
https://github.com/open-webui/open-webui

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform designed to operate entirely offline. It supports various LLM runners like Ollama and OpenAI-compatible APIs, with built-in inference engine for RAG, making it a powerful AI deployment solution.

### Ollama
https://github.com/ollama/ollama

Get up and running with large language models.

### Hugging Face
https://github.com/huggingface

The platform where the machine learning community collaborates on models, datasets, and applications.

### Docker
https://www.docker.com/

Docker helps developers build, share, run, and verify applications anywhere — without tedious environment configuration or management.


