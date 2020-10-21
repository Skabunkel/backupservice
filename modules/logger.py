import logging
import systemd.journal as journ

""" Creates a scoped logger with a systemd journal logger handler """

def get_journal_logger(scope):
  logger = logging.getLogger(scope)
  logger.addHandler(journ.JournalHandler())
  logger.setLevel(logging.INFO)
  return logger

