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

        self.button_check = QPushButton('Проверить')
        self.button_check.clicked.connect(self.press_button_check)

        self.button_hint = QPushButton('Подсказка')
        self.button_hint.clicked.connect(self.press_button_hint)

        base_layout = QVBoxLayout()
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.list_try)

        text_layout = QHBoxLayout()
        text_layout.addWidget(self.text_try)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_check)
        button_layout.addWidget(self.button_hint)

        base_layout.addLayout(list_layout)
        base_layout.addLayout(text_layout)
        base_layout.addLayout(button_layout)

        self.game = Game()

        widget = QWidget()
        widget.setLayout(base_layout)
        self.setCentralWidget(widget)

    def press_button_check(self):
        number = list(self.text_try.text())
        message = self.game.start_round(number)
        self.list_try.addItem(message)
        self.text_try.clear()

    def press_button_hint(self):
        hint = self.game.get_hint()
        message_hint = f'В загаданном числе точно есть цифра {hint}'
        self.list_try.addItem(message_hint)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
