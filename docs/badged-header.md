<p align="center">
  <picture>
    <!-- When the user prefers dark mode, show the white logo -->
    <source media="(prefers-color-scheme: dark)" srcset="./images/Blueprint-logo-white.png">
    <!-- When the user prefers light mode, show the black logo -->
    <source media="(prefers-color-scheme: light)" srcset="./images/Blueprint-logo-black.png">
    <!-- Fallback: default to the black logo -->
    <img src="./images/Blueprint-logo-black.png" width="35%" alt="Project logo"/>
  </picture>
</p>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Python](https://img.shields.io/badge/Python-3.12%2B%20(Apple%20Silicon)-blue)
[![Ollama](https://img.shields.io/badge/Ollama-gray?logo=ollama&logoColor=black&labelColor=white)](https://github.com/ggml-org/llama.cpp)
[![Gradio](https://img.shields.io/badge/Gradio-E76F00?logo=gradio&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr) <br>
[![Docs](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/docs.yaml/badge.svg)](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/docs.yaml/)
[![Tests](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/tests.yaml/badge.svg)](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/lint.yaml/)

[Blueprints Hub](https://developer-hub.mozilla.ai/)
| [Documentation](https://mozilla-ai.github.io/document-to-podcast/)
| [Getting Started](https://mozilla-ai.github.io/document-to-podcast/getting-started)
| [Supported Models](https://mozilla-ai.github.io/document-to-podcast/customization/#supported-models)
| [Contributing](CONTRIBUTING.md)

</div>

# LLM Document Parser: A Blueprint for extracting sturctured data from documents

This Blueprint provides a modular, locally runnable pipeline for parsing structured data (like bank transactions) from scanned or digital documents using open-source OCR and LLM tools.

Whether you're working with bank statements, receipts, or other sensitive documents, this system ensures data privacy and full customization—without relying on proprietary APIs.

<img src="./images/llm-document-parser-diagram.png" width="1200" alt="llm-document-parser Diagram" />

## 🚀 Quick Start
### Setup

#### Prepare the Project
```bash
# Clone the repo
git clone https://github.com/your-username/llm-document-parser.git
cd llm-document-parser

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -e .

# Edit the config with your desired settings and data model(s) using a code editor
vim src/config.py
```
MOVE OUT OF QUICK START v
#### Install TesseractOCR (optional - if using Tesseract for OCR)
[Tesseract Installation Documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html)

##### Ubuntu
```bash
sudo apt install tesseract-ocr
```

##### MacOS
```bash
# MacPorts
sudo port install tesseract

# Homebrew
brew install tesseract
```

##### Windows
[Download the installer](https://github.com/UB-Mannheim/tesseract/wiki)

MOVE ^

### Creating a Data Model
Docling uses Pydantic to force the LLM output to conform to an exact data model. In order to 

### Graphical Interface App

```bash
python -m llm_document_parser.gradio_app
```
### Command Line Interface
```bash
python -m llm_document_parser.cli
```

### 📄 `docs/step-by-step-guide.md`


## How it Works

### 1. Image Input

- Upload scanned or digital document images through the Gradio UI.

### 2. OCR Model

- Image is passed to an OCR model (Docling, Tesseract, or PP-OCRv4).
- Output is raw unstructured text.

### 3. LLM Inference

- Text is sent to an instructor-tuned LLM via `extract_json_data_using_ollama_llm()`.
- The LLM parses and returns structured JSON.

### 4. Export

- JSON is optionally saved as `.json` or converted to `.csv` using `export_data.py` utilities.

## System requirements

  - OS: Windows, macOS, or Linux
  - Python 3.10 or higher
  - Minimum RAM: 8 GB
  - Disk space: 6 GB minimum
  - GPU (optional): a GPU will enable the use of more powerful LLMs. 4GB+ of VRAM is recommended if using a GPU
