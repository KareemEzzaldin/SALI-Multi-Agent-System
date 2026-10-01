"""
FastAPI Routes for Multimodal Course Ingestion (AI #1 - Phase 1)
Receives uploaded PDF, PPTX, Image, and Audio/Video files and processes them.
"""
from __future__ import annotations
import uuid
import os
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from ..models.ingestion_schemas import IngestionResponse, ExtractedSegment, ModalityType
from ..parsers.pdf_parser import PDFParser
from ..parsers.pptx_parser import PPTXParser
from ..multimodal.gemini_ingestion import GeminiMultimodalProcessor

router = APIRouter(prefix="/api/v1/course-ingest", tags=["Course Ingestion (AI #1)"])

processor = GeminiMultimodalProcessor()


@router.get("/supported-formats")
def get_supported_formats():
    """Returns supported formats and active modalities."""
    return {
        "documents": [".pdf", ".pptx", ".ppt"],
        "images_ocr": [".png", ".jpg", ".jpeg", ".webp"],
        "audio_video_asr": [".mp3", ".wav", ".m4a", ".mp4"],
        "multimodal_engine": "Gemini 1.5 Flash (Vision & Audio Native)",
        "max_file_size_mb": 50
    }


@router.post("/upload", response_model=IngestionResponse, status_code=status.HTTP_200_OK)
async def upload_course_material(file: UploadFile = File(...)):
    """
    Ingests course materials across multiple modalities:
    1. PDF: Text extraction + PyMuPDF diagram isolation + Gemini 1.5 Flash OCR.
    2. PPTX: Slide titles, body bullets, speaker notes, tables + Gemini diagram OCR.
    3. Images: Full visual diagram analysis via Gemini 1.5 Flash Vision.
    4. Audio/Video: Lecture transcription via Gemini 1.5 Flash Audio.
    """
    file_bytes = await file.read()
    file_name = file.filename or "uploaded_document"
    ext = Path(file_name).suffix.lower()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    segments: List[ExtractedSegment] = []
    total_pages = 0

    # ── 1. PDF DOCUMENTS ────────────────────────────────────────────────────────
    if ext == ".pdf":
        try:
            pdf_segments, images = PDFParser.parse_pdf_bytes(file_bytes, file_name)
            segments.extend(pdf_segments)
            total_pages = len(pdf_segments)

            # Process up to first 3 significant diagrams via Gemini 1.5 Flash to prevent bloat
            for img in images[:3]:
                ocr_segment = processor.process_image_diagram(
                    image_bytes=img["image_bytes"],
                    mime_type=img["mime_type"],
                    source_file=file_name,
                    page_or_slide_num=img["page_num"]
                )
                segments.append(ocr_segment)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed parsing PDF: {e}")

    # ── 2. PPTX PRESENTATIONS ──────────────────────────────────────────────────
    elif ext in [".pptx", ".ppt"]:
        try:
            pptx_segments, images = PPTXParser.parse_pptx_bytes(file_bytes, file_name)
            segments.extend(pptx_segments)
            total_pages = len(pptx_segments)

            for img in images[:3]:
                ocr_segment = processor.process_image_diagram(
                    image_bytes=img["image_bytes"],
                    mime_type=img["mime_type"],
                    source_file=file_name,
                    page_or_slide_num=img["page_num"]
                )
                segments.append(ocr_segment)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed parsing PPTX: {e}")

    # ── 3. STANDALONE IMAGES / DIAGRAMS (OCR) ──────────────────────────────────
    elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
        mime_type = f"image/{ext.replace('.', '')}"
        ocr_seg = processor.process_image_diagram(
            image_bytes=file_bytes,
            mime_type=mime_type,
            source_file=file_name,
            page_or_slide_num=1,
            context_hint="Standalone course diagram/chart"
        )
        segments.append(ocr_seg)
        total_pages = 1

    # ── 4. AUDIO / VIDEO LECTURES (ASR) ─────────────────────────────────────────
    elif ext in [".mp3", ".wav", ".m4a", ".mp4"]:
        mime_type = "video/mp4" if ext == ".mp4" else f"audio/{ext.replace('.', '')}"
        audio_seg = processor.process_audio_lecture(
            audio_bytes=file_bytes,
            mime_type=mime_type,
            source_file=file_name
        )
        segments.append(audio_seg)
        total_pages = 1

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{ext}'. Supported: .pdf, .pptx, .png, .jpg, .mp3, .wav, .mp4"
        )

    total_chars = sum(len(s.content) for s in segments)

    return IngestionResponse(
        document_id=f"doc_{uuid.uuid4().hex[:8]}",
        file_name=file_name,
        file_type=ext.replace(".", "").upper(),
        total_pages_or_slides=total_pages,
        total_segments=len(segments),
        total_characters=total_chars,
        segments=segments,
        ingestion_summary=(
            f"Successfully processed '{file_name}' into {len(segments)} structured segments "
            f"({total_chars:,} characters) using PyMuPDF, python-pptx, and Gemini 1.5 Flash."
        )
    )
