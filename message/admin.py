from django.contrib import admin
from .models import Mutualist, Sms
import requests
import environ
from django.conf import settings

env = environ.Env()
environ.Env.read_env(env_file=str(settings.BASE_DIR/"mupeppbo_project"/".env"))

# Register your models here.

@admin.register(Mutualist)
class MutualistAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number']


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ['body']

    actions = ['send_sms']

    @admin.action(description="Envoyer sms")
    def send_sms(self, request, queryset):
        m = []
        for q in queryset:
            m += q.mutualist.all()
        m_list = [m.phone_number for m in m]
        body = ' '.join([qs.body for qs in queryset])

        url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B2250504522224/requests"
        headers = {
            "Authorization": env('SEND_TOKEN'),
            "Content-Type": "application/json"
        }

        for nb in m_list:
            payload = { 
            "outboundSMSMessageRequest": {
		            "address": f"tel:+225{nb}",
		            "senderAddress":"tel:+2250504522224",
		            "outboundSMSTextMessage": {
                        "message": f"{body}"
                    }
	            }
            }
            response = requests.post(url, json=payload, headers=headers)

            json_response = response.json()
            print(json_response)