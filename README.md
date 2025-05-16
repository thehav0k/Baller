# Baller ⚽

**Baller** is a web-based football quiz game built with Flask. It challenges your "ball knowledge" by asking you to name clubs or national teams associated with football players. Perfect for football fans who want to test themselves or compete with friends!

## 🎮 Gameplay

- The game has **20 rounds**.
- Each round, you're shown the **name of a football player**.
- You answer with either:
  - A **club** the player has played for → 🟢 +3 points  
  - A **national team** they’ve played for → 🟢 +2 points  
- ❌ Wrong answers → 🔴 -1 point
- ⏭️ You can **skip** a round, but **not two in a row**.
- Type `"I give up"` to end the game early.

## 🧠 Scoring Breakdown

After 20 rounds (or early surrender), your total score determines your rating:

| Score Range | Rating Title                   |
|-------------|--------------------------------|
| 60          | 🐐 GOATed ball knowledge        |
| 40–55       | ✅ W ball knowledge              |
| 20–39       | 😬 Man U level ball knowledge   |
| Below 20    | ⚠️ You're fighting relegation   |

Your **personal high score** is tracked across sessions using a unique random ID.

## 📦 Data Files

- `players.json`: Player data including clubs and national teams.
- `high_scores.json`: Stores high scores for each user.


## ✨ Example Round

1. You're shown: `Cristiano Ronaldo`
2. You type: `real madrid` → ✅ +3 points
3. Next round begins…

Good luck, and may your ball knowledge reign supreme! 👑
