import io
from typing import Union, TYPE_CHECKING
from werkzeug.datastructures import FileStorage

if TYPE_CHECKING:
    from pypdf import PdfReader
else:
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except ImportError:
            PdfReader = None


class PDFReader:
    """
    PDF Reader for Flask that works with:
    - Flask FileStorage (request.files["file"])
    - Raw bytes
    """

    def read(self, pdf_source: Union[FileStorage, bytes]) -> str:
        """
        Extract text from:
        - Flask FileStorage
        - Raw bytes

        Returns extracted text
        """
        
        # Runtime check for PdfReader
        if PdfReader is None:
            raise ImportError("Install pypdf: pip install pypdf")

        # Case 1: Flask uploaded file
        if isinstance(pdf_source, FileStorage):
            pdf_bytes = pdf_source.read()

        # Case 2: Raw bytes
        elif isinstance(pdf_source, bytes):
            pdf_bytes = pdf_source

        else:
            raise TypeError("pdf_source must be FileStorage or bytes")

        reader = PdfReader(io.BytesIO(pdf_bytes))

        text_parts = []
        total_pages = len(reader.pages)

        for i, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()

                if page_text and page_text.strip():
                    text_parts.append(
                        f"\n===== PAGE {i}/{total_pages} =====\n{page_text}\n"
                    )

            except Exception as e:
                text_parts.append(
                    f"\n===== PAGE {i}/{total_pages} =====\n[Error: {str(e)}]\n"
                )
                

        if not text_parts:
            extracted_text = "[No text found in PDF]"
        else:
            extracted_text = "\n".join(text_parts)


        return extracted_text