def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def determineMessage(pyreview, newUser, processState):
    ratingErr = 'You entered an invalid rating! Please enter a number between 0 and 10. '
    ratingErr += 'You can enter decimal numbers (5.6, 7.7, 8.3, etc).'
    
    undeterminedNum = 'Looks like your movie review has a number at the beginning and end. '
    undeterminedNum += 'Put a decimal point on your rating number (X.0) so I can tell!'

    if newUser:
        message = 'Welcome to movieRater! Type \'Help\' to view what you can send me. '
        if processState == 'new':
            message += 'Your review for ' + pyreview.title + ' was saved!'
        elif processState == 'ratingErr':
            message += ratingErr
        elif processState == 'undeterminedNum':
            message += undeterminedNum
        else:
            message += 'I couldn\'t detect a review, but you can now send me a review! '
    elif processState == 'undeterminedNum':
        message = undeterminedNum
    elif processState == 'new':
        message = 'I saved your review for ' + pyreview.title + '!'
    elif processState == 'updated':
        message = 'I updated your review for ' + pyreview.title + '!'
    elif processState == 'ratingErr':
        message = ratingErr
    else: # processState == noMatch
        message = 'I couldn\'t understand what you said, text me \'Help\' to view what you can send me.'
    return message

def titleFormat(s):
    exceptions = ['a', 'an', 'of', 'the', 'is']
    word_list = s.split()
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return ' '.join(final)