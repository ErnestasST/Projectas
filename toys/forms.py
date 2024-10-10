from django import forms
from .models import ToyDrawing, Toy, Accessory, Review, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ToyDrawingForm(forms.ModelForm):
    class Meta:
        model = ToyDrawing
        fields = ['name', 'description', 'width', 'height', 'color', 'special_instructions', 'image']  # Include image
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your drawing...'}),
            'width': forms.NumberInput(attrs={'min': 1, 'step': 0.1}),
            'height': forms.NumberInput(attrs={'min': 1, 'step': 0.1}),
            'color': forms.TextInput(attrs={'placeholder': 'Preferred color'}),
            'special_instructions': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special instructions?'}),
        }
        labels = {
            'width': 'Width (cm)',
            'height': 'Height (cm)',
            'color': 'Preferred Color',
            'special_instructions': 'Special Instructions',
            'image': 'Upload Your Drawing Image',
        }

    def clean(self):
        cleaned_data = super().clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')
        if width <= 0 or height <= 0:
            raise forms.ValidationError("width and Height must be greater then zero")
        return cleaned_data


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ToyForm(forms.ModelForm):
    class Meta:
        model = Toy
        fields = ['name', 'description', 'price', 'image', 'stock']


class AccessoryForm(forms.ModelForm):
    model = Accessory
    field = ['toy', 'name', 'description', 'price', 'image', 'stock']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
        }
        labels = {
            'rating': 'Rating (1-5)',
            'comment': 'Comment',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'shipping_address']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }