'''
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def job_function1(msg):
  print(msg)
  job_id.remove()
  scheduler.shutdown(wait=False)  # Shutdown the scheduler after the job is executed
  
  
scheduler = BlockingScheduler()
job_id = scheduler.add_job(job_function1, 'interval',seconds=5, args=['hello world'])
#parameters: 
# 1. function to be called   , what job we want to run
# 2. trigger type (interval, date, cron)  , how we want to trigger this job
# 3. trigger arguments (seconds, minutes, hours, etc.)  , when we want to run this job
# 4. id (optional) , unique identifier for the job
# 5. name (optional) , name of the job
# 6. replace_existing (optional) , if a job with the same id already exists, replace it
# 7. RETURN  a job instance

scheduler.start()

'''

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import time
from tasks.function1 import task1
from tasks.function2 import task2 
from tasks.function3 import task3
import logging
logger = logging.getLogger("uvicorn")

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


def main_job():
  logger.info("Main job running...")
  
  # remove pre sub-job for avoiding duplicate job
  for job_id in ['task1_job', 'task2_job', 'task3_job']:
    existing_job = scheduler.get_job(job_id=job_id)
    if existing_job:
      scheduler.remove_job(job_id=job_id)
      
  # add sub-jobs
  # id is unique identifier for each job
  # replace_existing=True will replace the job if it already exists if it is false it will create duplicate job
  # next_run_time=None , It controls job's first execution time. 
  # None dene ka matlab: don't execute immediately, just schedule the next run based on the interval.
  # Matlab agar aapne 12:00 baje scheduler start kiya, aur minutes=5 diya, to pehli baar job 12:05 pe chalega (turant nahi).
  # if we want to execute immediately then we can set next_run_time to current time using datetime.now()
  # next_run_time=datetime.now(IST)
  scheduler.add_job(task1, trigger=IntervalTrigger(seconds=5), id='task1_job', replace_existing=True, next_run_time=None)
  scheduler.add_job(task2, trigger=IntervalTrigger(seconds=10), id='task2_job', replace_existing=True, next_run_time=None)
  scheduler.add_job(task3, trigger=IntervalTrigger(seconds=15), id='task3_job', replace_existing=True, next_run_time=None)
    
  



scheduler.add_job(main_job, trigger=IntervalTrigger(minutes=1), id='main_job', replace_existing=True)

# if __name__ == "__main__":
#   scheduler.start()
#   try:
#     while True:
#       time.sleep(2)
#   except(KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()

app = FastAPI()
@app.on_event("startup")
def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started")
        
        
@app.on_event("shutdown")
def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shutdown")
