from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Level
from .models import Category, Question, Team, Tournament
from django.http import HttpResponseRedirect
# from django.views.generic import TemplateView
from django.shortcuts import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse


def index(request):
    if request.session.get("user"):
        pagetogo = "/choose"
    else:
        pagetogo = "/login"
    user=User.objects.all()
    return render(request, 'index.html', {"pagetogo":pagetogo,'user':user})


def firstview(request, tournament_id):
    if not request.user.is_authenticated:
        return render(request, "login.html", {"message": None})
    else:
        
        if not request.session.get("tournament"):
            url = "/master"+"/login/jeopardy"
            user = request.user
            request.session["user"]= request.user.id
            return redirect(url, {"user":user})
        else:
            t = request.session.get("tournament")
            tournament = Tournament.objects.get(pk=t)
            user = request.user
            levels = Level.objects.all()
            request.session["user"]= request.user.id
        return render(request, 'firstview.html', {"user":user.first_name, 'levels':levels,'tournament':tournament, 't':t})

def choose(request):
    user = request.user
    request.session["user"]= request.user.id
    return render(request, 'choose.html', {'user':user})

def choosetournament(request):
    user=request.session.get("user")
    user=User.objects.get(pk=user)
    tournaments = Tournament.objects.all().filter(user_id=user)
    if request.method == "POST":
        if not request.POST.get("tournament_name"):
            tournament_id = request.POST.get("tournament_id")
            request.session["tournament"]=tournament_id
            url = "polls/"+tournament_id
            return redirect(url, tournament_id)
        else:
            tournament_name = request.POST.get("tournament_name")
            t = Tournament(tournament_name=tournament_name,user_id=user)
            t.save()
            t = t.id
            request.session["tournament"]=t
            url = "polls/"+str(t)
            return redirect(url)
    return render(request, 'tournament.html', {'tournaments':tournaments})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            url="/polls/choose"
            return redirect(url)
        else:
            return render(request, "login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "login.html", {"message": None})

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "Logged out."})

def tournament(request):
    user=request.session.get("user")
    user=User.objects.get(pk=user)
    tournaments = Tournament.objects.all().filter(user_id=user)
    if request.method == "POST":
        if not request.POST.get("tournament_name"):
            tournament_id = request.POST.get("tournament_id")
            request.session["tournament"]=tournament_id
            url = "polls"+"/"
            return redirect(url)
        else:
            tournament_name = request.POST.get("tournament_name")
            t = Tournament(tournament_name=tournament_name,user_id=user)
            t.save()
            t = t.id
            request.session["tournament"]=t
            url = "polls"+"/"
            return redirect(url)
    return render(request, 'tournament.html', {"tournaments":tournaments,"user":user})

# def existing(request):
#     user=request.session.get("user")
#     tournaments = Tournament.objects.all().filter(user_id=user)
#     if request.method == "POST":
#         tournament_id = request.POST.get("tournament_id")
#         request.session["tournament"]=tournament_id
#         url = "polls"+"/"
#         return redirect(url)
#     return redirect(request, 'existing.html', {'tournaments':tournaments})


def teams(request, level_id, tournament_id):
    t = request.session.get("tournament")
    tournament = Tournament.objects.get(pk=t)
    teams = Team.objects.all().filter(tournament_id=tournament)
    level = Level.objects.get(pk=level_id)
    level.tournament_id = tournament
    level.save()
    user = request.session.get("user")
    user = User.objects.get(pk=user)
    if request.method == "POST":
        if request.POST.get("teamid")==None:
            error="Please choose the team"
            url="/polls/"+str(level_id)+'/teams'
            return redirect(url, {"error":error })
        else:
            team = request.POST.get("teamid")
            t = request.session.get("tournament")
            url="/polls/" + str(t) +'/'+str(level_id)+'/'
            request.session["teamplay"] = team
            return redirect(url)
        
    return render(request, 'teams.html', {'teams':teams,'level':level, 'user':user,'tournament':tournament})

def categories(request, level_id, tournament_id):
    # return HttpResponse("You're looking at level %s." % level_id)
    t = request.session.get("tournament")
    tournament = Tournament.objects.get(pk=t)
    level = Level.objects.get(pk=level_id)
    team = Team.objects.all().filter(tournament_id=tournament)
    teamchosen = request.session.get("teamplay")
    teamchoose = Team.objects.get(pk=teamchosen)
    question = Question.objects.all().filter(tournament_id=tournament)
    # intmarks_alloted = int(Question.marks_alloted)
    # marks_new = intmarks_alloted*0.5
    return render(request, 'categories.html', {'level': level,'team':team, 'teamchoose':teamchoose, 'teamchosen':teamchosen,'tournament':tournament})

def questions(request, category_id, level_id):
    # return HttpResponse("You're looking at level %s." % level_id)
    t = request.session.get("tournament")
    tournament = Tournament.objects.get(pk=t)
    teamchosen = request.session.get("teamplay")
    teamchoose = Team.objects.get(pk=teamchosen)
    level = Category.level
    category = Category.objects.get(pk=category_id)
    return render(request, 'questions.html', {'category': category, 'level':level},)

def specquestion(request, category_id, level_id, question_id,tournament_id):
    # return HttpResponse("You're looking at level %s." % level_id)
    t = request.session.get("tournament")
    tournament = Tournament.objects.get(pk=t)
    question = Question.objects.get(pk=question_id)
    print(question.status)
    category = Category.objects.get(pk=category_id)
    level = Level.objects.get(pk=level_id)
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
            elif question.status=="WA":
                teamchoose.team_points -= level.negative_marking
            elif question.status=="NA":
                teamchoose.team_points += 0
            question.save()
            teamchoose.save()
            url="/polls/"+str(tournament.id)+"/"+str(level_id)+'/teams'
            return redirect(url)
    return render(request, 'specquestions.html', {'question': question, 'level': level, 'team':team, 'category':category, 'teamchoose':teamchoose,'t':t})



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


