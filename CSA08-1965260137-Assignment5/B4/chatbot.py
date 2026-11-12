"""Basic rule-based chatbot (A5.2). Needs ../B1/aq.db (run B1/store_query.py first). Run: python chatbot.py"""
import os
import re
import sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "B1", "aq.db")


def answer(question, con):
    q = question.lower()
    names = [r[0] for r in con.execute("SELECT name FROM stations")]
    station = next((n for n in names if n.lower() in q), None)
    if re.search(r"\b(hi|hello|hey)\b", q):
        return "Hello! Ask me e.g. 'What is the PM2.5 in Adyar today?'"
    if "pm2.5" in q or "pm25" in q or "air" in q:
        if station is None:
            return "Which station? I know: " + ", ".join(sorted(names))
        day = con.execute("SELECT MAX(day) FROM readings").fetchone()[0]   # 'today' = latest day in DB
        row = con.execute("SELECT ROUND(AVG(pm25),1) FROM readings r JOIN stations s USING(station_id) "
                          "WHERE s.name = ? AND r.day = ?", (station, day)).fetchone()
        return f"The average PM2.5 in {station} on {day} was {row[0]} ug/m3."
    if "worst" in q or "highest" in q:
        row = con.execute("SELECT s.name, ROUND(AVG(pm25),1) m FROM readings r JOIN stations s "
                          "USING(station_id) GROUP BY s.name ORDER BY m DESC LIMIT 1").fetchone()
        return f"The station with the highest mean PM2.5 is {row[0]} ({row[1]} ug/m3)."
    return "Sorry, I did not understand. Try asking about PM2.5 at a station."


if __name__ == "__main__":
    con = sqlite3.connect(DB)
    for q in ["Hello", "What is the PM2.5 in Adyar today?", "air in guindy", "Which station is worst?",
              "What is the PM2.5?", "Will it rain tomorrow?", "pm2.5 in Adyr today"]:
        print("You:", q, "\nBot:", answer(q, con), "\n")
