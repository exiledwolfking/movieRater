from dbClasses import *


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def determineMessage(pyreview, newUser, processState, queryResults):
    ratingErr = 'You entered an invalid rating! Please enter a number between 0 and 10. '
    ratingErr += 'You can enter decimal numbers (5.6, 7.7, 8.3, etc).'
    
    undeterminedNum = 'Looks like your review has too many integers for me to understand it. '
    undeterminedNum += 'Put a decimal point on your rating number (X.0) so I can update your review!'

    if newUser:
        message = 'Welcome to movieRater! Type \'commands\' to view what you can send me. '
        if processState == 'new':
            message += 'Your review for ' + pyreview.title + ' was saved!'
        elif processState == 'ratingErr':
            message += ratingErr
        elif processState == 'undeterminedNum':
            message += undeterminedNum
        else:
            message += 'I couldn\'t detect a review, but you can now send me a review! '
    elif queryResults is not None:
        message = queryResults
    elif processState == 'undeterminedNum':
        message = undeterminedNum
    elif processState == 'new':
        message = 'I saved your review for ' + pyreview.title + '!'
    elif processState == 'updated':
        message = 'I updated your review for ' + pyreview.title + '!'
    elif processState == 'ratingErr':
        message = ratingErr
    else: # processState == noMatch
        message = 'I couldn\'t understand what you said, text me \'commands\' to view what you can send me.'
    return message

def titleFormat(s):
    exceptions = ['a', 'an', 'of', 'the', 'is']
    word_list = s.split()
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return ' '.join(final)

def getHelp():
    message = 'You can text me a review for a movie or tv show in any format. '
    message += 'Just enter 1) the name of the movie or show, 2) the rating you want to give '
    message += '(0.0 - 10.0), and 3) the season followed by the episode if it is a show. '
    message += 'You can give these three in any order. '
    message += 'To retrieve a review, enter 1) the name of a show or movie, and 2) '
    message += 'the season followed by the episode if it is a show'
    return message