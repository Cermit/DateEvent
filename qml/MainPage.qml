import QtQuick 1.1
import com.nokia.meego 1.0

import "functions.js" as JS

Page {
    tools: commonTools

    property alias setstartupdatetext: startupdate.text
    property alias setdayamountindex: dialog_days.selectedIndex

    Label {
        id: title
        text: "CalEvents"
        anchors.top: parent.top
        anchors.topMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: 20

        font.pixelSize: 70
    }

    Text {
        id: dayamount_title
        text: "Anzahl anzuzeigender Tage:"
        anchors.bottom: dayamount_combo.top
        anchors.bottomMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: 20

        font.pixelSize: 20
    }

    Button {
        id: dayamount_combo
        anchors.top: parent.top
        anchors.topMargin: 200
        anchors.horizontalCenter: parent.horizontalCenter

        text: "Tage"

        onClicked: {
            dialog_days.open()
        }
    }

    Text {
        id: calcombo_title
        text: "Anzahl anzuzeigender Kalender:"
        anchors.bottom: calendar_combo.top
        anchors.bottomMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: 20

        font.pixelSize: 20
    }

    Button {
        id: calendar_combo
        anchors.top: parent.top
        anchors.topMargin: 400
        anchors.horizontalCenter: parent.horizontalCenter

        text: "Kalender"

	//enabled: false

        onClicked: {
            JS.createListView(calendars)
            dialog_calendar.open()
        }
    }

    Button {
        id: startupdate
        objectName: "startupdate"

        anchors.top: parent.top
        anchors.topMargin: 600
        anchors.horizontalCenter: parent.horizontalCenter
        enabled: true

        text: "Start"

        onClicked: {
	    if(startupdate.text == "Start"){pyfunc.start(dialog_days.selectedIndex); startupdate.text = "Update"}
	    else{pyfunc.update_feed(dialog_days.selectedIndex)}
	    
	    pyfunc.new_dayamount(String(dialog_days.selectedIndex))
        }
    }

    MultiSelectionDialog {
        id: dialog_calendar
        titleText: "Kalender Auswahl"

        selectedIndexes: selected_calendars
        //selectedIndexes: []
        acceptButtonText: "Ok"

        model: ListModel {
            id: calender_listmodel
            //ListElement { name: "Persönlich" }
            //ListElement { name: "Studium" }
            //ListElement { name: "Arbeit" }
        }

        onAccepted: {
            console.log(dialog_calendar.selectedIndexes)
            pyfunc.update_calender_selection(String(dialog_calendar.selectedIndexes))
            }
    }

    SelectionDialog {
        id: dialog_days
        titleText: "Kalender Auswahl"

        selectedIndex: -1

        model: ListModel {
            id: days_listmodel
            ListElement { name: "1 Tag" }
            ListElement { name: "2 Tage" }
            ListElement { name: "3 Tage" }
            ListElement { name: "4 Tage" }
            ListElement { name: "5 Tage" }
            ListElement { name: "6 Tage" }
            ListElement { name: "7 Tage" }
            ListElement { name: "14 Tage" }
            ListElement { name: "30 Tage" }
        }
    }
}
