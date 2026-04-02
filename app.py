from flask import Flask, render_template, jsonify, request, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [2, 4, 6],              # diagonals
    ]
    for combo in wins:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], combo
    return None, None


def minimax(board, is_maximizing):
    winner, _ = check_winner(board)
    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if all(cell for cell in board):
        return 0

    if is_maximizing:
        best = -float("inf")
        for i in range(9):
            if not board[i]:
                board[i] = "O"
                score = minimax(board, False)
                board[i] = None
                best = max(best, score)
        return best
    else:
        best = float("inf")
        for i in range(9):
            if not board[i]:
                board[i] = "X"
                score = minimax(board, True)
                board[i] = None
                best = min(best, score)
        return best


def best_ai_move(board):
    best_score = -float("inf")
    move = None
    for i in range(9):
        if not board[i]:
            board[i] = "O"
            score = minimax(board, False)
            board[i] = None
            if score > best_score:
                best_score = score
                move = i
    return move


@app.route("/")
def index():
    session["board"] = [None] * 9
    session["mode"] = "pvp"
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = session.get("board", [None] * 9)
    mode = session.get("mode", "pvp")
    idx = data.get("index")
    player = data.get("player")

    if board[idx] is not None:
        return jsonify({"error": "Cell taken"}), 400

    board[idx] = player
    session["board"] = board

    winner, combo = check_winner(board)
    if winner:
        session["board"] = [None] * 9
        return jsonify({"board": board, "winner": winner, "combo": combo})

    if all(cell for cell in board):
        session["board"] = [None] * 9
        return jsonify({"board": board, "draw": True})

    if mode == "ai" and player == "X":
        ai_idx = best_ai_move(board)
        if ai_idx is not None:
            board[ai_idx] = "O"
            session["board"] = board
            winner, combo = check_winner(board)
            if winner:
                session["board"] = [None] * 9
                return jsonify({"board": board, "winner": winner, "combo": combo, "ai_move": ai_idx})
            if all(cell for cell in board):
                session["board"] = [None] * 9
                return jsonify({"board": board, "draw": True, "ai_move": ai_idx})
            return jsonify({"board": board, "ai_move": ai_idx})

    return jsonify({"board": board})


@app.route("/reset", methods=["POST"])
def reset():
    data = request.json
    session["board"] = [None] * 9
    session["mode"] = data.get("mode", "pvp")
    return jsonify({"board": session["board"], "mode": session["mode"]})


if __name__ == "__main__":
    app.run(debug=True)
