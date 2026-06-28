import json
import sqlite3
import os
import re

JSONL_FILE = "kaikki.org-dictionary-German.jsonl"
DB_DIR = "MasterDB"
DB_FILE = "german_nouns.db"

os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.join(DB_DIR, DB_FILE)


def get_article(entry):
    """
    Extract der/die/das from noun senses.
    """

    for sense in entry.get("senses", []):
        tags = sense.get("tags", [])

        if "masculine" in tags:
            return "der"

        if "feminine" in tags:
            return "die"

        if "neuter" in tags:
            return "das"

    return ""


def get_plural(entry):
    """
    Extract first plural form.
    """

    for form in entry.get("forms", []):
        tags = form.get("tags", [])

        if "plural" in tags:
            return form.get("form", "")

    return ""


def get_meaning(entry):
    """
    Extract up to 2 clean meanings.
    """

    for sense in entry.get("senses", []):

        glosses = sense.get("glosses", [])

        if not glosses:
            continue

        meaning = glosses[0]

        # Remove explanatory text in parentheses
        meaning = re.sub(r"\([^)]*\)", "", meaning)

        # Split on comma or semicolon
        parts = re.split(r"[;,]", meaning)

        parts = [
            p.strip()
            for p in parts
            if p.strip()
        ]

        # Return first 2 meanings
        return "; ".join(parts[:2])

    return ""


def get_audio(entry):
    """
    Audio priority:

    1. Germany
    2. Germany + Berlin
    3. Any De-* audio
    4. Any audio
    """

    sounds = entry.get("sounds", [])

    # Germany only
    for sound in sounds:

        tags = sound.get("tags", [])

        if tags == ["Germany"]:
            return (
                sound.get("audio", ""),
                sound.get("ogg_url")
                or sound.get("mp3_url")
                or ""
            )

    # Germany + Berlin
    for sound in sounds:

        tags = sound.get("tags", [])

        if "Germany" in tags and "Berlin" in tags:
            return (
                sound.get("audio", ""),
                sound.get("ogg_url")
                or sound.get("mp3_url")
                or ""
            )

    # Generic German audio
    for sound in sounds:

        audio = sound.get("audio", "")

        if audio.startswith("De-"):
            return (
                audio,
                sound.get("ogg_url")
                or sound.get("mp3_url")
                or ""
            )

    # Any audio
    for sound in sounds:

        audio = sound.get("audio")

        if audio:
            return (
                audio,
                sound.get("ogg_url")
                or sound.get("mp3_url")
                or ""
            )

    return "", ""


def create_database():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS nouns (
        word TEXT PRIMARY KEY,
        pos TEXT,
        article TEXT,
        plural TEXT,
        meaning TEXT,
        audio_file TEXT,
        audio_url TEXT
    )
    """)

    count = 0

    seen = set()

    with open(JSONL_FILE, "r", encoding="utf-8") as f:

        for line in f:

            try:
                entry = json.loads(line)

            except Exception:
                continue

            if entry.get("pos") != "noun":
                continue

            word = entry.get("word")

            if not word:
                continue

            article = get_article(entry)
            plural = get_plural(entry)
            meaning = get_meaning(entry)
            audio_file, audio_url = get_audio(entry)

            if word in seen:
                continue

            seen.add(word)

            cur.execute("""
            INSERT OR REPLACE INTO nouns
            (
                word,
                pos,
                article,
                plural,
                meaning,
                audio_file,
                audio_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                word,
                "noun",
                article,
                plural,
                meaning,
                audio_file,
                audio_url
            ))

            count += 1

            if count % 10000 == 0:
                print(f"Imported {count:,} nouns...")

    conn.commit()
    conn.close()

    print(f"\nDone. Imported {count:,} nouns.")
    print(f"Database saved as: {DB_FILE}")

if __name__ == "__main__":
    create_database()