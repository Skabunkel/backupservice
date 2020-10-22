from os import path
from croniter import croniter
from datetime import datetime
from dataclasses import field

""" Represents a backup job. """
class backup_job:
  """ time left in seconds. """
  priority: float

  name: str=field(compare=False)
  schedule: str=field(compare=False)
  url: str=field(compare=False)
  user: str=field(compare=False)
  targets: list=field(compare=False)
  def __init__(self, name, schedule, url, targets, user, now):
    self.name = name
    self.schedule = schedule
    self._schedule_itterator = croniter(schedule, now)
    self.url = url
    self.user = user
    self.targets = targets
    self.next(now)

  """ Updates next date, and updates the time left. """
  def next(self, now = datetime.now()):
    self._next = self._schedule_itterator.get_next(datetime)
    self.priority = (self._next - now).total_seconds()

  """ Updates the time left, and return the latest time. """
  def should_run(self):
    self.priority = (self._next - datetime.now()).total_seconds()
    return self.priority
  
  """ Gets the next date. """
  def get_next(self):
    return self._next
  
  """ self.priority < obj.priority """
  def __lt__(self, obj):
    return self.priority < obj.priority

  """ self.priority > obj.priority """
  def __gt__(self, obj):
      return self.priority > obj.priority

""" Creates and validates a job. """
def make_job(default_url, default_schedule, current_date, default_user, job):
  if not isinstance(job, dict):
      raise Exception("invalid job.")

  if 'name' not in job or not isinstance(job['name'], str):
    raise Exception("Invalid job name.")
  
  name = job['name']
  url = default_url
  schedule = default_schedule
  user = default_user
  targets = []

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
  
  return backup_job(name, schedule, url, targets, user, current_date)