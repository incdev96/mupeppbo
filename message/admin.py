from django.contrib import admin
from .models import Mutualist, Sms
import requests
import environ
from django.conf import settings
from .tasks import generate_token

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
        # token = generate_token()
        # m = []
        # for q in queryset:
        #     m += q.mutualist.all()
        # m_list = [m.phone_number for m in m]
        # body = ' '.join([qs.body for qs in queryset])

        # url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B2250504522224/requests"

        # headers = {
        #     "Authorization": f"Bearer {token}",
        #     "Content-Type": "application/json"
        # }

        # for nb in m_list:
        #     payload = { 
        #     "outboundSMSMessageRequest": {
		#             "address": f"tel:+225{nb}",
		#             "senderAddress":"tel:+2250504522224",
        #             "senderName": "MUPEPPBO",
		#             "outboundSMSTextMessage": {
        #                 "message": f"{body}"
        #             }
	    #         }
        #     }
        #     response = requests.post(url, json=payload, headers=headers)

        #     json_response = response.json()
        #     print(json_response)
        token = generate_token()
        for qs in queryset:
            body = qs.body
            phone_number = [m.phone_number for m in qs.mutualist.all()]
        
            for p in phone_number:
                url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B2250504522224/requests"

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }

                payload = { 
                    "outboundSMSMessageRequest": {
                    "address": f"tel:+225{p}",
                        "senderAddress":"tel:+2250504522224",
                        "senderName": "MUPEPPBO",
                        "outboundSMSTextMessage": {
                            "message": f"{body}"
                        }
                    }
                }
                response = requests.post(url, data=payload, headers=headers)