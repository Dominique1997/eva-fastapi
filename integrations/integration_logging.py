import os
from datetime import datetime


class IntegrationLogging:
    @classmethod
    def info(cls, infoText):
        cls._append_to_log_file("INFO", infoText)

    @classmethod
    def warning(cls, warningText):
        cls._append_to_log_file("WARNING", warningText)

    @classmethod
    def critical(cls, criticalText):
        cls._append_to_log_file("CRITICAL", criticalText)

    @classmethod
    def _append_to_log_file(cls, logLevel, logText):
        with open(f"{os.getcwd()}/logs/{datetime.now().date()}.log", "a") as logFile:
            logFile.write(f"{datetime.now().time()}: {logLevel}: {logText}")
            logFile.write("\n")
