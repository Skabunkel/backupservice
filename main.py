
import sys
from os import path

""" Only allow python3, and because it's python imp(importlib) was renamed after python 3.4 """
if sys.version_info[0] < 3:
  raise Exception("you should use Python 3 for this script.")

from modules import logger as log
from modules import processing as proc

import systemd.daemon as daemon
import yaml


config_yaml = "task.yml"

if __name__ == '__main__':
  log = log.get_journal_logger("backup")

  if not path.isfile(config_yaml):
    log.info(f"unable to find config file:\"{config_yaml}\"")

  with open(config_yaml) as file:
    config = yaml.safe_load(file)
  
  log.info("Starting")
  daemon.notify('READY=1')
  proc.start_processing(config, log)






  