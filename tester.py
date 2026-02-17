import requests
import json

BASE_URL = "http://127.0.0.1:8000"


# ---------------- ROOT TEST ----------------
def test_root():
    print("\n===== Testing ROOT endpoint =====")
    try:
        response = requests.get(BASE_URL)

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

    except Exception as e:
        print("❌ Root test failed:", str(e))


# ---------------- RESPOND TEST ----------------
def test_respond():
    print("\n===== Testing /respond endpoint =====")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Hello doctor"}
            ]
        }
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/respond",
            data={
                "messages": json.dumps(messages)
            }
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

    except Exception as e:
        print("❌ /respond test failed:", str(e))


# ---------------- CHAT TEST ----------------
def test_chat():
    print("\n===== Testing /chat endpoint =====")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "I have chest pain"}
            ]
        }
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            data={
                "messages": json.dumps(messages)
            }
        )

        print("Status Code:", response.status_code)

        data = response.json()

        print("Conversation ID:", data.get("conversation_id"))
        print("Response:", data.get("response"))

        return data.get("conversation_id")

    except Exception as e:
        print("❌ /chat test failed:", str(e))
        return None


# ---------------- CHAT CONTINUATION TEST ----------------
def test_chat_continue(conversation_id):
    print("\n===== Testing /chat continuation =====")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Now I also feel tired"}
            ]
        }
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            data={
                "messages": json.dumps(messages),
                "conversation_id": conversation_id
            }
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

    except Exception as e:
        print("❌ /chat continuation failed:", str(e))


# ---------------- MAIN ----------------
if __name__ == "__main__":

    test_root()

    test_respond()

    conv_id = test_chat()

    if conv_id:
        test_chat_continue(conv_id)