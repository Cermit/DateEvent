import QtQuick 1.1
import com.nokia.meego 1.0

import "functions.js" as JS

Page {
    tools: commonTools
    orientationLock: PageOrientation.LockPortrait

    property alias setstartupdatetext: startupdate.text
    property alias setnextontopslider: chronik_slider.checked 
    property alias setdayamountindex: dialog_days.selectedIndex
    property alias setmaxevents: dialog_items.selectedIndex
    property alias daemon_status: daemonbutton.text
    property alias infoDialog: infoDialog
    property alias resetDialog: resetDialog

    Label {
        id: title
        anchors {top: parent.top; topMargin: 20; left: parent.left; leftMargin: 20}
        text: qsTr("DateEvent")
        font.pixelSize: 70
    }

    Rectangle {
        id: headerline_p1
        anchors {top: title.bottom; topMargin: 10 }
        width: mainPage.width
        height: 2
        color: "lightgrey"

    }

    Rectangle {
        id: headerline_p2
        anchors.top: headerline_p1.bottom
        width: mainPage.width
        height: 2
        color: "white"
        }

    Text {
        id: dayamount_title
        anchors {bottom: dayamount_combo.top; bottomMargin: 20; left: parent.left; leftMargin: 20}
        text: qsTr("berücksichtigte Kalendertage:")
        font.pixelSize: 20
    }

    Button {
        id: dayamount_combo
        anchors {top: parent.top; topMargin: 180; horizontalCenter: parent.horizontalCenter}
        text: dialog_days.model.get(dialog_days.selectedIndex).name

        onClicked: {
            dialog_days.open()
        }

        Image {
                source: "image://theme/meegotouch-combobox-indicator"
                anchors {right: parent.right; rightMargin: 15; verticalCenter: parent.verticalCenter}
                }
    }

    Text {
        id: calcombo_title
        anchors {bottom: calendar_combo.top; bottomMargin: 20; left: parent.left; leftMargin: 20}
        text: qsTr("berücksichtigte Kalender:")
        font.pixelSize: 20
    }

    Button {
        id: calendar_combo
        anchors {top: parent.top; topMargin: 300; horizontalCenter: parent.horizontalCenter}
        text: qsTr("Auswahl Kalender")

        onClicked: {
            JS.create_listview_calendar(calendars)
            dialog_calendar.open()
        }

        Image {
                source: "image://theme/meegotouch-combobox-indicator"
                anchors {right: parent.right; rightMargin: 15; verticalCenter: parent.verticalCenter}
                }
    }

    Text {
        id: itemsAmount_title
        anchors {bottom: itemsAmount_combo.top; bottomMargin: 20; left: parent.left; leftMargin: 20}
        text: qsTr("angezeigte Termine:")
        font.pixelSize: 20
    }

    Button {
        id: itemsAmount_combo
        anchors {top: parent.top; topMargin: 420; horizontalCenter: parent.horizontalCenter}
        text: dialog_items.model.get(dialog_items.selectedIndex).name

        onClicked: {            
            dialog_items.open()
        }

        Image {
                source: "image://theme/meegotouch-combobox-indicator"
                anchors {right: parent.right; rightMargin: 15; verticalCenter: parent.verticalCenter}
                }
    }

    Text {
        id: chroniktext
        anchors {top: parent.top; topMargin: 500; left: parent.left; leftMargin: 20}
        text: qsTr("Nächste Termine zuerst zeigen:")
        font {pixelSize: 24}

            Switch {
                id: chronik_slider
                objectName : "chronik_slider"
                anchors {verticalCenter: parent.verticalCenter; left: parent.right; leftMargin: 20}

                onCheckedChanged: {
                    pyfunc.update_next_event_on_top(chronik_slider.checked)
                }
            }
        }

    Button {
        id: daemonbutton
        objectName: "daemonbutton" //for PySide binding
        anchors {top: parent.top; topMargin: 575; horizontalCenter: parent.horizontalCenter}
        text: qsTr("Daemon starten")

        onClicked: {
            if(dialog_calendar.selectedIndexes.length === 0 ){noCalDialog.open()}
        }
    }

    Button {
        id: startupdate
        objectName: "startupdate" //for PySide binding
        anchors {top: parent.top; topMargin: 650; horizontalCenter: parent.horizontalCenter}
        text: qsTr("Start")

        onClicked: {
            if(dialog_calendar.selectedIndexes.length === 0 ){noCalDialog.open()}
            if(startupdate.text == qsTr("Start")){pyfunc.start(dialog_days.selectedIndex); startupdate.text = qsTr("manuelles Update")}
            else{pyfunc.update_feed(dialog_days.selectedIndex)}
            }
    }

    MultiSelectionDialog {
        id: dialog_calendar
        titleText: qsTr("Kalender Auswahl:")
        selectedIndexes: selected_calendars
        acceptButtonText: qsTr("Ok")

        model: ListModel {
            id: calender_listmodel
            //ListElement { name: "Placeholder for Python list element" }
        }

        onAccepted: {
            pyfunc.update_calender_selection(String(dialog_calendar.selectedIndexes))
            }
    }

    SelectionDialog {
        id: dialog_days
        titleText: qsTr("Anzahl Tage:")
        selectedIndex: 0

        model: ListModel {
            id: days_listmodel
            ListElement { name: "1" }
            ListElement { name: "2" }
            ListElement { name: "3" }
            ListElement { name: "4" }
            ListElement { name: "5" }
            ListElement { name: "6" }
            ListElement { name: "7" }
            ListElement { name: "14" }
            ListElement { name: "30" }
            }

        onAccepted: {
            pyfunc.new_dayamount(String(dialog_days.selectedIndex))
        }
    }

    SelectionDialog {
        id: dialog_items
        titleText: qsTr("Anzahl Termine:")
        selectedIndex: 0

        model: ListModel {
            id: items_listmodel
            ListElement { name: "1" }
            ListElement { name: "2" }
            ListElement { name: "3" }
            ListElement { name: "4" }
            ListElement { name: "5" }
            ListElement { name: "7" }
            ListElement { name: "10" }
}

        onAccepted: {
            pyfunc.update_show_events_max(String(dialog_items.selectedIndex))
            }
    }

    QueryDialog {
        id: infoDialog
        titleText: qsTr("Information")
        message: qsTr("Diese Anwendung wurde von Boris Pohler und Gabriel Böhme entwickelt und sie steht unter der GPL3 Lizenz.")
        acceptButtonText: qsTr("Ok")

        onAccepted: {
            infoDialog.close()
            }
        }

    QueryDialog {
        id: resetDialog
        titleText: qsTr("Achtung!")
        message: qsTr("Möchtest du den Termin-Feed wirklich beenden?")
        acceptButtonText: qsTr("Ja")
        rejectButtonText: qsTr("Nein")

        onAccepted: {
            pyfunc.delete_feed(); mainPage.setstartupdatetext = qsTr("Start")
        }

        onRejected: {
            infoDialog.close()
        }
    }

    QueryDialog {
        id: noCalDialog
        titleText: qsTr("Warnung!")
        message: qsTr("Im Moment ist kein Kalender ausgewählt, der angezeigt werden kann.")
        acceptButtonText: qsTr("Jetzt wählen")
        rejectButtonText: qsTr("Abbrechen")

        onAccepted: {
            noCalDialog.close()
            dialog_calendar.open()
        }
    }
    }
