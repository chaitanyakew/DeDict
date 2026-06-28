import json
import sqlite3
import os

JSONL_FILE = "kaikki.org-dictionary-German.jsonl"
DB_DIR = "MasterDB"
DB_FILE = "german_adjectives.db"

os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.join(DB_DIR, DB_FILE)

def get_meaning(entry):

    for sense in entry.get("senses", []):

        glosses = sense.get("glosses", [])

        if not glosses:
            continue

        meaning = glosses[0]

        if "," in meaning:
            meaning = meaning.split(",")[0]

        if ";" in meaning:
            meaning = meaning.split(";")[0]

        return meaning.strip()

    return ""

def get_comparative(entry):
    """
    Extract comparative form.
    """

    for form in entry.get("forms", []):

        if form.get("tags") == ["comparative"]:
            return form.get("form", "")

    return ""

def get_superlative(entry):
    """
    Extract superlative form.
    """

    for form in entry.get("forms", []):

        if form.get("tags") == ["superlative"]:
            return form.get("form", "")

    return ""

def get_example(entry):
    """
    Prefer:
    1. type == example + translation
    2. any translated example
    3. any German example
    """

    fallback_de = ""
    fallback_en = ""

    # Pass 1: proper examples with translation
    for sense in entry.get("senses", []):

        for ex in sense.get("examples", []):

            if ex.get("type") != "example":
                continue

            de = ex.get("text", "").strip()
            en = (
                ex.get("translation")
                or ex.get("english")
                or ""
            ).strip()

            if de and en:
                return de, en

    # Pass 2: any translated example
    for sense in entry.get("senses", []):

        for ex in sense.get("examples", []):

            de = ex.get("text", "").strip()
            en = (
                ex.get("translation")
                or ex.get("english")
                or ""
            ).strip()

            if de and en:
                return de, en

            if de and not fallback_de:
                fallback_de = de
                fallback_en = en

    return fallback_de, fallback_en

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
    CREATE TABLE IF NOT EXISTS adjectives (
        word TEXT PRIMARY KEY,
        pos TEXT,
        meaning TEXT,
        comparative TEXT,
        superlative TEXT,
        example_de TEXT,
        example_en TEXT,
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

            if entry.get("pos") not in ("adj", "adjective"):
                continue

            word = entry.get("word")

            if not word:
                continue

            # Skip duplicates
            key = (word, "adj")

            if key in seen:
                continue

            seen.add(key)

            meaning = get_meaning(entry)
            comparative = get_comparative(entry)
            superlative = get_superlative(entry)

            example_de, example_en = get_example(entry)

            audio_file, audio_url = get_audio(entry)

            cur.execute("""
            INSERT OR REPLACE INTO adjectives
            (
                word,
                pos,
                meaning,
                comparative,
                superlative,
                example_de,
                example_en,
                audio_file,
                audio_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                word,
                "adj",
                meaning,
                comparative,
                superlative,
                example_de,
                example_en,
                audio_file,
                audio_url
            ))

            count += 1

            if count % 10000 == 0:
                print(f"Imported {count:,} adjectives...")

    conn.commit()
    conn.close()

    print(f"\nDone. Imported {count:,} adjectives.")
    print(f"Database saved as: {db_path}")

if __name__ == "__main__":
    create_database()