import cv2
import numpy as np
import joblib
import pytesseract  
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
 
# Load the number plate detection model
model_path = 'detection/svm_model.pkl'
plate_model = joblib.load(model_path)
 
# Function to preprocess the uploaded image
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((64, 64))                                                  # Adjusting the size to match the training data
    img_array = np.array(img).flatten()                                          # Flatten the image into a 1D array
    return img_array
 
# Detect number plate and extract text using OCR

def detect_number_plate(image: InMemoryUploadedFile):
    features, img = preprocess_image(image)                                      # Predicting the number plate region
                                                                                    
    plate_region = plate_model.predict(features)
    
    # Croping to the detected region 
    
    x, y, w, h = plate_region[0]                                                # Adjust this based on actual model output
    plate_img = img[y:y+h, x:x+w]
                                                                                # Perform OCR on the cropped plate region
    plate_text = pytesseract.image_to_string(plate_img, config='--psm 8')  
                                                                                # Processing the plate text to determine state and district
    state, district = extract_state_district(plate_text)
    return state, district
 
# Map number plate text to state and district
def extract_state_district(plate_text):
    plate_mappings = {
    'AP': 'Andhra Pradesh',
    'AR': 'Arunachal Pradesh',
    'AS': 'Assam',
    'BR': 'Bihar',
    'CG': 'Chhattisgarh',
    'GA': 'Goa',
    'GJ': 'Gujarat',
    'HR': 'Haryana',
    'HP': 'Himachal Pradesh',
    'JH': 'Jharkhand',
    'KA': 'Karnataka',
    'KL': 'Kerala',
    'MP': 'Madhya Pradesh',
    'MH': 'Maharashtra',
    'MN': 'Manipur',
    'ML': 'Meghalaya',
    'MZ': 'Mizoram',
    'NL': 'Nagaland',
    'OR': 'Odisha',
    'PB': 'Punjab',
    'RJ': 'Rajasthan',
    'SK': 'Sikkim',
    'TN': 'Tamil Nadu',
    'TS': 'Telangana',
    'TR': 'Tripura',
    'UP': 'Uttar Pradesh',
    'UK': 'Uttarakhand',
    'WB': 'West Bengal',
    'AN': 'Andaman and Nicobar Islands',
    'CH': 'Chandigarh',
    'DN': 'Dadra and Nagar Haveli and Daman and Diu',
    'DL': 'Delhi',
    'JK': 'Jammu and Kashmir',
    'LA': 'Ladakh',
    'LD': 'Lakshadweep',
    'PY': 'Puducherry'
    }
    # Extract state code from plate text
    state_code = plate_text[:2]
    state, district = plate_mappings.get(state_code, ("Unknown", "Unknown"))
    return state, district
 

def handle_uploaded_image(image: InMemoryUploadedFile):
    state, district = detect_number_plate(image)
    if state == "Unknown":
        return "Number plate could not be classified"
    else:
        return f"Vehicle belongs to {state}, {district}"