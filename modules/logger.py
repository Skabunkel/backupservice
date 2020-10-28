import logging
import sys
import systemd.journal as journ

""" Creates a scoped logger with a systemd journal logger handler """

def get_journal_logger(scope):
  logger = logging.getLogger(scope)
  handler = logging.StreamHandler(sys.stdout)
  handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
  #logger.addHandler(journ.JournalHandler())
  logger.addHandler(handler)
  logger.setLevel(logging.INFO)
  return logger

