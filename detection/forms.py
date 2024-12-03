
from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Select an image",
                             widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',  # Add Bootstrap or custom class
            'style': 'color: white; font-weight: bold;'  # Inline styling (optional)
    })
    )
    
class VideoUploadForm(forms.Form):
    video = forms.FileField(label="Upload a video file")

class CustomAuthenticationForm(forms.Form):
    username_or_email = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email', 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )


