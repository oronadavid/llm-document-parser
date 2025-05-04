import gradio as gr
from pathlib import Path
import sys
import os
import pandas as pd

# Add src/ to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from llm_document_parser.config import OCR_MODEL, OLLAMA_MODEL
from llm_document_parser.instructor_llm import extract_json_data_using_ollama_llm
from llm_document_parser.convert_doc_docling import (
    load_rapid_ocr_model,
    load_easy_ocr_model,
    load_ocr_mac_model,
    image_to_text
)

print("RUNNING gradio_app.py FROM:", __file__)

# Load OCR model based on config
def load_ocr_model_from_config(model_type: str):
    if model_type == "rapid":
        return load_rapid_ocr_model(
            "PP-OCRv4/ch_PP-OCRv4_det_server_infer.onnx",
            "PP-OCRv3/ch_PP-OCRv3_rec_infer.onnx",
            "PP-OCRv3/ch_ppocr_mobile_v2.0_cls_train.onnx"
        )
    elif model_type == "easy":
        return load_easy_ocr_model()
    elif model_type == "ocrmac":
        return load_ocr_mac_model()
    else:
        raise ValueError(f"Unknown OCR model type in config: {model_type}")

document_converter = load_ocr_model_from_config(OCR_MODEL)

# System prompt for LLM
SYSTEM_PROMPT = (
    "Extract all transactions from the following statement. "
    "Each transaction must be returned as a JSON object with the fields: "
    "transaction_date (YYYY-MM-DD), description, amount, and transaction_type "
    "('deposit' or 'withdrawal'). All of these must be returned as a list of "
    "JSON objects under a key called 'transactions'."
)

# Full processing pipeline
def run_pipeline(image_path):
    result = image_to_text(document_converter, Path(image_path))
    text_data = result.document.export_to_markdown()

    llm_result = extract_json_data_using_ollama_llm(SYSTEM_PROMPT, text_data, OLLAMA_MODEL)

    # Try parsing the JSON output to display it as a CSV-style DataFrame
    try:
        import json
        parsed = json.loads(llm_result)
        transactions = parsed.get("transactions", [])
        df = pd.DataFrame(transactions)
        return df.to_csv(index=False)
    except Exception as e:
        return f"Failed to format output: {e}\nRaw output:\n{llm_result}"

# Gradio interface
demo = gr.Interface(
    fn=run_pipeline,
    inputs=gr.Image(type="filepath", label="Upload Bank Statement Image"),
    outputs=gr.Textbox(label="Extracted Transactions (CSV)"),
    title="Bank Statement Parser",
    description=f"""This app extracts transaction data from a bank statement using OCR and a local LLM.
    
OCR Model: `{OCR_MODEL}`  
LLM Model: `{OLLAMA_MODEL}`  
Results are returned in CSV format.
"""
)

if __name__ == "__main__":
    demo.launch()
