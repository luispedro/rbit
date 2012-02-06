import QtQuick 1.0
import QtDesktop 0.1

Window {
    width: 1280
    height: 768
    title: "Rbit Mail"
    visible: true
    MenuBar {
        Menu {
            text: "File"
            MenuItem {
                text: "Open"
                shortcut: "Ctrl+O"
            }
            MenuItem {
                text: "Close"
                shortcut: "Ctrl+Q"
                onTriggered: Qt.quit()
            }
        }
        Menu {
            text: "Edit"
            MenuItem {
                text: "Copy Message"
            }
            MenuItem {
                id: paste_menuitem
                text: "Paste Message"
            }
        }
        Menu {
            text: "Help"
            MenuItem {
                text: "Help"
            }
        }
    }

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
            color: "#ffffff"
        }

    }

    Rectangle {
        id: messagelistcontainer
        width: 1024
        height: 256
        anchors { top: parent.top; left: mailboxlist.right }
        ListView {
            id: messagelist
            objectName: "messagelist"
            anchors {
                fill: parent
                margins: 5
            }

            model: iMessages
            delegate: Item {
                width: 256
                height: 48
                Row { Column {
                    Text { text: ("<b><i>"+from+"</i>:: "+subject+"</b>") }
                    Text { text: first }
                } }
            }
        }
    }
    Rectangle {
        id: message
        width: 1024
        height: 1280-256
        anchors { top: messagelistcontainer.bottom; left: mailboxlist.right }
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

}
