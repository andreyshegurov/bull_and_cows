import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QListWidget, \
    QLineEdit
from main import Game

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BULL'N'COWS")
        self.list_try = QListWidget()
        self.text_try = QLineEdit()
        self.button = QPushButton('Проверить')
        self.button.clicked.connect(self.press_button)
        self.game = Game()
        self.game.create_hidden_number()

        base_layout = QVBoxLayout()
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.list_try)

        text_layout = QHBoxLayout()
        text_layout.addWidget(self.text_try)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button)

        base_layout.addLayout(list_layout)
        base_layout.addLayout(text_layout)
        base_layout.addLayout(button_layout)

        widget = QWidget()
        widget.setLayout(base_layout)
        self.setCentralWidget(widget)

    def press_button(self):
        number = list(self.text_try.text())
        print(number)
        message = self.game.start_round(number)
        self.list_try.addItem(message)
        self.text_try.clear()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
