import instructor
from openai import OpenAI
from pydantic import BaseModel
from typing import Type

import ollama

def pull_ollama_model(model: str):
    """
    Pull a model from ollama if it is not already downloaded
    """
    if not model.__contains__(":"):
        model += ":latest"

    for downloaded_model in ollama.list()["models"]:
        if downloaded_model['model']== model:
            print(f"Model {downloaded_model['model']} is installed")
            return
    
    print(f"Model {model} is not installed")
    print(f"Downloading {model} model...")
    ollama.pull(model)

def extract_json_data_using_ollama_llm(prompt: str, text_data: str, ollama_model: str, response_model: Type[BaseModel]) -> str:
    """
    Pass prompt and data into an ollama LLM using instructor
    """
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
        response_model=response_model,
        max_retries=3
    )

    return resp.model_dump_json(indent=4)
