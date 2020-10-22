
import signal
import sys

""" Only allow python3, and because it's python imp(importlib) was renamed after python 3.4 """
if sys.version_info[0] < 3:
  raise Exception("you should use Python 3 for this script.")

from modules import logger as log
from modules import processing as proc

import systemd.daemon as daemon
import yaml

log = log.get_journal_logger("backup")
config_yaml = "task.yml"

""" Define signal handlers for SIGTERM, and SIGHUP(reload) """
def sigterm_handler(_signo, _stack):
  daemon.notify('STOPPING=1')
  proc.stop_processing()
  sys.exit(0)


def reload_handler(_signo, _stack):
  daemon.notify('RELOADING=1')

  #proc.stop_processing()
  # reload ini file, then task.yml file.
  #proc.start_processing()

  daemon.notify('READY=1')

if __name__ == '__main__':
  signal.signal(signal.SIGTERM, sigterm_handler)
  signal.signal(signal.SIGHUP, reload_handler) # SIGHUP is used as a reload signal for many daemons.

  daemon.notify('READY=1')

  config = yaml.safe_load(""" 
url: 'no'
schedule: '*/5 * * * *'
jobs:
 - name: 'Syncing system configs' # Syncs configs to default location.
   schedule: '0 */24 * * *'
   targets:
    - '/srv/'
 
 - name: 'Sync cheese stash'
   url: 'no'
   targets: 
    - '/home/niklas'
  """)

  proc.start_processing(config, log)






  