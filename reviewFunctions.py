from helperFunctions import isfloat

def parseReview(body, review):
    bodyList = body.split()
    if isfloat(bodyList[0]):
        review.rating = float(bodyList[0])
        titleList = bodyList[1:]
        review.title = " ".join(titleList)