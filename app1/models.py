from django.db import models

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=50,null=True)
    phone = models.CharField(max_length=20,null=True)
    image = models.FileField(upload_to='profile/',null=True)
    
class Contact(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=20)
    reference = models.ForeignKey(Profile,on_delete=models.CASCADE)
    