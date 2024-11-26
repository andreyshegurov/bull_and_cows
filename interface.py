import sys

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QHBoxLayout, QVBoxLayout, QWidget, QListWidget, \
    QLineEdit, QMessageBox, QLabel, QSpinBox, QGridLayout
from main import Game
from dialogs import WinDialog, RestartDialog


class MainWindow(QMainWindow):
    """Описывает класс основного окна игры."""

    def __init__(self):
        """Устанавливает атрибуты и виджеты основного окна."""
        super().__init__()
        self.window_settings = window_settings
        self.setWindowTitle("Быки и Коровы!")
        self.setFixedSize(440, 480)
        self.setWindowIcon(QIcon('icon.png'))

        # Создание виджетов основного окна игры.
        self.list_try = QListWidget()
        self.list_try.setFixedWidth(420)
        self.list_try.setFont(QFont('Times', 10))

        self.text_guess = QLineEdit()
        self.text_guess.setPlaceholderText('Введите число...')
        self.text_guess.setFixedSize(420, 40)
        self.text_guess.setFont(QFont('Times', 10))

        self.button_guess = QPushButton('Проверить число')
        self.button_guess.setFixedSize(200, 30)
        self.button_guess.clicked.connect(self.press_button_check)
        self.button_guess.setFont(QFont('Times', 10))

        self.button_hint = QPushButton(f'Подсказка ({self.window_settings.max_num_hint})')
        self.button_hint.setFixedSize(105, 30)
        self.button_hint.clicked.connect(self.press_button_hint)
        self.button_hint.setFont(QFont('Times', 10))

        self.button_again = QPushButton('Начать заново')
        self.button_again.setFixedSize(105, 30)
        self.button_again.clicked.connect(self.restart_game)
        self.button_again.setFont(QFont('Times', 10))

        # Создание макета основного окна игры.
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

        # Создание экземпляра класса Game, установка начальных параметров.
        self.game = Game(length_number=self.window_settings.length_number,
                         max_number_guess=self.window_settings.max_num_guess,
                         max_number_hint=self.window_settings.max_num_hint)
        self.game.reset_list_hint()
        self.number_user_guess = 0
        self.number_user_hint = 0
        self.list_try.addItem(f'Начнем игру! Вам нужно отгадать '
                              f'{self.game.length_number}-х значное число\n'
                              f'Количество попыток: '
                              f'{self.game.max_number_guess}\n'
                              f'Количество подсказок: '
                              f'{self.game.max_number_hint}\n'
                              f'_____________________________________________')

        widget = QWidget()
        widget.setLayout(base_layout)
        self.setCentralWidget(widget)

    def press_button_check(self) -> None:
        """Выполняется при нажатии кнопки 'Проверить'."""
        user_guess = self.text_guess.text()
        if self.game.check_user_guess(user_guess):
            # Проверка корректности введенного числа,подсчет "быков" и "коров".
            self.number_user_guess += 1
            user_guess = list(self.text_guess.text())
            result = self.game.start_round(user_guess)
            self.list_try.addItem(
                f'{self.number_user_guess}:   {self.text_guess.text()}    '
                f'Коровы: {result[0]}, Быки: {result[1]}')
            self.text_guess.clear()
            self.text_guess.setFocus()

            if result[1] == self.game.length_number:
                # Условие выполняется если пользователь угадал число.
                self.list_try.addItem('Поздравляю! Вы победили!')
                self.button_guess.setEnabled(False)
                self.button_hint.setEnabled(False)
                self.restart_game_after_win()
            else:
                # Вывод дополнительной информации (если требуется).
                if self.number_user_guess + 2 == self.game.max_number_guess:
                    self.list_try.addItem('Осталось две попытки!')
                    self.text_guess.setFocus()
                if self.number_user_guess + 1 == self.game.max_number_guess:
                    self.list_try.addItem('Осталась одна попытка!')
                    self.text_guess.setFocus()
                if self.number_user_guess == self.game.max_number_guess:
                    self.list_try.addItem(f'_______________________'
                                          f'______________________\n'
                                          f'К сожалению, максимальное число '
                                          f'попыток превышено.\n'
                                          f'Было загадано число '
                                          f'{self.game.get_hidden_number()}.\n'
                                          f'Попробуйте сыграть еще раз!')
                    self.button_guess.setEnabled(False)
                    self.button_hint.setEnabled(False)
        else:
            # Условие выполняется при вводе некорректного набора символов.
            self.show_error()
            self.text_guess.clear()
            self.text_guess.setFocus()

    def press_button_hint(self):
        """Выполняется при нажатии кнопки 'Подсказка'."""
        if self.number_user_hint < self.game.max_number_hint:
            self.number_user_hint += 1
            self.button_hint.setText(f'Подсказка ({self.window_settings.max_num_hint - self.number_user_hint})')
            if self.number_user_hint < 2:
                # Подсказка пользователю одной "коровы".
                hint = self.game.get_hint()
                message_hint = f'В загаданном числе точно есть цифра {hint[1]}'
                self.list_try.addItem(message_hint)
            else:
                # Подсказка пользователю одного "быка".
                hint = self.game.get_hint()
                message_hint = f'В загаданном числе цифра {hint[1]} ' \
                               f'расположена на {hint[0] + 1}-м месте'
                self.list_try.addItem(message_hint)
            if self.number_user_hint == self.game.max_number_hint:
                self.button_hint.setEnabled(False)

    def show_error(self):
        """Выполняется при некорректном вводе числа."""
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle('Ошибка!')
        error_dialog.setText(f'Нужно вводить '
                             f'{self.game.length_number}-х значное число \n'
                             f'Все цифры должны быть разные')
        error_dialog.exec()

    def restart_game(self):
        """Выполняется при нажатии кнопки 'Заново'."""
        message_restart = RestartDialog()
        if message_restart.exec():
            self.close()
            self.window_settings.show()

    def restart_game_after_win(self):
        """Выполняется при выборе сыграть еще раз из диалога при победе."""
        message_win = WinDialog()
        if message_win.exec():
            self.close()
            self.window_settings.show()
        else:
            self.close()
            self.window_settings.close()


class SettingsWindow(QMainWindow):
    """Описывает класс окна настроек игры."""

    def __init__(self):
        """Устанавливает атрибуты и виджеты окна настроек."""
        super().__init__()
        self.setWindowTitle("Быки и Коровы!")
        self.setFixedSize(440, 220)
        self.setWindowIcon(QIcon('icon.png'))

        self.length_number = 4
        self.max_num_guess = 99
        self.max_num_hint = 3

        # Создание виджетов окна настроек игры.
        self.label_hello = QLabel('Добро пожаловать в игру '
                                  '"Быки и коровы"! \n'
                                  'Ознакомьтесь с правилами и определите '
                                  'параметры игры:')
        self.label_hello.setFont(QFont('Times', 10))
        self.label_length_number = QLabel('Длина загадываемого числа')
        self.label_length_number.setFont(QFont('Times', 10))
        self.label_max_number_guess = QLabel('Максимальное количество попыток')
        self.label_max_number_guess.setFont(QFont('Times', 10))
        self.label_hint = QLabel('Играть с подсказками')
        self.label_hint.setFont(QFont('Times', 10))
        self.label_max_number_hint = QLabel('Количество подсказок')
        self.label_max_number_hint.setFont(QFont('Times', 10))

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
        self.button_start.setFixedSize(315, 40)
        self.button_start.clicked.connect(self.get_started)
        self.button_start.setFont(QFont('Times', 10))

        self.button_tutorial = QPushButton('Как играть?')
        self.button_tutorial.setFixedSize(100, 40)
        self.button_tutorial.clicked.connect(self.get_tutorial)
        self.button_tutorial.setFont(QFont('Times', 10))

        # Создание макета окна настроек игры.
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
        button_start_layout.setContentsMargins(0, 15, 0, 0)
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
        """Выполняется при нажатии на кнопку 'Начать'."""
        self.length_number = self.spinbox_length_number.value()
        self.max_num_guess = self.spinbox_max_number_guess.value()
        self.max_num_hint = self.spinbox_max_number_hint.value()
        self.window_main = MainWindow()
        self.hide()
        self.window_main.show()

    def get_tutorial(self):
        """Выполняется при нажатии на кнопку 'Как играть?'."""
        self.window_tutorial = TutorialWindow()
        self.hide()
        self.window_tutorial.show()


class TutorialWindow(QMainWindow):
    """Описывает класс с правилами игры."""

    def __init__(self):
        """Устанавливает атрибуты и виджеты окна с правилами игры."""
        super().__init__()
        self.window_settings = window_settings
        self.setWindowTitle("Быки и Коровы!")
        self.setFixedSize(440, 370)
        self.setWindowIcon(QIcon('icon.png'))

        # Создание виджетов окна с правилами игры.
        text_tutorial = "Правила игры: \n" \
                        "Компьютер задумывает число, состоящее из цифр " \
                        "от 0 до 9.\n" \
                        "Это может быть трех-, четырех- или " \
                        "пятизначное число, " \
                        "в зависимости от настроек игрока.\n" \
                        "Игрок делает ходы, чтобы угадать это число.\n" \
                        "В ответ компьютер показывает " \
                        "число отгаданных цифр, " \
                        "стоящих на своих местах (число быков) и " \
                        "число отгаданных цифр, стоящих не на " \
                        "своих местах (число коров).\n" \
                        "\n" \
                        "Пример: \n" \
                        "Компьютер задумал 0834.\n" \
                        "Игрок сделал ход 8134.\n" \
                        "Компьютер ответил: 2 быка (цифры 3 и 4) и 1 корова " \
                        "(цифра 8).\n" \
                        "\n" \
                        "Плохая новость - Вы должны уложиться в " \
                        "определенное количество попыток.\n" \
                        "Хорошая новость - у Вас есть подсказки!"

        self.text_label = QLabel(text_tutorial)
        self.text_label.setWordWrap(True)
        self.text_label.setFont(QFont('Times', 10))

        self.button_back = QPushButton('Назад')
        self.button_back.clicked.connect(self.get_back)
        self.button_back.setFixedSize(100, 40)
        self.button_back.setFont(QFont('Times', 10))

        # Создание макета окна с правилами игры.
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
        """Выполняется при нажатии на кнопку 'Назад'."""
        self.close()
        self.window_settings.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_settings = SettingsWindow()
    window_settings.show()

    app.exec()
