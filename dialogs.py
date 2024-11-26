from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class WinDialog(QDialog):
    """Описывает класс диалога, который реализуется после победы в игре."""
    def __init__(self):
        """Устанавливает атрибуты и виджеты окна диалога."""
        super().__init__()
        self.setWindowTitle("Быки и Коровы!")
        self.setWindowIcon(QIcon('icon.png'))

        button_win = (
                QDialogButtonBox.StandardButton.Ok |
                QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(button_win)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        message = QLabel("Поздавляем! Вы победили! \n"
                         "Сыграете еще раз?")

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


class RestartDialog(QDialog):
    """Описывает класс диалога, который реализуется при перезапуске игры."""
    def __init__(self):
        """Устанавливает атрибуты и виджеты окна диалога."""
        super().__init__()
        self.setWindowTitle("Быки и Коровы!")
        self.setWindowIcon(QIcon('icon.png'))

        button_restart = (
                QDialogButtonBox.StandardButton.Yes
                | QDialogButtonBox.StandardButton.No
        )

        self.buttonBox = QDialogButtonBox(button_restart)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Вы действительно хотите начать заново?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
