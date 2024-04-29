import chromadb
import ollama

# De esta clase hacer una subclase para hacerlo mas especifico de mi caso
class EmbeddingsDB:
    def __init__(self, pdf_reader=None, model: str = "phi3"):
        self.model = model
        self.pdf_reader = pdf_reader
        self.client = chromadb.Client()
        if self.pdf_reader:
            try:
                self.collection = self.client.create_collection(
                    name=self.pdf_reader.filename, 
                    metadata={"hnsw:space": "cosine"}
                )
            except:
                # print(f"Collection {self.pdf_reader.filename} already exists. Do you want to overwrite it?")
                # overwrite = input("Enter 'y' to overwrite, any other key to cancel: ")
                # if overwrite.lower() == 'y':
                #     self.client.delete_collection(name=self.pdf_reader.filename)
                #     self.collection = self.client.create_collection(
                #         name=self.pdf_reader.filename, 
                #         metadata={"hnsw:space": "cosine"}
                #     )
                # else:
                #     self.collection = self.collection = self.client.get_collection(name=self.pdf_reader.filename)
                self.client.delete_collection(name=self.pdf_reader.filename)
                self.collection = self.client.create_collection(
                    name=self.pdf_reader.filename, 
                    metadata={"hnsw:space": "cosine"}
                )
    def get_embedding(self, text):
        """Generate an embedding for the provided text using the 'llama3' model."""
        embedding_dict = ollama.embeddings(model=self.model, prompt=text)
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

class SimilaritySearch(EmbeddingsDB):
    def __init__(self, pdf_reader=None):
        super().__init__(pdf_reader=pdf_reader)
        if pdf_reader:
            self.add_documents_to_db()

    def similar_text(self, query_text, n_results=2):
        """Search for documents similar to the given text. Then get the ids of the documents and return the text using pdf_reader.get_part(id)."""
        results = self.query_documents(query_text, n_results=n_results)

        print(f"{query_text}--->{results}")
        # Get ids of the documents
        ids = [int(id) for id in results['ids'][0]]

        # Get the documents from the PDF reader
        text = ""
        for id in ids:
            text += self.pdf_reader.get_part(id).text + "\n"

        # Get the number of page
        pages = set([self.pdf_reader.get_part(id).metadata['page'] for id in ids])
        return text, pages
    
class Search(SimilaritySearch):
    def __init__(self, pdf_reader=None):
        super().__init__(pdf_reader=pdf_reader)
        self.query_company = "Company which won the contract"
        self.query_amount = 'Valor estimado del contrato'
        self.query_adjudicadora = 'Contracting Authority referred as "Organismo" or "Entidad adjudicadora"' # I do not write name because it is closer to the name of a person, for example Isabel, than to the name of an institution
        self.query_tipo = 'type of contract "Objetivo de contrato", "Tipo"'
        self.query_tramitacion = 'type of procedure "Procedimiento", "Tramitación"'


        self.text_company = self.similar_text(self.query_company, n_results=2)
        self.text_amount = self.similar_text(self.query_amount, n_results=2)
        self.text_adjudicadora = self.similar_text(self.query_adjudicadora, n_results=2)
        self.text_tipo = self.similar_text(self.query_tipo, n_results=2)
        self.text_tramitacion = self.similar_text(self.query_tramitacion, n_results=2)