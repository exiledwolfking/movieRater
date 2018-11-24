The following steps were taken from the tutorial on https://www.twilio.com/docs/sms/quickstart/python
The steps require python 3.4 or 2.7+
Install mongodb version 3.6+

Create a file consts.py to hold your mongo server connection string.  I used mongodb atlas:
https://www.mongodb.com/cloud/atlas

In consts.py add CONNECTION_STR=`<Connection String Here>`.  
In consts.py add PATH=`<Path to main project folder>`  
For example: "PATH='/home/`<userName>`/Documents/movieRater'"  
In consts.py add CRONUSER=`<username>`  
Since I installed mongod version 3.6.4, my connection string was similar to this: mongodb+srv://<username>:<pswd>@cluster0.mongodb.net/<dbName>

Install twilio: pip install twilio OR easy_install twilio

Install virtualenv: easy_install virtualenv (for python 2.4) OR pip install virtualenv (for python 3.4+) 

Navigate to the directory of your project. Create a virtual environment: virtualenv --no-site-packages .

Activate the virtual environment: source bin/activate

Install dependencies: bin/pip install -r requirements.txt

Install crontab if you wish to run average table cron job: pip install python-crontab

Install and sign up for ngrok: https://ngrok.com/download

To run, exit the installation terminal, and start a new terminal. Navigate to the directory: ./runNgrok.sh
This starts ngrok.  Copy the connection url and paste this into your twilio webhook for your number

Start a new command prompt and run: ./run.sh

Start a new command prompt and run to run the average table cron job: python crons.py

View running crons: crontab -l
