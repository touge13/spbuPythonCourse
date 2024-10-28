from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.game.src.game import Game
from project.game.src.bot import Bot, ConservativeBot, AggressiveBot, MixedBot
from project.game.src.card import Card, Deck


@pytest.fixture
def setup_game():
    bots = [ConservativeBot("Bot1"), AggressiveBot("Bot2"), MixedBot("Bot3")]
    game = Game(bots, max_steps=5)
    return game


def test_initial_state(setup_game):
    game = setup_game
    assert game.current_step == 0
    assert isinstance(game.deck, Deck)


def test_bot_decision(setup_game):
    game = setup_game
    for bot in game.bots:
        bot.add_card(game.deck.draw_card())
        bot.add_card(game.deck.draw_card())  # Добавляем две карты
        assert bot.decide() in [True, False]  # Проверяем, что бот принимает решение


def test_play_round(setup_game):
    game = setup_game
    game.play_game()
    assert game.current_step > 0  # Проверяем, что шаг увеличился


def test_bot_scores(setup_game):
    game = setup_game
    for bot in game.bots:
        bot.add_card(game.deck.draw_card())
        bot.add_card(game.deck.draw_card())

    # Проверяем, что счет бота правильно подсчитывается
    for bot in game.bots:
        score = bot.calculate_score()
        assert score >= 0  # Проверяем, что счет не отрицательный


def test_bust_condition(setup_game):
    game = setup_game
    bot = game.bots[0]
    # Создаем карты и добавляем их боту
    bot.add_card(Card("Hearts", 10))  # Карта 10
    bot.add_card(Card("Diamonds", 10))  # Еще одна карта 10
    bot.add_card(Card("Clubs", 2))  # Карта 2, суммарно 22 очка

    assert bot.calculate_score() > 21  # Проверяем, что бот "перетянул"


def test_winner_determination(setup_game):
    game = setup_game
    # Создаем карты и задаем счет ботам так, чтобы один из них победил
    game.bots[0].add_card(Card("Hearts", 10))
    game.bots[0].add_card(Card("Diamonds", 8))  # Счет 18
    game.bots[1].add_card(Card("Clubs", 10))
    game.bots[1].add_card(Card("Spades", 7))  # Счет 17
    game.bots[2].add_card(Card("Hearts", 10))
    game.bots[2].add_card(Card("Diamonds", 9))  # Счет 19

    winner = game.determine_winner()
    assert winner == game.bots[2]  # Бот с индексом 2 должен быть победителем


def test_game_over_condition(setup_game):
    game = setup_game
    game.current_step = game.max_steps  # Устанавливаем максимальное количество шагов
    winner = game.determine_winner()
    assert winner is not None  # Проверяем, что игра завершена и есть победитель


# Тесты для метакласса BotMeta
def test_conservative_bot_decision():
    bot = ConservativeBot("TestBot")
    bot.add_card(Card("Hearts", 10))  # Счет 10
    bot.add_card(Card("Diamonds", 5))  # Счет 15
    assert bot.decide()  # Счет 15, должен взять карту (15 < 16)

    bot.add_card(Card("Clubs", 2))  # Счет 17
    assert not bot.decide()  # Счет 17, не должен брать карту (17 >= 16)


def test_aggressive_bot_decision():
    bot = AggressiveBot("AggressiveBot")
    bot.add_card(Card("Hearts", 10))  # Счет 10
    bot.add_card(Card("Spades", 8))  # Счет 18
    assert bot.decide()  # Счет 18, должен взять карту (18 < 19)

    bot.add_card(Card("Clubs", 2))  # Счет 20
    assert not bot.decide()  # Счет 20, не должен брать карту (20 >= 19)


def test_mixed_bot_decision():
    bot = MixedBot("MixedBot")
    bot.add_card(Card("Hearts", 3))  # Счет 3
    bot.add_card(Card("Diamonds", 5))  # Счет 8
    assert bot.decide()  # Счет 8, четный, должен взять карту

    bot.add_card(Card("Spades", 2))  # Счет 10, четный
    assert bot.decide()  # Счет 10, четный, должен взять карту

    bot.add_card(Card("Clubs", 1))  # Счет 11, нечетный
    assert not bot.decide()  # Счет 11, нечетный, не должен брать карту


# Тесты для метакласса GameMeta
def test_default_target_score():
    game = Game(bots=[], max_steps=5)
    assert game.target_score == 21  # Значение по умолчанию должно быть 21


def test_custom_target_score():
    game = Game(bots=[], max_steps=5, target_score=15)
    assert game.target_score == 15  # Проверка на пользовательское значение


def test_game_initialization():
    bots = [ConservativeBot("Bot1"), AggressiveBot("Bot2")]
    game = Game(bots=bots, max_steps=10)
    assert game.bots == bots
    assert game.max_steps == 10


@pytest.fixture
def example_bots():
    return [ConservativeBot("Bot1"), AggressiveBot("Bot2"), MixedBot("Bot3")]


def test_game_target_score_change(example_bots):
    """
    Test that changing target_score for Game results in the attribute being set correctly.
    """
    new_target_score = 25
    game = Game(example_bots, max_steps=10, target_score=new_target_score)
    assert (
        game.target_score == new_target_score
    ), "target_score should match the new value"


def test_game_default_target_score(example_bots):
    """
    Test that Game defaults to target_score of 21 if no value is provided.
    """
    game = Game(example_bots, max_steps=10)
    assert game.target_score == 21, "Default target_score should be 21"


def test_bot_strategy_metaclass():
    """
    Test that BotMeta metaclass assigns decide method based on strategy.
    """

    class BalancedBot(Bot):
        """Bot that uses a balanced strategy."""

        strategy = "balanced"

    # Instantiate a BalancedBot and test that it has the expected decide method.
    balanced_bot = BalancedBot("BalancedBot")
    assert balanced_bot.strategy == "balanced", "The strategy should be 'balanced'"
    # Verify that the 'decide' method works based on custom logic for 'balanced' strategy
    balanced_bot.hand = [Card("Hearts", 5), Card("Diamonds", 5)]
    assert balanced_bot.decide() == (
        balanced_bot.calculate_score() < 17
    ), "Balanced strategy should draw if score < 17"


@pytest.mark.parametrize(
    "bot_class, strategy, expected_decision",
    [
        (ConservativeBot, "conservative", lambda score: score < 16),
        (AggressiveBot, "aggressive", lambda score: score < 19),
        (MixedBot, "mixed", lambda score: score % 2 == 0),
    ],
)
def test_bot_decide_methods(bot_class, strategy, expected_decision):
    """
    Test that bots' decide methods follow the correct strategy rules.
    """
    bot = bot_class("TestBot")
    bot.hand = [Card("Hearts", 5), Card("Diamonds", 5)]
    assert bot.strategy == strategy, f"The strategy should be {strategy}"
    assert bot.decide() == expected_decision(
        bot.calculate_score()
    ), f"Decide method for {strategy} strategy should match expected behavior"
