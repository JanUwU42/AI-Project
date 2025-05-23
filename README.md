# AI-Project
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
