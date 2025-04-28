import os
from pathlib import Path
from docling.datamodel.document import ConversionResult
from huggingface_hub import snapshot_download

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, OcrMacOptions, PdfPipeline, PdfPipelineOptions, PipelineOptions, RapidOcrOptions, TesseractOcrOptions
from docling.document_converter import DocumentConverter, ImageFormatOption, PdfFormatOption
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend, PyPdfiumPageBackend
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.pipeline.simple_pipeline import SimplePipeline


# TODO: REFACTOR LOAD OCR MODEL TO JUST EITHER USE SERVER MODELS OR MOBILE MODELS
def load_rapid_ocr_model(det_model: str, rec_model: str, cls_model: str) -> DocumentConverter:
    """
    Load the RapidOCR model from Hugging Face Hub.
    Args:
        det_model (str): Path to the detection model.
        rec_model (str): Path to the recognition model.
        cls_model (str): Path to the classification model.
    Returns:
        DocumentConverter: The loaded RapidOCR model.
    """
    print("Downloading RapidOCR models")
    download_path = snapshot_download(repo_id="SWHL/RapidOCR")

    det_model_path = os.path.join(
        download_path, det_model
    )
    rec_model_path = os.path.join(
        download_path, rec_model
    )
    cls_model_path = os.path.join(
        download_path, cls_model
    )

    ocr_options = RapidOcrOptions(
        det_model_path=det_model_path,
        rec_model_path=rec_model_path,
        cls_model_path=cls_model_path
    )

    pipeline_options = PdfPipelineOptions(
        ocr_options=ocr_options
    )

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.IMAGE: ImageFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )

    return doc_converter

def load_ocr_mac_model() -> DocumentConverter:
    """
    Load the OCR Mac model.
    Returns:
        DocumentConverter: The loaded OCR Mac model.
    """
    ocr_options = OcrMacOptions(
        framework='vision'
    )

    pipeline_options = PdfPipelineOptions(
        ocr_options=ocr_options
    )

    doc_converter = DocumentConverter(
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.IMAGE
        ],
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend, pipeline_options=pipeline_options
            ),
            InputFormat.IMAGE: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend, pipeline_options=pipeline_options
            )
        }
    )
    
    return doc_converter

def load_tesseract_model(tessdata_path: str) -> DocumentConverter:
    """
    Load the Tesseract OCR model. 
    Args:
        tessdata_path (str): Path to the Tesseract data directory.
    Returns:
        DocumentConverter: The loaded Tesseract OCR model.
    """
    os.environ["TESSDATA_PREFIX"] = tessdata_path

    ocr_options = TesseractOcrOptions()

    pipeline_options = PdfPipelineOptions(
        ocr_options=ocr_options
    )

    doc_converter = DocumentConverter(
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.IMAGE
        ],
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend, pipeline_options=pipeline_options
            ),
            InputFormat.IMAGE: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend, pipeline_options=pipeline_options
            )
        }
    )

    return doc_converter

def load_easy_ocr_model() -> DocumentConverter:
    """
    Load the EasyOCR model.
    Returns:
        DocumentConverter: The loaded EasyOCR model.
    """
    ocr_options = EasyOcrOptions()

    pipeline_options = PdfPipelineOptions(
        ocr_options=ocr_options
    )

    doc_converter = DocumentConverter(
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.IMAGE
        ],
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend, pipeline_options=pipeline_options
            ),
            InputFormat.IMAGE: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend, pipeline_options=pipeline_options
            )
        }
    )
    return doc_converter

def image_to_text(document_converter: DocumentConverter, file_path: Path) -> ConversionResult:
    """
    Convert an image to text using the specified document converter.
    Args:
        document_converter (DocumentConverter): The document converter to use.
        file_path (Path): Path to the image file.
    Returns:
        ConversionResult: The result of the conversion.
    """
    conv_results = document_converter.convert(file_path)
    return conv_results
