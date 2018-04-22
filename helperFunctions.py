def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def determineMessage(pyreview, newUser, reviewState):
    if newUser and reviewState == "new":
        message = "Welcome to movieRater, your review for " + pyreview.title + " was saved!"
    elif newUser:
        message = "Welcome to movieRater! I couldn't detect a review, but you can now send me a review! "
        message += "Enter 'Help' to view what you can send me."
    elif reviewState == "new":
        message = "I saved your review for " + pyreview.title + "!"
    elif reviewState == "updated":
        message = "I updated your review for " + pyreview.title + "!"
    else:
        message = "I couldn't understand what you said, text me 'Help' to view what you can send me."
    return message