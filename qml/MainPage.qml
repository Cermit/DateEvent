import QtQuick 1.1
import com.nokia.meego 1.0
import "functions.js" as JS

Page {
    tools: commonTools

    property alias setstartupdatetext: startupdate.text
    property alias setdayamountindex: dialog_days.selectedIndex

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
        text: qsTr("Anzahl Kalendertage:")
        font.pixelSize: 20
    }

    Button {
        id: dayamount_combo
        anchors {top: parent.top; topMargin: 200; horizontalCenter: parent.horizontalCenter}
        text: qsTr("Auswahl Tage")

        onClicked: {
            dialog_days.open()
        }
    }

    Text {
        id: calcombo_title
        anchors {bottom: calendar_combo.top; bottomMargin: 20; left: parent.left; leftMargin: 20}
        text: qsTr("Auswahl Kalender:")
        font.pixelSize: 20
    }

    Button {
        id: calendar_combo
        anchors {top: parent.top; topMargin: 350; horizontalCenter: parent.horizontalCenter}
        text: qsTr("Auswahl Kalender")

        onClicked: {
            JS.createListView(calendars)
            dialog_calendar.open()
        }
    }

    Text {
        id: chroniktext
        anchors {top: parent.top; topMargin: 450; left: parent.left; leftMargin: 20}
        text: qsTr("Nächste Termine zuerst zeigen:")
        font {pixelSize: 24}

            Switch {
                id: chronik_slider
                anchors {verticalCenter: parent.verticalCenter; left: parent.right; leftMargin: 20}
                checked: true
            }
        }

    Button {
        id: startupdate
        objectName: "startupdate" //for PySide binding
        anchors {top: parent.top; topMargin: 600; horizontalCenter: parent.horizontalCenter}
        text: qsTr("Start")

        onClicked: {
            if(startupdate.text == qsTr("Start")){pyfunc.start(dialog_days.selectedIndex); startupdate.text = qsTr("manuelles Update")}
	    else{pyfunc.update_feed(dialog_days.selectedIndex)}
	    
	    pyfunc.new_dayamount(String(dialog_days.selectedIndex))
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
