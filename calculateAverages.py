import consts
from dbClasses import *
from pymodm import connect

import logging
logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s')
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler('cronErrors.log')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


connect(
    consts.CONNECTION_STR,
    alias='my-atlas-app'
)

try:

    # calculate movie averages and save
    movieReviews = Review.objects.raw({'season': None, 'episode': None})
    movieResults = movieReviews.aggregate(
        { '$group': { '_id': '$title', 'average': { '$avg': '$rating'}}})

    averages = []
    for avg in movieResults:
        print(avg)
        Average(
            title=avg['_id'],
            average=avg['average']
        ).save()
        
    # calculate tv show averages and save
    tvReviews = Review.objects.raw({'season': { '$exists': True}, 'episode': { '$exists': True}})
    tvResults = tvReviews.aggregate(
        { '$group': { '_id': '$phone', '$project': '$title'}})

    averages = []
    for avg in tvResults:
        print(avg)

except Exception as e:
    rootLogger.error('calculateAverages ' + str(e))

