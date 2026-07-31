import sqlite3
import uuid
import os
from flask import Flask, request, jsonify, g

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "tasks.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            priority TEXT,
            completed INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"})


@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    db = get_db()

    if request.method == "GET":
        rows = db.execute("SELECT * FROM tasks").fetchall()
        return jsonify(
            [
                {
                    "id": row["id"],
                    "title": row["title"],
                    "priority": row["priority"],
                    "completed": bool(row["completed"]),
                }
                for row in rows
            ]
        )

    # POST
    data = request.get_json(silent=True) or {}

    if not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    task_id = str(uuid.uuid4())
    priority = data.get("priority", "medium")

    db.execute(
        "INSERT INTO tasks (id, title, priority) VALUES (?, ?, ?)",
        (task_id, data["title"], priority),
    )
    db.commit()

    return (
        jsonify(
            {
                "id": task_id,
                "title": data["title"],
                "priority": priority,
                "completed": False,
            }
        ),
        201,
    )


@app.route("/tasks/<task_id>/complete", methods=["POST"])
def complete_task(task_id):
    db = get_db()

    row = db.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()

    db.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
    )
    db.commit()

    return jsonify(
        {
            "id": row["id"],
            "title": row["title"],
            "priority": row["priority"],
            "completed": True,
        }
    )


@app.errorhandler(405)
def handle_405(e):
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
