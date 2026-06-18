from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from audio import lesson_to_audio
from database import ensure_database, get_schema, run_query
from lesson_engine import (
    badge_details,
    complete_lesson,
    get_lesson,
    load_progress,
    mixed_lessons,
    validate_lesson,
)

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")


@app.route("/")
def index():
    ensure_database()
    progress = load_progress()
    return render_template(
        "index.html",
        lessons=mixed_lessons(),
        progress=progress,
        badges=badge_details(progress),
        schema=get_schema(),
    )


@app.post("/api/run")
def api_run():
    payload = request.get_json(force=True)
    sql = payload.get("sql", "")
    return jsonify(run_query(sql))


@app.post("/api/check")
def api_check():
    payload = request.get_json(force=True)
    lesson_id = int(payload.get("lesson_id"))
    sql = payload.get("sql", "")
    lesson = get_lesson(lesson_id)
    if not lesson:
        return jsonify({"passed": False, "message": "Lesson not found."}), 404
    query_result = run_query(sql)
    validation = validate_lesson(lesson, sql, query_result)
    if validation["passed"]:
        completion = complete_lesson(lesson_id)
        validation.update(completion)
    return jsonify(validation)


@app.post("/api/audio")
def api_audio():
    payload = request.get_json(force=True)
    lesson_id = int(payload.get("lesson_id"))
    lesson = get_lesson(lesson_id)
    if not lesson:
        return jsonify({"ok": False, "message": "Lesson not found."}), 404
    text = f"Lesson {lesson['id']}: {lesson['title']}. {lesson['story']} Goal: {lesson['goal']} Steps: " + " ".join(lesson["steps"])
    return jsonify(lesson_to_audio(text))


@app.post("/api/reset-db")
def api_reset_db():
    ensure_database(reset=True)
    return jsonify({"ok": True, "message": "Sandbox database reset."})


if __name__ == "__main__":
    ensure_database()
    app.run(debug=True)
