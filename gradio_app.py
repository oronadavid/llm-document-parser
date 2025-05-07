import gradio as gr
from pathlib import Path
import sys
import os
import pandas as pd
import importlib
from docling.document_converter import DocumentConverter

# Add src/ to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

#from llm_document_parser.config import (
#    TESSERACT_TESSDATA_LOCATION,
#    OCR_MODEL,
#    LLM_PROMPT,
#    OLLAMA_MODEL,
#    RESPONSE_MODEL,
#    EXPORT_TYPE,
#    OUTPUT_FOLDER,
#    OUTPUT_FILE_NAME
#)

import llm_document_parser.config as config

from llm_document_parser.instructor_llm import extract_json_data_using_ollama_llm, pull_ollama_model
from llm_document_parser.convert_doc_docling import (
    load_rapid_ocr_model,
    load_easy_ocr_model,
    load_ocr_mac_model,
    load_tesseract_model,
    image_to_text
)
from llm_document_parser.export_data import export_as_csv, export_as_json, combine_json_data_into_df, convert_json_to_df

print("RUNNING gradio_app.py FROM:", __file__)

# Load OCR model based on config
def load_ocr_model_from_config(model_type: str) -> DocumentConverter:
    """
    Load the OCR model based on the configuration.
    Args:
        model_type (str): The type of OCR model to load.
    Returns:
        object: The loaded OCR model.
    """
    if model_type == "rapid":
        # TODO: REFACTOR LOAD OCR MODEL TO JUST EITHER USE SERVER MODELS OR MOBILE MODELS
        return load_rapid_ocr_model(
            "PP-OCRv4/ch_PP-OCRv4_det_server_infer.onnx",
            "PP-OCRv3/ch_PP-OCRv3_rec_infer.onnx",
            "PP-OCRv3/ch_ppocr_mobile_v2.0_cls_train.onnx"
        )
    if model_type == "easy":
        return load_easy_ocr_model()
    if model_type == "ocrmac":
        return load_ocr_mac_model()
    if model_type == "tesseract":
        return load_tesseract_model(config.TESSERACT_TESSDATA_LOCATION)

    raise ValueError(f"Unknown OCR model type in config: {model_type}")


def save_results(export_type: str, output_file_name: str, df: pd.DataFrame, output_folder: str) -> str:
    """
    Save the results in the specified format. 
    Args:
        export_type (str): The type of export (e.g., "csv").
        output_file_name (str): The name of the output file.
        json_data (str): The JSON data to save.
        output_folder (str): The folder to save the output file.
    Returns:
        output_data (str): The output data from the LLM formatted into the specified format
    """
    if export_type == "csv":
        return export_as_csv(df=df, output_folder=output_folder, output_file_name=output_file_name)
    if export_type == "json":
        return export_as_json(df=df, output_folder=output_folder, output_file_name=output_file_name)
    
    return ""

def process_file(input_path: Path, document_converter: DocumentConverter) -> str:
    conversion_result = image_to_text(document_converter, input_path)
    ocr_text_data = conversion_result.document.export_to_markdown()

    json_data = extract_json_data_using_ollama_llm(
        prompt=config.LLM_PROMPT,
        text_data=ocr_text_data,
        ollama_model=config.OLLAMA_MODEL,
        response_model=config.RESPONSE_MODEL
    )
    return json_data

# Full processing pipeline
def run_full_pipeline(file_inputs):
    document_converter = load_ocr_model_from_config(config.OCR_MODEL)
    pull_ollama_model(config.OLLAMA_MODEL)

    df = pd.DataFrame()
    if type(file_inputs) == list:
        json_data_objects = list()
        for file in file_inputs:
            json_data = process_file(file, document_converter)
            json_data_objects.append(json_data)
            df = combine_json_data_into_df(json_data_objects)
    else:
        json_data = process_file(Path(file_inputs), document_converter)
        df = convert_json_to_df(json_data)

    return save_results(export_type=config.EXPORT_TYPE,output_file_name=config.OUTPUT_FILE_NAME, df=df, output_folder=config.OUTPUT_FOLDER)

base_dir = Path(os.path.dirname(__file__))
config_file_path = base_dir / "src" / "llm_document_parser" / "config.py"
config_file_path = config_file_path.resolve()
code_contents = config_file_path.read_text()

def load_config():
    return config_file_path.read_text()

def save_config(updated_config):
    config_file_path.write_text(updated_config)
    importlib.reload(config)
    return "Config updated successfully!"

with gr.Blocks() as demo:
    gr.Markdown(f"""
    # LLM Document Parser

    This app extracts structured data from a document using OCR and a local LLM.
    """)
    

    file_input = gr.File(file_types=["image", ".pdf"], file_count="multiple", label="Upload Document(s) (Image/PDF)")

    run_button = gr.Button("Parse Documents")
    output_text = gr.Textbox(label="Extracted Data")
    run_button.click(fn=run_full_pipeline, inputs=file_input, outputs=output_text)


    gr.Markdown("""# Config
    To update the config, make changes, then click "Update Config" below
    """)
    config_editor = gr.Code(code_contents, language="python", label="Config")
    save_config_button = gr.Button("Update Config")
    status = gr.Textbox(label="Status")

    demo.load(fn=load_config, outputs=config_editor)
    save_config_button.click(fn=save_config, inputs=config_editor, outputs=status)

if __name__ == "__main__":
    demo.launch()
