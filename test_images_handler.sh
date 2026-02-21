#!/bin/bash

# Medical Images Handler API - Test Script
# Tests image and PDF upload with analysis

# Configuration
API_URL="http://localhost:5000/api/images-handler"
PATIENT_ID="p1"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================================================"
echo "🏥 MEDICAL IMAGES HANDLER API - TEST SCRIPT"
echo "========================================================================"
echo ""

# Test 1: Upload a single image
echo -e "${BLUE}Test 1: Single Image Upload${NC}"
echo "Creating a test image..."

# Create a simple test image using ImageMagick (if available) or skip
if command -v convert &> /dev/null; then
    convert -size 512x512 xc:white -fill black -pointsize 40 \
        -draw "text 50,250 'Medical Image Test'" \
        -draw "text 50,300 'Patient: p1'" \
        test_image.jpg
    echo "✓ Test image created: test_image.jpg"
else
    echo "⚠️  ImageMagick not available. Please provide your own test image."
    echo "   Place a medical image file in this directory and update the script."
fi

# Test with image file (if exists)
if [ -f "test_image.jpg" ] || [ -f "xray.jpg" ]; then
    IMAGE_FILE=$([ -f "test_image.jpg" ] && echo "test_image.jpg" || echo "xray.jpg")
    
    echo ""
    echo "Sending request to: $API_URL"
    echo "Patient ID: $PATIENT_ID"
    echo "File: $IMAGE_FILE"
    echo ""
    
    curl -X POST "$API_URL" \
      -F "patient_id=$PATIENT_ID" \
      -F "files=@$IMAGE_FILE" \
      -F "existing_report=Patient has history of hypertension and diabetes. Currently on Lisinopril 10mg and Metformin 500mg." \
      -w "\n\n⏱️  Time taken: %{time_total}s\n" \
      | python3 -m json.tool
    
    echo ""
    echo -e "${GREEN}✓ Test 1 completed${NC}"
else
    echo -e "${RED}✗ No test image found${NC}"
fi

echo ""
echo "========================================================================"
echo ""

# Test 2: Multiple files (image + PDF)
echo -e "${BLUE}Test 2: Multiple Files Upload (Image + PDF)${NC}"

# Create a test PDF
if command -v ps2pdf &> /dev/null; then
    echo "Creating test PDF..."
    cat > test_report.ps << 'EOF'
%!PS-Adobe-3.0
/Times-Roman findfont 12 scalefont setfont
72 700 moveto
(Medical Report - Patient p1) show
72 680 moveto
(Date: February 22, 2026) show
72 660 moveto
(Findings: Blood pressure elevated at 145/95) show
72 640 moveto
(Recommendations: Continue monitoring) show
showpage
EOF
    ps2pdf test_report.ps test_report.pdf
    rm test_report.ps
    echo "✓ Test PDF created: test_report.pdf"
fi

# Test with multiple files
if [ -f "test_image.jpg" ] && [ -f "test_report.pdf" ]; then
    echo ""
    echo "Sending request with multiple files..."
    echo ""
    
    curl -X POST "$API_URL" \
      -F "patient_id=$PATIENT_ID" \
      -F "files=@test_image.jpg" \
      -F "files=@test_report.pdf" \
      -F "existing_report=Patient baseline report: Age 55, male, hypertension, type 2 diabetes." \
      -w "\n\n⏱️  Time taken: %{time_total}s\n" \
      | python3 -m json.tool
    
    echo ""
    echo -e "${GREEN}✓ Test 2 completed${NC}"
else
    echo -e "${RED}✗ Test files not available${NC}"
fi

echo ""
echo "========================================================================"
echo ""

# Test 3: Error handling - missing patient_id
echo -e "${BLUE}Test 3: Error Handling - Missing Patient ID${NC}"
echo ""

if [ -f "test_image.jpg" ]; then
    curl -X POST "$API_URL" \
      -F "files=@test_image.jpg" \
      -w "\n\n⏱️  Time taken: %{time_total}s\n" \
      | python3 -m json.tool
    
    echo ""
    echo -e "${GREEN}✓ Test 3 completed (expected error)${NC}"
fi

echo ""
echo "========================================================================"
echo ""

# Test 4: Error handling - invalid file type
echo -e "${BLUE}Test 4: Error Handling - Invalid File Type${NC}"
echo ""

# Create invalid file
echo "This is not an image" > invalid_file.txt

curl -X POST "$API_URL" \
  -F "patient_id=$PATIENT_ID" \
  -F "files=@invalid_file.txt" \
  -w "\n\n⏱️  Time taken: %{time_total}s\n" \
  | python3 -m json.tool

echo ""
echo -e "${GREEN}✓ Test 4 completed (expected error)${NC}"

# Cleanup
echo ""
echo "========================================================================"
echo "🧹 Cleanup"
echo "========================================================================"
echo ""

read -p "Do you want to delete test files? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f test_image.jpg test_report.pdf invalid_file.txt
    echo "✓ Test files deleted"
fi

echo ""
echo "========================================================================"
echo "✅ All tests completed!"
echo "========================================================================"
