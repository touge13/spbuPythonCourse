from typing import List

from project.game.src.card import Card


class BotMeta(type):
    """Metaclass for creating bots with different strategies."""

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        """
        Creates a new bot class with the specified strategy.

        Args:
            cls: The metaclass.
            name: The name of the new class.
            bases: The base classes of the new class.
            attrs: The attributes of the new class.

        Returns:
            A new bot class with a decide method based on the strategy.
        """
        strategy = attrs.get("strategy", None)

        if strategy == "conservative":
            attrs["decide"] = lambda self: self.calculate_score() < 16
        elif strategy == "aggressive":
            attrs["decide"] = lambda self: self.calculate_score() < 19
        elif strategy == "mixed":
            attrs["decide"] = lambda self: self.calculate_score() % 2 == 0
        elif strategy == "balanced":
            attrs["decide"] = lambda self: self.calculate_score() < 17

        return super().__new__(cls, name, bases, attrs)


class Bot(metaclass=BotMeta):
    """Base class for bots in the game."""

    def __init__(self, name: str) -> None:
        """
        Initializes the bot with a name and an empty hand.

        Args:
            name: The name of the bot.
        """
        self.name = name
        self.hand: List["Card"] = []  # List of cards in the bot's hand
        self.is_active = True

    def add_card(self, card: "Card") -> None:
        """
        Adds a card to the bot's hand.

        Args:
            card: The card to be added.
        """
        self.hand.append(card)

    def calculate_score(self) -> int:
        """
        Calculates the current score of the bot based on the cards in hand.

        Returns:
            The current score of the bot.
        """
        score = sum(card.value for card in self.hand)
        aces = sum(1 for card in self.hand if card.rank == 1)
        while score <= 11 and aces:
            score += 10
            aces -= 1
        return score

    def reset_hand(self) -> None:
        """
        Resets the bot's hand, making it empty.
        """
        self.hand = []


class ConservativeBot(Bot):
    """Bot that uses a conservative strategy."""

    strategy = "conservative"


class AggressiveBot(Bot):
    """Bot that uses an aggressive strategy."""

    strategy = "aggressive"


class MixedBot(Bot):
    """Bot that uses a mixed strategy."""

    strategy = "mixed"
