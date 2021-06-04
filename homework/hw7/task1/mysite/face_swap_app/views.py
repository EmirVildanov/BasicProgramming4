from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from .forms import ImageForm
from .models import Question, Choice

from .face_swap_src.main import swap_and_save_loaded_image


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'face_swap_app/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'face_swap_app/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'face_swap_app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('face_swap_app:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'face_swap_app/results.html', {'question': question})


def image_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            handle_uploaded_file(request.FILES)
            return HttpResponseRedirect(reverse('face_swap_app:success'))
    else:
        form = ImageForm()
    return render(request, 'face_swap_app/upload.html', {'form': form})


def success(request):
    return render(request, 'face_swap_app/swap_results.html')


def handle_uploaded_file(files):
    items = list(list(files.items())[0])
    with open(f"media/images/uploaded_image.jpg", 'wb+') as destination:
        for chunk in items[1].chunks():
            destination.write(chunk)
    swap_and_save_loaded_image()
