from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from pymodm import connect
from dbClasses import *
from pyClasses import *
from reviewFunctions import *
from helperFunctions import *
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

    textNumber = request.values.get('From')
    textNumber = textNumber[1:]
    textBody = request.values.get('Body')
    newUser = False
    reviewState = None;
    
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

    parsed = parseReview(textBody, pyreview)

    if pyreview.title is not None:
        reviews = list(Review.objects.raw({'phone': pyreview.phone, 'title': pyreview.title}))
        if len(reviews) == 1 and pyreview.rating != -1:
             review = reviews[0]
             review.rating = pyreview.rating
             review.save()
             reviewState = "updated"
        elif pyreview.rating != -1:
            review = Review(
                phone=pyreview.phone,
                title=pyreview.title,
                rating=pyreview.rating
            ).save()
            reviewState = "new"
            
    message = determineMessage(pyreview, newUser, reviewState)


    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message)
	
    print(request.values.get('Body'))
    print(request.values.get('To')[1:])
    print(request.values.get('From')[1:])
    # for p in request.form.lists(): print p
    # {movie name} {rating}
    # {rating} {movie name}
    # {rating} {tv show name} {season} {episode}
    # {rating} {season} {episode} {tv show name}
    # {season} {episode} {rating} {tv show name}
    # {season} {episode} {tv show name} {rating}
    # {tv show name} {rating} {season} {episode}
    # {tv show name} {season} {episode} {rating}

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
