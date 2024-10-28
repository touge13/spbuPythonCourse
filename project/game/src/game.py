from project.game.src.card import Deck
from project.game.src.bot import Bot
from typing import List, Optional


class GameMeta(type):
    """
    Metaclass for the Game class to set default attributes.
    """

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        """
        Creates a new Game class with default attributes.

        Args:
            cls (type): The metaclass itself.
            name (str): The name of the new class.
            bases (tuple): The base classes.
            attrs (dict): The class attributes.

        Returns:
            type: The newly created class.
        """
        attrs["target_score"] = attrs.get("target_score", 21)  # Set default value
        return super().__new__(cls, name, bases, attrs)


class Game(metaclass=GameMeta):
    """
    Represents a game that involves a deck of cards and bots.

    Attributes:
        deck (Deck): The deck of cards used in the game.
        bots (List[Bot]): The list of bots participating in the game.
        max_steps (int): The maximum number of rounds to play.
        current_step (int): The current round number.
        output_file (Optional[str]): The file to log game output.
        target_score (int): The target score to reach to win the game.
    """

    target_score: int

    def __init__(
        self,
        bots: List,
        max_steps: int = 10,
        output_file: Optional[str] = None,
        target_score: Optional[int] = None,
    ) -> None:
        """
        Initializes a Game instance.

        Args:
            bots (List): A list of bots participating in the game.
            max_steps (int, optional): Maximum number of rounds to play. Defaults to 10.
            output_file (Optional[str], optional): File to log output. Defaults to None.
            target_score (Optional[int], optional): The target score to win. Defaults to the class default.
        """
        self.deck = Deck()
        self.bots = bots
        self.max_steps = max_steps
        self.current_step = 0
        self.output_file = output_file
        self.target_score = (
            target_score if target_score is not None else self.target_score
        )

    def log(self, message: str) -> None:
        """
        Logs a message to the output file and prints it.

        Args:
            message (str): The message to log.
        """
        if self.output_file:
            with open(self.output_file, "a") as f:
                f.write(message + "\n")
        print(message)

    def show_state(self) -> None:
        """
        Displays the current state of the game, including scores and hands of all bots.
        """
        state = "\nCurrent game state:\n"
        for bot in self.bots:
            state += f"{bot.name} ({bot.__class__.__name__}) score: {bot.calculate_score()} | Hand: {bot.hand}\n"
        self.log(state)

    def play_round(self) -> None:
        """
        Plays a single round of the game, allowing each active bot to draw cards or stay.
        """
        self.log(f"\n--- Round {self.current_step + 1} ---")
        for bot in self.bots:
            if bot.is_active:  # Only active bots can take actions
                if bot.calculate_score() < self.target_score:
                    if bot.decide():
                        card = self.deck.draw_card()
                        if card:
                            bot.add_card(card)
                            self.log(f"{bot.name} draws {card}")
                        else:
                            self.log("Deck is empty!")
                    else:
                        self.log(f"{bot.name} stays with score {bot.calculate_score()}")
                else:
                    bot.is_active = False  # Bot is deactivated if score exceeds target
                    self.log(
                        f"{bot.name} stays with score {bot.calculate_score()} (bust)"
                    )
        self.show_state()

    def determine_winner(self) -> Optional[Bot]:
        """
        Determines the winner of the game based on the scores of the bots.

        Returns:
            Optional[Bot]: The winning bot, or None if no winner is found.
        """
        valid_bots = [
            bot for bot in self.bots if bot.calculate_score() <= self.target_score
        ]
        if not valid_bots:
            self.log("All bots bust. No winner.")
            return None

        # Winning condition: if one of the bots reaches the target score
        winner = next(
            (bot for bot in valid_bots if bot.calculate_score() == self.target_score),
            None,
        )

        # If no winner with the target score, choose the one with the highest score
        if not winner:
            winner = max(valid_bots, key=lambda bot: bot.calculate_score())

        return winner

    def play_game(self) -> None:
        """Plays the game for the maximum number of steps or until a winner is found."""
        if self.output_file:
            open(
                self.output_file, "w"
            ).close()  # Clear the file before starting the game

        while self.current_step < self.max_steps:
            self.play_round()
            self.current_step += 1

            # Check for active bots after each round
            active_bots = [bot for bot in self.bots if bot.is_active]

            # Check if there is only one active bot left
            if len(active_bots) == 1:
                winner = active_bots[0]
                self.log(f"Game over: {winner.name} wins as the last remaining bot!")
                return  # End the game

            # Check for a winner (reaching target score)
            if any(bot.calculate_score() == self.target_score for bot in active_bots):
                winner = next(
                    bot
                    for bot in active_bots
                    if bot.calculate_score() == self.target_score
                )
                self.log(
                    f"Game over: {winner.name} wins with {self.target_score} points!"
                )
                return  # End the game

        # Determine the winner after all rounds are over
        winner = self.determine_winner()
        if winner:
            self.log(
                f"Game over: {winner.name} wins with a score of {winner.calculate_score()}!"
            )
        else:
            self.log("Game ended due to max steps without a winner.")
