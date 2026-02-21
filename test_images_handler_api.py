"""
Medical Images Handler API - Python Test Script

Tests the /api/images-handler endpoint with various file types.
"""

import requests
import json
import base64
import io
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


# Configuration
API_BASE_URL = "http://localhost:5000"
PATIENT_ID = "p1"


def create_test_image():
    """Create a simple test medical image."""
    # Create a white image
    img = Image.new('RGB', (512, 512), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw some text
    try:
        # Try to use a default font
        draw.text((50, 200), "MEDICAL IMAGE TEST", fill='black')
        draw.text((50, 250), f"Patient: {PATIENT_ID}", fill='black')
        draw.text((50, 300), f"Date: {datetime.now().strftime('%Y-%m-%d')}", fill='black')
    except:
        # Fallback without font
        draw.rectangle([50, 200, 450, 350], outline='black', width=2)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()


def create_test_pdf():
    """Create a simple test PDF with medical report content."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        pdf_bytes = io.BytesIO()
        c = canvas.Canvas(pdf_bytes, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "Medical Report")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, f"Patient ID: {PATIENT_ID}")
        c.drawString(100, 700, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        c.drawString(100, 680, "")
        c.drawString(100, 660, "Findings:")
        c.drawString(120, 640, "- Blood pressure: 145/95 mmHg (elevated)")
        c.drawString(120, 620, "- Heart rate: 82 bpm (normal)")
        c.drawString(120, 600, "- Temperature: 98.6°F (normal)")
        c.drawString(100, 580, "")
        c.drawString(100, 560, "Recommendations:")
        c.drawString(120, 540, "- Continue current medications")
        c.drawString(120, 520, "- Monitor blood pressure daily")
        c.drawString(120, 500, "- Follow up in 2 weeks")
        
        c.save()
        pdf_bytes.seek(0)
        
        return pdf_bytes.getvalue()
    except ImportError:
        print("⚠️  reportlab not available. PDF test will be skipped.")
        return None


def test_single_image():
    """Test 1: Single image upload."""
    print("\n" + "="*80)
    print("🧪 Test 1: Single Image Upload")
    print("="*80)
    
    image_data = create_test_image()
    
    files = {
        'files': ('test_xray.jpg', image_data, 'image/jpeg')
    }
    
    data = {
        'patient_id': PATIENT_ID,
        'existing_report': 'Patient has history of hypertension and diabetes. Currently on Lisinopril 10mg and Metformin 500mg.'
    }
    
    print(f"\n📤 Sending request to {API_BASE_URL}/api/images-handler")
    print(f"Patient ID: {PATIENT_ID}")
    print(f"Files: 1 image")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/images-handler",
            files=files,
            data=data,
            timeout=300
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success!")
            print(f"\n📊 Results:")
            print(f"  • Processed Files: {result.get('total_files')}")
            print(f"  • Processing Time: {result.get('processing_time_seconds')}s")
            
            if result.get('image_analysis_results'):
                print(f"\n🔬 Analysis Results:")
                analysis = result['image_analysis_results']
                if isinstance(analysis, dict) and 'image_analysis' in analysis:
                    for img_result in analysis['image_analysis'][:2]:  # Show first 2
                        print(f"    Image: {img_result.get('image_id')}")
                        print(f"    Features: {', '.join(img_result.get('identified_features', [])[:3])}")
                        print(f"    Abnormalities: {', '.join(img_result.get('abnormalities', [])[:3])}")
            
            # Save full result
            with open('test_single_image_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Full result saved to: test_single_image_result.json")
        else:
            print(f"\n❌ Request Failed")
            print(f"Error: {response.json()}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection Error: Could not connect to {API_BASE_URL}")
        print("Make sure the Flask server is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def test_multiple_files():
    """Test 2: Multiple files upload (image + PDF)."""
    print("\n" + "="*80)
    print("🧪 Test 2: Multiple Files Upload (Image + PDF)")
    print("="*80)
    
    image_data = create_test_image()
    pdf_data = create_test_pdf()
    
    if pdf_data is None:
        print("\n⚠️  Skipping PDF test (reportlab not available)")
        return
    
    files = [
        ('files', ('chest_xray.jpg', image_data, 'image/jpeg')),
        ('files', ('medical_report.pdf', pdf_data, 'application/pdf'))
    ]
    
    data = {
        'patient_id': PATIENT_ID,
        'existing_report': 'Patient baseline report: Age 55, male, hypertension, type 2 diabetes.'
    }
    
    print(f"\n📤 Sending request with multiple files")
    print(f"Files: 1 image + 1 PDF")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/images-handler",
            files=files,
            data=data,
            timeout=300
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success!")
            print(f"\n📊 Results:")
            print(f"  • Processed Files: {result.get('total_files')}")
            for file_info in result.get('processed_files', []):
                print(f"    - {file_info['filename']} ({file_info['type']}, {file_info['size_kb']} KB)")
            print(f"  • Processing Time: {result.get('processing_time_seconds')}s")
            
            # Save full result
            with open('test_multiple_files_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Full result saved to: test_multiple_files_result.json")
        else:
            print(f"\n❌ Request Failed")
            print(f"Error: {response.json()}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def test_error_handling():
    """Test 3: Error handling - missing patient_id."""
    print("\n" + "="*80)
    print("🧪 Test 3: Error Handling - Missing Patient ID")
    print("="*80)
    
    image_data = create_test_image()
    
    files = {
        'files': ('test_xray.jpg', image_data, 'image/jpeg')
    }
    
    # Don't send patient_id
    data = {}
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/images-handler",
            files=files,
            data=data,
            timeout=300
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("\n✅ Error handling works correctly (expected 400)")
        else:
            print("\n⚠️  Unexpected response")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def main():
    """Main test function."""
    print("="*80)
    print("MEDICAL IMAGES HANDLER API - TEST SUITE")
    print("="*80)
    print(f"\nAPI Base URL: {API_BASE_URL}")
    print(f"Patient ID: {PATIENT_ID}")
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        print(f"✅ Server is running: {response.json()}")
    except:
        print(f"❌ Server is not running at {API_BASE_URL}")
        print("Please start the server first: python app.py")
        return
    
    # Run tests
    print("\n" + "="*80)
    print("Select test to run:")
    print("1. Single Image Upload")
    print("2. Multiple Files Upload (Image + PDF)")
    print("3. Error Handling Test")
    print("4. All tests")
    print("="*80)
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        test_single_image()
    elif choice == '2':
        test_multiple_files()
    elif choice == '3':
        test_error_handling()
    elif choice == '4':
        test_single_image()
        test_multiple_files()
        test_error_handling()
    else:
        print("Invalid choice")
    
    print("\n" + "="*80)
    print("✅ Testing complete!")
    print("="*80)


if __name__ == "__main__":
    main()
