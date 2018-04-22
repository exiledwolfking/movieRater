from helperFunctions import isfloat
from dbClasses import *

def parseReview(body, review):
    bodyList = body.split()
    if isfloat(bodyList[0]) and len(bodyList) > 1:
        review.rating = float(bodyList[0])
        titleList = bodyList[1:]
        review.title = " ".join(titleList)
        return True
    elif isfloat(bodyList[-1]) and len(bodyList) > 1:
        review.rating = float(bodyList[-1])
        titleList = bodyList[:-1]
        review.title = " ".join(titleList)
        return True
    return False

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
    elif pyreview.rating < 0.0 or pyreview.rating > 10.0:
        return "rating err"
    else:
        return None
            