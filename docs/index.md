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
[![Ollama](https://img.shields.io/badge/Ollama-gray?logo=ollama&logoColor=black&labelColor=white)](hhttps://github.com/ollama/ollama)
[![Gradio](https://img.shields.io/badge/Gradio-E76F00?logo=gradio&logoColor=white&)](https://github.com/gradio-app/gradio)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr) <br>
[![Docs](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/docs.yaml/badge.svg)](https://github.com/oronadavid/llm-document-parser/actions/workflows/docs.yaml/)
[![Tests](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/tests.yaml/badge.svg)](https://github.com/oronadavid/llm-document-parser/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/mozilla-ai/document-to-podcast/actions/workflows/lint.yaml/)

[Blueprints Hub](https://developer-hub.mozilla.ai/)
| [Documentation](https://mozilla-ai.github.io/llm-document-parser/)
| [Getting Started](https://mozilla-ai.github.io/llm-document-parser/getting-started)
| [Supported Models](https://mozilla-ai.github.io/llm-document-parser/customization/#supported-models)
| [Contributing](CONTRIBUTING.md)

</div>

# LLM Document Parser: A Blueprint for extracting structured data from documents

This Blueprint provides a locally runnable pipeline for parsing structured data from scanned or digital documents using open-source OCR and LLMs. It takes in one or more documents in image and/or PDF formats as input and returns a single structured object with fields parsed from the documents. By defining a prompt and data model, the Blueprint will know how what fields to parse and what they should look like.

The example use case, parsing transaction data from bank statements, demonstrates how you can pass in multiple documents with differing formats and extract shared fields (transaction amount, description, and date). All of the bank statments from every document are compiled into one object. This Blueprint can be customized to work with any type of document to fit your needs.

<img src="./images/llm-document-parser-diagram.png" width="1200" alt="llm-document-parser Diagram" />

## 🚀 Quick Start
### Setup

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

### Graphical Interface App

```bash
python -m llm_document_parser.gradio_app
```
### Command Line Interface
```bash
python -m llm_document_parser.cli
```

## How it Works

### 1. Image Input

- Upload scanned digital document images or PDFs

### 2. OCR Model

- Input images are passed to an OCR model (Tesseract, EasyOCR, OCR Mac, RapidOCR).
- The OCR model outputs markdown-formatted text representing the document

### 3. LLM Inference

- Text is passed into an instructor-tuned LLM with a user-defined prompt and Pydantic data model
- The LLM parses and returns a structured JSON with the format specified by the data model

### 4. Export

- The output can be saved as `.json` or converted to `.csv`

## System requirements

  - OS: Windows, macOS, or Linux
  - Python 3.10 or higher
  - Minimum RAM: 8 GB
  - Disk space: 6 GB minimum
  - GPU (optional): a GPU will enable the use of more powerful LLMs. 4GB+ of VRAM is recommended if using a GPU

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.
