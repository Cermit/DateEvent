import QtQuick 1.1
import com.nokia.meego 1.0

PageStackWindow {
    id: appWindow
    initialPage: mainPage

    function set_startupdate(str) {
	if (str === "True"){mainPage.setstartupdatetext = "Start"}
	else {mainPage.setstartupdatetext = "Update"}
		}

    function set_dayamount(number) {
	console.log(number)
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
            MenuItem { text: qsTr("Feed beenden"); onClicked: {pyfunc.deleter(); mainPage.setstartupdatetext = "Start"} }
	    MenuItem { text: qsTr("Information") }
        }
    }
}
