from celery import shared_task
import requests
import environ
from django.conf import settings

env = environ.Env()
environ.Env.read_env(env_file=str(settings.BASE_DIR/"mupeppbo_project"/".env"))


@shared_task()
def generate_token():

    url = "https://api.orange.com/oauth/v3/token"
    headers = {
        "Authorization": env('AUTHORIZATION'),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    body = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, data=body, headers=headers)
    json_response = response.json()
    token = json_response["access_token"]
    return token


@shared_task()
def test_tasks():
    print("Hello world")


@shared_task()
def get_sms():
    url = "https://api.orange.com/sms/admin/v1/contracts"
    token = generate_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    sms = requests.get(url, headers=headers).json()
    data = {
        "quantity" : sms[0]["availableUnits"],
        "expire": sms[0]["expirationDate"]
    }
    return data