import random


class Puzzle:
    def __init__(self, size=4):
        self.size = size
        self.board = self.make_board()

    def make_board(self):
        # Start from the solved board.
        # 0 represents the blank tile.
        tiles = list(range(1, self.size * self.size)) + [0]
        blank = len(tiles) - 1

        # Scramble the puzzle using only legal blank-tile moves.
        # Therefore every generated board is reachable from
        # the solved state and is guaranteed to be solvable.
        for _ in range(self.size * self.size * 20):
            row, col = divmod(blank, self.size)
            neighbors = []

            # Blank can move up.
            if row > 0:
                neighbors.append(blank - self.size)

            # Blank can move down.
            if row < self.size - 1:
                neighbors.append(blank + self.size)

            # Blank can move left.
            if col > 0:
                neighbors.append(blank - 1)

            # Blank can move right.
            if col < self.size - 1:
                neighbors.append(blank + 1)

            # Choose one legal blank movement.
            next_blank = random.choice(neighbors)

            # Move the selected tile into the blank.
            tiles[blank], tiles[next_blank] = (
                tiles[next_blank],
                tiles[blank],
            )

            blank = next_blank

        # Convert the flat list into a 2D board.
        return [
            tiles[r * self.size:(r + 1) * self.size]
            for r in range(self.size)
        ]

    def blank_pos(self):
        """Return the row and column of the blank tile."""
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    return row, col

    def move(self, direction):
        """Move a tile into the blank if the requested move is legal."""

        # Reject unsupported directions safely.
        if direction not in {"w", "a", "s", "d"}:
            return False

        row, col = self.blank_pos()

        # Determine the new blank position.
        moves = {
            "w": (-1, 0),
            "s": (1, 0),
            "a": (0, -1),
            "d": (0, 1),
        }

        row_change, col_change = moves[direction]

        new_row = row + row_change
        new_col = col + col_change

        # Check whether the requested movement is inside the board.
        if not (
            0 <= new_row < self.size
            and 0 <= new_col < self.size
        ):
            return False

        # Swap the blank with the neighboring tile.
        self.board[row][col], self.board[new_row][new_col] = (
            self.board[new_row][new_col],
            self.board[row][col],
        )

        return True

    def solved(self):
        """Return True when the board is in the solved state."""

        solved_board = list(range(1, self.size * self.size)) + [0]

        return sum(self.board, []) == solved_board