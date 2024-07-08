from celery import shared_task
from time import sleep

@shared_task
def pages():
    sleep(5)
    print("hello tasks")
    return 
    