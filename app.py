from flask import Flask, render_template, request, session, redirect, url_for
import json
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session management

# Load player data
with open("players.json", "r") as f:
    PLAYERS = json.load(f)

# Load or initialize high scores
HIGH_SCORES_FILE = "high_scores.json"
if os.path.exists(HIGH_SCORES_FILE):
    with open(HIGH_SCORES_FILE, "r") as f:
        HIGH_SCORES = json.load(f)
else:
    HIGH_SCORES = {}

def save_high_scores():
    with open(HIGH_SCORES_FILE, "w") as f:
        json.dump(HIGH_SCORES, f)

@app.route("/", methods=["GET", "POST"])
def game():
    # Initialize session for new user
    if "round" not in session:
        session["round"] = 1
        session["score"] = 0
        session["used_players"] = []
        session["last_skipped"] = False
        session["user_id"] = str(random.randint(1000, 9999))  # Simple user ID

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        skip = "skip" in request.form

        current_player = PLAYERS[session["used_players"][-1]] if session["used_players"] else None

        if user_answer == "i give up":
            return end_game()

        if skip and not session["last_skipped"]:
            session["last_skipped"] = True
        elif skip and session["last_skipped"]:
            return render_template("index.html", round=session["round"], player=current_player["name"],
                                   score=session["score"], message="You can't skip twice in a row!")
        else:
            session["last_skipped"] = False
            if user_answer in [c.lower() for c in current_player["clubs"]]:
                session["score"] += 3
                message = f"Correct club! +3 points"
            elif user_answer in [n.lower() for n in current_player["national_teams"]]:
                session["score"] += 2
                message = f"Correct national team! +2 points"
            else:
                session["score"] -= 1
                message = f"Wrong! -1 point. {current_player['name']} played for {', '.join(current_player['clubs'])} and {', '.join(current_player['national_teams'])}"

        session["round"] += 1
        if session["round"] > 20:
            return end_game()

    # Select a new player
    available_players = [p for p in range(len(PLAYERS)) if p not in session["used_players"]]
    if not available_players:
        return end_game()  # Shouldn't happen with enough players
    new_player_idx = random.choice(available_players)
    session["used_players"].append(new_player_idx)
    
    return render_template("index.html", round=session["round"], player=PLAYERS[new_player_idx]["name"],
                           score=session["score"], message=message if "message" in locals() else "")

def end_game():
    final_score = session["score"]
    user_id = session["user_id"]

    # Determine result message
    if final_score == 60:
        result = "GOATed ball knowledge"
    elif 40 <= final_score <= 55:
        result = "W ball knowledge"
    elif 20 <= final_score <= 39:
        result = "Man U level ball knowledge"
    else:
        result = "You're fighting relegation"

    # Check for new high score
    old_high = HIGH_SCORES.get(user_id, 0)
    record_message = "New personal record!" if final_score > old_high else ""
    if final_score > old_high:
        HIGH_SCORES[user_id] = final_score
        save_high_scores()

    session.clear()  # Reset session
    return render_template("result.html", score=final_score, result=result, record_message=record_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)