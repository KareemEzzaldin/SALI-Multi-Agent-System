"""
PDF Parser for Course Materials
Extracts text, page numbers, and isolates embedded images for Gemini 1.5 Flash processing.
"""
from __future__ import annotations
import uuid
from typing import List, Tuple
import fitz  # PyMuPDF
from ..models.ingestion_schemas import ExtractedSegment, ModalityType


class PDFParser:
    @staticmethod
    def parse_pdf_bytes(pdf_bytes: bytes, file_name: str) -> Tuple[List[ExtractedSegment], List[dict]]:
        """
        Parses PDF bytes:
        - Extracts text per page as ExtractedSegment objects.
        - Identifies embedded images and returns their metadata/bytes for Gemini OCR.
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        segments: List[ExtractedSegment] = []
        extracted_images: List[dict] = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text").strip()

            if text:
                segments.append(
                    ExtractedSegment(
                        segment_id=f"seg_{uuid.uuid4().hex[:8]}",
                        modality=ModalityType.TEXT,
                        content=text,
                        source_file=file_name,
                        page_or_slide_num=page_num + 1,
                        metadata={"total_pages": len(doc), "char_count": len(text)}
                    )
                )

            # Check for embedded images on the page
            image_list = page.get_images(full=True)
            for img_index, img_meta in enumerate(image_list):
                xref = img_meta[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Filter out tiny icons (less than 5KB)
                if len(image_bytes) > 5120:
                    extracted_images.append({
                        "page_num": page_num + 1,
                        "image_index": img_index + 1,
                        "image_bytes": image_bytes,
                        "mime_type": f"image/{image_ext}",
                        "source_file": file_name
                    })

        doc.close()
        return segments, extracted_images
