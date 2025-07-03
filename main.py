# demo_flow.py

# 1. FastAPI Backend (main.py)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from langgraph_agents import run_agent_chain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryInput(BaseModel):
    query: str
    history: list[str] = []

@app.post("/process_query")
async def process_query(input_data: QueryInput):
    # summary, data = await run_agent_chain(input_data.query, input_data.history)
    # return {"summary": summary, "data": data}

    # MOCKED response (simulate GPT + SQL output)
    mock_summary = (
        "📉 In Q2 2024, revenue declined by 38% compared to Q1. "
        "This drop was primarily driven by a sharp rise in policy cancellations "
        "in the North American Auto segment, especially among SMB clients. "
        "Additionally, fewer high-premium policies were issued in Q2, and "
        "Enterprise customer activity dropped significantly."
    )

    mock_data = [
        {"quarter": "Q1-2024", "total_premium": 9900, "active_policies": 5, "cancelled_policies": 0},
        {"quarter": "Q2-2024", "total_premium": 3900, "active_policies": 2, "cancelled_policies": 3},
    ]

    return {"summary": mock_summary, "data": mock_data}

