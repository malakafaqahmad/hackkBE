import os
from medgemmaClient import MedGemmaClient
from PIL import Image


# ============================================================
# CONFIG
# ============================================================

SYSTEM_PROMPT = "You are a medical assistant."

# Change these paths to your actual test files
TEST_IMAGE_PATH = "/home/afaq-ahmad/Desktop/hackk/be/medgemma/a.png"
TEST_PDF_PATH = "/home/afaq-ahmad/Desktop/hackk/be/medgemma/1-s2.0-S2949953425000141-main.pdf"


# ============================================================
# CREATE DUMMY FILES IF NOT EXIST
# ============================================================

def create_dummy_image(path):
    if not os.path.exists(path):
        img = Image.new("RGB", (200, 200), color="red")
        img.save(path)
        print(f"Created dummy image: {path}")


def create_dummy_pdf(path):
    if not os.path.exists(path):
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(path)
        c.drawString(100, 750, "This is a test PDF file.")
        c.save()

        print(f"Created dummy PDF: {path}")


# ============================================================
# TEST STATELESS RESPOND
# ============================================================

def test_stateless_text(client):
    print("\n===== TEST STATELESS TEXT =====")

    response = client.respond(
        user_text="Hello MedGemma"
    )

    print("Response:", response)


def test_stateless_image(client):
    print("\n===== TEST STATELESS IMAGE =====")

    response = client.respond(
        user_text="Analyze this image",
        image_path=TEST_IMAGE_PATH
    )

    print("Response:", response)


def test_stateless_pdf(client):
    print("\n===== TEST STATELESS PDF =====")

    response = client.respond(
        user_text="Analyze this PDF",
        pdf_object=TEST_PDF_PATH
    )

    print("Response:", response)


# ============================================================
# TEST STATEFUL CHAT
# ============================================================

def test_chat(client):
    print("\n===== TEST STATEFUL CHAT =====")

    r1 = client.chat("Hello doctor")
    print("Response 1:", r1)

    r2 = client.chat(
        "Here is an image",
        image_path=TEST_IMAGE_PATH
    )
    print("Response 2:", r2)

    r3 = client.chat(
        "Here is a PDF",
        pdf_object=TEST_PDF_PATH
    )
    print("Response 3:", r3)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    create_dummy_image(TEST_IMAGE_PATH)
    create_dummy_pdf(TEST_PDF_PATH)

    client = MedGemmaClient(system_prompt=SYSTEM_PROMPT)

    # Stateless tests
    test_stateless_text(client)
    test_stateless_image(client)
    test_stateless_pdf(client)

    # Stateful tests
    test_chat(client)

    print("\n✅ All tests completed")