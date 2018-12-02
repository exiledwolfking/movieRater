The following steps were taken from the tutorial on https://www.twilio.com/docs/sms/quickstart/python
The steps require python 3.4 or 2.7+
Install mongodb version 3.6+

Create a file consts.py to hold your mongo server connection string.  I used mongodb atlas:
https://www.mongodb.com/cloud/atlas

In consts.py add CONNECTION_STR=`<Connection String Here>`.  
In consts.py add PATH=`<Path to main project folder>` and update the paths in your runs.sh and runNgrok.sh bash files.  
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

---- Automated startup and email ----

If you want these commands to be run on startup (for example, in case of server restart), you can copy the
rc.local file into your /etc/ folder, or copy the appropriate lines.  Make sure not to copy over any existing 
lines you may have in this file. You will also want to update the PATH within this rc.local file.

 If setting this up, you will want to also setup the email sent to your
email address containing the ngrok tunnel url to enter into twilio.

Since the free version of ngrok uses generated urls, an email can be sent to admins on server failure.
The email will include the ngRok tunnel url.
To setup server failure emails :

    Update your consts.py file to include these four items. The port and host are for gmail.
	You will need to look these up for other providers:
	ADMIN_EMAIL_ADDRESS=`<email_address_here`
	ADMIN_EMAIL_PASSWORD=`<generated_password_here`
	ADMIN_EMAIL_HOST='smtp.gmail.com'
	ADMIN_EMAIL_PORT=587
	

    You can test that the rc.local file and email feature work by running "sudo bash rc.local"

    You may also need to specify your bash files being run by rc.local as executable using "chmod +x filename"

