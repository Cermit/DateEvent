#!/usr/bin/env python
#-*- coding: utf-8 -*-

# just for testing with qtmobiliy-organizer

import sys
from QtMobility.Organizer import *
from PySide import QtCore
from PySide.QtCore import QDateTime, QDate, QTime


class QtMobilityTest(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        # Manager hat alle collections
        self.defaultManager = QOrganizerManager()
        self.collections = self.defaultManager.collections()
        # Kontrolle
        print len(self.collections)

        # Infos über collections mit metaData(), für alle Meta-Daten einfach nur metaData() aufrufen
        for collection in self.collections:
            print collection.metaData('Color'), collection.metaData('Name')

        # Filter erzeugen und mit ausgewählten Collections bestücken, hier über Namen
        self.collectionFilter = QOrganizerItemCollectionFilter()
        for collection in self.collections:
            if collection.metaData()['Name'] == u'Nokia N900':
                self.collectionFilter.setCollectionId(collection.id())
  
        now = QDateTime.currentDateTime()
        days_ahead = 150
        # ohne Filter liefert alle collection-einträge
        #self.items = self.defaultManager.items(now,now.addDays(days_ahead))

        # mit Filter nur die aus dem N900 Kalender
        self.items = self.defaultManager.items(now,now.addDays(days_ahead),self.collectionFilter)

        # Items je nach Typ umwandeln und Eigenschaften ausgeben lassen
        for item in self.items:
            if item.type() == 'Todo':
                todo = QOrganizerTodo(item)
                print (todo.dueDateTime().toString("dd.MM.yyyy hh:mm:ss"),
                       todo.displayLabel()) 
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
                       event.location(),
                       event.id())
        sys.exit(0)

if __name__ == "__main__":
    app = QtCore.QCoreApplication([])
    test = QtMobilityTest()
    app.exec_()
