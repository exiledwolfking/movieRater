from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from pymodm import connect
from dbClasses import User, Review, History
import consts

connect(
    consts.CONNECTION_STR,
    alias='my-atlas-app'
)

# The session object makes use of a secret key.
SECRET_KEY = consts.SECRET_KEY
app = Flask(__name__)
app.config.from_object(__name__)

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


@app.route("/", methods=['GET', 'POST'])
def hello():
    """Respond with the number of text messages sent between two parties."""


    from_number = request.values.get('From')
    from_number = from_number[1:]
    body = request.values.get('Body')
    
    bodyList = body.split(' ')
    rating = -1
    if isfloat(bodyList[0]):
        rating = float(bodyList[0])
        titleList = body[1:]
        title = " ".join(titleList)
    
    users = list(User.objects.raw({'phone': from_number}))
    if len(users) == 0:
        user = User(
            phone=from_number,
            first_name=" ",
            last_name=" "
        ).save()
    
    if rating != -1:
        rating = Review(
            phone=from_number,
            media=title,
            rating=rating
        ).save()

    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message("Done")
	
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
