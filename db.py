from pinecone.grpc import PineconeGRPC as Pinecone
from create_embeddings import create_embeddings

class PineconeVectorDB:
    def __init__(self):
        self.pc = Pinecone(
            api_key="pcsk_3VQuKn_TgeNaVxVikc14msUtJJXVEYsGcP46PS5w1gApkwijrFJ5erhSGhzPuGKxbp4SpD"
        )
        self.index = self.pc.Index("contech")

    def query(self, query, top_k=10):
        embedded_query = create_embeddings(query)
        results = self.index.query(
            vector=embedded_query,
            top_k=top_k,
            include_metadata=True
        )
        return results
