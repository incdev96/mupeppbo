from django.db import models
from .tasks import generate_token, get_sms
import requests
# Create your models here.

class Mutualist(models.Model):
    full_name = models.CharField('nom complet', max_length=200)
    phone_number = models.CharField('numero de telephone', max_length=10)

    class Meta:
        verbose_name = "Mutualiste"
        verbose_name_plural = "Mutualistes"

    def __str__(self):
        return self.full_name

class Sms(models.Model):
    mutualist = models.ManyToManyField(Mutualist)
    body = models.TextField('corps du message')


    class Meta:
        verbose_name = 'Sms à envoyer'
        verbose_name_plural = 'Sms à envoyer'


class Balance(models.Model):
    
    available_units = models.IntegerField("Sms restants ")
    expire_date = models.DateTimeField("Expire le ")

    class Meta:
        verbose_name = "Balance"
        verbose_name_plural = "Balance"


    url = "https://api.orange.com/sms/admin/v1/contracts"
    token = generate_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    sms = requests.get(url, headers=headers).json()
    available_units = sms[0]["availableUnits"]
    expire_date = sms[0]["expirationDate"]