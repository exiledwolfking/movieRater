from helperFunctions import isfloat, titleFormat, getHelp, formatReviews
from datetime import datetime
from dbClasses import *
import pymongo
import re

def parseReview(body, review):
    
    invalidShow1 = r'^\s*(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s+((\S+)(\s+\S+)*)\s*$' # {int} {int} {int} {tv show name} -> indecipherable rating,season,episode
    invalidShow2 = r'^\s*((\S+)(\s+\S+)*)\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s*$' # {tv show name} {int} {int} {int} -> indecipherable rating,season,episode
    invalidShows = [invalidShow1, invalidShow2]
    for pattern in invalidShows:
        compiled = re.compile(pattern)
        match = compiled.match(body)
        if match is not None:
            return 'undeterminedNum'
    
    
    showPattern1 = r'^\s*(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s+(?P<title>((\S+)(\s+\S+)*))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s*$' # {rating} {tv show name} {season} {episode}
    showPattern2 = r'^\s*(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<title>((\S+)(\s+\S+)*))\s+(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s*$' # {season} {episode} {tv show name} {rating}
    showPattern3 = r'^\s*(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<rating>(\.\d|\d{1,2}\.\d?))\s+(?P<title>((\S+)(\s+\S+)*))\s*$' # {season} {episode} {rating} {tv show name}
    showPattern4 = r'^\s*(?P<rating>(\.\d|\d{1,2}\.\d?))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<title>((\S+)(\s+\S+)*))\s*$' # {rating} {season} {episode} {tv show name}
    showPattern5 = r'^\s*(?P<title>((\S+)(\s+\S+)*))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<rating>(\.\d|\d{1,2}\.\d?))\s*$' # {tv show name} {season} {episode} {rating}
    showPattern6 = r'^\s*(?P<title>((\S+)(\s+\S+)*))\s+(?P<rating>(\.\d|\d{1,2}\.\d?))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s*$' # {tv show name} {rating} {season} {episode}

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
    
    invalidMovie = r'^\s*(\d{1,2})\s+((\S+)(\s+\S+)*)\s+(\d{1,2})\s*$' # {int} {partial movie} {int} -> int in movie & user gave int as a rating
    invalidMovieCompiled = re.compile(invalidMovie)

    match = invalidMovieCompiled.match(body)
    if match is not None:
        return 'undeterminedNum'
    
    moviePattern1 = r'^\s*(?P<title>((\S+)(\s+\S+)*))\s+(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s*$' # {movie name} {rating}
    moviePattern2 = r'^\s*(?P<rating>(\d{1,2}|\.\d|\d{1,2}\.\d?))\s+(?P<title>((\S+)(\s+\S+)*))\s*$' # {rating} {movie name}
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
    if 'previous reviews' in toLower or 'last reviews' in toLower:
        return formatReviewList(phone, 20)
    elif 'previous review' in toLower or 'last review' in toLower:
        return formatReviewList(phone, 1)

    # Check for previous or last requests
    lastXPattern = r'^\s*(last)\s+(?P<number>(\d+))((\s+(reviews))|(\s+(review)))?\s*$'
    previousXPattern = r'^\s*(previous)\s+(?P<number>(\d+))((\s+(reviews))|(\s+(review)))?\s*$'
    prevLastPatterns = [lastXPattern, previousXPattern]
    for pattern in prevLastPatterns:
        compiled = re.compile(pattern)
        match = compiled.match(toLower)
        if match is not None and int(match.group('number')) > 20:
            return 'Sorry, you can only view up to 20 previous reviews.'
        elif match is not None:
            return formatReviewList(phone, int(match.group('number')))
    
    # Check for highest or lowest rating requests
    highestPattern = r'^\s*highest\s+review\s*$'
    lowestPattern = r'^\s*lowest\s+review\s*$'
    if re.compile(highestPattern).match(toLower):
        return formatReviewList(phone, 1, timeSort=None, scoreSort=pymongo.DESCENDING)
    elif re.compile(lowestPattern).match(toLower):
        return formatReviewList(phone, 1, timeSort=None, scoreSort=pymongo.ASCENDING)
    lowestXPattern = r'^\s*((?P<number>(\d+))\s+)?(lowest)((\s+(reviews))|(\s+(review)))?\s*$'
    highestXPattern = r'^\s*((?P<number>(\d+))\s+)?(highest)((\s+(reviews))|(\s+(review)))?\s*$'
    lowHighPatterns = [lowestXPattern, highestXPattern]
    for pattern in lowHighPatterns:
        compiled = re.compile(pattern)
        match = compiled.match(toLower)
        if match is not None and match.group('number') is not None:
            if int(match.group('number')) > 20:
                return 'Sorry, you can only view up to 20 previous reviews.'
            if highestXPattern == pattern:
                return formatReviewList(phone, int(match.group('number')), timeSort=None, scoreSort=pymongo.DESCENDING)
            else:
                return formatReviewList(phone, int(match.group('number')), timeSort=None, scoreSort=pymongo.ASCENDING)
        elif match is not None:
            if highestXPattern == pattern:
                return formatReviewList(phone, 20, timeSort=None, scoreSort=pymongo.DESCENDING)
            else:
                return formatReviewList(phone, 20, timeSort=None, scoreSort=pymongo.ASCENDING)
    
    # check if user entered 'delete review X'
    deleteEpisodePattern1 = r'^\s*(delete)\s+(review)\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<title>((\S+)(\s+\S+)*))\s*$'
    deleteEpisodePattern2 = r'^\s*(delete)\s+(review)\s+(?P<title>((\S+)(\s+\S+)*))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s*$'
    deleteEpisodePattern3 = r'^\s*(delete)\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<title>((\S+)(\s+\S+)*))\s*$'
    deleteEpisodePattern4 = r'^\s*(delete)\s+(?P<title>((\S+)(\s+\S+)*))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s*$'
    deleteEpisodeReviewPatterns = [deleteEpisodePattern1, deleteEpisodePattern3, deleteEpisodePattern2, deleteEpisodePattern4]
    for pattern in deleteEpisodeReviewPatterns:
        compiled = re.compile(pattern)
        match = compiled.match(toLower)
        if match is not None:
            numDeleted = Review.objects.raw({
                'phone': phone,
                'title': titleFormat(match.group('title')),
                'season': int(match.group('season')),
                'episode': int(match.group('episode'))
            }).delete()
            if numDeleted != 0:
                return 'Review for ' + titleFormat(match.group('title')) + ' s: ' + match.group('season') + ' e: ' + match.group('episode') + ' was deleted'
    
    
    deleteReviewPattern = r'^\s*(delete)\s+(review)\s+(?P<title>((\S+)(\s+\S+)*))\s*$'
    deleteReviewMatch = re.compile(deleteReviewPattern).match(toLower)
    deletePattern = r'^\s*(delete)\s+(?P<title>((\S+)(\s+\S+)*))\s*$'
    deleteMatch = re.compile(deletePattern).match(toLower)
    if deleteReviewMatch is not None:
        numDeleted = Review.objects.raw({
            'phone': phone,
            'title': titleFormat(deleteReviewMatch.group('title'))
        }).delete()
        if numDeleted == 0:
            return 'No reviews were found for ' + titleFormat(deleteReviewMatch.group('title'))
        else:
            return 'Review(s) for ' + titleFormat(deleteReviewMatch.group('title')) + ' were deleted'
    elif deleteMatch is not None:
        numDeleted = Review.objects.raw({
            'phone': phone,
            'title': titleFormat(deleteMatch.group('title'))
        }).delete()
        if numDeleted != 0:
            return 'Review(s) for ' + titleFormat(deleteMatch.group('title')) + ' were deleted'
    
    #check if user entered 'my average of ' or 'average of' for personal average or userbase average
    averageOfPattern = r'^\s*(average)\s+(of)\s+(?P<title>((\S+)(\s+\S+)*))\s*$'
    averageOfMatch = re.compile(averageOfPattern).match(toLower)
    myAverageOfPattern = r'^\s*(my)\s+(average)\s+(of)\s+(?P<title>((\S+)(\s+\S+)*))\s*$'
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
        titleInput = titleFormat(myAverageOfMatch.group('title'))
        result = getMyAverageOf(phone, titleInput)
        if result is not None:
            return result
    
    # check if user typed in tv show with season/episode to retrieve rating
    showPattern1 = r'^\s*(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s+(?P<title>((\S+)(\s+\S+)*))\s*$' # {season} {episode} {tv show name}
    showPattern2 = r'^\s*(?P<title>((\S+)(\s+\S+)*))\s+(?P<season>(\d{1,2}))\s+(?P<episode>(\d{1,2}))\s*$' # {tv show name} {season} {episode}
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
    moviePattern = r'^\s*(?P<title>((\S+)(\s+\S+)*))\s*$' # {movie name} or {show name}
    compiled = re.compile(moviePattern)
    match = compiled.match(body)
    if match is not None:
        titleInput = titleFormat(match.group('title'))
        result = getMyAverageOf(phone, titleInput)
        if result is not None:
            return result
    return None

def getMyAverageOf(phone, titleInput):
    reviews = list(Review.objects.raw({
        'phone': phone,
        'title': titleInput,
        'season': None,
        'episode': None
    }))
    if len(reviews) == 1:
        title = reviews[0].title
        rating = reviews[0].rating
        return 'Your rating for ' + title + ' is ' + str(rating) + '.'

    reviews = list(Review.objects.raw({
        'phone': phone,
        'title': titleInput,
        'season': { '$exists': True},
        'episode': { '$exists': True}
    }))
    if len(reviews) > 0:
        sum = 0.0
        for review in reviews:
            sum += review.rating
        average = sum / len(reviews)
        return 'Your review average for ' + reviews[0].title + ' is ' + str(average) + '.'
    return None;

def formatReviewList(phone, limitBy, timeSort=pymongo.DESCENDING, scoreSort=None):
    qs = Review.objects.raw({
        'phone': phone
    })
    aggregateSort = None
    if scoreSort is None:
        aggregateSort = {'time': timeSort}
    else:
        aggregateSort = {'rating': scoreSort}
    reviews = qs.aggregate(
        {'$sort': aggregateSort},
        {'$limit': limitBy}
    )
    reviewList = list(reviews)
    if reviewList:
        return formatReviews(reviewList)
    else:
        return 'You have no previous reviews.'