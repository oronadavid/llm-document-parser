# llm_postprocessing.py
"""
This module provides functions to postprocess the output from a large language model (LLM).
It includes functions to clean the response, normalize spacing,
and extract JSON data.
It uses regular expressions for text manipulation."""

# imports
import re
import json

def strip_markdown(text):
    """
    Remove markdown formatting from the text.
    Args:
        text (str): The input text with markdown formatting.
    Returns:
        str: The text without markdown formatting.
    """
    # Remove code blocks and markdown symbols
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"[#*_`]+", "", text)
    return text

def normalize_spacing(text):
    """
    Normalize spacing in the text.
    Args:
        text (str): The input text.
    Returns:
        str: The text with normalized spacing.
    """
    return re.sub(r'\s+', ' ', text).strip()

def extract_json(text):
    """
    Extract JSON data from the text.
    Args:
        text (str): The input text.
    Returns:
        dict: The extracted JSON data.
    """
    try:
        json_match = re.search(r'{.*}', text, flags=re.DOTALL)
        return json.loads(json_match.group()) if json_match else {}
    except Exception as e:
        return {"error": f"Failed to extract JSON: {str(e)}"}

def clean_response(
    response: str,
    strip_markdown=True,
    normalize_spacing=True,
    extract_json=False
):
    """
    Clean the LLM response based on the provided configuration.
    Args:
        response (str): The LLM response.
        strip_markdown (bool): Whether to strip markdown formatting.
        normalize_spacing (bool): Whether to normalize spacing.
        extract_json (bool): Whether to extract JSON data.
    Returns:
        str or dict: The cleaned response, either as a string or a dictionary.
    """
    # Apply steps one at a time based on config
    if strip_markdown:
        response = strip_markdown(response)
    
    if normalize_spacing:
        response = normalize_spacing(response)
    
    if extract_json:
        return extract_json(response)

    return response
