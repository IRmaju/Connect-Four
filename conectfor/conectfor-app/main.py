import streamlit as st
import numpy as np

# Constants
ROW_COUNT = 6
COL_COUNT = 7

# Create board
def create_board():
    return np.zeros((ROW_COUNT, COL_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Horizontal
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    # Vertical
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    # Diagonal /
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    # Diagonal \
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False

def display_board(board):
    st.markdown("### Connect Four")
    for r in reversed(range(ROW_COUNT)):
        cols = st.columns(COL_COUNT)
        for c in range(COL_COUNT):
            if board[r][c] == 0:
                cols[c].markdown("⚪")
            elif board[r][c] == 1:
                cols[c].markdown("🔴")
            else:
                cols[c].markdown("🟡")

# Session state init
if "board" not in st.session_state:
    st.session_state.board = create_board()
    st.session_state.turn = 0
    st.session_state.game_over = False
    st.session_state.message = ""

display_board(st.session_state.board)

# Input buttons for each column
if not st.session_state.game_over:
    col_buttons = st.columns(COL_COUNT)
    for i in range(COL_COUNT):
        if col_buttons[i].button(f"Drop in {i+1}"):
            if is_valid_location(st.session_state.board, i):
                row = get_next_open_row(st.session_state.board, i)
                piece = 1 if st.session_state.turn == 0 else 2
                drop_piece(st.session_state.board, row, i, piece)
                if winning_move(st.session_state.board, piece):
                    st.session_state.message = f"🎉 Player {piece} wins!"
                    st.session_state.game_over = True
                st.session_state.turn ^= 1

st.markdown(f"**{st.session_state.message}**")

if st.button("🔁 Restart Game"):
    st.session_state.board = create_board()
    st.session_state.turn = 0
    st.session_state.game_over = False
    st.session_state.message = ""
