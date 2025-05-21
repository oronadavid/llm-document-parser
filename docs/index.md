# 🧾 Document Parser Blueprint

This Blueprint provides a modular, locally runnable pipeline for parsing structured data (like bank transactions) from scanned or digital documents using open-source OCR and LLM tools.

Whether you're working with bank statements, receipts, or other sensitive documents, this system ensures data privacy and full customization—without relying on proprietary APIs.

---

## ✅ Built With

- Python 3.10+
- Docling OCR / Tesseract / PP-OCRv4
- Ollama (for local LLMs like LLaMA, Phi)
- Instructor-tuned language models
- Gradio (UI)
- MkDocs (for documentation)

---

## 🚀 Quick Start

- [Getting Started](getting-started.md): Set up the project locally and test your first extraction.
- [Step-by-Step Guide](step-by-step-guide.md): Understand how OCR, LLM parsing, and export work together.

---

## 🧠 Architecture Overview

- [API Reference](api.md): Dive into modules like `convert_doc_docling`, `instructor_llm`, and `export_data`.
- [Customization Guide](customization.md): Swap models, adjust prompts, and tune the output format.

---

## 🌱 Future Development

- [Future Features & Contributions](future-features-contributions.md): Ideas for plugging in new OCR models, exporting to databases, or customizing response formats.

---

## 🧩 Why This Blueprint?

Unlike commercial or cloud-based pipelines, this project runs fully offline—giving developers full control over:

- Model selection (OCR + LLM)
- Prompt logic and output schema
- Data security and reproducibility

Perfect for developers building secure, customizable AI tools for document understanding.

---

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/mozilla-ai/blueprint-template/blob/main/LICENSE)
[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr)

</div>
