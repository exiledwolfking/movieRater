import json
import os 
import consts
import smtplib

from email.message import EmailMessage

import logging
logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s')
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler('errors.log')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

try:
    # only send email if consts configured
    if (consts.ADMIN_EMAIL_ADDRESS is not None and
        consts.ADMIN_EMAIL_HOST is not None and
        consts.ADMIN_EMAIL_PORT is not None and
        consts.ADMIN_EMAIL_PASSWORD is not None):
        os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

        with open('tunnels.json') as data_file:
            datajson = json.load(data_file)

        # retrieve url
        url = None;
        if len(datajson['tunnels']) > 0:
            url = datajson['tunnels'][0]['public_url']

        print(url)
        # construct email message
        msg = 'Ngrok serverer restarted.  '

        if url is None:
            msg = msg + 'Error retrieving tunnel url.'
        else:
            msg = msg + 'Tunnel url is: ' + url

        # start email server
        smtpServer = smtplib.SMTP(host=consts.ADMIN_EMAIL_HOST, port=consts.ADMIN_EMAIL_PORT)
        smtpServer.starttls()
        smtpServer.login(consts.ADMIN_EMAIL_ADDRESS, consts.ADMIN_EMAIL_PASSWORD)

        # create email
        emailEntity = EmailMessage()
        emailEntity.set_content(msg)
        emailEntity['Subject'] = 'NGROK Server restarted'
        emailEntity['From'] = consts.ADMIN_EMAIL_ADDRESS
        emailEntity['To'] = consts.ADMIN_EMAIL_ADDRESS

        # send email
        smtpServer.send_message(emailEntity)
        smtpServer.quit()
except Exception as e:
    rootLogger.error('sendNgrokPortEmail.py ERROR: ' + str(e))
