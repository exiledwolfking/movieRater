The following steps were taken from the tutorial on https://www.twilio.com/docs/sms/quickstart/python
The steps require python 3.4 or 2.7+
Install mongodb version 3.6+

Create a file consts.py to hold your mongo server connection string.  I used mongodb atlas:
https://www.mongodb.com/cloud/atlas

In consts.py add CONNECTION_STR=<Connection String Here>. 
Since I installed mongod version 3.6.4, my connection string was similar to this: mongodb+srv://<username>:<pswd>@cluster0.mongodb.net/<dbName>

INSTALL TWILIO: pip install twilio OR easy_install twilio

INSTALL VIRUALENV: easy_install virtualenv (for python 2.4) OR pip install virtualenv (for python 3.4+) 

NAVIGATE TO THE DIRECTORY OF YOUR PROJECT. CREATE A VIRTUAL ENVIRONMENT: virtualenv --no-site-packages .

ACTIVATE THE VIRTUAL ENVIRONMENT: source bin/activate

INSTALL DEPENDENCIES: bin/pip install -r requirements.txt

INSTALL CRONTAB: pip install python-crontab

INSTALL AND SIGN UP FOR NGROK: https://ngrok.com/download

TO RUN, EXIT THE INSTALLATION CMD, START A NEW COMMAND PROMPT.  NAVIGATE TO THE DIRECTORY: ./runNgrok.sh
THIS STARTS NGROK.  COPY THE CONNECTION URL AND PASTE THIS INTO YOUR TWILIO WEBHOOK FOR YOUR NUMBER

START A SECOND COMMAND PROMPT: ./run.sh

OPEN NEW COMMAND PROMPT: pip install python-crontab
TO RUN CRON JOBS: python crons.py
VIEW RUNNING CRONS: crontab -l
