from modules import backupJobs
from datetime import datetime
from queue import PriorityQueue
import os

"""
I'm still thinking about this file, i'll get back to you.
"""

""" STUB WILL CHANGE """
def start_processing(config, logger):
  if not isinstance(config, dict):
    raise Exception("invalid configuration provided.")
  
  if ('schedule' not in config) or (not isinstance(config['schedule'], str)):
    raise Exception("Default schedule is missing.")

  if ('jobs' not in config) or (not isinstance(config['jobs'], list)):
    raise Exception("No jobs to perform.")

  url = 'localhost'
  schedule = config['schedule']
  date = datetime.now()
  user = os.environ["USER"]
  taskqueue = PriorityQueue()

  if ('user' in config) and isinstance(config['user'], str):
    user = config['user']
  
  if ('url' in config) and isinstance(config['url'], str):
    url = config['url']

  for job_conf in config['jobs']:
    job = backupJobs.make_job(url, schedule, date, user, job_conf)

    if len(job.targets) != 0:
      taskqueue.put(job)
  
  config.clear()




""" STUB WILL CHANGE """
def stop_processing():
  print("STUB!")



def processor(queue, logger):
  print("STUB!")
  # something like this
  # rsync -a --delete from user@host:to
  # -a is for archive.
  # --delete sync file deletions to the target