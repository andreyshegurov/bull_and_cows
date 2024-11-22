import random


class Game:
    def __init__(self, length_number: int = 4):
        self.length_number = length_number
        self.__hidden_number = self.create_hidden_number()

    list_hint = []

    def create_hidden_number(self) -> list:
        all_numbers = list(range(0, 10))
        random.shuffle(all_numbers)
        hidden_number = all_numbers[:self.length_number]
        return hidden_number

    def start_round(self, user_guess: list):
        user_guess = [int(elem) for elem in user_guess]
        cows = self.count_cows(user_guess)
        bulls = self.count_bulls(user_guess)
        if bulls < self.length_number:
            message = f'{user_guess}, Коровы: {cows}, Быки: {bulls}'
            # print(f'Коровы: {self.count_cows(user_guess)}')
            # print(f'Быки: {self.count_bulls(user_guess)}')
            # print('------------------------------')
            # user_guess = list(input('Введите число: '))
            # user_guess = [int(elem) for elem in user_guess]
            # self.start_round(user_guess)
        else:
            message = f'{user_guess}, YOU WIN!'
        return message

    def get_tutorial(self):
        pass

    def get_hint(self):
        list_not_hint = [item for item in self.__hidden_number if item not in self.list_hint]
        hint = random.choice(list_not_hint)
        self.list_hint.append(hint)
        return hint

    def count_bulls(self, user_number: list) -> int:
        counter_bulls = 0
        for i in range(self.length_number):
            if self.__hidden_number[i] == user_number[i]:
                counter_bulls += 1
        return counter_bulls

    def count_cows(self, user_number: list) -> int:
        counter_cows = 0
        for i in range(self.length_number):
            if (user_number[i] in self.__hidden_number) and (user_number[i] != self.__hidden_number[i]):
                counter_cows += 1
        return counter_cows
