import cv2
import numpy as np
import pytesseract
import re
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class NutritionLabelOCR:
    def __init__(self):
        # Initialize pytesseract configuration
        self.config = '--psm 6'  # Assume a single uniform block of text
        
    def preprocess_image(self, image_path):
        """
        Preprocess the image to enhance text detection
        """
        # Read the image
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to get binary image
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Apply dilation to connect text
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=1)
        
        # Convert back to PIL Image format
        pil_img = Image.fromarray(cv2.bitwise_not(dilated))
        
        return pil_img, img
    
    def extract_text(self, pil_img):
        """
        Extract text from the preprocessed image
        """
        return pytesseract.image_to_string(pil_img, config=self.config)
    
    def extract_ingredients(self, text):
        """
        Parse and extract ingredients from the OCR text
        """
        ingredients_pattern = r"(?i)ingredients[:\s]+(.*?)(?:\n\n|\Z)"
        ingredients_match = re.search(ingredients_pattern, text, re.DOTALL)
        
        if ingredients_match:
            ingredients_text = ingredients_match.group(1)
            # Clean up the text
            ingredients_text = re.sub(r'\s+', ' ', ingredients_text).strip()
            return ingredients_text
        
        return "No ingredients found"
    
    def extract_nutrition_facts(self, text):
        """
        Parse and extract nutrition facts from the OCR text
        """
        nutrition_data = {}
        
        # Look for common nutrition label patterns
        calories_pattern = r"(?i)calories[:\s]+(\d+)"
        fat_pattern = r"(?i)total\s+fat[:\s]+(\d+\.?\d*)\s*g"
        carbs_pattern = r"(?i)total\s+carbohydrate[s]?[:\s]+(\d+\.?\d*)\s*g"
        protein_pattern = r"(?i)protein[:\s]+(\d+\.?\d*)\s*g"
        sugar_pattern = r"(?i)sugars?[:\s]+(\d+\.?\d*)\s*g"
        sodium_pattern = r"(?i)sodium[:\s]+(\d+\.?\d*)\s*mg"
        
        # Extract values using regex
        calories_match = re.search(calories_pattern, text)
        if calories_match:
            nutrition_data["Calories"] = calories_match.group(1)
            
        fat_match = re.search(fat_pattern, text)
        if fat_match:
            nutrition_data["Total Fat"] = fat_match.group(1) + "g"
            
        carbs_match = re.search(carbs_pattern, text)
        if carbs_match:
            nutrition_data["Total Carbohydrates"] = carbs_match.group(1) + "g"
            
        protein_match = re.search(protein_pattern, text)
        if protein_match:
            nutrition_data["Protein"] = protein_match.group(1) + "g"
            
        sugar_match = re.search(sugar_pattern, text)
        if sugar_match:
            nutrition_data["Sugars"] = sugar_match.group(1) + "g"
            
        sodium_match = re.search(sodium_pattern, text)
        if sodium_match:
            nutrition_data["Sodium"] = sodium_match.group(1) + "mg"
        
        return nutrition_data
    
    def process_label(self, image_path):
        """
        Process a nutrition label image and extract ingredients and nutrition facts
        """
        # Preprocess the image
        pil_img, original_img = self.preprocess_image(image_path)
        
        # Extract text from image
        text = self.extract_text(pil_img)
        
        # Extract ingredients and nutrition facts
        ingredients = self.extract_ingredients(text)
        nutrition_facts = self.extract_nutrition_facts(text)
        
        return {
            "raw_text": text,
            "ingredients": ingredients,
            "nutrition_facts": nutrition_facts
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract nutrition information from food labels")
    parser.add_argument("image_path", help="Path to the image file of nutrition label")
    args = parser.parse_args()
    
    ocr = NutritionLabelOCR()
    result = ocr.process_label(args.image_path)
    
    print("=== NUTRITION LABEL OCR RESULTS ===")
    print("\n== INGREDIENTS ==")
    print(result["ingredients"])
    
    print("\n== NUTRITION FACTS ==")
    for key, value in result["nutrition_facts"].items():
        print(f"{key}: {value}")
    
    # Uncomment to print the raw OCR text for debugging
    print("\n== RAW OCR TEXT ==")
    print(result["raw_text"])


if __name__ == "__main__":
    main()
