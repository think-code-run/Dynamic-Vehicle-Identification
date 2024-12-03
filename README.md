# Dynamic-Vehicle-Identification

Navigation Menu

Code
Issues
Pull requests
Breadcrumbsvehicle-identification
/README.md
Latest commit
Manideeptheexplorer
Manideeptheexplorer
last week
History
115 lines (85 loc) · 3.9 KB
File metadata and controls

Preview

Code

Blame
Vehicle Number Plate Recognition
A Django-based web application that detects static and dynamic vehicle number plates and identifies the state to which the vehicle belongs. This application leverages Pytesseract for OCR functionality and is styled using Bootstrap for a modern, responsive interface.

#🚀 Features
Home Page: A welcoming page with navigation options.
User Authentication: Register and log in securely.
Image Upload: Detect vehicle number plates and states from uploaded images.
Video Upload: Perform dynamic number plate recognition from video files.
Results Pages: View the extracted vehicle number plate and state.
Contact Page: Submit queries or feedback via a contact form.
Responsive Design: Styled with Bootstrap for compatibility across all devices.
#🛠 Technologies Used
Backend: Django Framework
OCR Tool: Pytesseract
Frontend: HTML, CSS, JavaScript, Bootstrap
Database: SQLite (db.sqlite3)
#📂 Project Structure
vehiclerecognition/ ├── manage.py # Django management script ├── db.sqlite3 # SQLite database ├── requirements.txt # Python dependencies ├── vehiclerecognition/ # Main application directory │ ├── settings.py # Django project settings │ ├── urls.py # URL routing configuration │ ├── views.py # Core application logic │ ├── forms.py # Form handling logic │ ├── utils.py # OCR and plate recognition logic │ ├── templates/ # HTML templates for the website │ ├── static/ # Static files (CSS, JS, images) │ ├── media/ # Uploaded images and videos

#⚙️ Installation and Setup
1. Clone the Repository
bash git clone https://github.com/your-username/vehicle-number-plate-recognition.git cd vehicle-number-plate-recognition

2. Set Up Virtual Environment
python -m venv venv source venv/bin/activate # On Windows: .\venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Pytesseract
Install Tesseract OCR on your system.
Update the path to the Tesseract executable in utils.py: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
5. Apply Migrations
python manage.py makemigrations python manage.py migrate

6. Run the Application
python manage.py runserver

7. Access the Application
Open your browser and navigate to http://127.0.0.1:8000.
#🖼 Usage
Register or log in to the application.
Use the Image Upload feature to detect number plates and the state for static images.
Use the Video Upload feature for dynamic recognition of number plates.
View the results in the Results Page.
Submit feedback or queries using the Contact Page.
#💡 Key Functionality
Pytesseract OCR: Extracts number plate text from images and videos.
State Identification: Maps number plates to their respective states.
Image and Video Support: Handles both static and dynamic inputs.
Responsive Design: Ensures usability across devices using Bootstrap.
#🧪 Testing
Test the application with sample images and videos of vehicle number plates.
Supported formats: .jpg, .png, .jpeg (for images) and .mp4, .avi (for videos).
#📝 Notes
Pytesseract must be correctly installed and configured for the OCR functionality to work.
The application uses SQLite (db.sqlite3) as the default database.
#🤝 Acknowledgements
Pytesseract: OCR tool used for number plate recognition.
Django Framework: Backend framework powering the application.
Bootstrap: Frontend framework for responsive styling.
