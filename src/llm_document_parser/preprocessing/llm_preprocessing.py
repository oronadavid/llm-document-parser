# llm_preprocessing.py
"""
This module provides functions to preprocess text for a large language model (LLM).
It includes functions to clean the text, normalize whitespace,
remove headers and footers, standardize dates and amounts,
and extract transaction lines.
It uses regular expressions for text manipulation.
"""

# imports
import re

def clean_text(text):
    """
    Clean the text by removing unnecessary whitespace and newlines. 
    Args:
        text (str): The input text.
    Returns:
        str: The cleaned text.
    """
    lines = text.splitlines()
    return "\n".join([line.strip() for line in lines if line.strip()])

def normalize_whitespace(text):
    """
    Normalize whitespace in the text by replacing multiple spaces with a single space.
    Args:
        text (str): The input text.
    Returns:
        str: The text with normalized whitespace.
    """
    return re.sub(r'\s+', ' ', text)

def remove_headers_footers(text):
    """
    Remove headers and footers from the text.
    Args:
        text (str): The input text.
    Returns:
        str: The text without headers and footers.
    """
    return re.sub(r'Page \d+ of \d+|CONFIDENTIAL', '', text, flags=re.IGNORECASE)

def standardize_dates(text):
    """
    Standardize dates in the text to YYYY-MM-DD format.
    Args:
        text (str): The input text.
    Returns:
        str: The text with standardized dates.
    """
    pattern = re.compile(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b')
    def fix(match):
        month, day, year = match.groups()
        year = f"20{year}" if len(year) == 2 else year
        return f"{year}-{int(month):02d}-{int(day):02d}"
    return pattern.sub(fix, text)

def standardize_amounts(text):
    """
    Standardize amounts in the text by removing commas and converting to float.
    Args:
        text (str): The input text.
    Returns:
        str: The text with standardized amounts.
    """
    return re.sub(r'\$?(-?\d[\d,]*\.?\d{0,2})', lambda m: str(float(m.group(1).replace(',', ''))), text)

def extract_transaction_lines(text):
    """
    Extract transaction lines from the text based on a regex pattern.
    Args:
        text (str): The input text.
    Returns:
        str: The text with only transaction lines.
    """
    pattern = re.compile(r'\b(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})\b.+?\$?\s*-?\d[\d,]*\.?\d{0,2}')
    return "\n".join([line for line in text.splitlines() if pattern.search(line)])

def preprocess_text(
    text,
    clean=True,
    normalize=True,
    remove_headers=True,
    standardize_dates_flag=True,
    standardize_amounts_flag=True,
    extract_lines=True
):
    """
    Preprocess the text for LLM input.
    Args:
        text (str): The input text.
        clean (bool): Whether to clean the text.
        normalize (bool): Whether to normalize whitespace.
        remove_headers (bool): Whether to remove headers and footers.
        standardize_dates_flag (bool): Whether to standardize dates.
        standardize_amounts_flag (bool): Whether to standardize amounts.
        extract_lines (bool): Whether to extract transaction lines.
    Returns:
        str: The preprocessed text.
    """
    if clean:
        text = clean_text(text)
    if normalize:
        text = normalize_whitespace(text)
    if remove_headers:
        text = remove_headers_footers(text)
    if standardize_dates_flag:
        text = standardize_dates(text)
    if standardize_amounts_flag:
        text = standardize_amounts(text)
    if extract_lines:
        text = extract_transaction_lines(text)
    return text
