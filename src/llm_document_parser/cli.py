from pathlib import Path
from llm_document_parser.export_data import export_as_csv
from llm_document_parser.config import (
    OCR_MODEL,
    OLLAMA_MODEL,
    LLM_PROMPT,
    TESSERACT_TESSDATA_LOCATION,
    INPUT_PATH,
    OUTPUT_FOLDER,
    OUTPUT_FILE_NAME,
    EXPORT_TYPE
)

from llm_document_parser.instructor_llm import extract_json_data_using_ollama_llm
from llm_document_parser.convert_doc_docling import (
    load_rapid_ocr_model,
    load_easy_ocr_model,
    load_ocr_mac_model,
    load_tesseract_model,
    image_to_text
)

def load_ocr_model_from_config(model_type: str):
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
        return load_tesseract_model(TESSERACT_TESSDATA_LOCATION)

    raise ValueError(f"Unknown OCR model type in config: {model_type}")


def save_results(export_type: str, output_file_name: str, json_data: str, output_folder: str)
    """
    Save the results in the specified format. 
    Args:
        export_type (str): The type of export (e.g., "csv").
        output_file_name (str): The name of the output file.
        json_data (str): The JSON data to save.
        output_folder (str): The folder to save the output file.
    """
    if export_type == "csv":
        export_as_csv(json_data=json_data,output_folder=output_folder, output_file_name=output_file_name)


if __name__ == "__main__":
    document_converter = load_ocr_model_from_config(OCR_MODEL)
    conversion_result = image_to_text(document_converter, Path(INPUT_PATH))

    bank_statement = conversion_result.document.export_to_markdown()
    print(bank_statement)

    json_data = extract_json_data_using_ollama_llm(
        prompt=LLM_PROMPT,
        text_data=bank_statement,
        ollama_model=OLLAMA_MODEL
    )

    print(json_data)
    save_results(export_type=EXPORT_TYPE,output_file_name=OUTPUT_FILE_NAME, json_data=json_data, output_folder=OUTPUT_FOLDER)


