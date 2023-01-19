from django.db import models
import requests
# Create your models here.

class Mutualist(models.Model):
    full_name = models.CharField('nom complet', max_length=200)
    phone_number = models.CharField('numero de telephone', max_length=10)

    class Meta:
        verbose_name = "Mutualiste"

    def __str__(self):
        return self.full_name

class Sms(models.Model):
    mutualist = models.ManyToManyField(Mutualist)
    body = models.TextField('corps du message')

    class Meta:
        
        verbose_name = 'Message'

    def __str__(self):
        return f"message {self.id}"
