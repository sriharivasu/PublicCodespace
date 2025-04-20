import streamlit as st
import random
import time
import re

MAX_ROWS = 4
MAX_COLS = 4


def multiplay():

    def maxit_game():
        st.title("Multiplayer Maxit Game :video_game:")
        place = st.container(border=True)
        scoreboard = st.empty()
        global lastbutton
        lastbutton = st.empty()
        # Initialize the game
        if not "players" in st.session_state:
            st.session_state.players = [
                {"name": "player1", "score": 0},
                {"name": "player2", "score": 0},
            ]

        currentPlayer = st.session_state.get("currentPlayer", 0)
        turns = st.empty()
        if currentPlayer == 0:
            turns.write("###### Player: Player 1! " + ":o:")
        elif currentPlayer == 1:
            turns.write("###### Player: Player 2! " + ":x:")

        scoreboard.write(
            f"Player 1: {st.session_state.players[0]['score']} | Player 2: {st.session_state.players[1] ['score']}   "
        )
        if "board" not in st.session_state:
            st.session_state.board = [
                [random.randint(1, 9) for _ in range(MAX_ROWS)] for _ in range(MAX_COLS)
            ]

        if "buttonClicked" not in st.session_state:
            st.session_state["buttonClicked"] = ""
            st.session_state["rowClicked"] = -1
            st.session_state["colClicked"] = -1
            st.session_state["movesLeft"] = MAX_ROWS * MAX_COLS
        disabled_buttons = 0
        with place:
            for i in range(4):
                cols = st.columns(MAX_COLS)
                for j in range(MAX_ROWS):
                    labels = f"{st.session_state.board[i][j]}"
                    disabled = is_disabled(i, j)
                    if disabled:
                        disabled_buttons += 1
                    cols[j].button(
                        labels,
                        key=f"btn_{i}_{j}",
                        on_click=btn_select,
                        args=(currentPlayer, i, j),
                        disabled=is_disabled(i, j),
                    )

        if disabled_buttons == MAX_ROWS * MAX_COLS and st.session_state.movesLeft > 0:
            ending(currentPlayer)

        elif st.session_state.movesLeft == 0:
            ending(currentPlayer)

    def btn_select(currentPlayer, i, j):
        val = st.session_state["board"][i][j]
        if type(st.session_state["board"][i][j]) is int:
            st.session_state.players[currentPlayer]["score"] += val
            if currentPlayer == 0:
                st.session_state["board"][i][j] = ":o:"
            else:
                st.session_state["board"][i][j] = ":x:"
            currentPlayer = 1 - currentPlayer
            st.session_state.currentPlayer = currentPlayer
            st.session_state["movesLeft"] -= 1
            st.session_state["buttonClicked"] = val
            st.session_state["rowClicked"] = i
            st.session_state["colClicked"] = j

    def is_disabled(i, j):
        if type(st.session_state["board"][i][j]) is not int:
            return True
        if st.session_state["buttonClicked"] == "":
            return False
        elif st.session_state["rowClicked"] == i:
            return False
        elif st.session_state["colClicked"] == j:
            return False
        else:
            return True

    def ending(currentPlayer):
        if (
            st.session_state.players[currentPlayer]["score"]
            > st.session_state.players[1 - currentPlayer]["score"]
        ):
            lastbutton.write(f"Player {currentPlayer + 1} wins!")
        elif (
            st.session_state.players[currentPlayer]["score"]
            < st.session_state.players[1 - currentPlayer]["score"]
        ):

            lastbutton.write(f"Player {1 - currentPlayer + 1} wins!")
        else:
            lastbutton.write("It's a tie!")

        if st.button("Play again?"):
            reset()

    def reset():
        st.session_state.board = [
            [random.randint(1, 9) for _ in range(MAX_ROWS)] for _ in range(MAX_COLS)
        ]
        st.session_state.players = [
            {"name": "Human", "score": 0},
            {"name": "Robot", "score": 0},
        ]
        st.session_state.buttonClicked = ""
        st.session_state.rowClicked = -1
        st.session_state.colClicked = -1
        st.session_state.movesLeft = MAX_ROWS * MAX_COLS
        st.session_state.currentPlayer = 0

    maxit_game()


# Robot starts here!
def roboplay():

    def maxit_game2():
        st.title("Robot Maxit Game :video_game:")
        place2 = st.container(border=True)
        SCOREBOARD = st.empty()
        global LASTBUTTON
        LASTBUTTON = st.empty()
        # Initialize the game
        if not "players" in st.session_state:
            st.session_state.players = [
                {"name": "Human", "score": 0},
                {"name": "Robot", "score": 0},
            ]

        currentPlayer = st.session_state.get("currentPlayer", 0)
        turns = st.empty()
        if currentPlayer == 0:
            turns.write("###### Player: You! " + ":man_in_tuxedo:")
        elif currentPlayer == 1:
            turns.write("###### Player: Robot! " + "🤖")

        SCOREBOARD.write(
            f"You: {st.session_state.players[0]['score']} | Robot: {st.session_state.players[1] ['score']}   "
        )
        if "board" not in st.session_state:
            st.session_state.board = [
                [random.randint(1, 9) for _ in range(MAX_ROWS)] for _ in range(MAX_COLS)
            ]

        if "buttonClicked" not in st.session_state:
            st.session_state["buttonClicked"] = ""
            st.session_state["rowClicked"] = -1
            st.session_state["colClicked"] = -1
            st.session_state["movesLeft"] = MAX_ROWS * MAX_COLS
        disabled_buttons = 0
        with place2:
            for i in range(4):
                cols = st.columns(MAX_COLS)
                for j in range(MAX_ROWS):
                    labels = f"{st.session_state.board[i][j]}"
                    disabled = is_disabled2(i, j)
                    if disabled:
                        disabled_buttons += 1
                    cols[j].button(
                        labels,
                        key=f"btn_{i+MAX_ROWS+1}_{j+MAX_ROWS+1}",
                        on_click=btn_select2,
                        args=(currentPlayer, i, j),
                        disabled=is_disabled2(i, j),
                    )
        if disabled_buttons == MAX_ROWS * MAX_COLS and st.session_state.movesLeft > 0:
            turns.empty()
            ending2()

        elif st.session_state.movesLeft == 0:
            turns.empty()
            ending2()

    def find_max_in_row_and_column(board, row_index, col_index):
        """
        Finds the maximum value in the same row or column, prioritizing row over column if equal.
        Returns the maximum value and its coordinates (row, col).
        """
        # Extract valid values and their positions from the row
        row_values = [
            (board[row_index][col], row_index, col)
            for col in range(len(board[0]))
            if isinstance(board[row_index][col], int)
        ]

        # Extract valid values and their positions from the column
        col_values = [
            (board[row][col_index], row, col_index)
            for row in range(len(board))
            if isinstance(board[row][col_index], int)
        ]

        # Combine all valid moves
        all_values = row_values + col_values

        # Find the maximum value and its position
        if not all_values:
            return None, None, None  # No valid moves left

        max_value, max_row, max_col = max(
            all_values, key=lambda x: x[0]
        )  # Find max by value
        return max_value, max_row, max_col

    def btn_select2(currentPlayer, i, j):
        val = st.session_state["board"][i][j]
        if type(val) is int:
            st.session_state.players[currentPlayer]["score"] += val
            st.session_state["board"][i][j] = ":man_in_tuxedo:"
            st.session_state["rowClicked"] = i
            st.session_state["colClicked"] = j
            st.session_state["buttonClicked"] = val
            st.session_state["movesLeft"] -= 1
            currentPlayer = 1 - currentPlayer
            st.session_state.currentPlayer = currentPlayer
            time.sleep(0.5)
            robot_move()

    def robot_move():
        row_index = st.session_state["rowClicked"]
        col_index = st.session_state["colClicked"]

        max_value, max_row, max_col = find_max_in_row_and_column(
            st.session_state["board"], row_index, col_index
        )

        if max_value is not None:
            st.session_state.players[1]["score"] += max_value
            st.session_state["board"][max_row][max_col] = "🤖"
            st.session_state["rowClicked"] = max_row
            st.session_state["colClicked"] = max_col
            st.session_state["movesLeft"] -= 1
            st.session_state.currentPlayer = 0

    def is_disabled2(i, j):
        if type(st.session_state["board"][i][j]) is not int:
            return True
        if st.session_state["buttonClicked"] == "":
            return False
        elif st.session_state["rowClicked"] == i:
            return False
        elif st.session_state["colClicked"] == j:
            return False
        else:
            return True

    def ending2():
        if st.session_state.players[0]["score"] > st.session_state.players[1]["score"]:
            LASTBUTTON.header(f":green[You win!]")
            st.balloons()
            st.toast(":green[Congratulations, you beat the robot!]")
        elif (
            st.session_state.players[0]["score"] < st.session_state.players[1]["score"]
        ):

            LASTBUTTON.header(f":blue[The robot wins...]")
            st.snow()
            st.toast(":blue[Too bad, you froze to death and the robot beat you.]")
        elif (
            st.session_state.players[0]["score"] == st.session_state.players[1]["score"]
        ):
            LASTBUTTON.subheader("It's a tie!")

        if st.button("Play again?"):
            reset()

    def reset():
        st.session_state.board = [
            [random.randint(1, 9) for _ in range(MAX_ROWS)] for _ in range(MAX_COLS)
        ]
        st.session_state.players = [
            {"name": "Human", "score": 0},
            {"name": "Robot", "score": 0},
        ]
        st.session_state.buttonClicked = ""
        st.session_state.rowClicked = -1
        st.session_state.colClicked = -1
        st.session_state.movesLeft = MAX_ROWS * MAX_COLS
        st.session_state.currentPlayer = 0

    maxit_game2()


def rules():
    st.write(":red[Rule Number 1:]")
    st.markdown(":blue[• You can only click on a number once.]")
    st.write(":red[Rule Number 2:]")
    st.markdown(":blue[• You can only click on a number in the same row or column.]")
    st.write(":red[Rule Number 3:]")
    st.markdown(":blue[• You cannot leave the game without clicking all the numbers.]")
    st.write(":red[Rule Number 4:]")
    st.markdown(":blue[• You cannot purposely lose.]")


pgs = st.navigation(
    [
        st.Page(rules, title="Rules", default=True),
        st.Page(multiplay, title="Multiplayer"),
        st.Page(roboplay, title="Against Robot"),
    ]
)

pgs.run()
