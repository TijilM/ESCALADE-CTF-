import random
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth

from .models import Booster, Opposer, Question
from registration.models import Team


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect("/start")
    if request.method == 'POST':
        TeamName = request.POST['TeamName']
        password=request.POST['password']

        team = auth.authenticate(teamName=TeamName, password=password)
        
        if team is not None :
            auth.login(request, team)
            print("logged in successfully")
            return redirect('/start')
        
        else:
            messages.info(request, "Invalid Credentials")
            print("lmao")
            return redirect('/login')
    return render(request, 'game/login.html')

def logout(request):
    if request.user.is_anonymous:
        return redirect('/login')
    auth.logout(request)
    return redirect('/login')

def getRandomQuestion(team, prev_ques_id):
    level = 1 if team.position<=20 else 2 if team.position<=40 else 3 if team.position<=60 else 4
    ques_str = team.level1 if level==1 else team.level2 if level==2 else team.level3 if level==3 else team.level4
    if len(ques_str)==0:
        ques_bank = Question.objects.filter(level=level)
        ques = random.choice(ques_bank)
        while ques.id==prev_ques_id:
            ques = random.choice(ques_bank)
        return ques
    if level==1:
        idx = random.randrange(0, len(team.level1), 2)
        ques_id = team.level1[idx: idx+2]
        team.level1 = ques_str.replace(ques_id, '')
    elif level==2:
        idx = random.randrange(0, len(team.level2), 2)
        ques_id = team.level2[idx: idx+2]
        team.level2 = ques_str.replace(ques_id, '')
    elif level==3:
        idx = random.randrange(0, len(team.level3), 2)
        ques_id = team.level3[idx: idx+2]
        team.level3 = ques_str.replace(ques_id, '')
    else:
        idx = random.randrange(0, len(team.level4), 2)
        ques_id = team.level4[idx: idx+2]
        team.level4 = ques_str.replace(ques_id, '')
    print('ques_id', ques_id)
    ques_id = int(ques_id)
    ques = Question.objects.get(id=ques_id)
    return ques

@login_required(login_url="/login")
def play(request):
    team = request.user
    if team.position>80:
        return render(request, "game/game_over.html",context={'teamName':team.teamName})
    if request.method=="POST":
        answer = request.POST.get("answer")
        if team.current_ques==None:
            print('current question null')
            return redirect('/play')
        if answer!=team.current_ques.ans:
            messages.error(request, "wrongAnswer", 'wrong')
            return redirect('/play')
            # return render(request, "game/test.html", context={
            #     "wrongAnswer": "true"
            # })
        ques_str = team.level1 if team.position<=20 else team.level2 if team.position<=40 else team.level3 if team.position<=60 else team.level4
        if len(ques_str):
            team.points += 10
        team.position += team.dice_value
        if team.position>80:
            team.position = 81
            team.dice_value = None
            team.current_ques = None
            team.save()
            return redirect("/play")
        team.dice_value = random.randint(1, 6)
        prev_ques_id = team.current_ques.id
        team.current_ques = getRandomQuestion(team, prev_ques_id)
        beforeLocation = team.position
        opposerPresent = False
        boosterPresent = False
        opposer = Opposer.objects.filter(boardNo=team.board, start=team.position).first()
        if opposer is not None:
            opposerPresent = True
            team.position = opposer.end
        else:
            booster = Booster.objects.filter(boardNo=team.board, start=team.position).first()
            if booster is not None:
                boosterPresent = True
                team.position = booster.end
        team.save()
        messages.success(request, "correctAnswer", 'correct')
        if opposerPresent:
            messages.info(request, "opposerPresent", 'opposer')
        if boosterPresent:
            messages.info(request, "opposerPresent", 'booster')
        messages.info(request, f"{beforeLocation}", 'before_location')
        return redirect('/play')
        # return render(request, 'game/test.html', context={
        #     'correctAnswer': 'true',
        #     'opposer': opposerPresent,
        #     'booster': boosterPresent,
        #     'beforeLocation': beforeLocation
        # })
    context = {}
    if team.current_ques==None:
        team.current_ques = getRandomQuestion(team, -1)
        team.dice_value = random.randint(1, 6)
        team.save()
    else:
        msgs = messages.get_messages(request)
        for msg in msgs:
            print(str(msg.tags))
            if msg.tags=='correct success':
                context['correctAnswer'] = True
            elif msg.tags=='opposer info':
                context['opposer'] = True
            elif msg.tags=='booster info':
                context['booster'] = True
            elif msg.tags=='before_location info':
                context['beforeLocation'] = str(msg)
            elif msg.tags=='wrong error':
                context['wrongAnswer'] = True
        msgs.used = True
    return render(request, 'game/test.html', context=context)

@require_http_methods(['POST'])
@login_required(login_url="/login")
def hint(request):
    team = request.user
    hint = ''
    if team.points>=10:
        hint = team.current_ques.hint
        team.points -= 10
        team.save()
    return JsonResponse({
        'value': hint,
        'points': team.points
    })

@require_http_methods(["POST"])
@login_required(login_url="/login")
def sneakPeek(request):
    team = request.user
    value = ""
    if team.points>=25:
        team.points -= 25
        nextPos = team.position + team.dice_value
        booster = False
        opposer = Opposer.objects.filter(start=nextPos).exists()
        if not opposer:
            booster = Booster.objects.filter(start=nextPos).exists()
        value = "opposer" if opposer else "booster" if booster else "none"
        team.save()
    return JsonResponse({
        'value': value,
        'points': team.points
    })

@require_http_methods(["POST"])
@login_required(login_url='/login')
def reRoll(request):
    team = request.user
    if team.points>=15:
        team.points -= 15
        prevVal = team.dice_value
        value = random.randint(1, 6)
        while value==prevVal:
            value = random.randint(1, 6)
        team.dice_value = value
        team.save()
    return JsonResponse({
        'value': team.dice_value,
        'points': team.points
    })
    
# @login_required(login_url='/login')
def leaderboard(request):
    top5=Team.objects.all().values('teamName','position').order_by('-position', '-points')[:5]
    # print(list(top5))
    team1={
        'teamName': top5[0]['teamName'],
        'position': top5[0]['position']
    }
    team2={
        'teamName': top5[1]['teamName'],
        'position': top5[1]['position']
    }
    team3={
        'teamName': top5[2]['teamName'],
        'position': top5[2]['position']
    }
    team4={
        'teamName': top5[3]['teamName'],
        'position': top5[3]['position']
    }
    team5={
        'teamName': top5[4]['teamName'],
        'position': top5[4]['position']
    }
   
    # return render(request, "game/scoreboard.html",context={'teams':list(top5)})
    return render(request, "game/scoreboard.html",context={
        'team1': team1,
        'team2': team2,
        'team3': team3,
        'team4': team4,
        'team5': team5,
        'teams':list(top5)
    })
    
@login_required(login_url='/login')
def start(request):
    return render(request, "game/start.html")

# @login_required(login_url='/login')
def game_over(request):
    team=request.user
    teamName=team.teamName
    return render(request, "game/game_over.html",context={'teamName':teamName})
