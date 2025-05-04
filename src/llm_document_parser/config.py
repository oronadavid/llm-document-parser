# config.py

# Options: "rapid", "easy", "ocrmac", "tesseract"
OCR_MODEL = "ocrmac"

# Must be set when using the tesseract OCR model
# Linux: "/usr/share/tesseract-ocr/4.00/tessdata"
# Windows: "C:\\Program Files\\Tesseract-OCR\\tessdata"
# Mac: "/usr/local/share/tessdata" or "/opt/homebrew/share/tessdata"
TESSERACT_TESSDATA_LOCATION = "/usr/share/tesseract-ocr/4.00/tessdata"

OLLAMA_MODEL = "llama3.2"

LLM_PROMPT = """
        Extract all transactions from the following statement. Each transaction must be returned as a JSON object with the fields: transaction_date (YYYY-MM-DD), description, amount, and transaction_type ('deposit' or 'withdrawal'). All of these must be returned as a list of JSON objects under a key called 'transactions'.
"""

# Options: "csv", "json", "excel"
EXPORT_TYPE = "csv"

# Can be a file or directory
INPUT_PATH = ""
OUTPUT_FOLDER = ""
OUTPUT_FILE_NAME = "output"
