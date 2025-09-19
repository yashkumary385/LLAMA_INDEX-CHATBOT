import os
from fastapi import FastAPI
from pydantic import BaseModel
 
app = FastAPI()

# making schmea
class QuerySchema(BaseModel):
    query :str

    
# import pinecone
from dotenv import load_dotenv
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.gemini import Gemini
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex,StorageContext
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


# print(PINECONE_API_KEY)
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME= os.getenv("PINECONE_INDEX_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#intialization of pinecone 
pc = Pinecone(api_key=PINECONE_API_KEY)
# pinecone.init(api_key=PINECONE_API_KEY, environment="eu-west1-gcp")
pinecone_index =pc.Index(PINECONE_INDEX_NAME)
print(PINECONE_INDEX_NAME)

# pinecone_index = pinecone.Index(PINECONE_INDEX_NAME)
#turn this into an pinecone vector store
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# # to put into storage for llama to query
# #StorageContext is like a container for your vector store, ready to use in an index.
storage_context = StorageContext.from_defaults(vector_store=vector_store)
#  #embed model 
embed_model = GoogleGenAIEmbedding(model_name="text-embedding-004")#making index
index =VectorStoreIndex.from_vector_store(vector_store=vector_store,
storage_context=storage_context,
embed_model=embed_model)


llm = Gemini(model_name="gemini-2.5-flash",
            #  generation_config={
            #      "max_output_tokens":256
            #  }
             )

from llama_index.core.response_synthesizers import get_response_synthesizer
response_synthesizer = get_response_synthesizer(llm=llm)

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
postprocessor = SimilarityPostprocessor(similarity_cutoff=0.50) # for similarity greater than 
retriever = VectorIndexRetriever(index=index, similarity_top_k=2) # takes out the top chunks from the database
query_engine = RetrieverQueryEngine(retriever=retriever, response_synthesizer= response_synthesizer,node_postprocessors=[postprocessor]) # retriever engine give the chunks and text to the llm for text generation 




@app.get("/")
def working():
    return {"Message":"Everything is working"}



@app.post("/query")
def query(req : QuerySchema):
    print(req.query)
    response = query_engine.query(req.query)
    # print(response.response)
    return {"answer":response.response}