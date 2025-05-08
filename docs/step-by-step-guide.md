
---

### 📄 `docs/step-by-step-guide.md`

```markdown
# Step-by-Step Guide

This guide walks through how the document parsing pipeline works internally.

## 1. Image Input

- Users upload scanned or digital document images through the Gradio UI.

## 2. OCR Model

- Image is passed to an OCR model (Docling, Tesseract, or PP-OCRv4).
- Output is raw unstructured text.

## 3. LLM Inference

- Text is sent to an instructor-tuned LLM via `extract_json_data_using_ollama_llm()`.
- The LLM parses and returns structured JSON.

## 4. Export

- JSON is optionally saved as `.json` or converted to `.csv` using `export_data.py` utilities.
