from crontab import CronTab
import logging
import consts
logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s')
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler('cronErrors.log')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

try:
    cron = CronTab(user="kyle")
    cron.remove_all()
    
    commandStr = "python " + consts.PATH + "/calculateAverages.py"
    averageJob = cron.new(command=commandStr);
    averageJob.minutes.every(5)
    averageJob.enable()
    cron.write()
except Exception as e:
        rootLogger.error("crons.py: " + str(e))