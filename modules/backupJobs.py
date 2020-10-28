from os import path
from croniter import croniter
from datetime import datetime
from dataclasses import field
from urllib.parse import urlparse

""" Represents a backup job. """
class backup_job:
  """  """
  name: str=field(compare=False)
  schedule: str=field(compare=False)
  url: str=field(compare=False)
  user: str=field(compare=False)
  destination:  str=field(compare=False)
  targets: list=field(compare=False)
  def __init__(self, name, schedule, url, targets, user, destination, now):
    self.name = name
    self.schedule = schedule
    self._schedule_itterator = croniter(schedule, now)
    self.url = url
    self.user = user
    self.targets = targets
    self.moveto_next(now)
    self.destination = destination
    self._fallback_time = 2 # Fallback time.

  """ Updates next date, and updates the time left. """
  def moveto_next(self, now = datetime.now()):
    self._next = self._schedule_itterator.get_next(datetime)
    return self._next

  """ fetches the time left to run. """
  def wait_to_run(self):
    priority = (self._next - datetime.now()).total_seconds()
    return min(priority, self._fallback_time)
  
  """ Gets the next date. """
  def get_next(self):
    return self._next
  
  """ self.priority < obj.priority """
  def __lt__(self, obj):
    return self._next < obj._next

  """ self.priority > obj.priority """
  def __gt__(self, obj):
      return self._next > obj._next

def format_sync_destination(hostname, sync_destination):
  if '{hostname}' in sync_destination:
    return sync_destination.replace('{hostname}', hostname)
  return sync_destination

# This function is realy chonk now... damn
""" Creates and validates a job. """
def make_job(hostname, default_url, default_schedule, current_date, default_user, default_destination, job):
  if not isinstance(job, dict):
      raise Exception("invalid job.")

  if 'name' not in job or not isinstance(job['name'], str):
    raise Exception("Invalid job name.")

  name = job['name']
  url = default_url
  schedule = default_schedule
  user = default_user
  destination = default_destination
  targets = []

  if ('to' in job) and isinstance(job['to'], str):
    destination = format_sync_destination(hostname, job['to'])

  if ('url' in job) and isinstance(job['url'], str):
    url = job['url']

  if ('user' in job) and isinstance(job['user'], str):
    user = job['user']
  
  if ('schedule' in job) and isinstance(job['schedule'], str):
    schedule = job['schedule']

  if ('targets' in job) and isinstance(job['targets'], list):
    for target in job['targets']:
      if isinstance(target, str):
        if path.isfile(target) or path.isdir(target):
          targets.append(target)
  
  return backup_job(name, schedule, url, targets, user, destination, current_date)