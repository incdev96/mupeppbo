from celery import shared_task
import requests
import environ
from django.conf import settings

env = environ.Env()
environ.Env.read_env(env_file=str(settings.BASE_DIR/"mupeppbo_project"/".env"))


@shared_task()
def print_token():
    print(12345678)


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
    return json_response