# llm.py
"""
This module provides functions to analyze bank statements using a large language model (LLM).
It includes functions to preprocess the text, run the LLM, and postprocess the output.
It also includes a function to run the LLM on a folder of images.
"""

# imports
import os
import json
from preprocessing.llm_preprocessing import preprocess_text
from ollama import chat, ChatResponse
from postprocessing.llm_postprocessing import clean_response


# Load LLM preprocessing settings from config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")
with open(CONFIG_PATH) as f:
    config = json.load(f)
# Load the config file, including LLM preprocessing and postprocessing settings
llm_cfg = config.get("llm_preprocessing", {})
llm_settings = config.get("llm", {})
llm_prompt = llm_settings.get("prompt", "You are an assistant.")
llm_post_cfg = config.get("llm_postprocessing", {})


def analyze_bank_statement(text, bboxes, model="llama3.2"):
    """
    Analyze a bank statement using a large language model (LLM).
    Args:
        text (str): The raw OCR text.
        bboxes (list): List of bounding boxes from OCR.
        model (str): The LLM model to use.
    Returns:
        str: The LLM's response.
    """
    response: ChatResponse = chat(model=model, messages=[
        {
            'role': 'system',
            'content': llm_prompt
        },
        {
            'role': 'user',
            'content': f"Extracted Text:\n{text}\n\nBounding Box Metadata:\n{json.dumps(bboxes)}"
        },
    ])
    return response['message']['content']


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run LLM on OCR outputs.")
    parser.add_argument("model", type=str, help="Model to use")
    parser.add_argument("--input_dir", default="outputs", help="Directory with .txt and .json files")

    args = parser.parse_args()

    for fname in os.listdir(args.input_dir):
        if fname.endswith(".txt"):
            base = os.path.splitext(fname)[0]

            # Load raw OCR text and bounding boxes
            with open(os.path.join(args.input_dir, f"{base}.txt"), "r", encoding="utf-8") as f:
                raw_text = f.read()
            with open(os.path.join(args.input_dir, f"{base}.json"), "r", encoding="utf-8") as f:
                bboxes = json.load(f)

            # Apply preprocessing steps to the OCR text based on config
            preprocessed_text = preprocess_text(
                raw_text,
                clean=llm_cfg.get("clean_text", True),
                normalize=llm_cfg.get("normalize_whitespace", True),
                remove_headers=llm_cfg.get("remove_headers_footers", True),
                standardize_dates_flag=llm_cfg.get("standardize_dates", True),
                standardize_amounts_flag=llm_cfg.get("standardize_amounts", True),
                extract_lines=llm_cfg.get("extract_transaction_lines", True)
            )

            #  Run LLM on the preprocessed text
            llm_output = analyze_bank_statement(preprocessed_text, bboxes, args.model)
            # Postprocess the LLM's response using config toggles
            final_result = clean_response(
                llm_output,
                strip_markdown=llm_post_cfg.get("strip_markdown", True),
                normalize_spacing=llm_post_cfg.get("normalize_spacing", True),
                extract_json=llm_post_cfg.get("extract_json", False)
            )

            # Output the final result
            print(f"\n[{args.model}] --- {base} ---")
            print(final_result)


