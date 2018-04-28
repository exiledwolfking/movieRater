from dbClasses import *
from datetime import datetime
import re

def saveHistory(textNumber, textBody):
    History(
        phone=textNumber,
        content=textBody,
        time=datetime.now()
    ).save()