#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from QtMobility.Organizer import *
from PySide import QtCore
from PySide.QtCore import QDateTime, QDate, QTime


class QtMobilityTest(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.defaultManager = QOrganizerManager()
        now = QDateTime.currentDateTime()
        days_ahead = 30
        self.items = self.defaultManager.items(now,now.addDays(days_ahead))

        for item in self.items:
            if item.type() == 'EventOccurrence':
                occurrence = QOrganizerEventOccurrence(item)
                print (occurrence.startDateTime().toString("dd.MM.yyyy hh:mm:ss"),
                       occurrence.endDateTime().toString("dd.MM.yyyy hh:mm:ss"), 
                       occurrence.displayLabel(), 
                       occurrence.location()) 
            if item.type() == 'Event':
                event = QOrganizerEvent(item)
                print (event.startDateTime().toString("dd.MM.yyyy hh:mm:ss"), 
                       event.endDateTime().toString("dd.MM.yyyy hh:mm:ss"),
                       event.displayLabel(),
                       event.location())
        sys.exit(0)

if __name__ == "__main__":
    app = QtCore.QCoreApplication([])
    test = QtMobilityTest()
    app.exec_()
