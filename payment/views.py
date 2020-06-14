from django.shortcuts import render, redirect
from django.urls import reverse
import pyqrcode
from .models import Seatres, booking
from pyqrcode import QRCode

import stripe
stripe.api_key = "sk_test_g16mqCpueK42qQBfKCkus9UW00JIRkOIIt"

# Create your views here.

def seatres(request):
    if request.method == 'POST':
        boatid = request.POST.get('fboatid')
        ffr = request.POST.get('ffr')
        fto = request.POST.get('fto')
        ftime = request.POST.get('ftime')
        fdate = request.POST.get('fdate')
        ffare = request.POST.get('ffare')
        Dict = {}
        Dict['Boatid'] = boatid
        Dict['From'] = ffr
        Dict['To'] = fto
        Dict['Time'] = ftime
        Dict['Date'] = fdate
        Dict['Fare'] = ffare

        return render(request, 'payment/seatres.html', {'print': Dict})
    else:
        return render(request, 'payment/seatres.html', {'print': Dict})

def seatdetails(request):
    if request.method == 'POST':
        boatid = request.POST.get('fboatid')
        ffr = request.POST.get('ffr')
        fto = request.POST.get('fto')
        ftime = request.POST.get('ftime')
        fdate = request.POST.get('fdate')
        ffare = request.POST.get('ffare')
        Dict = {}
        Dict['Boatid'] = boatid
        Dict['From'] = ffr
        Dict['To'] = fto
        Dict['Time'] = ftime
        Dict['Date'] = fdate


        v = request.POST.getlist('checks[]')
        vstr = ""
        count = 0
        for i in v:
            if(len(vstr)==0):
                vstr += i
                count+=1
            else:
                vstr += '-'
                vstr += i
                count+=1
        Dict['Seats'] = vstr
        Dict['Fare'] = int(ffare) * count
        emails = None
        if request.user.is_authenticated:
            emails = request.user.email
        c = Seatres(boatid = boatid, email = emails, seatid=vstr)
        c.save()
        return render(request, 'payment/seatdetails.html', {'print': Dict})
    else:
        return render(request, 'payment/seatdetails.html', {'print': Dict})

def payment(request):
    if request.method == 'POST':
        boatid = request.POST.get('fboatid')
        ffr = request.POST.get('ffr')
        fto = request.POST.get('fto')
        ftime = request.POST.get('ftime')
        fdate = request.POST.get('fdate')
        fseats = request.POST.get('fseats')
        ffare = request.POST.get('ffare')
        Dict = {}
        Dict['Boatid'] = boatid
        Dict['From'] = ffr
        Dict['To'] = fto
        Dict['Time'] = ftime
        Dict['Date'] = fdate
        Dict['Seats'] = fseats
        Dict['Fare'] = ffare
        return render(request, 'payment/paymenthome.html', {'print': Dict})
    else:
        return render(request, 'payment/paymenthome.html')


def charge(request):
    if request.method == 'POST':
        amount = int(request.POST['ffare'])
        email = request.user.email
        name = request.user.first_name
        uname = request.user.username
        customer = stripe.Customer.create(
            email = email,
            name = name,
            source = request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer = customer,
            amount = amount*100,
            currency = 'inr',
            description = 'Payment by '+request.user.username
        )
        boatid = request.POST.get('fboatid')
        ffr = request.POST.get('ffr')
        fto = request.POST.get('fto')
        ftime = request.POST.get('ftime')
        fdate = request.POST.get('fdate')
        fseats = request.POST.get('fseats')

        b = booking(boatid = boatid, name = name, email = email,
                    seats = fseats, date = fdate, time = ftime, fromm = ffr, to = fto, amount = amount, paymentmode = "Stripe")
        b.save()
        Dict={}
        Dict['From'] = ffr
        Dict['To'] = fto
        Dict['Seats'] = fseats
        Dict['Amount'] = amount
        Dict['Boatid'] = boatid
        Dict['Name'] = name
        Dict['Date'] = fdate
        Dict['Time'] = ftime
        return render(request, 'payment/paymentstatus.html', {'print': Dict})

def chargepaypal(request):
    if request.method == 'POST':
        email = request.user.email
        name = request.user.first_name
        uname = request.user.username
        boatid = request.POST.get('fboatid')
        ffr = request.POST.get('ffr')
        fto = request.POST.get('fto')
        ftime = request.POST.get('ftime')
        fdate = request.POST.get('fdate')
        fseats = request.POST.get('fseats')
        amount = int(request.POST['ffare'])
        b = booking(boatid=boatid, name=name, email=email,
                    seats=fseats, date=fdate, time=ftime, fromm=ffr, to=fto, amount=amount, paymentmode = "Paypal")
        b.save()
        Dict = {}
        Dict['Amount'] = amount
        Dict['Boatid'] = boatid
        Dict['From'] = ffr
        Dict['To'] = fto
        Dict['Seats'] = fseats
        Dict['Name'] = name
        Dict['Date'] = fdate
        Dict['Time'] = ftime
        return render(request, 'payment/paymentstatus.html', {'print': Dict})

def paymentstatus(request):
    return render(request, 'payment/paymentstatus.html')


def qrcode(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        boatid = request.POST.get('fboatid')
        ffr = request.POST.get('ffr')
        fto = request.POST.get('fto')
        ftime = request.POST.get('ftime')
        fdate = request.POST.get('fdate')
        fseats = request.POST.get('fseats')
        current_user = request.user
        s = "email="+current_user.email
        url = pyqrcode.create(s)
        url.svg("payment\static\payment\images\qrcode_ticket.svg", scale=8)
        Dict={}
        Dict['Name'] = name
        Dict['Boatid'] = boatid
        Dict['From'] = ffr
        Dict['To'] = fto
        Dict['Time'] = ftime
        Dict['Date'] = fdate
        Dict['Seats'] = fseats

        return render(request, 'payment/qrcode.html', {'b': Dict})


