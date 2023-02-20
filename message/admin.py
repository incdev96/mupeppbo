from django.contrib import admin
from .models import Mutualist, Sms
import requests
import environ
from django.conf import settings
from .tasks import send_message_task

env = environ.Env()
environ.Env.read_env(env_file=str(settings.BASE_DIR/"mupeppbo_project"/".env"))

@admin.register(Mutualist)
class MutualistAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number']
    search_fields = ['full_name', 'phone_number']


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ['body']

    actions = ['send_sms', 'print_token']

    @admin.action(description="Envoyer sms")
    def send_sms(self, request, queryset):
        """This function send an sms to each member. """
        members = [] 
        for qs in queryset:
            members += qs.mutualist.all()
        phone_numbers = [member.phone_number for member in members]
        body = ' '.join([qs.body for qs in queryset])

        send_message_task.delay(body, phone_numbers)