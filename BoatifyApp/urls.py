from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome , name='welcome'),
    path('homepage', views.homepage, name='homepage'),
    path('tracking', views.tracking, name='tracking'),
    path('schedulelist', views.schedulelist, name='schedulelist'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('contact', views.contact, name='contact'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('rgs', views.rgs, name='rgs'),
    path('payment/', include('payment.urls'))
    ]
