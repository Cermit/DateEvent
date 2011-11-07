#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
if os.path.exists('/usr/share/dateevent'):
    sys.path.append("/usr/share/dateevent")
import ConfigParser
# kann raus, wenn config läuft
import pickle
import subprocess
import dbus
import dbus.mainloop.glib
from sqlite3 import *
from time import time
from datetime import datetime
from eventfeed import EventFeedService, EventFeedItem
from PySide import QtCore
from PySide.QtCore import Qt
from PySide import QtGui
from PySide import QtDeclarative

#OpenGL Rendering
from PySide import QtOpenGL

class CalEvent(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        #Oberfläche und Instanzierungen für QML2Py Funktionen
        self.view = QtDeclarative.QDeclarativeView()

        #OpenGL Rendering
        self.glw = QtOpenGL.QGLWidget()
        self.view.setViewport(self.glw)

        if os.path.exists('/usr/share/dateevent/qml'):
             self.view.setSource('/usr/share/dateevent/qml/main.qml')
        else:
             self.view.setSource(os.path.join('qml','main.qml'))

        self.root = self.view.rootObject()

        # set data
        self.all_calendars = self.get_calendars()
        self.calendar_names = self.get_calendar_names(self.all_calendars)
        self.calendar_ids = self.get_calendar_ids(self.all_calendars)
        self.choice_days_ahead = ['1','2','3','4','5','6','7','14','30']
        self.choice_show_max_events = ['1','2','3','4','5','unbegrenzt']
        #instantiate the Python object
	self.pyfunc = pyfunc()

	# Reagiert auf UpdateButton und ruft Klasse auf,
	# welche die gewählte Tageszahl speichert
	self.pyfunc.new_dayamount.connect(self.new_dayamount)

        # reagiert auf onAccepted des MultiSelectionDialogs
        self.pyfunc.update_calender_selection.connect(self.new_cal_selection)

	# reagiert auf drücken des "Start"/"Update" Buttons und bindet an
	self.pyfunc.start.connect(self.start)

	# reagiert (nur) auf Update-Button - aktualisiert den Feed!
	self.pyfunc.update_feed.connect(self.update_feed) 

	#löscht den Termine-Feed
	self.pyfunc.delete_feed.connect(self.delete_feed)

	# Config stuff
        self.config = ConfigParser.ConfigParser()
        if os.path.exists(os.path.expanduser('~/.config/dateevent.cfg')):
            self.readconf()
            # startbutton "manuelles Update" in QML
            self.root.set_startupdate("False")
        else:
            self.defaultconf()
            self.readconf()
            # startbutton "Start" in QML
            self.root.set_startupdate("True")
        
        #expose the object to QML
	self.context = self.view.rootContext()
	self.context.setContextProperty("pyfunc", self.pyfunc)
        self.context.setContextProperty("calendars", self.calendar_names)
        self.context.setContextProperty("selected_calendars", self.selected_calendars)
        self.context.setContextProperty("next_event_on_top", self.next_event_on_top)
        self.context.setContextProperty("show_events_max", self.show_events_max)
        self.context.setContextProperty("choice_days_ahead", self.choice_days_ahead)
        self.context.setContextProperty("choice_show_max_events", self.choice_show_max_events)
        self.root.set_dayamount(self.selected_dayamount)
        
        #dbus
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus()
        try:
            # Get the remote object
            self.remote_object = self.bus.get_object("org.freedesktop.Tracker1",
                                       "/org/freedesktop/Tracker1/Resources")
            # Get the remote interface for the remote object
            self.iface = dbus.Interface(self.remote_object, "org.freedesktop.Tracker1.Resources")
        except dbus.DBusException:
            print_exc()
            sys.exit(1)
                
        self.iface.connect_to_signal("GraphUpdated", self.calendar_db_changed)

#-------------------------------------------------------------------------
# config-methods
    def defaultconf(self):
            self.config.add_section('General')
            self.config.set('General', 'selected_dayamount', '2')
            self.config.set('General', 'selected_calendars', [])
            self.config.set('General', 'next_event_on_top', 'True')
            self.config.set('General', 'show_events_max', '5')
            self.save_config()      

    def readconf(self):
            self.config.readfp(open(os.path.expanduser(
                               '~/.config/dateevent.cfg'), 'rwb'))
            self.selected_dayamount = int(self.config.get('General', 
                                                      'selected_dayamount'))
            self.selected_calendars = list(eval(self.config.get('General', 
                                                      'selected_calendars')))
            self.next_event_on_top = eval(self.config.get('General',
                                                     'next_event_on_top'))
            self.show_events_max = int(self.config.get('General', 
                                                      'show_events_max'))

    def save_config(self):
        with open(os.path.expanduser('~/.config/dateevent.cfg'), 'wb') as configfile:
            self.config.write(configfile)      
#----------------------------------------------------------------------------

    def delete_feed(self):
        service = EventFeedService('dateevent', 'DateEvent')
	service.remove_items()

    def calendar_db_changed(self, arg1, arg2, arg3):
        if arg1 =='http://www.semanticdesktop.org/ontologies/2007/04/02/ncal#Event':
            print "kalender-db verändert, update event-screen"
            self.update_feed(6)

           
    #Speichert geänderte Werte bei der Anzahl der Tage
    def new_dayamount(self, new_dayamount):
        self.selected_dayamount = int(new_dayamount) 
        self.config.set('General', 'selected_dayamount', new_dayamount)
        self.save_config()

    def new_cal_selection(self, indexes_selected_calendars):
        if indexes_selected_calendars:
            if len(indexes_selected_calendars) == 1:
                self.selected_calendars = [int(indexes_selected_calendars)]
            else:
                self.selected_calendars = eval(indexes_selected_calendars)
        else:
            self.selected_calendars = []
        self.config.set('General', 'selected_calendars', self.selected_calendars)
        self.save_config()

	#Vielleicht unnötig! :)
    def start(self, new_dayamount):
	self.get_events(new_dayamount, self.selected_calendars, self.show_events_max)

    def get_calendars(self):
        # verbindung zur sqlite-db
        conn = connect("/home/user/.calendar/db")
        curs = conn.cursor()
        # SQL-Abfrage für alle Kalender 
	query_calendars = "SELECT CalendarId,Name,Color\
                           FROM Calendars\
                           WHERE modifiedDate > 1306879230"
        # SQL-Abfrage durchführen und Ergebnisse ausgeben
        curs.execute(query_calendars)
        all_calendars = curs.fetchall()
        conn.close()
        return all_calendars

    def get_calendar_names(self,calendarlist):
        calendar_names = []
        for calId, name, color in calendarlist:
            calendar_names.append(name)
        return calendar_names

    def get_calendar_ids(self,calendarlist):
        calendar_ids = []
        for calId, name, color in calendarlist:
            calendar_ids.append(calId)
        print "cal-ids:"
        print calendar_ids
        return calendar_ids

    def get_events(self, dayamount, calendar_ids, show_events_max):
	# verbindung zur sqlite-db
	conn = connect("/home/user/.calendar/db")
	curs = conn.cursor()
	# nächsten tage, die abgefragt werden sollen
	days_ahead = int(self.choice_days_ahead[int(dayamount)])
        print show_events_max
        # calendars
        selected_calender = [self.all_calendars[i][0] for i in calendar_ids]
        selected_calender = unicode("','".join(selected_calender))
	# unix zeit von heute 
	unixtime_now = int(time())
	unixtime_in_days_ahead = unixtime_now + days_ahead*86400

	# SQL-Abfrage der Events nur für die ausgewählten Kalender
        # zweite Datestartabfrage für die faketime
	query_events = "SELECT Summary, Location, DateStart, Notebook, DateStart FROM Components \
               		WHERE DateStart BETWEEN {0} AND {1}\
               		AND Notebook in ('{2}')\
               		AND DateDeleted = '0'".format(unixtime_now,
                                                      unixtime_in_days_ahead,
                                                      selected_calender)
	curs.execute(query_events)
	all_events = curs.fetchall()
        print all_events

        if self.next_event_on_top:
            all_events = self.change_events_timeline(all_events)

	for summary, location, datestart, cal, faketime in all_events[:show_events_max]:
            calId = self.calendar_ids.index(cal)
            faketime = datetime.fromtimestamp(faketime)
            datestart = datetime.fromtimestamp(datestart)
            day = int(str(datestart)[8:10])	
            self.feeder(summary, location, faketime, day, calId)
        # Verbindung zur DB beenden
	conn.close()

    def change_events_timeline(self, events):
        events = sorted(events, key = lambda event: event[2])
        time_last_event = events[-1][2]
        for i, event in enumerate(events):
            events[i] = list(event)
            time_event = event[2]
            days_delta = (time_last_event - time_event)/86400
            faketime = time_event + days_delta * 86400 + (len(events)-i)*86400
            events[i][4] = faketime
        return events

#--------------------------------------------------------------------------------------------------

    def feeder(self, summary, location, datestart, day, calId):
        calendarname = self.all_calendars[calId][1]
        calendarcolor = self.all_calendars[calId][2]

        service = EventFeedService('dateevent', 'DateEvent')

        if os.path.exists('/usr/share/dateevent/img'):
             icon = '/usr/share/dateevent/img/icon-l-calendar-{0}.png'.format(day)
        else:
             icon = '/home/user/MyDocs/dateevent/img/icon-l-calendar-{0}.png'.format(day)
	
        item = EventFeedItem(icon,
               u'Termin aus Kalender: <font color="{0}">{1}</font>'.format(calendarcolor,calendarname),
               datestart) 
        #gültiger Timestamp: datetime.datetime(2011, 11, 02, 8, 30, 0, 0)		
        item.set_body(summary)
	item.set_footer(location)
		
	item.set_custom_action(self.on_item_clicked)
	service.add_item(item)

#--------------------------------------------------------------------------------------------------

    def update_feed(self, dayamount):
        print "machen wir mal nur ein Update!"		
        service = EventFeedService('dateevent', 'DateEvent')
        service.remove_items()
        self.get_events(dayamount,self.selected_calendars, self.show_events_max)

#--------------------------------------------------------------------------------------------------

	# Muss ausgelagert werden in den zukünftigen "Deamon",
	# sonst wird es logischer Weise mit beendet - dann gibt es keine Reaktion mehr!
    def on_item_clicked(self):
        print 'the user clicked the item'
        subprocess.Popen(['/usr/bin/organiser'])

#--------------------------------------------------------------------------------------------------

# Klasse für Funktionen die aus QML heraus angesprochen werden sollen:
class pyfunc(QtCore.QObject):
    start = QtCore.Signal(str)
    delete_feed = QtCore.Signal()
    new_dayamount = QtCore.Signal(str)
    update_calender_selection = QtCore.Signal(str)
    update_feed = QtCore.Signal(str)

    def __init__(self):
        QtCore.QObject.__init__(self)

#Starten der App
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    start = CalEvent()
    start.view.showFullScreen()
    sys.exit(app.exec_())

