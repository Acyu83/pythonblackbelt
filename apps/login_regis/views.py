from django.shortcuts import render, HttpResponse, redirect
from .models import User, Travel
from django.contrib import messages

def index(request):

    if id in request.session:
        request.session.clear()

    print User.objects.all()
    return render(request, 'login_regis/index.html')

def process(request):
    x = User.objects.register(request.POST)
    if x[0] == True:
        messages.success(request, "Registration Successful")
    else:
        for error in x[1]:
            messages.error(request, error)
    return redirect("/")

def login(request):
    y = User.objects.login(request.POST)

    if y[0] == True:
        request.session["id"] = y[2]
        return redirect("/success")
    else:
        for error in y[1]:
            messages.error(request, error)
        return redirect("/")

def success(request):
    print request.session["id"]
    this_user = User.objects.get(id=request.session["id"])

    context = {
        "names" : User.objects.get(id=request.session["id"])
    }

    try:
        this_user = User.objects.get(id=request.session["id"])
        x=Travel.objects.get(id=request.session["travel_id"])
        x.trips.add(this_user)
        print x
        context2 = {
        "vacay" : this_user.Group.all()
        }
    except:
        context2 = 'null'
    return render(request, "login_regis/success.html", context, context2)

def logout(request):
    return redirect("/")

def addpage(request):
    return render(request, "login_regis/add.html")

def add_process(request):
    z = Travel.objects.add_trip(request.POST)
    if z[0] == True:
        request.session["travel_id"] = z[2]
    else:
        for error in z[1]:
            messages.error(request, error)
    return redirect("/success")

def error(request):
    return redirect("/")
