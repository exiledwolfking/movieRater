from helperFunctions import isfloat, titleFormat
from dbClasses import *
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
            