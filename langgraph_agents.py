# 2. LangGraph Agent Chain (langgraph_agents.py)
from langgraph.graph import StateGraph
from snowflake_client import run_query
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4")

async def generate_sql(state):
    question = state["question"]
    prompt = PromptTemplate.from_template("""
        Translate the business question into a Snowflake SQL query over the `policies_2024` table.
        Question: {question}
        Focus on fields like issue_date, region, product_line, customer_segment, premium_amount, and status.
    """)
    sql = await llm.apredict(prompt.format(question=question))
    return {"sql": sql.strip()}

async def execute_sql(state):
    sql = state["sql"]
    data = run_query(sql)
    return {"data": data}

async def summarize(state):
    data = state["data"]
    question = state["question"]
    prompt = PromptTemplate.from_template("""
        Given the data: {data}
        Answer the question: {question}
        Provide a business executive summary that is relevant to leadership in the insurance domain.
    """)
    summary = await llm.apredict(prompt.format(data=str(data), question=question))
    return {"summary": summary}

def build_langgraph():
    builder = StateGraph()
    builder.add_node("GenerateSQL", generate_sql)
    builder.add_node("RunSQL", execute_sql)
    builder.add_node("Summarize", summarize)
    builder.set_entry_point("GenerateSQL")
    builder.add_edge("GenerateSQL", "RunSQL")
    builder.add_edge("RunSQL", "Summarize")
    builder.set_finish_point("Summarize")
    return builder.compile()

async def run_agent_chain(question, history):
    graph = build_langgraph()
    result = await graph.invoke({"question": question})
    return result["summary"], result.get("data", [])
