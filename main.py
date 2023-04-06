import json
import subprocess
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pyperclip
from pynput import keyboard, mouse

mouse_controller = mouse.Controller()

with open("assets/emojis.json") as f:
    emojis = json.load(f)

categories = {
    "Gestures": "1",
    "Emojis": "2",
    "Objects": "3",
    "Food": "4",
    "Places": "5",
    "Love": "6",
    "Flags": "7",
    "Other": "8",
    "New": "9"
}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        subprocess.Popen(["notify-send", "Mint Emojis now running in the background.\n\nCTRL+Shift+E to open the menu."])
        super().__init__(None, QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool))
        self.setWindowState(QtCore.Qt.WindowMinimized)
        self.show()
        self.setWindowState(QtCore.Qt.WindowNoState)
        self.setGeometry(0, 0, 500, 100)
        self.setWindowTitle("Mint Emojis")
        self.setStyleSheet("background-color: darkred;")
        self.setWindowIcon(QtGui.QIcon("assets/icon.png"))

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.notebook = QtWidgets.QTabWidget()
        self.layout.addWidget(self.notebook)

        for category, key in categories.items():
            frame = QtWidgets.QWidget()
            self.notebook.addTab(frame, category)

            layout = QtWidgets.QVBoxLayout(frame)
            scroll_area = QtWidgets.QScrollArea()
            layout.addWidget(scroll_area)

            scrollable_frame = QtWidgets.QWidget()
            scroll_area.setWidget(scrollable_frame)
            scroll_area.setWidgetResizable(True)

            inner_layout = QtWidgets.QHBoxLayout(scrollable_frame)

            selected_emojis = emojis[category]
            for emoji in selected_emojis:
                button = QtWidgets.QPushButton(emoji)
                button.setFont(QtGui.QFont("Noto Color Emoji", 24))
                button.setFixedWidth(50)
                button.setFixedHeight(50)
                button.clicked.connect(lambda _, e=emoji: self.copy_to_clipboard(e))
                inner_layout.addWidget(button)

            scrollbar = scroll_area.horizontalScrollBar()
            scrollbar.setMinimumHeight(scrollbar.sizeHint().height())
            scrollbar.setSingleStep(20)

            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

            frame.setFixedWidth(500)
            scroll_area.setFixedHeight(80)

        shortcut = keyboard.GlobalHotKeys({'<ctrl>+<shift>+e': self.toggle_visibility})
        shortcut.start()

    def copy_to_clipboard(self, emoji):
        pyperclip.copy(emoji)
        subprocess.Popen(["notify-send", "Emoji Copied to Clipboard"])

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            x, y = mouse_controller.position
            self.move(x, y)
            self.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())