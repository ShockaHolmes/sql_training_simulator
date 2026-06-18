from database import ensure_database, run_query
from lesson_engine import load_lessons, validate_lesson


def test_lesson_count():
    assert len(load_lessons()) == 100


def test_database_query_runs():
    ensure_database(reset=True)
    result = run_query("SELECT * FROM customers;")
    assert result["ok"] is True
    assert result["row_count"] >= 8


def test_blocks_write_queries():
    result = run_query("DROP TABLE customers;")
    assert result["ok"] is False


def test_lesson_validation():
    lesson = load_lessons()[0]
    result = run_query(lesson["starter_sql"])
    checked = validate_lesson(lesson, lesson["starter_sql"], result)
    assert checked["passed"] is True
