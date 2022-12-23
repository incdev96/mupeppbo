from django.contrib import admin
from .models import Mutualist, Sms

# Register your models here.

@admin.register(Mutualist)
class MutualistAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number']


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ['body']