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
    conv_results = document_converter.convert(file_path)
    return conv_results
