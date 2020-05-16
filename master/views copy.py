from django.shortcuts import render
from django.http import HttpResponse
from .models import Level
from .models import Category, Question, Answer, Team
from django.http import HttpResponseRedirect
# from django.views.generic import TemplateView
from django.shortcuts import reverse
from django.shortcuts import redirect, get_object_or_404


def index(request):
    levels = Level.objects.all()
    return render(request, 'index.html', {'levels': levels})

def teams(request, level_id):
    teams = Team.objects.all()
    level = Level.objects.get(pk=level_id)
    if request.method == "POST":
        if request.POST.get("teamid")==None:
            error="Please choose the team"
            url="/polls/"+str(level_id)+'/teams'
            return redirect(url, {"error":error })
        else:
            team = request.POST.get("teamid")
            url="/polls/"+str(level_id)+'/'
            request.session["teamplay"] = team
            return redirect(url)
        
    return render(request, 'teams.html', {'teams':teams,'level':level})

def categories(request, level_id):
    # return HttpResponse("You're looking at level %s." % level_id)
    level = Level.objects.get(pk=level_id)
    team = Team.objects.all()
    teamchosen = request.session.get("teamplay")
    teamchoose = Team.objects.get(pk=teamchosen)
    question = Question.objects.all()
    # intmarks_alloted = int(Question.marks_alloted)
    # marks_new = intmarks_alloted*0.5
    return render(request, 'categories.html', {'level': level,'team':team, 'teamchoose':teamchoose, 'teamchosen':teamchosen})

def questions(request, category_id, level_id):
    # return HttpResponse("You're looking at level %s." % level_id)
    teamchosen = request.session.get("teamplay")
    teamchoose = Team.objects.get(pk=teamchosen)
    level = Category.level
    category = Category.objects.get(pk=category_id)
    return render(request, 'questions.html', {'category': category, 'level':level},)

def specquestion(request, category_id, level_id, question_id,):
    # return HttpResponse("You're looking at level %s." % level_id)
    question = Question.objects.get(pk=question_id)
    print(question.status)
    category = Category.objects.get(pk=category_id)
    level = Category.level
    answer = Answer.objects.all()
    team = Team.objects.all()
    teamchosen = request.session.get("teamplay")
    teamchoose = Team.objects.get(pk=teamchosen)
    if request.method == "POST":
         if request.POST.get('status'):
            question.status=request.POST.get('status')
            print('for save '+question.status)
            question.save()
            print('after save ' + question.status)
            if question.status=="RA":
                teamchoose.team_points += question.marks_alloted
            elif question.status=="PQ":
                question.pass_count += 1
                if question.pass_count == 1:
                    question.marks_alloted = question.marks_alloted/2
                elif question.pass_count >= 2:
                    question.marks_alloted = question.marks_alloted
                teamchoose.team_points += 0
            else:
                teamchoose.team_points += 0
            question.save()
            teamchoose.save()
            url="/polls/"+str(level_id)+'/teams'
            return redirect(url)
    return render(request, 'specquestions.html', {'question': question, 'level': level, 'answer': answer, 'team':team, 'category':category, 'teamchoose':teamchoose})



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
    return render(request, 'team_edit.html', {'form': form,})


