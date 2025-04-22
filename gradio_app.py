import gradio as gr
from pathlib import Path

from config import OCR_MODEL
from llm_document_parser.instructor_llm import extract_json_data_using_ollama_llm
from llm_document_parser.convert_doc_docling import (
    load_rapid_ocr_model,
    load_easy_ocr_model,
    load_ocr_mac_model,
    image_to_text
)

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

SYSTEM_PROMPT = (
    "Extract all transactions from the following statement. "
    "Each transaction must be returned as a JSON object with the fields: "
    "transaction_date (YYYY-MM-DD), description, amount, and transaction_type "
    "('deposit' or 'withdrawal'). All of these must be returned as a list of "
    "JSON objects under a key called 'transactions'."
)

OLLAMA_MODEL = "llama3.2"

def run_pipeline(image_path):
    result = image_to_text(document_converter, Path(image_path))
    text_data = result.document.export_to_markdown()
    return extract_json_data_using_ollama_llm(SYSTEM_PROMPT, text_data, OLLAMA_MODEL)

demo = gr.Interface(
    fn=run_pipeline,
    inputs=gr.Image(type="filepath", label="Upload Bank Statement Image"),
    outputs=gr.Textbox(label="Extracted Transactions (JSON)"),
    title="Bank Statement Parser",
    description="This app extracts transaction data from a bank statement using OCR and a local LLM."
)

if __name__ == "__main__":
    demo.launch()
