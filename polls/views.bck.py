from django.shortcuts import render
from django.http import HttpResponse
from .models import Level
from .models import Category, Question, Answer, Team
from django.http import HttpResponseRedirect
# from django.views.generic import TemplateView
from django.shortcuts import reverse
from .forms import QuestionForm
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView
from django.views.generic import UpdateView


template_view = 'polls/specsquestions.html'


def index(request):
    levels = Level.objects.all()
    return render(request, 'index.html', {'levels': levels})


def categories(request, level_id):
    # return HttpResponse("You're looking at level %s." % level_id)
    level = Level.objects.get(pk=level_id)
    return render(request, 'categories.html', {'level': level})

def questions(request, category_id, level_id):
    # return HttpResponse("You're looking at level %s." % level_id)
    level = Category.level
    category = Category.objects.get(pk=category_id)
    return render(request, 'questions.html', {'category': category, 'level':level},)

def specquestion(request, category_id, level_id, question_id,):
    # return HttpResponse("You're looking at level %s." % level_id)
    level = Category.level
    question = Question.objects.get(pk=question_id)
    answer = Answer.objects.all()
    team = Team.objects.all()
    return render(request, 'specquestions.html', {'question': question, 'level': level, 'answer': answer, 'team':team})


def post_edit(request, pk, ):
    status = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=status)
        if form.is_valid():
            status = form.save(commit=False)
            status.save()
            return redirect('/', pk=status.pk)
    else:
        form = QuestionForm(instance=status)
    return render(request, 'specquestions.html', {'form': form,})

