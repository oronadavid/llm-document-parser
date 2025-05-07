from pathlib import Path
import pandas as pd
from docling.document_converter import DocumentConverter
from llm_document_parser.export_data import combine_json_data_into_df, export_as_csv, convert_json_to_df, export_as_json
from llm_document_parser.config import (
    OCR_MODEL,
    OLLAMA_MODEL,
    LLM_PROMPT,
    TESSERACT_TESSDATA_LOCATION,
    INPUT_PATH,
    OUTPUT_FOLDER,
    OUTPUT_FILE_NAME,
    EXPORT_TYPE,
    RESPONSE_MODEL
)

from llm_document_parser.instructor_llm import extract_json_data_using_ollama_llm, pull_ollama_model
from llm_document_parser.convert_doc_docling import (
    load_rapid_ocr_model,
    load_easy_ocr_model,
    load_ocr_mac_model,
    load_tesseract_model,
    image_to_text
)

def load_ocr_model_from_config(model_type: str) -> DocumentConverter:
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


def save_results(export_type: str, output_file_name: str, df: pd.DataFrame, output_folder: str):
    #df = convert_json_to_df(json_data)
    if export_type == "csv":
        export_as_csv(df=df, output_folder=output_folder, output_file_name=output_file_name)
    if export_type == "json":
        export_as_json(df=df, output_folder=output_folder, output_file_name=output_file_name)
        #export_as_json(json_data=json_data, output_folder=output_folder, output_file_name=output_file_name)

def process_file(input_path: Path, document_converter: DocumentConverter) -> str:
    conversion_result = image_to_text(document_converter, input_path)
    ocr_text_data = conversion_result.document.export_to_markdown()
    print(f"Extracted OCR text from file {input_path}:")
    print(ocr_text_data)

    json_data = extract_json_data_using_ollama_llm(
        prompt=LLM_PROMPT,
        text_data=ocr_text_data,
        ollama_model=OLLAMA_MODEL,
        response_model=RESPONSE_MODEL
    )

    print(json_data)
    return json_data


if __name__ == "__main__":
    document_converter = load_ocr_model_from_config(OCR_MODEL)
    pull_ollama_model(OLLAMA_MODEL)

    df = pd.DataFrame()
    if Path(INPUT_PATH).is_dir():
        print("DIR!")
        json_data_objects = list()
        for file in Path(INPUT_PATH).iterdir():
            json_data = process_file(file, document_converter)
            json_data_objects.append(json_data)
            df = combine_json_data_into_df(json_data_objects)
    else:
        print("FILE!")
        json_data = process_file(Path(INPUT_PATH), document_converter)
        df = convert_json_to_df(json_data)

#    conversion_result = image_to_text(document_converter, Path(INPUT_PATH))
#
#    ocr_text_data = conversion_result.document.export_to_text()
#    print("Extracted OCR text:")
#    print(ocr_text_data)
#
#    json_data = extract_json_data_using_ollama_llm(
#        prompt=LLM_PROMPT,
#        text_data=ocr_text_data,
#        ollama_model=OLLAMA_MODEL,
#        response_model=RESPONSE_MODEL
#    )
#
#    print(json_data)
    save_results(export_type=EXPORT_TYPE,output_file_name=OUTPUT_FILE_NAME, df=df, output_folder=OUTPUT_FOLDER)

