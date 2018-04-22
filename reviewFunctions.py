from helperFunctions import isfloat, titleFormat
from dbClasses import *
import re

def parseReview(body, review):
    moviePattern1 = r'^(?P<movie>((\w+)(\s+\w+)*))\s+(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s*$' # {movie name} {rating}
    moviePattern2 = r'^(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s+(?P<movie>((\w+)(\s+\w+)*))\s*$' # {rating} {movie name}
    movieCompiled1 = re.compile(moviePattern1)
    movieCompiled2 = re.compile(moviePattern2)
    match = movieCompiled1.match(body)
    if match is None:
        match = movieCompiled2.match(body)
        if match is None:
            return False
    print("rating:" + match.group('rating'))
    print("title:" + match.group("movie"))
    review.rating = float(match.group('rating'))
    review.title = titleFormat(match.group('movie'))
    return True
    #bodyList = body.split()
    #if isfloat(bodyList[0]) and len(bodyList) > 1:
    #    review.rating = float(bodyList[0])
    #    titleList = bodyList[1:]
    #    review.title = titleFormat(" ".join(titleList))
    #   return True
    #elif isfloat(bodyList[-1]) and len(bodyList) > 1:
    #    review.rating = float(bodyList[-1])
    #    titleList = bodyList[:-1]
    #    review.title = titleFormat(" ".join(titleList))
    #    return True
    #return False

def updateAddReview(parsed, pyreview):
    if parsed and pyreview.rating >= 0 and pyreview.rating <= 10:
        reviews = list(Review.objects.raw({'phone': pyreview.phone, 'title': pyreview.title}))
        if len(reviews) == 1 and pyreview.rating != -1:
             review = reviews[0]
             review.rating = pyreview.rating
             review.save()
             return "updated"
        elif pyreview.rating != -1:
            review = Review(
                phone=pyreview.phone,
                title=pyreview.title,
                rating=pyreview.rating
            ).save()
            return "new"
    elif pyreview.rating is None or pyreview.rating < 0.0 or pyreview.rating > 10.0:
        return "rating err"
    else:
        return None
            