"""
Usage:
    python text_extraction_demo.py <image_path>
    python text_extraction_demo.py  # (will prompt for path)
    
Or drag and drop an image file onto this script.
"""

import pytesseract
from PIL import Image
import sys
import os

def extract_text(image_path):
    """Extract text from an image using Tesseract OCR."""
    try:
        # Open and process the image
        img = Image.open(image_path)
        
        # Extract text
        text = pytesseract.image_to_string(img)
        
        return text
    
    except FileNotFoundError:
        return f"Error: Image file not found at '{image_path}'"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Get image path from command line argument or prompt user
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter image path (or drag and drop image here): ").strip()
        # Remove quotes if user dragged and dropped
        image_path = image_path.strip('"').strip("'")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found at '{image_path}'")
        sys.exit(1)
    
    print(f"\nExtracting text from: {image_path}")
    print("=" * 60)
    
    # Extract and display text
    result = extract_text(image_path)
    print(result)
    print("=" * 60)