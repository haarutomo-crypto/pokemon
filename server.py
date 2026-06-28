from flask import Flask, render_template, request, jsonify
from app import BattleTracker
import json
import os

app = Flask(__name__)
tracker = BattleTracker("records.jsonl")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/records", methods=["GET"])
def get_records():
    keyword = request.args.get("q", "")
    records = tracker.search_records(keyword)
    return jsonify(records)

@app.route("/api/records", methods=["POST"])
def create_record():
    data = request.json
    tracker.save_record(
        name=data.get("name", ""),
        nature=data.get("nature", ""),
        hp=data.get("hp", 0),
        attack=data.get("attack", 0),
        defense=data.get("defense", 0),
        sp_atk=data.get("sp_atk", 0),
        sp_def=data.get("sp_def", 0),
        speed=data.get("speed", 0),
        ev_hp=data.get("ev_hp", 0),
        ev_attack=data.get("ev_attack", 0),
        ev_defense=data.get("ev_defense", 0),
        ev_sp_atk=data.get("ev_sp_atk", 0),
        ev_sp_def=data.get("ev_sp_def", 0),
        ev_speed=data.get("ev_speed", 0),
        notes_text=data.get("notes", "")
    )
    return jsonify({"status": "success"}), 201

@app.route("/api/records/<record_id>", methods=["PUT"])
def update_record(record_id):
    data = request.json
    tracker.update_record(
        record_id=record_id,
        name=data.get("name", ""),
        nature=data.get("nature", ""),
        hp=data.get("hp", 0),
        attack=data.get("attack", 0),
        defense=data.get("defense", 0),
        sp_atk=data.get("sp_atk", 0),
        sp_def=data.get("sp_def", 0),
        speed=data.get("speed", 0),
        ev_hp=data.get("ev_hp", 0),
        ev_attack=data.get("ev_attack", 0),
        ev_defense=data.get("ev_defense", 0),
        ev_sp_atk=data.get("ev_sp_atk", 0),
        ev_sp_def=data.get("ev_sp_def", 0),
        ev_speed=data.get("ev_speed", 0),
        notes_text=data.get("notes", "")
    )
    return jsonify({"status": "success"})

@app.route("/api/records/<record_id>", methods=["DELETE"])
def delete_record(record_id):
    tracker.delete_record(record_id)
    return jsonify({"status": "success"})

@app.route("/api/suggestions", methods=["GET"])
def get_suggestions():
    names = tracker.get_all_names()
    return jsonify(names)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
