import random


class Game:
    def __init__(self, length_number: int = 4):
        self.length_number = length_number
        self.__hidden_number = []

    # загадываем число
    def create_hidden_number(self) -> list:
        all_numbers = list(range(0, 10))
        random.shuffle(all_numbers)
        self.__hidden_number = all_numbers[:self.length_number]
        return self.__hidden_number

    def count_bulls(self, user_number: list):
        counter_bulls = 0
        for i in range(self.length_number):
            if self.__hidden_number[i] == user_number[i]:
                counter_bulls += 1
        return counter_bulls

    def count_cows(self, user_number: list):
        counter_cows = 0
        for i in range(self.length_number):
            if (user_number[i] in self.__hidden_number) and (user_number[i] != self.__hidden_number[i]):
                counter_cows += 1
        return counter_cows


game = Game(4)
try_user_number = list(input())
try_user_number = [int(elem) for elem in try_user_number]
print(try_user_number)
print(game.create_hidden_number())
print(game.count_cows(try_user_number))
print(game.count_bulls(try_user_number))

