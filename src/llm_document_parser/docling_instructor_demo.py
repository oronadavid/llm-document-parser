from pathlib import Path

from llm_document_parser.instructor_llm import extract_json_data_using_ollama_llm
from llm_document_parser.convert_doc_docling import load_rapid_ocr_model, image_to_text, load_easy_ocr_model

if __name__ == "__main__":
    current_dir = Path(__file__)
    source = current_dir.parent / "test_data" / "test2.png"

    #document_converter = load_rapid_ocr_model(
    #    "PP-OCRv4/ch_PP-OCRv4_det_server_infer.onnx",
    #    "PP-OCRv3/ch_PP-OCRv3_rec_infer.onnx",
    #    "PP-OCRv3/ch_ppocr_mobile_v2.0_cls_train.onnx"
    #)
    #document_converter = load_tesseract_model()
    document_converter = load_easy_ocr_model()
    #document_converter = load_ocr_mac_model()

    conversion_result = image_to_text(document_converter, source)

    bank_statement = conversion_result.document.export_to_markdown()
    print(bank_statement)

    prompt = "Extract all transactions from the following statement. Each transaction must be returned as a JSON object with the fields: transaction_date (YYYY-MM-DD), description, amount, and transaction_type ('deposit' or 'withdrawal'). All of these must be returned as a list of JSON objects under a key called 'transactions'."

    print(extract_json_data_using_ollama_llm(prompt=prompt, text_data=bank_statement, ollama_model="llama3.2"))
