from modules import backupJobs
from datetime import datetime
from queue import PriorityQueue
import os
import time
import platform
import urllib
import subprocess

""" 
Reads the jobs from the task file.
Then starts running then jobs forever.
"""
def start_processing(config, logger):
  if not isinstance(config, dict):
    raise Exception("invalid configuration provided.")
  
  if ('schedule' not in config) or (not isinstance(config['schedule'], str)):
    raise Exception("Default schedule is missing.")

  if ('jobs' not in config) or (not isinstance(config['jobs'], list)):
    raise Exception("No jobs to perform.")

  hostname = platform.node()

  url = 'localhost'
  schedule = config['schedule']
  date = datetime.now()
  user = os.environ["USER"]
  to = '/tmp/'
  taskqueue = PriorityQueue()

  if ('user' in config) and isinstance(config['user'], str):
    user = config['user']

  if ('to' in config) and isinstance(config['to'], str):
    to = backupJobs.format_sync_destination(hostname, config['to'])
  
  if ('url' in config) and isinstance(config['url'], str):
    url = config['url']

  for job_conf in config['jobs']:
    job = backupJobs.make_job(hostname, url, schedule, date, user, to, job_conf)

    if len(job.targets) != 0:
      taskqueue.put(job)
  
  config.clear()

  processor(taskqueue, logger)

"""
Starts processing of syncing data from source to destination.
Syncs data from a host to another, this host expects to have access via ssh to the destination.
"""
def processor(queue, logger):
  if queue.empty():
    logger.error("No valid tasks where found.")
    return
  
  while True:
    job = queue.get()
    time_left = job.wait_to_run()
    if time_left <= 0:
      _sync(job, logger)
    
    queue.put(job)
    if time_left > 0:
      time.sleep(time_left)


"""
Syncs data from a host to another, this host expects to have access via ssh to the destination.
"""
def _sync(job, logger):

  user_host = f'{job.user}@{job.url}'
  dest_root = job.destination
  for target in job.targets:
    source = target
    destination = f'{user_host}:{os.path.join(dest_root)}'
    logger.info(f'syncing from:\"{target}\" to:\"{destination}\"')
    
    proc = subprocess.run(['rsync', '-a', '--relative', '--delete', source, destination],  shell=True)

    if proc.returncode != 0:
      logger.error(f'Job:\"{job.name}\" did not finish with a successfull error code, rescheduled for:\"{job.moveto_next()}\"')
    else:
      logger.info(f'Job:\"{job.name}\" is done, rescheduled for:\"{job.moveto_next()}\"')
    #logger.info(' '.join(['rsync', '-a', '--delete', source, destination]))
    # something like this
    # rsync -a --delete from user@host:to
    # -a is for archive.
    # --delete sync file deletions to the target