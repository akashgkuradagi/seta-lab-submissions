import time

from puzzle import Puzzle


class SlidingPuzzle:
    def __init__(self, size):
        self.size = size
        self.puzzle = Puzzle(self.size)

        # Session values are initialized once when a new game starts.
        self.moves = 0
        self.started = time.monotonic()
        self.finished = False

    def display(self):
        print()

        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))

        print(
            "Moves:",
            self.moves,
            " Time:",
            int(time.monotonic() - self.started),
            "s",
        )

    def run(self):
        print(
            f"Sliding Puzzle {self.size}x{self.size} "
            "— W/A/S/D moves the tile into the blank. Q quits."
        )

        while True:
            # Stop immediately if the puzzle has already been solved.
            if self.puzzle.solved():
                self.finished = True
                self.display()
                print("Solved!")
                return

            self.display()

            key = input("> ").strip().lower()

            # Quit the current game.
            if key == "q":
                return

            # Only accept exact valid movement commands.
            if key not in {"w", "a", "s", "d"}:
                print("Use W/A/S/D.")
                continue

            # Do not allow movement after completion.
            if self.finished:
                return

            # Only a successful movement increments the counter.
            if self.puzzle.move(key):
                self.moves += 1

                # Check immediately after every successful move.
                if self.puzzle.solved():
                    self.finished = True
                    self.display()
                    print("Solved!")
                    return
            else:
                print("That move is not possible.")