def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def determineMessage(pyreview, newUser, reviewState):
    ratingErr = "You entered an invalid rating! Please enter a number between 0 and 10. "
    ratingErr += "You can enter decimal numbers (5.6, 7.7, 8.3, etc)."
    if newUser:
        message = "Welcome to movieRater! "
        if reviewState == "new":
            message += "Your review for " + pyreview.title + " was saved!"
        elif reviewState == "rating err":
            message += ratingErr
        else:
            message += "I couldn't detect a review, but you can now send me a review! "
            message += "Enter 'Help' to view what you can send me."
    elif reviewState == "new":
        message = "I saved your review for " + pyreview.title + "!"
    elif reviewState == "updated":
        message = "I updated your review for " + pyreview.title + "!"
    elif reviewState == "rating err":
        message = ratingErr
    else:
        message = "I couldn't understand what you said, text me 'Help' to view what you can send me."
    return message