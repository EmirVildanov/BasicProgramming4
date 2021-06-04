from django import forms

from .models import Image, SurnameInput


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]


class SurnametInputForm(forms.ModelForm):
    class Meta:
        model = SurnameInput
        fields = ["surname"]
