from datetime import datetime
class IntegrationLogging:
    @classmethod
    def log(cls, logtext):
        with open(f"logs/{datetime.now().date()}.txt", "a") as logfile:
            logfile.write(datetime.now().strftime("%H:%M") + "\r")
            logfile.writelines(logtext + "\r")
            logfile.writelines("--------------------------------------------------" + "\r")
