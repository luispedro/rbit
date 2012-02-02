import QtQuick 1.0

Rectangle {
    width: 1280
    height: 768
    Rectangle {
        id: mailboxlist
        width: 256
        height: 768
        Text {
            anchors { top: parent.top; left: parent.left }
            text: "Mailboxes"
            font {
                bold: true
            }
        }
        border {
            width: 2
            color: Qt.black
        }

    }

    Rectangle {
        id: messagelist
        width: 1024
        height: 256
        anchors { top: parent.top; left: mailboxlist.right }
        Text {
            text: "Messages"
        }
    }
    Rectangle {
        id: message
        width: 1024
        height: 1280-256
        anchors { top: messagelist.bottom; left: mailboxlist.right }
        Rectangle {
            id: header
            width: 1024
            height: 64
            color: "#dd0000"
            visible: true
            anchors.top: parent.top
            Text {
                id: subject
                text: "Subject"
                font {
                    bold: true
                }
            }
        }
        Rectangle {
            id: messagetextcont
            width: parent.width
            height: parent.height - header.height
            anchors { top: header.bottom; left: parent.left }
            Text {
                id: messagetext
                text: "From me to you"
            }
        }
    }

    MouseArea {
        x: 424
        y: 37
        drag.minimumY: -1000
        drag.minimumX: -1000
        drag.maximumY: 1000
        drag.maximumX: 1000
        anchors.rightMargin: -424
        anchors.bottomMargin: -37
        anchors.leftMargin: 424
        anchors.topMargin: 37
        anchors.fill: parent
        onClicked: {
            Qt.quit();
        }
    }
}
