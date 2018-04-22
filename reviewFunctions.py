from helperFunctions import isfloat, titleFormat
from dbClasses import *
import re

def parseReview(body, review):
    movieNumInName = r'^(\d{1,2})\s+((\w+)(\s+\w+)*)\s+(\d{1,2})\s*$' # {int} {partial movie} {int} -> int in movie & user gave int as a rating
    numInNameCompiled = re.compile(movieNumInName)
    match = numInNameCompiled.match(body)
    if match is not None:
        return 'undeterminedNum'
    
    moviePattern1 = r'^(?P<movie>((\w+)(\s+\w+)*))\s+(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s*$' # {movie name} {rating}
    moviePattern2 = r'^(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s+(?P<movie>((\w+)(\s+\w+)*))\s*$' # {rating} {movie name}
    patterns = [moviePattern1, moviePattern2]
    for pattern in patterns:
        compiled = re.compile(pattern)
        match = compiled.match(body)
        if match is not None:
            break

    if match is None:
        return 'noMatch'
    print("rating:" + match.group('rating'))
    print("title:" + match.group("movie"))
    review.rating = float(match.group('rating'))
    review.title = titleFormat(match.group('movie'))
    return 'valid'

def updateAddReview(parsedState, pyreview):
    if pyreview.rating >= 0 and pyreview.rating <= 10:
        reviews = list(Review.objects.raw({'phone': pyreview.phone, 'title': pyreview.title}))
        if len(reviews) == 1 and pyreview.rating != -1:
             review = reviews[0]
             review.rating = pyreview.rating
             review.save()
             return 'updated'
        elif pyreview.rating != -1:
            review = Review(
                phone=pyreview.phone,
                title=pyreview.title,
                rating=pyreview.rating
            ).save()
            return 'new'
    elif pyreview.rating is None or pyreview.rating < 0.0 or pyreview.rating > 10.0:
        return 'ratingErr'
    else:
        return None
            