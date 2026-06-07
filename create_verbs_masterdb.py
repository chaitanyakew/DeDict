import json
import sqlite3
import re
import os

JSONL_FILE = "kaikki.org-dictionary-German.jsonl"
DB_DIR = "MasterDB"
DB_FILE = "german_verbs.db"

os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.join(DB_DIR, DB_FILE)

INSEPARABLE_PREFIXES = {
    "be",
    "emp",
    "ent",
    "er",
    "ge",
    "miss",
    "ver",
    "zer"
}

SEPARABLE_PREFIXES = {
    "ab",
    "an",
    "auf",
    "aus",
    "bei",
    "ein",
    "fest",
    "fort",
    "her",
    "hin",
    "los",
    "mit",
    "nach",
    "vor",
    "weg",
    "wieder",
    "zu",
    "zurück",
    "zusammen"
}

def get_meaning(entry):

    for sense in entry.get("senses", []):

        glosses = sense.get("glosses", [])

        if not glosses:
            continue

        meaning = glosses[0]

        meaning = re.sub(r"\([^)]*\)", "", meaning)

        return "; ".join(
            part.strip()
            for part in meaning.split(",")
            if part.strip()
        )

    return ""

def get_preterite(entry):
    """
    Example:
    wohnen -> wohnte
    gehen -> ging
    aufstehen -> stand auf
    """

    for form in entry.get("forms", []):

        tags = form.get("tags", [])

        if (
            "preterite" in tags
            and "first-person" in tags
            and "singular" in tags
        ):
            return form.get("form", "")

    return ""

def get_participle(entry):
    """
    Example:
    gewohnt
    gegangen
    aufgestanden
    """

    for form in entry.get("forms", []):

        tags = form.get("tags", [])

        if (
            "participle" in tags
            and "past" in tags
        ):
            return form.get("form", "")

    return ""

def get_auxiliary(entry):

    values = set()

    for form in entry.get("forms", []):

        if "auxiliary" in form.get("tags", []):

            aux = form.get("form", "").strip()

            if aux in ("haben", "sein", "haben or sein"):
                values.add(aux)

    if "haben or sein" in values:
        return "haben or sein"

    if values == {"haben", "sein"}:
        return "haben or sein"

    if values == {"haben"}:
        return "haben"

    if values == {"sein"}:
        return "sein"

    return ""

def get_regularity(entry):

    for sense in entry.get("senses", []):

        tags = sense.get("tags", [])

        if "irregular" in tags:
            return "irregular"

        if "strong" in tags:
            return "irregular"

    return "regular"

def get_separable(entry):

    for template in entry.get("etymology_templates", []):

        if template.get("name") != "prefix":
            continue

        prefix = template.get("args", {}).get("2", "").lower()

        if prefix in INSEPARABLE_PREFIXES:
            return "inseparable"

        if prefix in SEPARABLE_PREFIXES:
            return "separable"

    return "simple"

def get_example(entry):

    fallback_de = ""

    for sense in entry.get("senses", []):

        for example in sense.get("examples", []):

            german = example.get("text", "").strip()

            english = (
                example.get("translation")
                or example.get("english")
                or ""
            ).strip()

            if german and english:
                return german, english

            if german and not fallback_de:
                fallback_de = german

    return fallback_de, ""

def get_audio_file_name(entry):
    """
    Prefer:
    1. Germany recording
    2. Generic recording
    3. Any recording
    """

    generic = None
    fallback = None

    for sound in entry.get("sounds", []):

        audio_file = sound.get("audio")

        if not audio_file:
            continue

        tags = sound.get("tags", [])

        if "Germany" in tags:
            return audio_file

        if not tags and generic is None:
            generic = audio_file

        if fallback is None:
            fallback = audio_file

    return generic or fallback or ""

def get_audio_file_url(entry):
    """
    Prefer:
    1. Germany recording
    2. Generic recording
    3. Any recording
    """

    generic = None
    fallback = None

    for sound in entry.get("sounds", []):

        audio_url = sound.get("ogg_url")

        if not audio_url:
            continue

        tags = sound.get("tags", [])

        if "Germany" in tags:
            return audio_url

        if not tags and generic is None:
            generic = audio_url

        if fallback is None:
            fallback = audio_url

    return generic or fallback or ""

def create_database():

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS verbs (
        word TEXT PRIMARY KEY,
        pos TEXT,
        meaning TEXT,
        preterite TEXT,
        participle TEXT,
        auxiliary TEXT,
        regularity TEXT,
        separable TEXT,
        example_de TEXT,
        example_en TEXT,
        audio_file_name TEXT,
        audio_file_url TEXT
    )
    """)

    count = 0

    with open(JSONL_FILE, "r", encoding="utf-8") as f:

        for line in f:

            try:
                entry = json.loads(line)
            except Exception:
                continue

            if entry.get("pos") != "verb":
                continue

            word = entry.get("word")

            if not word:
                continue

            meaning = get_meaning(entry)
            preterite = get_preterite(entry)
            participle = get_participle(entry)
            auxiliary = get_auxiliary(entry)
            regularity = get_regularity(entry)
            separable = get_separable(entry)
            example_de, example_en = get_example(entry)
            audio_file_name = get_audio_file_name(entry)
            audio_file_url = get_audio_file_url(entry)

            cur.execute("""
            INSERT OR REPLACE INTO verbs (
                word,
                pos,
                meaning,
                preterite,
                participle,
                auxiliary,
                regularity,
                separable,
                example_de,
                example_en,
                audio_file_name,
                audio_file_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                word,
                "verb",
                meaning,
                preterite,
                participle,
                auxiliary,
                regularity,
                separable,
                example_de,
                example_en,
                audio_file_name,
                audio_file_url
            ))

            count += 1

            if count % 5000 == 0:
                print(f"Imported {count:,} verbs...")

    conn.commit()
    conn.close()

    print(f"\nDone. Imported {count:,} verbs.")
    print(f"Database saved as: {db_path}")

if __name__ == "__main__":
    create_database()