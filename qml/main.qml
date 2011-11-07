import QtQuick 1.1
import com.nokia.meego 1.0

PageStackWindow {
    id: appWindow 
    initialPage: mainPage

    function set_startupdate(str) {
        if (str === "True"){mainPage.setstartupdatetext = qsTr("Start")}
        else {mainPage.setstartupdatetext = qsTr("manuelles Update")}
		}

    function set_dayamount(number) {
	mainPage.setdayamountindex = number
	}

    MainPage {
        id: mainPage
    }

    ToolBarLayout {
        id: commonTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (myMenu.status == DialogStatus.Closed) ? myMenu.open() : myMenu.close()
        }
    }

    Menu {
        id: myMenu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: qsTr("Feed beenden"); onClicked: {mainPage.resetDialog.open()}}
            MenuItem { text: qsTr("Information"); onClicked: mainPage.infoDialog.open() }
            }
        }
    }
