# Getting Started

## Prepare the Project
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
## Install TesseractOCR (optional - if using Tesseract for OCR)
[Tesseract Installation Documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html)

### Ubuntu
```bash
sudo apt install tesseract-ocr
```

### MacOS
```bash
# MacPorts
sudo port install tesseract

# Homebrew
brew install tesseract
```

### Windows
[Download the installer](https://github.com/UB-Mannheim/tesseract/wiki)

MOVE ^

## Creating a Data Model
Docling uses Pydantic to force the LLM output to conform to an exact data model. In order to 

## Graphical Interface App

```bash
python -m llm_document_parser.gradio_app
```
## Command Line Interface
```bash
python -m llm_document_parser.cli
```
