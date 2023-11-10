"""A simple Connect4 game."""
from __future__ import annotations

import enum
import random
from typing import Any

BOARD_SIZE: int = 8
Board = list[list[Any]]


class PlayerColour(str, enum.Enum):
    """An enum to represent the colours of the players."""

    RED = "🔴"
    YELLOW = "🟡"


class Player:
    """A class to represent a player."""

    def __init__(self, colour: PlayerColour) -> None:
        """
        Initialise the player.

        Params
        ------
        colour: :class:`PlayerColour`
            The colour of the player.
        """
        self.name = colour.name.title()
        self.icon = colour.value
        self.is_move = False

    def input(self) -> int:
        """Ask the player for a move."""
        while True:
            ans = input(f"{self.name} move: ")
            if ans.isdigit() and 1 <= int(ans) <= BOARD_SIZE:
                return int(ans) - 1

            print("Please enter a column number between 1 and 8.")


class AIPlayer(Player):
    """A class to represent an AI player."""

    def input(self, board: Board) -> int:
        """Generate a move for the AI."""
        for col in range(BOARD_SIZE):
            if self.is_winning_move(col, board):
                return col

        for col in range(BOARD_SIZE):
            if self.is_blocking_move(col, board):
                return col

        # If no winning or blocking move, choose a random move
        return random.randint(0, BOARD_SIZE - 1)  # noqa: S311

    def is_winning_move(self, col: int, board: list[list[Any]]) -> bool:
        """Check if placing a token in the given column results in a winning move."""
        temp_board = [row[:] for row in board]
        for i in range(7, -1, -1):
            if temp_board[i][col] is None:
                temp_board[i][col] = self.icon
                if Connect4(temp_board, self, Player(PlayerColour.RED)).is_win(self):
                    return True
                break
        return False

    def is_blocking_move(self, col: int, board: list[list[Any]]) -> bool:
        """Check if a move in the given column blocks the opponent from winning."""
        temp_board = [row[:] for row in board]
        for i in range(7, -1, -1):
            if temp_board[i][col] is None:
                temp_board[i][col] = Player(PlayerColour.RED).icon
                if Connect4(temp_board, self, Player(PlayerColour.RED)).is_win(
                    Player(PlayerColour.RED),
                ):
                    return True
                break
        return False


class Connect4:
    """A class to represent a Connect4 game."""

    def __init__(
        self,
        board: Board | None = None,
        player1: Player | None = None,
        player2: Player | None = None,
    ) -> None:
        """
        Initialise the board and players.

        Params
        ------
        board: Optional[list[list[Any]]]
            The initial state of the board. If not provided, a new board is created.

        player1: Optional[:class:`Player`]
            The first player. If not provided, a new player is created.

        player2: Optional[:class:`Player`]
            The second player. If not provided, a new player is created.
        """
        self.player1 = player1 if player1 else Player(PlayerColour.RED)
        self.player2 = player2 if player2 else AIPlayer(PlayerColour.YELLOW)
        self.board: Board = (
            board
            if board
            else [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        )

    def __str__(self) -> str:
        """Return a string representation of the board."""
        return "\n".join(
            " ".join("⚪" if v is None else v for v in row) for row in self.board
        )

    def move(self, player: Player) -> None:
        """Ask the player for a move and update the board."""
        while player.is_move:
            if isinstance(player, AIPlayer):
                row = player.input(self.board)
            else:
                row = player.input()

            for i in range(7, -1, -1):
                if self.board[i][row] is None:
                    self.board[i][row] = player.icon
                    player.is_move = False
                    break
            else:
                print("Please choose a column that is not full.")

    def is_win(self, player: Player) -> bool:  # noqa: C901
        """Check if the player has won the game."""
        for i in range(8):
            for j in range(5):
                if all(self.board[i][j + k] == player.icon for k in range(4)):
                    return True

        for i in range(5):
            for j in range(BOARD_SIZE):
                if all(self.board[i + k][j] == player.icon for k in range(4)):
                    return True

        for i in range(5):
            for j in range(5):
                if all(self.board[i + k][j + k] == player.icon for k in range(4)):
                    return True

        for i in range(5):
            for j in range(3, BOARD_SIZE):
                if all(self.board[i + k][j - k] == player.icon for k in range(4)):
                    return True
        return False

    def play(self) -> None:
        """Game loop for Connect4."""
        while True:
            print(self)
            self.player1.is_move = True
            self.move(self.player1)

            if self.is_win(self.player1):
                print(f"{self.player1.name} wins!")
                break
            print(self)

            self.player2.is_move = True
            self.move(self.player2)

            if self.is_win(self.player2):
                print(self)
                print(f"{self.player2.name} wins!")
                break


def main() -> None:
    """Play a game of Connect 4."""
    game = Connect4()
    game.play()
    print(game)


if __name__ == "__main__":
    main()
