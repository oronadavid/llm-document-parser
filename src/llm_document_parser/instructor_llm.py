from typing import List, Literal
import instructor
from openai import OpenAI
from pydantic import BaseModel
from datetime import date

import ollama

class BankStatementEntry(BaseModel):
    transaction_date: date | None
    description: str | None
    amount: float | None
    transaction_type: Literal['deposit', 'withdrawal', None]

class BankStatement(BaseModel):
    transactions: List[BankStatementEntry]

def pull_ollama_model(model: str):
    """
    Pull a model from ollama if it is not already downloaded
    """
    for downloaded_model in ollama.list()["models"]:
        if downloaded_model == model:
            return
    
    print(f"Downloading {model} model...")
    ollama.pull(model)

def extract_json_data_using_ollama_llm(prompt: str, text_data: str, ollama_model: str) -> str:
    """
    Pass prompt and data into an ollama LLM using instructor
    """
    pull_ollama_model(ollama_model)

    client = instructor.from_openai(
        OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        ),
        mode=instructor.Mode.JSON
    )

    resp = client.chat.completions.create(
        model=ollama_model,
        messages=[
            {
                'role': 'system',
                'content': prompt
            },
            {
                'role': 'user',
                'content': text_data
            },
        ],
        response_model=BankStatement,
        max_retries=3
    )

    return resp.model_dump_json(indent=4)
