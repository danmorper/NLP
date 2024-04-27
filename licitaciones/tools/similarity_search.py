import chromadb
import ollama

# De esta clase hacer una subclase para hacerlo mas especifico de mi caso
class EmbeddingsDB:
    def __init__(self, pdf_reader=None):
        self.pdf_reader = pdf_reader
        self.client = chromadb.Client()
        if self.pdf_reader:
            try:
                self.collection = self.client.create_collection(
                    name=self.pdf_reader.filename, 
                    metadata={"hnsw:space": "cosine"}
                )
            except:
                print(f"Collection {self.pdf_reader.filename} already exists. Do you want to overwrite it?")
                overwrite = input("Enter 'y' to overwrite, any other key to cancel: ")
                if overwrite.lower() == 'y':
                    self.collection = self.client.delete_collection(name=self.pdf_reader.filename)
                    self.collection = self.client.create_collection(
                        name=self.pdf_reader.filename, 
                        metadata={"hnsw:space": "cosine"}
                    )
                else:
                    self.collection = self.collection = self.client.get_collection(name=self.pdf_reader.filename)
    def get_embedding(self, text):
        """Generate an embedding for the provided text using the 'llama3' model."""
        embedding_dict = ollama.embeddings(model='llama3', prompt=text)
        vector = embedding_dict['embedding']
        return vector

    def add_documents_to_db(self):
        """Add documents to the database with their embeddings."""
        if not self.pdf_reader:
            raise ValueError("PDF reader is not initialized.")
        
        for i, part in enumerate(self.pdf_reader.document_parts, start=1):
            vector = self.get_embedding(part.text)
            self.collection.add(
                embeddings=[vector],
                documents=[part.text],
                metadatas=[part.metadata],
                ids=[str(i)]
            )

    def query_documents(self, query_text, n_results=3):
        """Query the database for documents similar to the given text."""
        query_vector = self.get_embedding(query_text)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=n_results
        )
        return results