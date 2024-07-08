from celery import shared_task
from time import sleep
from .models import Istoriya

@shared_task
def posttast():
    print("hello")
    return None

