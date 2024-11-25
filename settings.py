from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

from interface import MainWindow


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Быки и Коровы!")
        self.setFixedSize(420, 200)
        self.setWindowIcon(QIcon('icon.png'))

        self.length_number = 4
        self.max_number_guess = 99
        self.max_number_hint = 3

        self.label_hello = QLabel('Добро пожаловать в игру "Быки и коровы" \n'
                                  'Определите параметры игры:')
        self.label_length_number = QLabel('Длина загадываемого числа')
        self.label_max_number_guess = QLabel('Максимальное количество попыток')
        self.label_hint = QLabel('Играть с подсказками')
        self.label_max_number_hint = QLabel('Количество подсказок')

        self.spinbox_length_number = QSpinBox()
        self.spinbox_length_number.setFixedWidth(100)
        self.spinbox_length_number.setMinimum(3)
        self.spinbox_length_number.setMaximum(5)
        self.spinbox_length_number.setSingleStep(1)
        self.spinbox_length_number.lineEdit().setReadOnly(True)
        self.spinbox_length_number.setValue(4)

        self.spinbox_max_number_guess = QSpinBox()
        self.spinbox_max_number_guess.setFixedWidth(100)
        self.spinbox_max_number_guess.setMinimum(6)
        self.spinbox_max_number_guess.setMaximum(100)
        self.spinbox_max_number_guess.setSingleStep(1)
        self.spinbox_max_number_guess.lineEdit().setReadOnly(True)
        self.spinbox_max_number_guess.setValue(10)

        self.spinbox_max_number_hint = QSpinBox()
        self.spinbox_max_number_hint.setFixedWidth(100)
        self.spinbox_max_number_hint.setMinimum(0)
        self.spinbox_max_number_hint.setMaximum(3)
        self.spinbox_max_number_hint.setSingleStep(1)
        self.spinbox_max_number_hint.lineEdit().setReadOnly(True)
        self.spinbox_max_number_hint.setValue(1)

        self.button_start = QPushButton('Начать')
        self.button_start.setFixedSize(400, 40)
        self.button_start.clicked.connect(self.get_started)

        base_layout = QVBoxLayout()

        label_hello_layout = QHBoxLayout()
        label_hello_layout.addWidget(self.label_hello)

        length_number_layout = QHBoxLayout()
        length_number_layout.addWidget(self.label_length_number)
        length_number_layout.addWidget(self.spinbox_length_number)

        max_number_guess_layout = QHBoxLayout()
        max_number_guess_layout.addWidget(self.label_max_number_guess)
        max_number_guess_layout.addWidget(self.spinbox_max_number_guess)

        max_number_hint_layout = QHBoxLayout()
        max_number_hint_layout.addWidget(self.label_max_number_hint)
        max_number_hint_layout.addWidget(self.spinbox_max_number_hint)

        button_start_layout = QHBoxLayout()
        button_start_layout.addWidget(self.button_start)

        base_layout.addLayout(label_hello_layout)
        base_layout.addLayout(length_number_layout)
        base_layout.addLayout(max_number_guess_layout)
        base_layout.addLayout(max_number_hint_layout)
        base_layout.addLayout(button_start_layout)

        widget = QWidget()
        widget.setLayout(base_layout)
        self.setCentralWidget(widget)

    def get_started(self):
        self.length_number = self.spinbox_length_number.value()
        self.max_number_guess = self.spinbox_max_number_guess.value()
        self.max_number_hint = self.spinbox_max_number_hint.value()
        # MainWindow.get_settings(self.length_number, self.max_number_guess, self.max_number_hint)
        self.window_main = MainWindow()
        self.hide()
        self.window_main.show()

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(
    #         self,
    #         "Выход",
    #         "Вы точно хотите выйти?",
    #         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    #         QMessageBox.StandardButton.Yes)
    #
    #     if reply == QMessageBox.StandardButton.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

