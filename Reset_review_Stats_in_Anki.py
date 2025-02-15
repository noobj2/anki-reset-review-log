#// auth_ Mohamad Janati
#// AmirHassan Asvadi ;)
#// Modified by Nolan Games
#// Copyright (c) 2020 Mohamad Janati (freaking stupid, right? :|)

from aqt import mw
from aqt.utils import showInfo, askUser
from aqt.qt import *

from time import mktime,time
from datetime import datetime
from os.path import dirname

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

def time_window():
    addon_path = dirname(__file__)
    decks = mw.col.decks.all()
    window = QDialog()
    window.setWindowTitle("Delete revlog")
    window.setWindowIcon(QIcon(addon_path + "/icon.png"))
    delete_button = QPushButton("Delete")
    for_label = QLabel("Review log for all cards in")
    deck = QComboBox()
    deck.addItem('Whole Collection', 'collection')
    did_list = []
    for item in decks:
        deck_name = item["name"]
        deck_id = item["id"]
        deck.addItem(deck_name, deck_id)
        did_list.append(deck_id)
    from_label = QLabel("Reviewed from")
    from_date = QDateTimeEdit()
    from_date.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
    from_date.setMinimumDate(QDate(2006, 10, 5))
    from_date.setDate(QDate.currentDate().addDays(-10))
    from_date.setCalendarPopup(True)
    to_label = QLabel("to")
    to_date = QDateTimeEdit()
    to_date.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
    to_date.setMinimumDate(QDate(2006, 10, 5))
    to_date.setDate(QDate.currentDate())
    to_date.setCalendarP