from fastapi import FastAPI, Query
from rag_engine import generate_recommendation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend")
def recommend(destination: str = Query(...), budget: str = Query(None)):
    return generate_recommendation(destination, budget)
