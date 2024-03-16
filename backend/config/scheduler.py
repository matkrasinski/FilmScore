from apscheduler.schedulers.background import BackgroundScheduler


def init_datetime_scheduler(task, day=22, hour=3, minute=00, second=40):
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, "cron", day=day, hour=hour,
                      minute=minute, second=second)
    scheduler.start()
