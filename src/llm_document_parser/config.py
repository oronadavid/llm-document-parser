# config.py
from pydantic import BaseModel
from datetime import date
from typing import List

# Options: "rapid", "easy", "ocrmac", "tesseract"
OCR_MODEL = "easy"

# Must be set when using the tesseract OCR model
# Linux: "/usr/share/tesseract-ocr/4.00/tessdata"
# Windows: "C:\\Program Files\\Tesseract-OCR\\tessdata"
# Mac: "/usr/local/share/tessdata" or "/opt/homebrew/share/tessdata"
TESSERACT_TESSDATA_LOCATION = "/usr/share/tesseract-ocr/4.00/tessdata"

OLLAMA_MODEL = "llama3:instruct"

LLM_PROMPT = """
        Extract all transactions from the following statement. Each transaction must be returned as a JSON object with the fields: transaction_date (YYYY-MM-DD), description, amount, and transaction_type ('deposit' or 'withdrawal'). All of these must be returned as a list of JSON objects under a key called 'transactions'. Here is an example:
        [
            {
                transaction_date: 2025-01-24,
                description: "Walmart",
                amount: 34.24,
                transaction_type: "withdrawl"
            }
        ]
"""

# Options: "csv", "json", "excel"
EXPORT_TYPE = "json"

# Can be a file or directory
INPUT_PATH = "/home/david/Projects/school/capstone/llm-document-parser/src/llm_document_parser/test_data/"
OUTPUT_FOLDER = "/home/david/Desktop/"
OUTPUT_FILE_NAME = "output"

# Define Pydantic response models for instructor:

class BankStatementEntry(BaseModel):
    transaction_date: date | None | str
    description: str | None
    amount: float | None
    #transaction_type: Literal['deposit', 'withdrawal', None]
    transaction_type: str | None

class BankStatement(BaseModel):
    transactions: List[BankStatementEntry] | None

# The model that LLM output will conform to
RESPONSE_MODEL = BankStatement