from game import SlidingPuzzle


def choose_size():
    print("Sliding Puzzle")
    print("Choose board size:")
    print("1. 3x3")
    print("2. 4x4")
    print("3. 5x5")

    while True:
        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            return 3
        elif choice == "2":
            return 4
        elif choice == "3":
            return 5
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    size = choose_size()
    SlidingPuzzle(size).run()