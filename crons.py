from crontab import CronTab

cron = CronTab()

averageJob = cron.new(command="python calculateAverages.py");
averageJob.minutes.every(5)

cron.write()