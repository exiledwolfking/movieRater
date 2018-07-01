#!/usr/bin/python

import consts
from dbClasses import *
from pymodm import connect
import datetime

import logging
logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s')
rootLogger = logging.getLogger()

filePath = consts.PATH + "/cronErrors.log"
fileHandler = logging.FileHandler(filePath)
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
    logPath = consts.PATH + "/cronLog.log"
    file = open(logPath, "w+")
    file.write("calculateAverages start: " + datetime.datetime.now().strftime("%d %B %Y %I:%M:%S"))

    # calculate movie averages and save
    movieReviews = Review.objects.raw({'season': None, 'episode': None})
    movieResults = movieReviews.aggregate(
        { '$group': { '_id': '$title', 'average': { '$avg': '$rating'}}})

    averages = []
    for avg in movieResults:
        Average(
            title=avg['_id'],
            average=avg['average']
        ).save()
        
    # calculate tv show averages and save
    tvReviews = Review.objects.raw({'season': { '$ne': None}, 'episode': { '$ne': None}})
    tvResultsPerUser = tvReviews.aggregate(
        {
            '$group': {
                '_id': {
                    'phone': '$phone',
                    'title': '$title'
                },
                'userAvg': {
                    '$avg': '$rating'
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'phone': '$_id.phone',
                'title': '$_id.title',
                'userAvg': True
            }
        }, {
            '$group': {
                '_id': {
                    'title': '$title'
                },
                'totalAvg': {
                    '$avg': '$userAvg'
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'title': '$_id.title',
                'totalAvg': True
            }
        }
    )

    averages = []
    for avg in tvResultsPerUser:
        Average(
            title=avg['title'],
            average=avg['totalAvg']
        ).save()
        
    file.write("\ncalculateAverages end: " + datetime.datetime.now().strftime("%d %B %Y %I:%M:%S"))
    file.close()

except Exception as e:
    rootLogger.error('calculateAverages ' + str(e))

