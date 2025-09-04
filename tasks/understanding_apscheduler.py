from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
scheduler = BackgroundScheduler()
# method 1
jobStores = {
  'mongo': MongoDBJobStore(),
  'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
  'default': ThreadPoolExecutor(20),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': False,
  'max_instances': 3
}
scheduler.configure(jobStores=jobStores, executors=executors, job_defaults=job_defaults,timezone= timezone('Asia/Kolkata'))


#method 2
schedulerr = BackgroundScheduler({
  'apscheduler.jobstores.mongo':{
    'type':'mongodb'
  },
  'apscheduler.jobstores.default':{
    'type':'sqlalchemy',
    'url':'sqlite:///jobs.sqlite'
  },
  'apscheduler.executors.default':{
    'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
    'max_workers':'20'
    },
  'apscheduler.executors.processpool':{
    'type':'processpool',
    'max_workers':'5'
  },
  'apscheduler.job_defaults.coalesce':'false',
  'apscheduler.job_defaults.max_instances':'3',
  'apscheduler.timezone':'Asia/Kolkata'
})

#method 3
schedulerrr = BackgroundScheduler()
jobstores = {
  'mongo': {'type':'mongodb'},
  'default': {'type':'sqlalchemy', 'url':'sqlite:///jobs.sqlite'}
}

executors = {
  'default': {'class': 'apscheduler.executors.pool:ThreadPoolExecutor','max_workers':'20'},
  'processpool': {'type': 'processpool','max_workers':'5'}
}
job_defaults = {
  'coalesce': 'false',
  'max_instances': '3'
}
schedulerrr.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='Asia/Kolkata')

# Starting the scheduler is done by simply calling start()
# There are two ways to add jobs to a scheduler:

# by calling add_job()
# by decorating a function with scheduled_job()
# The add_job() method returns a apscheduler.job.Job instance that you can use to modify or remove the job later.
# replace_existing = True (same id ke job ko replace kar dega)
# scheduler.add_job(my_job, 'interval', minutes=2, id='my_job_id', replace_existing=True)
# removing job
# scheduler.remove_job('my_job_id') on job id
# scheduler.remove()  on the job instance got from add_job()
'''
Matlab agar tum job add karte waqt jo Job object/instance return hota hai usko save kar lo (ek variable me ya DB me),
to baad me us instance ke through tum us job ko pause, resume, modify ya remove kar sakte ho.
Ye thoda convenient hai, lekin condition ye hai ki tumhe wo Job instance yaad rakhna padega.

Agar tum jobs ko decorator se schedule karte ho (jaise @scheduler.scheduled_job(...)),
to us case me tumhe pehle wala method (job ki id use karke manage karna) hi use karna padega,
kyunki decorator wali jobs me tumhe Job instance directly nahi milta.
'''
def myfun():
  print("Hello World")
  
job = scheduler.add_job(myfun, 'interval', minutes='2')
job.remove()  # removing job using job instance

#remove using job_id
scheduler.add_job(myfun, 'interval', minutes='3', id="my_fun_id")
scheduler.remove_job('my_fun_id')

# Pausing and resuming jobs
# You can easily pause and resume jobs through either the Job instance or the scheduler itself. 
# When a job is paused, its next run time is cleared and no further run times will be 
# calculated for it until the job is resumed. To pause a job, use either method:
# apscheduler.job.Job.pause()
# apscheduler.schedulers.base.BaseScheduler.pause_job(job_id)
# RESUME A JOB
# apscheduler.job.Job.resume()
# apscheduler.schedulers.base.BaseScheduler.resume_job(job_id)

#Geeting list of jobs
# To get a machine processable list of the scheduled jobs, we can use the get_jobs() method. 
# It will return a list of Job instances.
scheduler.get_jobs()
# get_jobs() → list of Job objects (machine-processable).
# get_jobs('alias') → got only one job store job
# print_jobs() → print formatted list of jobs (human-readable)

# Modifying jobs
# You can modify any job attributes by calling either apscheduler.job.Job.modify() 
# or modify_job(). we can modify any Job attributes(properties) except for id
# Example: job's trigger (interval), next run time, arguments, etc.
# if has job instance== job.modify(seconds=20)
# if has job id == scheduler.modify_job('job_id', seconds=20)

#rescheduling jobs
# we can modified the trigger type or trigger time of a job by using 
# if has a job instance == job.reschedule('interval', minutes=5)
# if has a job id == scheduler.reschedule_job('job_id', trigger='interval', minutes=5)

# Shutting down the scheduler
scheduler.shutdown()
# By default, the scheduler shuts down its job stores and executors and waits until all currently
# executing jobs are finished. If you don’t want to wait, you can do:
scheduler.shutdown(wait=False)
# does not wait for any running tasks to complete.
# It is also possible to start the scheduler in paused state, that is, without the first wakeup call:

# Agar aapko scheduler chalana hai lekin jobs ko turant run nahi karwana.
# Tum pehle jobs add/update karna chahte ho aur baad me manually scheduler.resume() karke start karna chahte ho
# Start scheduler in paused state
scheduler.start(paused=True)

# Limiting the number of concurrently executing instances of a job
# By default, only one instance of each job is allowed to be run at the same time.
# Agar wo job abhi chal rahi hai aur usi waqt scheduler usko fir run karna chahta hai, to wo allow nahi karega.
# This means that if the job is about to be run but the previous run hasn’t finished yet, then the latest run is considered a misfire.
# It is possible to set the maximum number of instances for a particular job that the scheduler
# will let run concurrently, by using the max_instances keyword argument when adding the job.

# Missed job executions and coalescing
# misfire_grace_time
# Jab scheduler dobara start hota hai, to wo check karta hai ki job ke missed runs abhi bhi execute kiye jaane chahiye ya nahi.
# Misfire = job apne scheduled time pe nahi chali (scheduler band ya delay).
# misfire_grace_time = decide karta hai ki miss hone ke baad bhi run karna chahiye ya nahi.
# coalescing = multiple missed runs ko ek run me combine kar deta hai (taaki job ek hi baar chale).
coalesce = True
coalesce = False
# Agar coalesce True hai, to agar job ke multiple missed runs hain, to wo unko combine karke sirf ek run karega.
# Agar coalesce False hai, to wo har missed run ko alag-alag execute karega (agar wo misfire_grace_time ke andar hain).
# misfire_grace_time = 30 (seconds)

#scheduler events
# Jab bhi scheduler me koi special activity/event hoti hai (jaise job add hona, job execute hona,
# job fail hona, scheduler start/stop hona, etc.), to scheduler ek event fire karta hai.
# Agar tumhe sirf ye sunna hai ki "job complete hua" ya "job fail hua", to tum add_listener() me ek mask argument doge jo specify karega kaunsa event sunna hai.
# Multiple events sunne ke liye constants ko OR (|) karke pass kar sakte ho.
# Listener ko jab call kiya jata hai, tab use ek event object diya jata hai jisme details hoti hain (job ka ID, run time, exception, etc. depending on event).
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')

scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


#Exporting and importing jobs
# agar aap APScheduler ke jobs ek job store (DB, memory, etc.) se dusre job store me shift karna
# chahte ho, to tumhe unhe export (JSON file/document me save) karna hoga aur phir import (wapas load) karna hoga.
# use cases
# Tum apna app migrate kar rahe ho ek server se dusre server par
# Job store change karna hai (jaise MemoryJobStore → MongoDBJobStore)
# Jobs ko backup karke rakhna hai future ke liye
import json
from apscheduler.jobstores.base import JobLookupError

# Export jobs to JSON file
def export_jobs(scheduler, filename="jobs.json"):
    jobs = scheduler.get_jobs()   # list totals jobs
    job_dicts = [job.__getstate__() for job in jobs]  # converting jobs into dicts
    with open(filename, "w") as f:
        json.dump(job_dicts, f, indent=4)
    print(f"📤 Jobs exported to {filename}")


# Example usage
export_jobs(scheduler)


# IMPORTING JOBS
from apscheduler.job import Job

def my_job():
  print("job executed imported")
# Import jobs from JSON file
def import_jobs(scheduler, filename="jobs.json"):
    with open(filename, "r") as f:
        job_dicts = json.load(f)

    for job_dict in job_dicts:
        # need to update function reference 
        job_dict['func'] = my_job  
        scheduler.add_job(**job_dict)

    print(f"📥 Jobs imported from {filename}")


# Import and start
import_jobs(scheduler)
scheduler.start()


#Troubleshooting

import logging

# Logging setup
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


