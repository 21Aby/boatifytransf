from django.shortcuts import render
from .models import Contact, Schedule
from django.contrib import messages
from django.contrib.auth.models import User, auth


# Create your views here.
def welcome(request):
    return render(request, 'BoatifyApp/welcome.html')


def homepage(request):
    return render(request, 'BoatifyApp/homepage.html')

def tracking(request):
    return render(request, 'BoatifyApp/tracking.html')


def schedulelist(request):
    if request.method == 'POST':
        fromm = request.POST.get('from')
        to = request.POST.get('to')
        time = request.POST.get('time')

        date = request.POST.get('date')
        fromm = fromm.upper()
        to = to.upper()

        d = Schedule.objects.filter(time=time, fr=fromm, to=to)
        return render(request, 'BoatifyApp/schedulelist.html', {'Schedules': d, 'date':date, 'time': time})
    #return render(request, 'BoatifyApp/schedulelist.html')


def contact(request):
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        subject_r = request.POST.get('subject')
        message_r = request.POST.get('message')

        c = Contact(name= name_r, email=email_r, subject=subject_r, message=message_r)
        c.save()

        return render(request, 'BoatifyApp/thankyou.html')
    else:
        return render(request, 'BoatifyApp/contact.html')

def thankyou(request):
    return render(request, 'BoatifyApp/thankyou.html')



def logout(request):
    auth.logout(request)
    return render(request, 'BoatifyApp/homepage.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'BoatifyApp/loginsuccess.html')
        else:
            messages.info(request, 'invalid credentials')
            return render(request, 'BoatifyApp/login.html')
    else:
        return render(request, 'BoatifyApp/login.html')


def register(request):
    if (request.method == 'POST'):
        name1 = request.POST.get('name1')
        #name2 = request.POST.get('name2')
        username = request.POST.get('uname')
        email = request.POST.get('emailr')
        password_r1 = request.POST.get('pwr1')
        password_r2 = request.POST.get('pwr2')
        if password_r1==password_r2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken!!')
                return render(request, 'BoatifyApp/register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken!!')
                return render(request, 'BoatifyApp/register.html')
            else:
                user = User.objects.create_user(username=username, password=password_r1, email=email, first_name=name1)
                user.save()
                return render(request, 'BoatifyApp/regsuccess.html')
        else:
            messages.info(request, 'Passwords not match .!!')
            return render(request, 'BoatifyApp/register.html')

    else:
        return render(request, 'BoatifyApp/register.html')


#not needed
def rgs(request):
    return render(request, 'BoatifyApp/rgs.html')