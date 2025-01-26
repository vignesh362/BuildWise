import os
from dotenv import load_dotenv
from createEmbeddings import creatEmbedding
from pinecone.grpc import PineconeGRPC as Pinecone

load_dotenv()

class PineconeVectorDB:

    def __init__(self):
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = pc.Index("contech")
    
    def insert_data(self, data):
        self.index.upsert(data)
    
    def query(self, query, top_k=10):
        embeded_query = creatEmbedding(query)
        results = self.index.query(vector=embeded_query, top_k=top_k, include_metadata=True)
        return results

pinecone_vector_db = PineconeVectorDB()
pinecone_vector_db.query(query="example")
