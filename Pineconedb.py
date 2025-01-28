import os
from dotenv import load_dotenv
from llm import LLM
from pinecone.grpc import PineconeGRPC as Pinecone

load_dotenv()

class PineconeVectorDB:

    def __init__(self):
        try:
            # Initialize Pinecone with API key
            self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            self.index = self.pc.Index("buildwise")
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
            self.pc = None
            self.index = None

    def insert_data(self, data):
        try:
            if self.index:
                self.index.upsert(data)
            else:
                print("Error: Pinecone index not initialized.")
        except Exception as e:
            print(f"Error inserting data into Pinecone: {e}")

    def query(self, query, top_k=10):
        try:
            if not self.index:
                print("Error: Pinecone index not initialized.")
                return None

            lm = LLM()
            embeded_query = lm.get_embeddings(query)
            results = self.index.query(vector=embeded_query, top_k=top_k, include_metadata=True)
            return results
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return None

# # Example usage
# try:
#     pinecone_vector_db = PineconeVectorDB()
#     if pinecone_vector_db.index:  # Ensure the index is properly initialized
#         results = pinecone_vector_db.query(query="example")
#         if results:
#             print(results)
#         else:
#             print("No results returned.")
# except Exception as e:
#     print(f"An error occurred in the main program: {e}")