# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
pip install flask
python app.py
```

The server starts at `http://127.0.0.1:5000` in debug mode.

## Architecture

This is a single-page Flask app with two files:

- [app.py](app.py) — Flask backend with three routes (`/`, `/move`, `/reset`) and server-side game logic. Board state is stored in the Flask session as a list of 9 elements (`None | "X" | "O"`). The AI uses an unmodified minimax algorithm, making it unbeatable.
- [templates/index.html](templates/index.html) — Single HTML file with all CSS and JS inline. The frontend manages turn tracking, scores, and UI state; the backend is the source of truth for the board.

## Game Modes

- **PvP**: Both players click alternately; frontend tracks whose turn it is.
- **vs AI**: Player is always X. After each X move, the `/move` endpoint runs minimax and returns the AI's move (`ai_move` index) in the same response.

## Key Design Details

- Session resets the board on game over (win or draw) server-side, so `/reset` is only needed for "New Game".
- `check_winner` returns both the winner symbol and the winning cell combo (used by the frontend to highlight cells).
- The frontend score counter is client-side only and resets on page refresh.
