import requests
import json
import os
import io
from typing import Optional, Dict, Any, List, Tuple, Union, TYPE_CHECKING
from PIL import Image

if TYPE_CHECKING:
    from pypdf import PdfReader
else:
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            PdfReader = None

base_url = "http://127.0.0.1:8000"

class MedGemmaClient:
    """
    /respond  → PURE STATELESS (no history at all)
    /chat     → Stateful (backend stores memory)
    """

    def __init__(self, system_prompt: str):
        self.base_url = base_url.rstrip("/")
        self.system_prompt = system_prompt

        # Only used for /chat
        self.conversation_id: Optional[str] = None
        self.system_sent_to_server = False

    # ============================================================
    # MESSAGE BUILDER
    # ============================================================

    def _build_message(
        self,
        role: str,
        text: Optional[str],
        image_path: Optional[str] = None,
        image_object: Optional[Union[Image.Image, bytes]] = None,
        pdf_object: Optional[Union[bytes, str]] = None
    ) -> Tuple[Dict[str, Any], Optional[List[Tuple]]]:

        content = []
        files = None
        file_to_close = None

        # Handle PDF conversion to text
        if pdf_object is not None:
            if PdfReader is None:
                raise ImportError("pypdf or PyPDF2 is required to handle PDF files. Install with: pip install pypdf")
            
            pdf_text = self._extract_pdf_text(pdf_object)
            
            # Append PDF text to the existing text or create new text
            if text:
                text = f"{text}\n\n--- PDF Content ---\n{pdf_text}"
            else:
                text = pdf_text
        
        # Add text content
        if text:
            content.append({
                "type": "text",
                "text": text
            })

        # Handle image from path
        if image_path and os.path.exists(image_path):
            filename = os.path.basename(image_path)

            content.append({
                "type": "image",
                "image_file": filename
            })

            file_obj = open(image_path, "rb")
            file_to_close = file_obj

            files = [
                ("files", (filename, file_obj, "image/png"))
            ]
        
        # Handle image from object (PIL Image or bytes)
        elif image_object is not None:
            image_bytes, filename = self._process_image_object(image_object)
            
            content.append({
                "type": "image",
                "image_file": filename
            })
            
            # Create BytesIO object from bytes
            file_obj = io.BytesIO(image_bytes)
            
            files = [
                ("files", (filename, file_obj, "image/png"))
            ]

        message = {
            "role": role,
            "content": content
        }

        return message, files

    # ============================================================
    # HELPER METHODS FOR IMAGE AND PDF PROCESSING
    # ============================================================

    def _process_image_object(self, image_object: Union[Image.Image, bytes]) -> Tuple[bytes, str]:
        """
        Process image object (PIL Image or bytes) and return bytes and filename.
        
        Args:
            image_object: PIL Image object or image bytes
            
        Returns:
            Tuple of (image_bytes, filename)
        """
        if isinstance(image_object, bytes):
            # Already bytes, use as-is
            return image_object, "image.png"
        
        elif isinstance(image_object, Image.Image):
            # Convert PIL Image to bytes
            byte_arr = io.BytesIO()
            # Save as PNG to preserve quality
            image_object.save(byte_arr, format='PNG')
            byte_arr.seek(0)
            return byte_arr.getvalue(), "image.png"
        
        else:
            raise TypeError(f"Unsupported image type: {type(image_object)}. Expected PIL.Image or bytes.")
    
    def _extract_pdf_text(self, pdf_object: Union[bytes, str]) -> str:
        """
        Extract text from PDF object.
        
        Args:
            pdf_object: PDF as bytes or file path
            
        Returns:
            Extracted text from PDF
        """
        try:
            if isinstance(pdf_object, str):
                # It's a file path
                if not os.path.exists(pdf_object):
                    raise FileNotFoundError(f"PDF file not found: {pdf_object}")
                with open(pdf_object, 'rb') as f:
                    pdf_reader = PdfReader(f)
                    text = self._read_pdf_pages(pdf_reader)
            elif isinstance(pdf_object, bytes):
                # It's bytes
                pdf_reader = PdfReader(io.BytesIO(pdf_object))
                text = self._read_pdf_pages(pdf_reader)
            else:
                raise TypeError(f"Unsupported PDF type: {type(pdf_object)}. Expected bytes or file path string.")
            
            return text
        
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")
    
    def _read_pdf_pages(self, pdf_reader) -> str:
        """
        Read all pages from PDF reader.
        
        Args:
            pdf_reader: PdfReader instance
            
        Returns:
            Combined text from all pages
        """
        text_parts = []
        num_pages = len(pdf_reader.pages)
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            try:
                page_text = page.extract_text()
                if page_text.strip():
                    text_parts.append(f"--- Page {page_num}/{num_pages} ---\n{page_text}\n")
            except Exception as e:
                text_parts.append(f"--- Page {page_num}/{num_pages} ---\n[Error extracting text: {str(e)}]\n")
        
        if not text_parts:
            return "[No text content could be extracted from PDF]"
        
        return "\n".join(text_parts)

    # ============================================================
    # PURE STATELESS RESPONSE
    # ============================================================

    def respond(
        self,
        user_text: str,
        image_path: Optional[str] = None,
        image_object: Optional[Union[Image.Image, bytes]] = None,
        pdf_object: Optional[Union[bytes, str]] = None
    ) -> Dict[str, Any]:
        """
        Completely stateless.
        Sends only:
            system
            user
        Gets single response.
        No memory stored anywhere.
        
        Args:
            user_text: The user's text message
            image_path: Optional path to an image file
            image_object: Optional PIL Image object or image bytes
            pdf_object: Optional PDF bytes or file path (will be converted to text)
        """

        system_msg = {
            "role": "system",
            "content": [
                {"type": "text", "text": self.system_prompt}
            ]
        }

        user_msg, files = self._build_message(
            role="user",
            text=user_text,
            image_path=image_path,
            image_object=image_object,
            pdf_object=pdf_object
        )

        messages = [system_msg, user_msg]
        # print("\n" + "=" * 60)
        # print(f"Sending messages to /respond endpoint: {messages}")
        # print(f"📍 URL: {self.base_url}/respond")
        # print("=" * 60)
        # print("files received in client: ", user_msg)

        if image_object is not None:
            print("Image object provided, size in bytes:", len(image_object) if isinstance(image_object, bytes) else "N/A")

        try:
            print("🔄 Sending request to medgemma server...")
            response = requests.post(
                f"{self.base_url}/respond",
                data={
                    "messages": json.dumps(messages)
                },
                files=files,
                timeout=1008
            )
            print(f"✅ Received response: {response.status_code}")
        except requests.exceptions.Timeout:
            print("❌ Request timed out after 100 seconds")
            raise RuntimeError(f"Medgemma server timed out. URL: {self.base_url}/respond")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            raise RuntimeError(f"Failed to connect to medgemma server: {str(e)}")
        finally:
            if files:
                files[0][1][1].close()

        return self._handle_response(response)

    # ============================================================
    # STATEFUL CHAT (SERVER MEMORY)
    # ============================================================

    def chat(
        self,
        user_text: str,
        image_path: Optional[str] = None,
        image_object: Optional[Union[Image.Image, bytes]] = None,
        pdf_object: Optional[Union[bytes, str]] = None,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Uses backend memory.
        Sends system prompt only once.
        Sends only new user message.
        
        Args:
            user_text: The user's message
            image_path: Optional path to an image file
            image_object: Optional PIL Image object or image bytes
            pdf_object: Optional PDF bytes or file path (will be converted to text)
            conversation_id: Optional conversation ID to use (overrides internal state)
        """

        messages = []

        # Determine which conversation_id to use (parameter takes priority)
        active_conversation_id = conversation_id if conversation_id is not None else self.conversation_id

        # Send system prompt only once per server conversation
        if active_conversation_id is None and not self.system_sent_to_server:

            messages.append({
                "role": "system",
                "content": [
                    {"type": "text", "text": self.system_prompt}
                ]
            })

            self.system_sent_to_server = True

        user_msg, files = self._build_message(
            role="user",
            text=user_text,
            image_path=image_path,
            image_object=image_object,
            pdf_object=pdf_object
        )

        messages.append(user_msg)

        payload = {
            "messages": json.dumps(messages)
        }

        if active_conversation_id:
            payload["conversation_id"] = active_conversation_id
        
        # print("\n" + "=" * 60)
        # print(f"\n📤 Sending chat message with payload: {payload}")
        # print(f"📍 URL: {self.base_url}/chat")
        # print("=" * 60)

        try:
            response = requests.post(
                f"{self.base_url}/chat",
                data=payload,
                files=files,
            )
        finally:
            if files:
                files[0][1][1].close()

        data = self._handle_response(response)

        # Save conversation_id returned by backend
        if "conversation_id" in data:
            self.conversation_id = data["conversation_id"]

        return data

    # ============================================================
    # RESET SERVER MEMORY
    # ============================================================

    def reset_chat(self):
        """
        Starts a fresh backend conversation.
        """
        self.conversation_id = None
        self.system_sent_to_server = False

    # ============================================================
    # RESPONSE HANDLER
    # ============================================================

    def _handle_response(self, response):

        if response.status_code != 200:
            raise RuntimeError(
                f"API Error {response.status_code}:\n{response.text}"
            )

        try:
            return response.json()
        except Exception:
            raise RuntimeError(
                f"Invalid JSON response:\n{response.text}"
            )