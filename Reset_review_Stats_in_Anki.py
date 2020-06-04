#// auth_ Mohamad Janati
#// AmirHassan Asvadi ;)
#// Copyright (c) 2020 Mohamad Janati (freaking stupid, right? :|)

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, askUser
# import all of the Qt GUI library
from aqt.qt import *

from time import mktime,time
from datetime import datetime

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)

def epochTodayMidnight():
	n = datetime.now()
	midnight = datetime(n.year, n.month, n.day)
	return mktime(midnight.timetuple())

def deleteRevlog(timeinfo):
#    showInfo("TIME: %d %d" % (timeinfo * 1000, time() * 1000))
	mw.col.db.execute("delete from revlog where id > ?", timeinfo * 1000)

def resetYearAgo():
    reset = askUser("Are you sure you want to delete review history for all cards reviewed in past year? This can't be undone.")
    if reset:
        deleteRevlog(epochTodayMidnight() - DAY*365)
    else:
        return

def resetMonthAgo():
    reset = askUser("Are you sure you want to delete review history for all cards reviewed in past month? This can't be undone.")
    if reset:
        deleteRevlog(epochTodayMidnight() - DAY*30)
    else:
        return

def resetThreeWeeksAgo():
    reset = askUser("Are you sure you want to delete review history for all cards reviewed in past three weeks? This can't be undone.")
    if reset:
        deleteRevlog(epochTodayMidnight() - DAY*21)
    else:
        return

def resetTwoWeeksAgo():
    reset = askUser("Are you sure you want to delete review history for all cards reviewed in past two weeks? This can't be undone.")
    if reset:
        deleteRevlog(epochTodayMidnight() - DAY*14)
    else:
        return

def resetOneWeekAgo():
    reset = askUser("Are you sure you want to delete review history for all cards reviewed in past week? This can't be undone.")
    if reset:
        deleteRevlog(epochTodayMidnight() - DAY*7)
    else:
        return

def resetYesterday():
    reset = askUser("Are you sure you want to delete review history for all cards reviewed in yesterday? This can't be undone.")
    if reset:
        deleteRevlog(epochTodayMidnight() - DAY)
    else:
        return

def resetToday():
    reset = askUser("Are you sure you want to delete review history for all cards reviewed in today? This can't be undone.")
    if reset:
        deleteRevlog(epochTodayMidnight())
    else:
        return

def resetLastHour():
    reset = askUser("Are you sure you want to delete review history for all cards reviewed in past hour? This can't be undone.")
    if reset:
        deleteRevlog(time() - HOUR)
    else:
        return


# Day in seconds
DAY = 86400
# Hour in seconds
HOUR = 3600

# Create menu Reset Study
resetStudy = mw.form.menuTools.addMenu("Reset Study")
resetLastHourAction = resetStudy.addAction("Last hour")
resetTodayAction = resetStudy.addAction("Today")
resetYesterdayAction = resetStudy.addAction("Yesterday")
resetOneWeekAction = resetStudy.addAction("One Week")
resetTwoWeeksAction = resetStudy.addAction("Two Weeks")
resetThreeWeeksAction = resetStudy.addAction("Three Weeks")
resetMonthAction = resetStudy.addAction("A month ago")
resetYearAction = resetStudy.addAction("A year ago")

# Connect actions to functions
resetLastHourAction.triggered.connect(resetLastHour)
resetTodayAction.triggered.connect(resetToday)
resetOneWeekAction.triggered.connect(resetYesterday)
resetTwoWeeksAction.triggered.connect(resetOneWeekAgo)
resetThreeWeeksAction.triggered.connect(resetTwoWeeksAgo)
resetThreeWeeksAction.triggered.connect(resetThreeWeeksAgo)
resetMonthAction.triggered.connect(resetMonthAgo)
resetYearAction.triggered.connect(resetYearAgo)


# # create a new menu item, "test"
# action = QAction("test", mw)
# # set it to call testFunction when it's clicked
# action.triggered.connect(testFunction)
# # and add it to the tools menu
# mw.form.menuTools.addAction(action)
