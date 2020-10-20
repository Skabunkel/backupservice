import logging
import systemd.journal as journ

""" Creates a scoped logger with a systemd journal logger handler """
@logger.journalctl_logger
def get_journal_logger(scope, logLevel):
  logger = logging.getLogger(scope)
  logger.addHandler(journ.JournaldLogHandler())
  log.setLevel(logLevel)


print("imported logging")
