from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import *

# REGISTRATION AND LOGIN
def index(request):
    print("INDEX ROUTE EXECUTED")

    if 'id' in request.session:
        return redirect('/loggedIn')

    # DELETES EVERYTHING IN DATABASE
    # User.objects.all().delete()
    # Plan.objects.all().delete()

    return render(request, 'travel_app/index.html')

# PROCESS
def processRegister(request):
    print("PROCESS REGISTER ROUTE EXECUTED")
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/', messages)
        else:
            hash_brown = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User(full_name=request.POST['full_name'], username=request.POST['username'], password=hash_brown)
            user.save()

            #store user id in session
            request.session['id'] = user.id
            request.session['full_name']= user.full_name

            return redirect('/loginTemplate')
    else:
        return HttpResponse("You Must POST your data. Stop trying to hack me...")

# TEMPLATE
def loginTemplate(request):
    print("LOGIN TEMPLATE ROUTE EXECUTED")
    return render(request, 'travel_app/login.html')

# PROCESS
def processLogin(request):
    print("PROCESS LOGIN ROUTE EXECUTED")

    print(request.POST)

    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/loginTemplate', messages)
        else:
            user = User.objects.get(username=request.POST['username'])
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                print("password match")
                request.session['id'] = user.id
                request.session['full_name'] = user.full_name
                print("I MADE SOME COOKIES!")
                return redirect('/loggedIn')
            else:
                print("failed password")
                messages.error(request, "Wrong password")
                return redirect('/loginTemplate')
            
    else:
        return HttpResponse("You Must POST your data. Stop trying to hack me...")


# MAIN HUB
def loggedIn(request):
    print("LOGGED IN ROUTE EXECUTED")
    if 'id' in request.session:
        all_plans=Plan.objects.all()
        user_favorites=Favorite.objects.filter(user_id=request.session['id'])

        for i in user_favorites:
            all_plans=all_plans.exclude(id=i.plan_id)

        context={
            'all_plans':all_plans,
            'user_favorites': user_favorites
        }
        return render(request, 'travel_app/loggedIn.html', context)
    else:
        return HttpResponse("You must be logged in...")


# PROCESS
# DELETE COOKIES 
def clearSession(request):
    print("CLEAR SESSION EXECUTED")
    print(request.session['id'])
    print(request.session['full_name'])
    request.session.clear()
    # del request.session['id']
    return redirect('/')

# END OF REGISTRATION AND LOGIN



# TEMPLATE
def addPlanTemplate(request):
    return render(request, 'travel_app/addPlan.html')

# PROCESS
def create_plan(request):
    print(request.POST)

    errors = Plan.objects.basic_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)


        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/addPlanTemplate')

    else:
        temp = Plan.objects.create(added_by_id=request.session['id'], destination=(request.POST['destination']), start_date=(request.POST['start_date']), end_date=(request.POST['end_date']), description=(request.POST['description']))
        temp.save()
        Favorite.objects.create(plan_id=temp.id, user_id=request.session['id'])
        # added_by_id=request.session['id']
        return redirect('/loggedIn')

# PROCESS
def joinPlan(request, plan_id):
    Favorite.objects.create(plan_id=plan_id, user_id=request.session['id'])
    # SAVE OBJECT POSSIBLY???? OR AUTOMATICALLY DONE?
    # print(movie_id)
    return redirect('/loggedIn')

# PROCESS
def show(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    user_favorites=Favorite.objects.filter(plan_id=plan_id)

    for i in user_favorites:
        joinedUsers = user_favorites.exclude(id=plan_id)

    context = {
        'plan': plan,
        'joinedUsers': joinedUsers
    }
    return render(request, 'travel_app/show.html', context)
