import pytest
from main import Game


@pytest.fixture()
def new_game():
    new_game = Game(4, 10, 3)
    new_game._set_hidden_number([1, 2, 3, 4])
    return new_game


def test_create_hidden_number(length_number=4):
    game = Game(length_number, 10, 3)
    hidden_number = game.create_hidden_number()
    hidden_number = ''.join([str(elem) for elem in hidden_number])
    if hidden_number.isdigit() and \
            (len(hidden_number) == length_number) and \
            (len(hidden_number) == len(set(hidden_number))):
        check = True
    else:
        check = False
    assert check


@pytest.mark.parametrize(
    'expected_result',
    ['1234'])
def test_get_hidden_number(new_game, expected_result):
    assert new_game.get_hidden_number() == expected_result


@pytest.mark.parametrize(
    'input_arg, expected_result',
    [([1, 2, 3, 4], (0, 4)),
     ([1, 0, 3, 4], (0, 3)),
     ([1, 2, 4, 3], (2, 2)),
     ([0, 1, 2, 3], (3, 0)),
     ([4, 3, 2, 1], (4, 0)),
     ([6, 7, 8, 9], (0, 0)),
     ([6, 7, 8, 4], (0, 1)),
     ([4, 6, 5, 9], (1, 0))]
)
def test_start_round(new_game, input_arg, expected_result):
    assert new_game.start_round(input_arg) == expected_result


def test_get_hint():
    game = Game(4, 10, 3)
    hidden_number = game.get_hidden_number()
    for i in range(4):
        game.get_hint()
    set_hint = set(game.list_hint)
    set_hidden_number = set([int(elem) for elem in hidden_number])
    assert set_hint == set_hidden_number


@pytest.mark.parametrize(
    'input_arg, expected_result',
    [([1, 2, 3, 4], 4),
     ([0, 2, 3, 4], 3),
     ([1, 0, 3, 4], 3),
     ([4, 3, 2, 1], 0),
     ([1, 2, 4, 3], 2),
     ([1, 5, 6, 9], 1),
     ([6, 7, 8, 9], 0)]
)
def test_count_bulls(new_game, input_arg, expected_result):
    assert new_game.count_bulls(input_arg) == expected_result


@pytest.mark.parametrize(
    'input_arg, expected_result',
    [([1, 2, 3, 4], 0),
     ([0, 2, 3, 4], 0),
     ([0, 3, 4, 1], 3),
     ([4, 3, 2, 1], 4),
     ([1, 2, 4, 3], 2),
     ([3, 5, 6, 9], 1),
     ([6, 7, 8, 9], 0)]
)
def test_count_cows(new_game, input_arg, expected_result):
    assert new_game.count_cows(input_arg) == expected_result


@pytest.mark.parametrize(
    'input_arg, expected_result',
    [('1234', True),
     ('1134', False),
     ('a1234', False),
     ('123', False),
     ('4321', True),
     ('43215', False),
     ('asdasfa ', False)]
)
def test_check_user_guess(new_game, input_arg, expected_result):
    assert new_game.check_user_guess(input_arg) == expected_result
