from apscheduler.schedulers.background import BackgroundScheduler
# import logging
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def task1():
  print("Task 1 executed...")

scheduler = BackgroundScheduler()

scheduler.add_job(task1, 'interval', seconds=3,id='task1', replace_existing=True,coalesce=True, max_instances=1)

scheduler.start()
try:
    import time
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()