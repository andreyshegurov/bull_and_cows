import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QListWidget, \
    QLineEdit, QMessageBox, QLabel, QSpinBox, QGridLayout
from main import Game
from dialogs import WinDialog, RestartDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_settings = window_settings
        self.setWindowTitle("Быки и Коровы!")
        self.setFixedSize(420, 460)
        self.setWindowIcon(QIcon('icon.png'))

        self.list_try = QListWidget()
        self.list_try.setFixedWidth(400)

        self.text_guess = QLineEdit()
        self.text_guess.setPlaceholderText(f'Введите число...')
        self.text_guess.setFixedSize(400, 40)

        self.button_guess = QPushButton('Проверить число')
        # self.button_guess.autoDefault(True)
        self.button_guess.setFixedSize(200, 30)
        self.button_guess.clicked.connect(self.press_button_check)

        self.button_hint = QPushButton('Подсказка')
        self.button_hint.setFixedSize(95, 30)
        self.button_hint.clicked.connect(self.press_button_hint)

        self.button_again = QPushButton('Начать заново')
        self.button_again.setFixedSize(95, 30)
        self.button_again.clicked.connect(self.restart_game)

        base_layout = QVBoxLayout()
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.list_try)

        text_layout = QHBoxLayout()
        text_layout.addWidget(self.text_guess)

        checkbutton_layout = QHBoxLayout()
        checkbutton_layout.addWidget(self.button_guess)
        checkbutton_layout.addWidget(self.button_hint)
        checkbutton_layout.addWidget(self.button_again)

        base_layout.addLayout(list_layout)
        base_layout.addLayout(text_layout)
        base_layout.addLayout(checkbutton_layout)

        self.game = Game(length_number=self.window_settings.length_number,
                         max_number_guess=self.window_settings.max_number_guess,
                         max_number_hint=self.window_settings.max_number_hint)
        self.game.reset_list_hint()

        self.number_user_guess = 0
        self.number_user_hint = 0

        self.list_try.addItem(f'Начнем игру! Вам нужно отгадать {self.game.length_number}-х значное число\n'
                              f'Количество попыток: {self.game.max_number_guess}\n'
                              f'Количество подсказок: {self.game.max_number_hint}\n'
                              f'_____________________________________________')

        widget = QWidget()
        widget.setLayout(base_layout)
        self.setCentralWidget(widget)

    def press_button_check(self):

        user_guess = self.text_guess.text()
        if self.game.check_user_guess(user_guess):
            self.number_user_guess += 1
            user_guess = list(self.text_guess.text())
            result = self.game.start_round(user_guess)
            self.list_try.addItem(
                f'{self.number_user_guess}:   {self.text_guess.text()}    Коровы: {result[0]}, Быки: {result[1]}')
            self.text_guess.clear()
            self.text_guess.setFocus()
            if result[1] == self.game.length_number:
                self.list_try.addItem(f'Поздравляю! Вы победили!')
                self.button_guess.setEnabled(False)
                self.button_hint.setEnabled(False)
                self.restart_game_after_win()

            else:
                if self.number_user_guess + 2 == self.game.max_number_guess:
                    self.list_try.addItem('Осталось две попытки!')
                    self.text_guess.setFocus()
                if self.number_user_guess + 1 == self.game.max_number_guess:
                    self.list_try.addItem('Осталась одна попытка!')
                    self.text_guess.setFocus()
                if self.number_user_guess == self.game.max_number_guess:
                    self.list_try.addItem(f'_____________________________________________\n'
                                          f'К сожалению, максимальное число попыток превышено.\n'
                                          f'Было загадано число {self.game.get_hidden_number()}.\n'
                                          f'Попробуйте сыграть еще раз!')
                    self.button_guess.setEnabled(False)
                    self.button_hint.setEnabled(False)
                    self.game.list_hint = []
        else:
            self.show_error()
            self.text_guess.clear()
            self.text_guess.setFocus()

    def press_button_hint(self):
        if self.number_user_hint < self.game.max_number_hint:
            self.number_user_hint += 1
            if self.number_user_hint < 2:
                hint = self.game.get_hint()
                message_hint = f'В загаданном числе точно есть цифра {hint[1]}'
                self.list_try.addItem(message_hint)
            else:
                hint = self.game.get_hint()
                message_hint = f'В загаданном числе цифра {hint[1]} расположена на {hint[0] + 1}-м месте'
                self.list_try.addItem(message_hint)
        else:
            self.list_try.addItem('Подсказок больше нет :(')
            self.button_hint.setEnabled(False)

    def show_error(self):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle(f'Ошибка!')
        error_dialog.setText(f'Нужно вводить {self.game.length_number}-х значное число \nВсе цифры должны быть разные')
        error_dialog.exec()

    def restart_game(self):
        message_restart = RestartDialog()
        if message_restart.exec():
            self.close()
            self.window_settings.show()

    def restart_game_after_win(self):
        message_win = WinDialog()
        if message_win.exec():
            self.close()
            self.window_settings.show()
        else:
            self.close()
            self.window_settings.close()


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Быки и Коровы!")
        self.setFixedSize(420, 210)
        self.setWindowIcon(QIcon('icon.png'))

        self.length_number = 4
        self.max_number_guess = 99
        self.max_number_hint = 3

        self.label_hello = QLabel('Добро пожаловать в игру "Быки и коровы"! \n'
                                  'Ознакомьтесь с правилами, определите параметры игры и начинайте!')
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
        self.button_start.setFixedSize(290, 40)
        self.button_start.clicked.connect(self.get_started)

        self.button_tutorial = QPushButton('Как играть?')
        self.button_tutorial.setFixedSize(100, 40)
        self.button_tutorial.clicked.connect(self.get_tutorial)

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
        button_start_layout.addWidget(self.button_tutorial)

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

    def get_tutorial(self):
        self.window_tutorial = TutorialWindow()
        self.hide()
        self.window_tutorial.show()

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


class TutorialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_settings = window_settings
        self.setWindowTitle("Быки и Коровы!")
        self.setFixedSize(420, 360)
        self.setWindowIcon(QIcon('icon.png'))

        text_tutorial = f"Правила игры:\n" \
                        f"Компьютер задумывает число, состоящее из цифр от 0 до 9.\n" \
                        f"Это может быть трех-, четырех- или пятизначное число, в " \
                        f"зависимости от настроек игрока.\n" \
                        f"Игрок делает ходы, чтобы угадать это число.\n" \
                        f"В ответ компьютер показывает число отгаданных цифр, стоящих на своих местах (число быков) и " \
                        f"число отгаданных цифр, стоящих не на своих местах (число коров).\n" \
                        f"\n" \
                        f"Пример:\n" \
                        f"Компьютер задумал 0834.\n" \
                        f"Игрок сделал ход 8134.\n" \
                        f"Компьютер ответил: 2 быка (цифры 3 и 4) и 1 корова (цифра 8).\n"\
                        f"\n"\
                        f"Плохая новость - Вы должны уложиться в определенное количество попыток.\n" \
                        f"Хорошая новость - у Вас есть подсказки!"

        self.text_label = QLabel(text_tutorial)
        self.text_label.setWordWrap(True)

        self.button_back = QPushButton('Назад')
        self.button_back.clicked.connect(self.get_back)
        self.button_back.setFixedSize(100, 40)

        base_layout = QVBoxLayout()

        text_tutorial_layout = QHBoxLayout()
        text_tutorial_layout.addWidget(self.text_label)

        button_layout = QGridLayout()
        button_layout.addWidget(self.button_back, 1, 0)

        base_layout.addLayout(text_tutorial_layout)
        base_layout.addLayout(button_layout)

        widget = QWidget()
        widget.setLayout(base_layout)
        self.setCentralWidget(widget)

    def get_back(self):
        self.close()
        self.window_settings.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_settings = SettingsWindow()
    window_settings.show()

    app.exec()
