import json
import os 
import consts
import smtplib
from time import sleep

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
        
        maxAttempts = 25 # default max attempts
        try:
            maxAttempts = int(consts.MAX_ATTEMPTS)
        except Exception:
            pass
        
        succeeded = False
        for i in range(0, maxAttempts):
            try:
                cmdResponse = os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
                
                # 0 is successful response
                if cmdResponse == 0:
                    succeeded = True
            except Exception as tunnelException:
                pass
                
            if not succeeded:
                sleep(2)
            else:
                break
        
        url = None
        if succeeded: 
            with open('tunnels.json') as data_file:
                datajson = json.load(data_file)

            # retrieve url
            if len(datajson['tunnels']) > 0:
                url = datajson['tunnels'][0]['public_url']
        else:
            rootLogger.error('sendNgrokPortEmail.py ERROR: failed tunnel attempt ' + str(maxAttempts))

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
        os.remove("tunnels.json")
except Exception as e:
    rootLogger.error('sendNgrokPortEmail.py ERROR: ' + str(e))
