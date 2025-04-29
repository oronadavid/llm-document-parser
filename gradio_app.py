import gradio as gr
from pathlib import Path

import sys
from pathlib import Path

# Add the src/ directory to Python path
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from llm_document_parser.config import (
    OCR_MODEL,
    LLM_PROMPT,
    OLLAMA_MODEL,
    RESPONSE_MODEL
)
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

def run_pipeline(image_path):
    result = image_to_text(document_converter, Path(image_path))
    text_data = result.document.export_to_markdown()
    return extract_json_data_using_ollama_llm(prompt=LLM_PROMPT, text_data=text_data, ollama_model=OLLAMA_MODEL, response_model=RESPONSE_MODEL)

demo = gr.Interface(
    fn=run_pipeline,
    inputs=gr.Image(type="filepath", label="Upload Bank Statement Image"),
    outputs=gr.Textbox(label="Extracted Transactions (JSON)"),
    title="Bank Statement Parser",
    description=f"""This app extracts transaction data from a bank statement using OCR and a local LLM.
    Both models are specified in the config.py file.
    Current settings:
    - OCR: {OCR_MODEL}
    - LLM: {OLLAMA_MODEL}
    """
)

if __name__ == "__main__":
    demo.launch()
