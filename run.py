from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from pymodm import connect
from dbClasses import *
from pyClasses import *
from reviewFunctions import *
from historyFunctions import *
from helperFunctions import *
import logging
logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s')
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler('errors.log')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

#logging.basicConfig(filename='errors.log')
import consts

connect(
    consts.CONNECTION_STR,
    alias='my-atlas-app'
)

# The session object makes use of a secret key.
SECRET_KEY = consts.SECRET_KEY
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    """Respond with the number of text messages sent between two parties."""
    try:
        textNumber = request.values.get('From')
        textNumber = textNumber[1:]
        textBody = request.values.get('Body')
        newUser = False

        pyreview = pyReview(textNumber)
        saveHistory(textNumber, textBody)

        users = list(User.objects.raw({'_id': pyreview.phone}))
        if len(users) == 0:
            newUser = True
            user = User(
                phone=pyreview.phone,
                firstName=None,
                lastName=None
            ).save()
        
        processState = None
        queryResults = checkForQuery(textNumber, textBody) # check if user requested info
        if queryResults is None: #else user is adding/updating a review
            processState = parseReview(textBody, pyreview)
            if processState == 'valid':
                processState = updateAddReview(processState, pyreview)

        message = determineMessage(pyreview, newUser, processState, queryResults)
    except Exception as e:
        rootLogger.error(request.values.get('From') + ': ' + request.values.get('Body') + ': ' + str(e))
        message = "Uh oh, I encountered an issue, please try again!"

    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message)
	
    # for p in request.form.lists(): print p
    # {movie name} {rating} # movie can't have num at start DONE
    # {rating} {movie name} # movie can't have num at end DONE
    # {rating} {tv show name} {season} {episode} DONE
    # {rating} {season} {episode} {tv show name} rating must be double DONE
    # {season} {episode} {rating} {tv show name} rating must be double DONE
    # {season} {episode} {tv show name} {rating} DONE
    # {tv show name} {rating} {season} {episode} rating must be double
    # {tv show name} {season} {episode} {rating} rating must be double

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
