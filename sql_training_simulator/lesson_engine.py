from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

LESSON_PATH = Path("lessons/lessons.json")
PROGRESS_PATH = Path("data/progress.json")

BADGES = [
    {"id": "first_query", "name": "First Query", "description": "Complete your first SQL lesson.", "threshold": 1},
    {"id": "filter_finder", "name": "Filter Finder", "description": "Complete 5 lessons.", "threshold": 5},
    {"id": "join_jumper", "name": "Join Jumper", "description": "Complete 15 lessons.", "threshold": 15},
    {"id": "aggregate_ace", "name": "Aggregate Ace", "description": "Complete 30 lessons.", "threshold": 30},
    {"id": "cte_champion", "name": "CTE Champion", "description": "Complete 50 lessons.", "threshold": 50},
    {"id": "window_wizard", "name": "Window Wizard", "description": "Complete 75 lessons.", "threshold": 75},
    {"id": "sql_master", "name": "SQL Master", "description": "Complete all 100 lessons.", "threshold": 100},
]


def load_lessons() -> list[dict[str, Any]]:
    return json.loads(LESSON_PATH.read_text())


def get_lesson(lesson_id: int) -> dict[str, Any] | None:
    for lesson in load_lessons():
        if lesson["id"] == lesson_id:
            return lesson
    return None


def mixed_lessons() -> list[dict[str, Any]]:
    lessons = load_lessons()
    beginner = [lesson for lesson in lessons if lesson["level"] == "beginner"]
    intermediate = [lesson for lesson in lessons if lesson["level"] == "intermediate"]
    advanced = [lesson for lesson in lessons if lesson["level"] == "advanced"]
    random.shuffle(beginner)
    random.shuffle(intermediate)
    random.shuffle(advanced)
    mixed = []
    while beginner or intermediate or advanced:
        for bucket in (beginner, intermediate, advanced):
            if bucket:
                mixed.append(bucket.pop())
    return mixed


def load_progress() -> dict[str, Any]:
    PROGRESS_PATH.parent.mkdir(exist_ok=True)
    if not PROGRESS_PATH.exists():
        return {"completed": [], "xp": 0, "badges": []}
    return json.loads(PROGRESS_PATH.read_text())


def save_progress(progress: dict[str, Any]) -> None:
    PROGRESS_PATH.parent.mkdir(exist_ok=True)
    PROGRESS_PATH.write_text(json.dumps(progress, indent=2))


def validate_lesson(lesson: dict[str, Any], sql: str, query_result: dict[str, Any]) -> dict[str, Any]:
    if not query_result.get("ok"):
        return {"passed": False, "message": "Fix the SQL error first, then try checking the lesson again."}

    lowered = " ".join(sql.lower().replace("\n", " ").split())
    missing = []
    for required in lesson.get("requires", []):
        if required.lower() not in lowered:
            missing.append(required)

    if missing:
        return {
            "passed": False,
            "message": f"You are close. Your query should include: {', '.join(missing)}."
        }

    if lesson.get("min_rows") is not None and query_result.get("row_count", 0) < lesson["min_rows"]:
        return {"passed": False, "message": "Your query ran, but it returned fewer rows than expected. Check the filters or joins."}

    return {"passed": True, "message": "Great work. Lesson complete!"}


def complete_lesson(lesson_id: int) -> dict[str, Any]:
    progress = load_progress()
    if lesson_id not in progress["completed"]:
        progress["completed"].append(lesson_id)
        progress["xp"] += 10

    completed_count = len(progress["completed"])
    earned = []
    for badge in BADGES:
        if completed_count >= badge["threshold"] and badge["id"] not in progress["badges"]:
            progress["badges"].append(badge["id"])
            earned.append(badge)

    save_progress(progress)
    return {"progress": progress, "earned": earned}


def badge_details(progress: dict[str, Any]) -> list[dict[str, Any]]:
    earned = set(progress.get("badges", []))
    return [{**badge, "earned": badge["id"] in earned} for badge in BADGES]
