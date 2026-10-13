import time


# --------------------------------------------------
# Class 1: Player
# --------------------------------------------------

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.number_of_moves = 0
        self.result = "In Progress"
        self.game_time = 0

    def show_information(self):        # mehthod show_information()
        print("Player:", self.name)
        print("Color:", self.color)
        print("Number of moves:", self.number_of_moves)
        print("Result:", self.result)


# --------------------------------------------------
# Class 2: Checker
# --------------------------------------------------

class Checker:
    def __init__(self, color, king=False):  # to define normal checker
        self.color = color
        self.king = king

    def promote_to_king(self):        # to define king checker  // method promote_to_king()
        self.king = True

    def get_symbol(self):                 # method get_symbol()
        if self.color == "Red":
            if self.king:
                return "R"    # king checker
            return "r"   # nomral red checker

        if self.king:
            return "B"    # king checker

        return "b"         # normal black checker


# --------------------------------------------------
# Class 3: Board
# --------------------------------------------------

class Board:
    def __init__(self):
        self.size = 8
        self.checkers = []
        self.initialize_board()

    def initialize_board(self):        # method initiallize_board()
        self.checkers = []

        for row in range(self.size):
            current_row = []

            for col in range(self.size):
                current_row.append(None)

            self.checkers.append(current_row)

        # Red checkers occupy the top three rows.
        for row in range(3):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    self.checkers[row][col] = Checker("Red")

        # Black checkers occupy the bottom three rows.
        for row in range(5, 8):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    self.checkers[row][col] = Checker("Black")

    def display_board(self):                # method display board
        print("\n    0 1 2 3 4 5 6 7")
        print("   -----------------")

        for row in range(self.size):
            print(row, "|", end=" ")

            for col in range(self.size):
                checker = self.checkers[row][col]

                if checker is None:
                    print(".", end=" ")
                else:
                    print(checker.get_symbol(), end=" ")

            print()

        print("\nSymbols:")
        print("r = Red checker, R = Red king")
        print("b = Black checker, B = Black king")
        print(". = Empty square")

    def inside_board(self, row, col):  # method inside_board() - to check if the checker is inside
        return (
            0 <= row < self.size
            and 0 <= col < self.size
        )

    def get_checker(self, row, col):     # method get_checker() - to check certain row and column
        if not self.inside_board(row, col):
            return None

        return self.checkers[row][col]

    def get_valid_moves(self, row, col, player_color):    # method get_valid_moves()  to check validity of the move
        checker = self.get_checker(row, col)

        if checker is None:
            return []

        if checker.color != player_color:
            return []

        valid_moves = []

        # Regular checkers move forward.
        if checker.king:
            directions = [-1, 1]
        elif checker.color == "Red":
            directions = [1]
        else:
            directions = [-1]

        for direction in directions:
            for col_direction in [-1, 1]:   # defining directions

                new_row = row + direction
                new_col = col + col_direction

                # Normal move.
                if self.inside_board(new_row, new_col):
                    if self.checkers[new_row][new_col] is None:
                        valid_moves.append(
                            (new_row, new_col, None)
                        )

                # Capture move.    
                capture_row = row + 2 * direction
                capture_col = col + 2 * col_direction

                if self.inside_board(capture_row, capture_col):
                    middle_checker = self.checkers[new_row][new_col]

                    if (
                        middle_checker is not None
                        and middle_checker.color != player_color
                        and self.checkers[capture_row][capture_col] is None
                    ):
                        valid_moves.append(
                            (
                                capture_row,
                                capture_col,
                                (new_row, new_col)
                            )
                        )

        # If a capture is available, it must be made.
        capture_moves = [
            move for move in valid_moves
            if move[2] is not None
        ]

        if capture_moves:
            return capture_moves

        return valid_moves

    def has_valid_move(self, player_color):
        for row in range(self.size):
            for col in range(self.size):
                checker = self.checkers[row][col]

                if checker is not None:
                    if checker.color == player_color:
                        if self.get_valid_moves(
                            row, col, player_color
                        ):
                            return True

        return False

    def move_checker(self, start_row, start_col, end_row, end_col):
        checker = self.get_checker(start_row, start_col)

        if checker is None:
            return False, False

        possible_moves = self.get_valid_moves(
            start_row, start_col, checker.color
        )

        selected_move = None

        for move in possible_moves:
            if move[0] == end_row and move[1] == end_col:
                selected_move = move
                break

        if selected_move is None:
            return False, False

        captured = selected_move[2]

        # Move the checker.
        self.checkers[end_row][end_col] = checker
        self.checkers[start_row][start_col] = None

        # Remove the captured checker.
        if captured is not None:
            captured_row, captured_col = captured
            self.checkers[captured_row][captured_col] = None

        # Promote to king when the opposite end is reached.
        if checker.color == "Red" and end_row == 7:
            checker.promote_to_king()

        elif checker.color == "Black" and end_row == 0:
            checker.promote_to_king()

        return True, captured is not None

    def count_checkers(self, color):
        count = 0

        for row in self.checkers:
            for checker in row:
                if checker is not None and checker.color == color:
                    count += 1

        return count


# --------------------------------------------------
# Class 4: Game
# --------------------------------------------------

class Game:
    def __init__(self, player1_name, player2_name):
        self.player1 = Player(player1_name, "Red")
        self.player2 = Player(player2_name, "Black")

        self.board = Board()
        self.current_player = self.player1

        self.number_of_moves = 0
        self.start_time = time.time()
        self.end_time = None

        self.game_over = False
        self.winner = None

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def make_move(self):
        player = self.current_player

        print("\nCurrent player:", player.name)
        print("Color:", player.color)

        try:
            start_row = int(input("Enter starting row (0-7): "))
            start_col = int(input("Enter starting column (0-7): "))
            end_row = int(input("Enter destination row (0-7): "))
            end_col = int(input("Enter destination column (0-7): "))

        except ValueError:
            print("Invalid input. Please enter numbers.")
            return False

        if not all(
            0 <= value <= 7
            for value in [
                start_row, start_col, end_row, end_col
            ]
        ):
            print("Coordinates must be between 0 and 7.")
            return False

        checker = self.board.get_checker(start_row, start_col)

        if checker is None:
            print("There is no checker at the starting position.")
            return False

        if checker.color != player.color:
            print("You cannot move your opponent's checker.")
            return False

        valid, captured = self.board.move_checker(
            start_row, start_col, end_row, end_col
        )

        if not valid:
            print("Invalid move. Try again.")
            return False

        self.number_of_moves += 1
        player.number_of_moves += 1

        print("\nMove completed successfully.")

        if captured:
            print("An opponent's checker was captured.")

        self.board.display_board()

        # Check whether the opponent has any possible moves.
        opponent = (
            self.player2
            if player == self.player1
            else self.player1
        )

        if (
            self.board.count_checkers(opponent.color) == 0
            or not self.board.has_valid_move(opponent.color)
        ):
            self.game_over = True
            self.winner = player
            self.winner.result = "Winner"
            opponent.result = "Lost"

        else:
            self.switch_player()

        return True

    def play(self):
        print("================================")
        print("       CHECKERS GAME")
        print("================================")

        print("Player 1:", self.player1.name, "- Red")
        print("Player 2:", self.player2.name, "- Black")

        self.board.display_board()

        while not self.game_over:

            print("\n--------------------------------")
            print("Current player:", self.current_player.name)
            print("Total moves:", self.number_of_moves)

            print("1. Make a move")
            print("2. Finish the game")

            choice = input("Choose an option (1 or 2): ").strip()

            if choice == "1":
                self.make_move()

            elif choice == "2":
                print("\nThe game was finished by the player.")
                break

            else:
                print("Invalid choice. Please select 1 or 2.")

        self.end_time = time.time()

        if self.winner is None:
            self.player1.result = "Game Ended"
            self.player2.result = "Game Ended"

        self.player1.game_time = self.end_time - self.start_time
        self.player2.game_time = self.player1.game_time

        self.show_summary()

    def show_summary(self):
        print("\n================================")
        print("         GAME SUMMARY")
        print("================================")

        print("Player 1:", self.player1.name)
        print("Color:", self.player1.color)
        print("Moves:", self.player1.number_of_moves)
        print("Result:", self.player1.result)

        print("\nPlayer 2:", self.player2.name)
        print("Color:", self.player2.color)
        print("Moves:", self.player2.number_of_moves)
        print("Result:", self.player2.result)

        print("\nTotal moves:", self.number_of_moves)

        duration = self.end_time - self.start_time

        print("Game duration:", round(duration, 2), "seconds")

        print("\nRemaining Red checkers:",
              self.board.count_checkers("Red"))

        print("Remaining Black checkers:",
              self.board.count_checkers("Black"))

        if self.winner is not None:
            print("Winner:", self.winner.name)
        else:
            print("Winner: No winner (game ended early)")

        print("================================")


# --------------------------------------------------
# Main program
# --------------------------------------------------

if __name__ == "__main__":

    print("Welcome to the Checkers Game!")

    player1_name = input("Enter the name of Player 1 (Red): ")
    player2_name = input("Enter the name of Player 2 (Black): ")

    game = Game(player1_name, player2_name)
    game.play()