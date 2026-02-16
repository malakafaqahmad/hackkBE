import requests
import json
import os
from typing import Optional, Dict, Any, List, Tuple

base_url = "https://532c-121-52-146-240.ngrok-free.app"

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
        image_path: Optional[str]
    ) -> Tuple[Dict[str, Any], Optional[List[Tuple]]]:

        content = []
        files = None

        if text:
            content.append({
                "type": "text",
                "text": text
            })

        if image_path and os.path.exists(image_path):
            filename = os.path.basename(image_path)

            content.append({
                "type": "image",
                "image_file": filename
            })

            file_obj = open(image_path, "rb")

            files = [
                ("files", (filename, file_obj, "image/png"))
            ]

        message = {
            "role": role,
            "content": content
        }

        return message, files

    # ============================================================
    # PURE STATELESS RESPONSE
    # ============================================================

    def respond(
        self,
        user_text: str,
        image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Completely stateless.
        Sends only:
            system
            user
        Gets single response.
        No memory stored anywhere.
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
            image_path=image_path
        )

        messages = [system_msg, user_msg]

        try:
            response = requests.post(
                f"{self.base_url}/respond",
                data={
                    "messages": json.dumps(messages)
                },
                files=files
            )
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
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Uses backend memory.
        Sends system prompt only once.
        Sends only new user message.
        
        Args:
            user_text: The user's message
            image_path: Optional path to an image
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
            image_path=image_path
        )

        messages.append(user_msg)

        payload = {
            "messages": json.dumps(messages)
        }

        if active_conversation_id:
            payload["conversation_id"] = active_conversation_id
        
        # print("\n" + "=" * 60)
        # print(f"\n📤 Sending chat message with payload: {payload}")
        # print("=" * 60)

        try:
            response = requests.post(
                f"{self.base_url}/chat",
                data=payload,
                files=files
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