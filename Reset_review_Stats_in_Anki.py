"""
Author: Mohamad Janati
Contributors: AmirHassan Asvadi, Nolan Games, Aneeq Weerasinghe
Copyright: 2020 Mohamad Janati
"""

from aqt import mw
from aqt.utils import ask_user, showInfo
from aqt.qt import *
from datetime import datetime
from os.path import dirname
from time import mktime, time

# Constants


DAY = 86400
HOUR = 3600

# Generic functions


def epoch_today_midnight():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day)
    return mktime(midnight.timetuple())


def delete_revlog(start_epoch):
    """Delete review logs after a given epoch timestamp (in seconds)."""
    mw.col.db.execute("DELETE FROM revlog WHERE id > ?", start_epoch * 1000)


def reset_period(seconds_ago, label):
    """Generic function to delete logs for a period ago."""
    reset = ask_user(
        f"Are you sure you want to delete review history for all cards reviewed in {label}? This can't be undone."
    )
    if reset:
        delete_revlog(epoch_today_midnight() - seconds_ago)


# UI for custom date range


def time_window():
    addon_path = dirname(__file__)
    decks = mw.col.decks.all()

    window = QDialog()
    window.setWindowTitle("Delete revlog")
    window.setWindowIcon(QIcon(addon_path + "/icon.png"))

    delete_button = QPushButton("Delete")
    deck_label = QLabel("Review log for all cards in")
    deck_combo = QComboBox()
    deck_combo.addItem("Whole Collection", "collection")

    for item in decks:
        deck_combo.addItem(item["name"], item["id"])
    from_label = QLabel("Reviewed from")
    from_date = QDateTimeEdit()
    from_date.setMinimumDate(QDate(2006, 10, 5))
    from_date.setDate(QDate.currentDate().addDays(-10))
    from_date.setCalendarPopup(True)

    to_label = QLabel("to")
    to_date = QDateTimeEdit()
    to_date.setMinimumDate(QDate(2006, 10, 5))
    to_date.setDate(QDate.currentDate())
    to_date.setCalendarPopup(True)

    delete_button.clicked.connect(
        lambda: custom_reset(deck_combo, from_date.dateTime(), to_date.dateTime())
    )

    layout = QHBoxLayout()
    layout.addWidget(delete_button)
    layout.addWidget(deck_label)
    layout.addWidget(deck_combo)
    layout.addWidget(from_label)
    layout.addWidget(from_date)
    layout.addWidget(to_label)
    layout.addWidget(to_date)
    window.setLayout(layout)

    window.exec()


def custom_reset(deck_combo, from_dt, to_dt):
    """Delete revlog entries for a custom deck and date range."""
    deck_filter = ""
    if deck_combo.currentData() != "collection":
        deck_filter = (
            f"AND cid IN (SELECT id FROM cards WHERE did = {deck_combo.currentData()})"
        )
    reset = ask_user(
        f'Are you sure you want to delete review history for all cards in "{deck_combo.currentText()}" '
        f'reviewed from "{from_dt.toString("MM/dd/yyyy")}" to "{to_dt.toString("MM/dd/yyyy")}"? '
        "This can't be undone."
    )

    if reset:
        mw.col.db.execute(
            "DELETE FROM revlog WHERE ? > id AND id > ? {}".format(deck_filter),
            (to_dt.toSecsSinceEpoch() * 1000, from_dt.toSecsSinceEpoch() * 1000),
        )
        showInfo("Done")


# Menu setup


reset_study = mw.form.menuTools.addMenu("Reset Study")

# Map labels to seconds


periods = {
    "Last hour": HOUR,
    "Today": 0,
    "Yesterday": DAY,
    "One Week": 7 * DAY,
    "Two Weeks": 14 * DAY,
    "Three Weeks": 21 * DAY,
    "A month ago": 30 * DAY,
    "A year ago": 365 * DAY,
}

for label, seconds in periods.items():
    action = reset_study.addAction(label)
    if label == "Today":
        action.triggered.connect(lambda s=seconds: reset_period(0, "today"))
    else:
        action.triggered.connect(lambda s=seconds, l=label: reset_period(s, l))
# Custom date range


custom_action = reset_study.addAction("Custom")
custom_action.triggered.connect(time_window)
