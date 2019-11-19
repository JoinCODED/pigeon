from django.db import models
from main.functions import sendSms,sendEmail

# Create your models here.
class Recipient(models.Model):
    name = models.CharField(max_length=250)
    number = models.CharField(max_length=250,null=True,blank=True)
    email = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=250)
    members = models.ManyToManyField(Recipient,related_name="groups")
    def __str__(self):
        return self.name

    @property
    def counter(self):
        return len(self.members.all())

    def sms(self, message):
        for recipient in self.members.all():
            sendSms(recipient,message)
    
    def email(self, subject,message):
        for recipient in self.members.all():
            sendEmail(recipient,subject,message)
    


