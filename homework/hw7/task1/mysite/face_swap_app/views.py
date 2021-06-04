import os
import sys

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from .forms import ImageForm, SurnametInputForm

from .face_swap_src.main import swap_and_save_loaded_image


def index(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES)
            except RuntimeError:
                print(sys.exc_info()[1])
                error_message = (
                    "Your image does not contain face or contains more than one face. Please load another " "image. "
                )
                return render(request, "face_swap_app/index.html", {"form": form, "error_message": error_message})
            return HttpResponseRedirect(reverse("face_swap_app:result"))
    else:
        form = ImageForm()
    return render(request, "face_swap_app/index.html", {"form": form})


def handle_uploaded_file(files):
    items = list(list(files.items())[0])
    path = os.path.join("media", "images", "uploaded_image.jpg")
    with open(path, "wb+") as destination:
        for chunk in items[1].chunks():
            destination.write(chunk)
    swap_and_save_loaded_image()


def result(request):
    if request.method == "POST":
        form = SurnametInputForm(request.POST)

        if form.is_valid():
            answer = form.cleaned_data["surname"]
            if check_answer(answer):
                return render(request, "face_swap_app/result.html", {"form": form, "success": True})
            return render(request, "face_swap_app/result.html", {"form": form, "failure": True})
    else:
        form = SurnametInputForm()
        return render(request, "face_swap_app/result.html", {"form": form})


def check_answer(answer: str) -> bool:
    if answer.lower() == "putin":
        return True
    return False
