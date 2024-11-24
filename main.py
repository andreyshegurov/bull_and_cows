import random


class Game:
    def __init__(self, length_number: int, max_number_guess, max_number_hint):
        self.length_number = length_number
        self.max_number_guess = max_number_guess
        self.max_number_hint = max_number_hint
        self.__hidden_number = self.create_hidden_number()

    list_hint = []

    def reset_list_hint(self):
        self.list_hint = []

    def create_hidden_number(self) -> list:
        all_numbers = list(range(0, 10))
        random.shuffle(all_numbers)
        hidden_number = all_numbers[:self.length_number]
        return hidden_number

    def get_hidden_number(self):
        hidden_number_showed = self.__hidden_number
        hidden_number_showed = ''.join(str(el) for el in hidden_number_showed)
        return hidden_number_showed

    def start_round(self, user_guess: list):
        user_guess = [int(elem) for elem in user_guess]
        cows = self.count_cows(user_guess)
        bulls = self.count_bulls(user_guess)
        # if bulls < self.length_number:
        #     message = f'Коровы: {cows}, Быки: {bulls}'
        # else:
        #     message = f'YOU WIN!'
        return cows, bulls

    def get_light_hint(self):
        self.list_hint = []
        print(self.list_hint)
        list_not_hint = [item for item in self.__hidden_number if item not in self.list_hint]
        hint = random.choice(list_not_hint)
        self.list_hint.append(hint)
        print(self.list_hint)
        print(list_not_hint)
        return hint

    def get_hard_hint(self):
        list_not_hint = [item for item in self.__hidden_number if item not in self.list_hint]
        hint = random.choice(list_not_hint)
        index_hint = self.__hidden_number.index(hint)
        self.list_hint.append(hint)
        print(hint, list_not_hint, self.list_hint)
        return index_hint, hint

    def count_bulls(self, user_guess: list) -> int:
        counter_bulls = 0
        for i in range(self.length_number):
            if self.__hidden_number[i] == user_guess[i]:
                counter_bulls += 1
        return counter_bulls

    def count_cows(self, user_guess: list) -> int:
        counter_cows = 0
        for i in range(self.length_number):
            if (user_guess[i] in self.__hidden_number) and (user_guess[i] != self.__hidden_number[i]):
                counter_cows += 1
        return counter_cows

    def check_user_guess(self, user_guess: str) -> bool:
        if user_guess.isdigit() and (len(user_guess) == self.length_number) and (
                len(user_guess) == len(set(user_guess))):
            check = True
        else:
            check = False
        return check

