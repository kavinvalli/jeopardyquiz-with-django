from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Level, Tournament
from polls.models import Category, Question, Team
from django.http import HttpResponseRedirect
# from django.views.generic import TemplateView
from django.shortcuts import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse



def index(request):
    if not request.user.is_authenticated:
        return render(request, "loginmaster.html", {"message": None})
    user= request.user.username
    request.session["user"] = user
    tournament = Tournament.objects.all().filter(user_id=user)
    return render(request, "user.html", {"user": request.user,"tournament":tournament})

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        url = "/master/"
        return redirect(url)
    else:
        return render(request, "loginmaster.html", {"message": "Invalid credentials."})

def register(request):
    
    if request.method == "POST":
        
        first_name = request.POST.get("first_name")
        email_id = request.POST.get("email_id")
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            User.objects.get(username=username)
            return render(request, "register.html", {"message": "Username exists"})
        except:
            if "@" not in email_id:
                return render(request, "register.html", {"message": "Invalid Email Id"})
            else:
                if len(password) < 6:
                    return render(request, "register.html", {"message": "Password needs to be atleast 8 characters long"})
                else:
                    user = User.objects.create_user(username, email_id, password)
                    user.first_name = first_name
                    user.save()
                    url = "/polls"
                    return redirect(url, {"message":None})
    return render(request, "register.html")

def logout_view(request):
    logout(request)
    return render(request, "loginmaster.html", {"message": "Logged out."})

def jeopardy(request):
    user = request.user
    user = user.id
    user=User.objects.get(pk=user)
    category = Category.objects.order_by('level').all()
    tournament = Tournament.objects.all().filter(user_id=user.username).order_by('-date_created')
    levels = Level.objects.all()
    teams = Team.objects.all()
    return render(request, 'jeopardy.html', {'category':category, 'levels':levels, 'tournament':tournament,'teams':teams, 'user':user})

def category(request, category_id, tournament_id):
    category = Category.objects.get(pk=category_id)
    level = category.level_id
    level = Level.objects.get(pk=level)
    question = Question.objects.all()
    tournament = Tournament.objects.get(pk=tournament_id)
    return render(request, 'category.html', {'category':category, 'question':question, 'tournament':tournament,'level':level})

def createtournament(request):
    user=request.session.get("user")
    user=User.objects.get(username=user)
    tournaments = Tournament.objects.all().filter(user_id=user)
    if request.method == "POST":
        tournament_name = request.POST.get("tournament_name")
        t = Tournament(tournament_name=tournament_name,user_id=user)
        t.save()
        t = t.id
        request.session["tournament"]=t
        url = "/master/login/jeopardy"
        return redirect(url)
    return render(request, 'createtournament.html')

def createlevel(request):
    if request.method == "POST":
        level_name = request.POST.get("level_name")
        image_url = request.POST.get("image_url")
        negative_marking = request.POST.get("negative_marking")
        tournament = request.POST.get("tournament_id")
        tournament = Tournament.objects.get(pk=tournament)
        if image_url:
            l = Level(level_name=level_name,image_url=image_url,negative_marking=negative_marking,tournament_id=tournament)
            l.save()
            url = "/master/login/levels"
            return redirect(url)
        else:
            image_url="http://www.simonandschusterpublishing.com/readytoreadnew/images/Levels_WhiteStroke_Blue.svg"
            l = Level(level_name=level_name,image_url=image_url,negative_marking=negative_marking,tournament_id=tournament)
            l.save()
            url = "/master/login/levels"
            return redirect(url)
    return render(request, 'createlevel.html')

def createcategory(request):
    if request.method=="POST":
        if request.POST.get("level_id") is None:
            url = "/master/login/categories2"
            tournament = request.POST.get("tournament_id")
            request.session["tourchosen"]=tournament
            return redirect(url, {"tournament":tournament})
        else:
            category_name = request.POST.get("category_name")
            tournament = request.session.get("tourchosen")
            level_id = request.POST.get("level_id")
            tournament = Tournament.objects.get(pk=tournament)
            
            c = Category(category_name=category_name,image_url="http://via.placeholder.com/72",level_id=level_id,tournament_id=tournament)
            c.save()
            url = "/master/login/categories"
            return redirect(url)
    return render(request, 'createcategory.html',{'level':level,'tournament':tournament})

def createquestion(request):
    if request.method=="POST":
        if request.POST.get("level_id") is None and request.POST.get("category_id") is None:
            url = "/master/login/questions2"
            tournament = request.POST.get("tournament_id")
            request.session["tourchosen"]=tournament
            return redirect(url)
        elif request.POST.get("level_id") and request.POST.get("category_id") is None:
            url = "/master/login/questions3"
            tournament=request.session["tourchosen"]
            tournament = Tournament.objects.get(pk=tournament)
            level = request.POST.get("level_id")
            request.session["levelchosen"]=level
            return redirect(url, {"tournament":tournament})
        else: 
            question_number = request.POST.get("question_number")
            question_text = request.POST.get("question_text")
            image_url = request.POST.get("image_url")
            marks_alloted = request.POST.get("marks_alloted")
            answer = request.POST.get("answer")
            tournament = request.session.get("tourchosen")
            tournament_id = Tournament.objects.get(pk=tournament)
            level_id = request.session.get("levelchosen")
            category_id = request.POST.get("category_id")
            q = Question(question_text=question_text,image_url=image_url,category_id=category_id,marks_alloted=marks_alloted,level_id=level_id,question_number=0,status="NA",answer=answer,pass_count=0, tournament_id=tournament_id)
            q.save()
            url = "/master/login/questions"
            return redirect(url)
    return render(request, 'createquestion.html',{'tournament':tournament,"level":level,"category":category})

def createteam(request):
    image_url = request.POST.get("image_url")
    if request.method == "POST":
        team_name = request.POST.get("team_name")
        image_url = request.POST.get("image_url")
        tournament = request.POST.get("tournament_id")
        tournament = Tournament.objects.get(pk=tournament)
        t = Team(team_name=team_name, images=image_url, tournament_id=tournament)
        t.save()
        url = "/master/login/teams"
        return redirect(url)
    return render(request, 'createteam.html')

def masterlevels(request):
    user = request.user
    user = user.id
    user=User.objects.get(pk=user)
    category = Category.objects.order_by('level').all()
    tournament = Tournament.objects.all().filter(user_id=user.username)
    levels = Level.objects.all()
    teams = Team.objects.all()
    return render(request, 'masterlevels.html', {'category':category, 'levels':levels, 'tournament':tournament,'teams':teams, 'user':user})

def mastercats(request):
    user = request.user
    user = user.id
    user=User.objects.get(pk=user)
    category = Category.objects.order_by('level').all()
    tournament = Tournament.objects.all().filter(user_id=user.username)
    levels = Level.objects.all()
    teams = Team.objects.all()
    return render(request, 'mastercats.html', {'category':category, 'levels':levels, 'tournament':tournament,'teams':teams, 'user':user})

def mastercats2(request):
    user = request.user
    user = user.id
    user=User.objects.get(pk=user)
    category = Category.objects.order_by('level').all()
    tournament_chosen = request.session.get("tourchosen")
    tournament_chosen = Tournament.objects.get(pk=tournament_chosen)
    tournament = Tournament.objects.all().filter(user_id=user.username)
    leveloutput = Level.objects.all().filter(tournament_id=tournament_chosen)
    levels = Level.objects.all()
    teams = Team.objects.all()
    return render(request, 'mastercats2.html', {'category':category, 'levels':levels, 'tournament':tournament,'teams':teams, 'user':user, 'tournament_chosen':tournament_chosen})

def masterquestions(request):
    user = request.user
    user = user.id
    user=User.objects.get(pk=user)
    category = Category.objects.order_by('level').all()
    tournament = Tournament.objects.all().filter(user_id=user.username)
    levels = Level.objects.all()
    teams = Team.objects.all()
    return render(request, 'masterquestions.html', {'category':category, 'levels':levels, 'tournament':tournament,'teams':teams, 'user':user})

def masterquestions2(request):
    user = request.user
    user = user.id
    user=User.objects.get(pk=user)
    category = Category.objects.order_by('level').all()
    tournament_chosen = request.session.get("tourchosen")
    tournament_chosen = Tournament.objects.get(pk=tournament_chosen)
    tournament = Tournament.objects.all().filter(user_id=user.username)
    leveloutput = Level.objects.all().filter(tournament_id=tournament_chosen)
    levels = Level.objects.all()
    teams = Team.objects.all()
    return render(request, 'masterquestions2.html', {'category':category, 'levels':levels, 'tournament':tournament,'teams':teams, 'user':user, 'tournament_chosen':tournament_chosen})

def masterquestions3(request):
    user = request.user
    user = user.id
    user=User.objects.get(pk=user)
    category = Category.objects.order_by('level').all()
    tournament_chosen = request.session.get("tourchosen")
    tournament_chosen = Tournament.objects.get(pk=tournament_chosen)
    tournament = Tournament.objects.all().filter(user_id=user.username)
    leveloutput = Level.objects.all().filter(tournament_id=tournament_chosen)
    level_chosen = request.session.get("levelchosen")
    level_chosen = Level.objects.get(pk=level_chosen)
    categoryoutput = Category.objects.all().filter(level=level_chosen)
    levels = Level.objects.all()
    teams = Team.objects.all()
    return render(request, 'masterquestions3.html', {'category':category, 'levels':levels, 'tournament':tournament,'teams':teams, 'user':user, 'tournament_chosen':tournament_chosen, 'level_chosen':level_chosen})

def masterteams(request):
    user = request.user
    user = user.id
    user=User.objects.get(pk=user)
    tournament = Tournament.objects.all().filter(user_id=user.username)
    team = Team.objects.all()
    return render(request, 'masterteams.html', {'tournament':tournament,'team':team})

def edittournament(request):
    if request.method == "POST":
        tournament_name0 = request.POST.get("tournament_id")
        tournament0 = Tournament.objects.get(pk=tournament_name0)
        newname = request.POST.get("tournament_name")
        tournament0.tournament_name = newname
        tournament0.save()
        url = "/master/login/jeopardy"
        return redirect(url)

def editlevel(request):
    if request.method == "POST":
        level_name0 = request.POST.get("level_id")
        level0 = Level.objects.get(pk=level_name0)
        newname = request.POST.get("level_name")
        level0.level_name = newname
        level0.save()
        url = "/master/login/levels"
        return redirect(url)

def editteam(request):
    if request.method == "POST":
        team_name0 = request.POST.get("team_id")
        team0 = Team.objects.get(pk=team_name0)
        newname = request.POST.get("team_name")
        team0.team_name = newname
        team0.save()
        url = "/master/login/teams"
        return redirect(url)

def editcategory(request):
    if request.method == "POST":
        category_name0 = request.POST.get("category_id")
        category0 = Category.objects.get(pk=category_name0)
        newname = request.POST.get("category_name")
        category0.category_name = newname
        category0.save()
        url = "/master/login/categories"
        return redirect(url)

def editquestion(request):
    if request.method == "POST":
        question_name0 = request.POST.get("question_id")
        answer_name = request.POST.get("answer_name")
        question0 = Question.objects.get(pk=question_name0)
        newname = request.POST.get("question_name")
        question0.question_text = newname
        question0.answer = answer_name
        question0.save()
        url = "/master/login/questions"
        return redirect(url)

def removetournament(request, tournament_id):
    t = Tournament.objects.get(pk=tournament_id)
    t.delete()
    url = "/master/login/jeopardy"
    return redirect(url)

def removelevel(request, level_id):
    l = Level.objects.get(pk=level_id)
    l.delete()
    url = "/master/login/levels"
    return redirect(url)

def removecategory(request, category_id):
    c = Category.objects.get(pk=category_id)
    c.delete()
    url = "/master/login/categories"
    return redirect(url)

def removequestion(request, question_id):
    q = Question.objects.get(pk=question_id)
    q.delete()
    url = "/master/login/questions"
    return redirect(url)

def removeteam(request, team_id):
    t = Team.objects.get(pk=team_id)
    t.delete()
    url = "/master/login/teams"
    return redirect(url)