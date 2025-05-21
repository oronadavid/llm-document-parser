# Customization Guide

Modify and tailor the blueprint to your specific needs.

## Swap OCR Models

In `convert_doc_docling.py`, choose one of:

- `load_rapid_ocr_model()`
- `load_easy_ocr_model()`
- `load_ocr_mac_model()`

## Use a Different LLM

In `instructor_llm.py`:

- Change the system prompt in `config.py`
- Use a different model with Ollama (e.g., `phi`, `llama3`, `dolphin3`)

## Adjust Output

- Modify the output schema returned by the LLM
- Customize `export_as_csv()` or `convert_json_to_df()` to fit your format
