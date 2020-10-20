
import signal
import sys

""" Only allow python3, and because it's python imp(importlib) was renamed after python 3.4 """
if sys.version_info[0] < 3:
  raise Exception("you should use Python 3 for this script.")
elif sys.version_info[1] >= 4:
  import importlib as imp
else:
  import imp

from modules import logger as log
from modules import processing as proc
import configparser

""" Define signal handlers for SIGTERM, and SIGHUP(reload) """
def sigterm_handler(_signo, _stack):
  systemd.daemon.notify('STOPPING=1')
  proc.stop_processing()
  sys.exit(0)


def reload_handler(_signo, _stack):
  systemd.daemon.notify('RELOADING=1')

  proc.stop_processing()
  # reload ini file, then task.yml file.
  proc.start_processing()

  systemd.daemon.notify('READY=1')

if __name__ == '__main__':
  import systemd.daemon
  
  #register termination, and reload signals
  signal.signal(signal.SIGTERM, sigterm_handler)
  signal.signal(signal.SIGHUP, reload_handler) # SIGHUP is used as a reload signal for many deamons.

  systemd.daemon.notify('READY=1')
  log = log.get_journal_logger("backup")
  log.info("HELLO")






  