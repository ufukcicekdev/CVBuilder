from .utils import *
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def start():

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_generated_cv, 'cron', day_of_week='mon,fri', hour=9)
    scheduler.add_job(update_cv, 'cron', day_of_week='mon,fri', hour=9)


    #scheduler.add_job(check_generated_cv, 'interval', seconds=10)
    #scheduler.add_job(update_cv, 'interval', seconds=10)


 

    scheduler.start()