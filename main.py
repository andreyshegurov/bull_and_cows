import random


class Game:
    """
    Описывает класс с основным функционалом игры "Быки и коровы".
    """
    def __init__(self, length_number: int,
                 max_number_guess: int,
                 max_number_hint: int):
        """Устанавливает атрибуты для объекта Game.

        Args:
            length_number: Длина загадываемого числа.
            max_number_guess: Максимальное количество попыток.
            max_number_hint: Максимальное количество подсказок
        """
        self.length_number = length_number
        self.max_number_guess = max_number_guess
        self.max_number_hint = max_number_hint
        self.__hidden_number = self.create_hidden_number()

    list_hint: list = []

    def create_hidden_number(self) -> list[int]:
        """Создание загадываемого числа.

        Returns:
            Загадываемое число в виде списка.

        """
        all_numbers = list(range(0, 10))
        random.shuffle(all_numbers)
        hidden_number = all_numbers[:self.length_number]
        return hidden_number

    def get_hidden_number(self) -> str:
        """Получение загадываемого числа.

        Returns:
            Загадываемое число в виде строки.

        """
        hidden_number_showed = self.__hidden_number
        hidden_number_showed = ''.join(str(el) for el in hidden_number_showed)
        return hidden_number_showed

    def start_round(self, user_guess: list) -> (int, int):
        """Подсчет количества "коров" и "быков".

        Args:
            user_guess: Число, введенное пользователем (в формате списка).

        Returns:
            Количество "коров" и "быков" в числе, введенном пользователем.

        """
        user_guess = [int(elem) for elem in user_guess]
        cows = self.count_cows(user_guess)
        bulls = self.count_bulls(user_guess)
        return cows, bulls

    def get_hint(self) -> tuple[int, int]:
        """Получение подсказки.

        Получение цифры из загадываемого числа,
        которая будет использована в качестве подсказки.

        Returns:
            Индекс цифры и цифра, которая будет использована
            в качестве подсказки.

        """
        list_not_hint = [item for item in self.__hidden_number
                         if item not in self.list_hint]
        hint = random.choice(list_not_hint)
        index_hint = self.__hidden_number.index(hint)
        self.list_hint.append(hint)
        return index_hint, hint

    def reset_list_hint(self):
        """Обнуление списка цифр, которые использовались в качестве подсказок.

        Returns:
            Пустой список, который будет использоваться для хранения цифр,
            предоставленных в качестве подсказок.

        """
        self.list_hint = []

    def count_bulls(self, user_guess: list[int]) -> int:
        """Посчет количества "быков".

        Args:
            user_guess: Число, введенное пользователем (в формате списка).

        Returns:
            Количество "быков".

        """
        counter_bulls = 0
        for i in range(self.length_number):
            if self.__hidden_number[i] == user_guess[i]:
                counter_bulls += 1
        return counter_bulls

    def count_cows(self, user_guess: list) -> int:
        """Посчет количества "коров".

        Args:
            user_guess: Число, введенное пользователем (в формате списка).

        Returns:
            Количество "коров".

        """
        counter_cows = 0
        for i in range(self.length_number):
            if (user_guess[i] in self.__hidden_number) \
                    and (user_guess[i] != self.__hidden_number[i]):
                counter_cows += 1
        return counter_cows

    def check_user_guess(self, user_guess: str) -> bool:
        """Проверка числа, введенного пользователем.

        Функция проверяет, что строка, введенная пользователем,
        состоит только из цифр, цифры в строке не повторяются,
        и количество цифр в пользовательской строке
        соответствует длине загаданного числа.

        Args:
            user_guess: Число, введенное пользователем (в формате строки).

        Returns:
            True, если строка, введенная пользователем,
            соответствует критериям. False, если строка не соответствует
            хотя бы одному критерию.

        """
        if user_guess.isdigit() \
                and (len(user_guess) == self.length_number) \
                and (len(user_guess) == len(set(user_guess))):
            check = True
        else:
            check = False
        return check

    def _set_hidden_number(self, new_hidden_number: list[int]):
        """Принудительная установка загадываемого числа.

        Функция используется только для тестирования кода.

        Args:
            new_hidden_number: Новое загаданное число.

        """
        self.__hidden_number = new_hidden_number
