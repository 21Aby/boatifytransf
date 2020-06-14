from django.db import models


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=20, default="")
    email = models.EmailField()
    subject = models.CharField(max_length=196)
    message = models.TextField()

    def __str__(self):
        return self.name

class Schedule(models.Model):
    boatid = models.IntegerField(default= 0)
    fr = models.CharField(max_length=20)
    to = models.CharField(max_length=20)
    time = models.TimeField()
    fare = models.IntegerField()

    def __str__(self):
        name=self.fr + '-' + self.to
        return name




