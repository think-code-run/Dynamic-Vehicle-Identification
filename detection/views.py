from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .forms import CustomAuthenticationForm
from .forms import ImageUploadForm
from .forms import VideoUploadForm
from PIL import Image
import numpy as np
import pytesseract
import os
import cv2
import re
from .utils import detect_number_plate
from django.contrib.auth import views as auth_views



# Replacing 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' with the actual installation path on your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


state_district_map = {
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


# Function to extract state and district from the vehicle number
def extract_state_and_district(plate_text):
    # Extracting the first two characters to identify the state
    state_code = plate_text[:2].upper()
    state = state_district_map.get(state_code, "Unknown State")
    
    return state

# Home view
def home_view(request):
    return render(request, 'base.html')

#contact page view
def contact_page_view(request):
    return render(request,'detection/contactme.html')

#services page view
def service_page_view(request):
    return render(request,'detection/services.html')
# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'detection/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = AuthenticationForm()
    return render(request, 'detection/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')



# Upload Image view for vehicle number plate detection
def upload_image_view(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to upload images.")
        return redirect('login')

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            try:
                img = Image.open(image)
                
                # Using pytesseract to extract text from the image
                plate_text = pytesseract.image_to_string(img, config='--psm 8')
                plate_text = plate_text.replace("\n", "").strip()  # Clean up the text

                if plate_text:
                    # Extracting state and district from the detected text
                    state = extract_state_and_district(plate_text)
                    result = f"Detected Vehicle Number: {plate_text}, State: {state}"
                else:
                    result = "No text detected. Please try again with a clearer image."

                # Returning the result or render a template with the result
                return render(request, 'detection/result.html', {'prediction': result})

            except Exception as e:
                messages.error(request, f"An error occurred while processing the image: {str(e)}")
                return redirect('upload_image')
        else:
            messages.error(request, "Please upload a valid image.")

    else:
        form = ImageUploadForm()

    return render(request, 'detection/upload_image.html', {'form': form})

def number_plate_detection(img):
    def clean2_plate(plate):
        gray_img = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_img, 110, 255, cv2.THRESH_BINARY)
        num_contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if num_contours:
            contour_area = [cv2.contourArea(c) for c in num_contours]
            max_cntr_index = np.argmax(contour_area)
            max_cnt = num_contours[max_cntr_index]
            x, y, w, h = cv2.boundingRect(max_cnt)

            if not ratio_check(contour_area[max_cntr_index], w, h):
                return plate, None

            final_img = thresh[y:y + h, x:x + w]
            return final_img, [x, y, w, h]
        else:
            return plate, None

    def ratio_check(area, width, height):
        ratio = float(width) / float(height) if height > 0 else 0
        if area < 1063.62 or area > 73862.5 or ratio < 3 or ratio > 6:
            return False
        return True

    img2 = cv2.GaussianBlur(img, (5, 5), 0)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.Sobel(img2, cv2.CV_8U, 1, 0, ksize=3)
    _, img2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
    morph_img_threshold = cv2.morphologyEx(img2, cv2.MORPH_CLOSE, kernel=element)
    num_contours, _ = cv2.findContours(morph_img_threshold, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    for cnt in num_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        plate_img = img[y:y + h, x:x + w]
        clean_plate, rect = clean2_plate(plate_img)
        if rect:
            plate_im = Image.fromarray(clean_plate)
            text = pytesseract.image_to_string(plate_im, lang='eng')
            return "".join(re.split("[^a-zA-Z0-9]*", text)).upper()
    return ""

def normalize_plate_text(plate_text):
    """Normalize the plate text to handle minor variations in OCR results."""
    # Removing any unwanted characters, extra spaces, and make the text uppercase
    normalized_text = ''.join(re.split(r'\W+', plate_text)).upper()  # Only keep alphanumeric characters
    return normalized_text.strip()

# Display detected results from video
def upload_video_result(request):
    # print("hello")
    detected_numbers = request.session.get('detected_numbers', [])
    return render(request, 'detection/upload_video_result.html', {'detected_numbers': detected_numbers})

from django.conf import settings
from django.core.files.storage import FileSystemStorage

def video_upload_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to upload images.")
        return redirect('login')
    if request.method == 'POST' and request.FILES['video']:
        video_file = request.FILES['video']
        fs = FileSystemStorage()  # Defaults to MEDIA_ROOT
        filename = fs.save(video_file.name, video_file)
        video_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Process the video to detect number plates
        cap = cv2.VideoCapture(video_path)
        detected_numbers = set()
        frame_counter = 0
        frame_interval = 30

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            plate_text = number_plate_detection(frame)
            plate_text_normalized = normalize_plate_text(plate_text)

            if plate_text_normalized and plate_text_normalized not in detected_numbers and frame_counter % frame_interval == 0:
                detected_numbers.add(plate_text_normalized)

            frame_counter += 1

        cap.release()
        detected_boards = []
        for board in detected_numbers:
            state = board[:2].upper()
            detected_boards.append(board + '\t-\t' + state_district_map.get(state, ''))
            
        request.session['detected_numbers'] = detected_boards
        return redirect('upload_video_result')

    return render(request, 'detection/upload_video.html')


