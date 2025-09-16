from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    query :str

@app.get("/")
def get_answer():
    return {"message": "hiiii"}


@app.post("/")
def post_query(query:QueryRequest):
    response = query_engine(query)
    return {"answer": response}
    