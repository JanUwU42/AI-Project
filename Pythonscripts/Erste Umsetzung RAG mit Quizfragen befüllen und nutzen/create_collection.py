import weaviate
from weaviate.classes.config import Configure

client = weaviate.connect_to_local()

questions = client.collections.create(
    name="Question",
    vectorizer_config=Configure.Vectorizer.text2vec_ollama(     
        api_endpoint="http://host.docker.internal:11434",       
        model="nomic-embed-text",                               
    ),
    generative_config=Configure.Generative.ollama(              
        api_endpoint="http://host.docker.internal:11434",       
        model="llama3.2",                                       
    )
)

client.close()  