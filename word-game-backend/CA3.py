from flask import Flask, render_template, request, request, redirect, jsonify
import os
import logic 
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'SECRET_KEY'

@app.route("/")
def start_screen():
    return jsonify({"status": "ok"})

@app.post("/input")
def input_screen():
    sourceWord = logic.getSourceWord()
    startTime = time.time()
    return jsonify({
        "sourceWord": sourceWord,
        "startTime": startTime,
    })

@app.post("/process_pattern")
def process_pattern():
    data = request.get_json()
    attempt = data["attempt"]
    startTime = data["startTime"]
    timeTaken = time.time() - startTime
    result = logic.applyRuleset(data["sourceWord"], attempt, timeTaken)
    attemptTime = result[2]
    return jsonify({
        "result": result[0],
        "win": result[1],
        "attemptTime": attemptTime,
        "attempt": attempt
    })

@app.post("/enter_details")
def enter_details():
    data = request.get_json()
    logic.enterToDatabase(
        data["username"],
        data["sourceWord"],
        data["win"],
        data["attempt"],
        data["attemptTime"]
    )
    return jsonify({"status": "ok"})

@app.get("/top10")
def show_high_scores():
    high_scores = logic.getHighScores()
    return jsonify([{"time": h[0], "who": h[1], "sourceWord": h[2], 
                     "attempt": h[3]} for h in high_scores])