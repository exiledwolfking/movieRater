from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from pymodm import connect
from dbClasses import *
from pyClasses import *
from reviewFunctions import *
from helperFunctions import *
import logging
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
        pyhistory = pyHistory(textNumber, textBody)

        users = list(User.objects.raw({'_id': pyreview.phone}))
        if len(users) == 0:
            newUser = True
            user = User(
                phone=pyreview.phone,
                firstName=None,
                lastName=None
            ).save()

        processState = parseReview(textBody, pyreview)
        if processState == 'valid':
            processState = updateAddReview(processState, pyreview)

        message = determineMessage(pyreview, newUser, processState)
    except Exception as e:
        logging.error("error: " + str(e))
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
