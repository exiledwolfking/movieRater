from helperFunctions import isfloat, titleFormat, getHelp, formatReviews
from datetime import datetime
from dbClasses import *
import pymongo
import re

def parseReview(body, review):
    
    invalidShow1 = r'^\s*(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s+((\w+)(\s+\w+)*)\s*$' # {int} {int} {int} {tv show name} -> indecipherable rating,season,episode
    invalidShow2 = r'^\s*((\w+)(\s+\w+)*)\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s*$' # {tv show name} {int} {int} {int} -> indecipherable rating,season,episode
    invalidShows = [invalidShow1, invalidShow2]
    for pattern in invalidShows:
        compiled = re.compile(pattern)
        match = compiled.match(body)
        if match is not None:
            return 'undeterminedNum'
    
    
    showPattern1 = r'^\s*(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s+(?P<title>((\w+)(\s+\w+)*))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s*$' # {rating} {tv show name} {season} {episode}
    showPattern2 = r'^\s*(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<title>((\w+)(\s+\w+)*))\s+(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s*$' # {season} {episode} {tv show name} {rating}
    showPattern3 = r'^\s*(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<rating>(\.\d|\d{1,2}\.\d?))\s+(?P<title>((\w+)(\s+\w+)*))\s*$' # {season} {episode} {rating} {tv show name}
    showPattern4 = r'^\s*(?P<rating>(\.\d|\d{1,2}\.\d?))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<title>((\w+)(\s+\w+)*))\s*$' # {rating} {season} {episode} {tv show name}
    showPattern5 = r'^\s*(?P<title>((\w+)(\s+\w+)*))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<rating>(\.\d|\d{1,2}\.\d?))\s*$' # {tv show name} {season} {episode} {rating}
    showPattern6 = r'^\s*(?P<title>((\w+)(\s+\w+)*))\s+(?P<rating>(\.\d|\d{1,2}\.\d?))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s*$' # {tv show name} {rating} {season} {episode}

    showPatterns = [showPattern1, showPattern2, showPattern3, showPattern4, showPattern5, showPattern6]
    for pattern in showPatterns:
        compiled = re.compile(pattern)
        match = compiled.match(body)
        if match is not None:
            review.rating = float(match.group('rating'))
            review.title = titleFormat(match.group('title'))
            review.season = int(match.group('season'))
            review.episode = int(match.group('episode'))
            return 'valid'
            break
    
    invalidMovie = r'^\s*(\d{1,2})\s+((\w+)(\s+\w+)*)\s+(\d{1,2})\s*$' # {int} {partial movie} {int} -> int in movie & user gave int as a rating
    invalidMovieCompiled = re.compile(invalidMovie)

    match = invalidMovieCompiled.match(body)
    if match is not None:
        return 'undeterminedNum'
    
    moviePattern1 = r'^\s*(?P<title>((\w+)(\s+\w+)*))\s+(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s*$' # {movie name} {rating}
    moviePattern2 = r'^\s*(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s+(?P<title>((\w+)(\s+\w+)*))\s*$' # {rating} {movie name}
    patterns = [moviePattern1, moviePattern2]
    for pattern in patterns:
        compiled = re.compile(pattern)
        match = compiled.match(body)
        if match is not None:
            review.rating = float(match.group('rating'))
            review.title = titleFormat(match.group('title'))
            return 'valid'
            break

    return 'noMatch'

def updateAddReview(parsedState, pyreview):
    if pyreview.rating >= 0 and pyreview.rating <= 10:
        reviews = list(Review.objects.raw({
            'phone': pyreview.phone,
            'title': pyreview.title,
            'season': pyreview.season,
            'episode': pyreview.episode
        }))
        if len(reviews) == 1:
            review = reviews[0]
            review.rating = pyreview.rating
            review.season = pyreview.season
            review.episode = pyreview.episode
            review.time = datetime.now()
            review.save()
            return 'updated'
        else:
            review = Review(
                phone = pyreview.phone,
                title = pyreview.title,
                season = pyreview.season,
                episode = pyreview.episode,
                rating = pyreview.rating,
                time= datetime.now()
            ).save()
            return 'new'
    elif pyreview.rating is None or pyreview.rating < 0.0 or pyreview.rating > 10.0:
        return 'ratingErr'
    else:
        return None

def checkForQuery(phone, body):
    if 'commands' == body.strip().lower():
        print('IN HERE')
        return getHelp()
    # check if user is request previous x reviews
    toLower = body.lower()
    if 'previous review' in toLower or 'last review' in toLower:
        return formatReviewList(phone, 1)
    lastXPattern = r'^\s*(last)\s+(?P<number>(\d+))((\s+(reviews))|(\s+(review)))?\s*$'
    previousXPattern = r'^\s*(previous)\s+(?P<number>(\d+))((\s+(reviews))|(\s+(review)))?\s*$'
    xPatterns = [lastXPattern, previousXPattern]
    for pattern in xPatterns:
        compiled = re.compile(pattern)
        match = compiled.match(toLower)
        if match is not None and int(match.group('number')) > 20:
            return 'Sorry, you can only view up to 20 previous reviews.'
        elif match is not None:
            return formatReviewList(phone, int(match.group('number')))
    
    #check if user entered 'my average of ' or 'average of' for personal average or userbase average
    splitString = body.strip().split()
    averageOfPattern = r'^\s*(average)\s+(of)\s+(?P<title>((\w+)(\s+\w+)*))\s*$'
    averageOfMatch = re.compile(averageOfPattern).match(toLower)
    myAverageOfPattern = r'^\s*(my)\s+(average)\s+(of)\s+(?P<title>((\w+)(\s+\w+)*))\s*$'
    myAverageOfMatch = re.compile(myAverageOfPattern).match(toLower)
    if averageOfMatch is not None:
        averages = list(Average.objects.raw({
            '_id': titleFormat(averageOfMatch.group('title'))
        }))
        if len(averages) == 1:
            return 'The app review average for ' + averages[0].title + ' is ' + str(averages[0].average) + '.'
        else:
            return 'No reviews were found for ' + titleFormat(averageOfMatch.group('title'))
    elif myAverageOfMatch is not None:
        reviews = list(Review.objects.raw({
            'phone': phone,
            'title': titleFormat(myAverageOfMatch.group('title')),
            'season': None,
            'episode': None
        }))
        # if a movie, just return review
        if len(reviews) == 1:
            title = reviews[0].title
            rating = reviews[0].rating
            return 'Your rating for ' + title + ' is ' + str(rating) + '.'
        
        reviews = list(Review.objects.raw({
            'phone': phone,
            'title': titleFormat(myAverageOfMatch.group('title')),
            'season': { '$exists': True},
            'episode': { '$exists': True}
        }))
        if len(reviews) > 0:
            sum = 0.0
            for review in reviews:
                sum += review.rating
            average = sum / len(reviews)
            return 'Your review average for ' + reviews[0].title + ' is ' + str(average) + '.'
    
    # check if user typed in tv show with season/episode to retrieve rating
    showPattern1 = r'^\s*(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<title>((\w+)(\s+\w+)*))\s*$' # {season} {episode} {tv show name}
    showPattern2 = r'^\s*(?P<title>((\w+)(\s+\w+)*))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s*$' # {tv show name} {season} {episode}
    showPatterns = [showPattern1, showPattern2]
    for pattern in showPatterns:
        compiled = re.compile(pattern)
        match = compiled.match(body)
        if match is not None:
            reviews = list(Review.objects.raw({
                'phone': phone,
                'title': titleFormat(match.group('title')),
                'season': int(match.group('season')),
                'episode': int(match.group('episode'))
            }))
            if len(reviews) == 1:
                title = reviews[0].title
                rating = reviews[0].rating
                return 'Your rating for ' + title + ' season ' + match.group('season') + ', episode ' + match.group('episode') + ' is ' + str(rating) + '.'
    
    #check if user typed in movie or tv show title for personal tv show average
    moviePattern = r'^\s*(?P<title>((\w+)(\s+\w+)*))\s*$' # {movie name} or {show name}
    compiled = re.compile(moviePattern)
    match = compiled.match(body)
    if match is not None:
        reviews = list(Review.objects.raw({
            'phone': phone,
            'title': titleFormat(match.group('title')),
            'season': None,
            'episode': None
        }))
        if len(reviews) == 1:
            title = reviews[0].title
            rating = reviews[0].rating
            return 'Your rating for ' + title + ' is ' + str(rating) + '.'
        
        reviews = list(Review.objects.raw({
            'phone': phone,
            'title': titleFormat(match.group('title')),
            'season': { '$exists': True},
            'episode': { '$exists': True}
        }))
        if len(reviews) > 0:
            sum = 0.0
            for review in reviews:
                sum += review.rating
            average = sum / len(reviews)
            return 'Your review average for ' + reviews[0].title + ' is ' + str(average) + '.'
    return None

def formatReviewList(phone, limitBy):
    qs = Review.objects.raw({
        'phone': phone
    })
    reviews = qs.aggregate(
        {'$sort': {'time': pymongo.DESCENDING}},
        {'$limit': limitBy}
    )
    reviewList = list(reviews)
    if reviewList:
        return formatReviews(reviewList)
    else:
        return 'You have no previous reviews.'