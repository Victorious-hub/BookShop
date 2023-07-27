from celery import shared_task
from time import sleep

@shared_task
def sleeptime(total_time):
    sleep(total_time)
    return None
