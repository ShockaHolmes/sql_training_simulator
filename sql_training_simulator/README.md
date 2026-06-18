# SQL Quest Academy

An interactive Python + SQLite training simulator that teaches SQL step by step. Learners read guided lessons, run SQL against a real SQLite database, see results immediately, get helpful error feedback, earn badges, and can optionally listen to lessons through the ElevenLabs Text-to-Speech API.

## Features

- 100 SQL lessons from beginner to advanced
- Real SQLite sandbox database with customers, products, orders, employees, departments, projects, tickets, students, courses, and more
- Interactive query runner with visible results
- Lesson validation checks expected SQL concepts
- Friendly error explanations for common SQL mistakes
- Badges and XP for completed lessons
- Randomized lesson mix every new session
- Progress saved locally in `data/progress.json`
- Optional ElevenLabs audio narration
- Teacher-friendly design for guided learning

## Tech Stack

- Python 3.11+
- Flask
- SQLite
- Pandas
- ElevenLabs API optional

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
python app.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

## Optional ElevenLabs Audio

Create a `.env` file:

```env
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

Then use the **Read Lesson Aloud** button in the app.

The app will still work without ElevenLabs. If no key is provided, the audio feature returns a helpful message instead of breaking.

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial SQL Quest Academy simulator"
git branch -M main
git remote add origin https://github.com/ShockaHolmes/sql-quest-academy.git
git push -u origin main
```

Create the repo first on GitHub using the name `sql-quest-academy`.

## Folder Structure

```text
sql-quest-academy/
├── app.py
├── database.py
├── lesson_engine.py
├── audio.py
├── requirements.txt
├── lessons/
│   └── lessons.json
├── app/
│   └── static + templates
├── data/
│   └── generated at runtime
└── tests/
```

## Lesson Topics

The lesson set covers SELECT, WHERE, sorting, aggregation, joins, subqueries, CASE, CTEs, window functions, schema design, indexes, transactions, views, data cleaning, reporting queries, and analytics-style SQL.
