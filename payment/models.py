from django.db import models

# Create your models here.


class Seatres(models.Model):
    boatid = models.IntegerField()
    email = models.EmailField()
    seatid = models.CharField(max_length=50)


    def __str__(self):
        return str(self.boatid)

class booking(models.Model):
    boatid = models.IntegerField()
    name = models.CharField(max_length=20)
    email = models.EmailField()
    seats = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    fromm = models.CharField(max_length=30)
    to = models.CharField(max_length=30)
    amount = models.IntegerField()
    paymentmode = models.CharField(max_length=20,default="")

    def __str__(self):
        name = self.name + ' ' + str(self.date)
        return name



