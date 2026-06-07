import sqlite3
import csv
import os

CSV_DIR = "CSVS"
os.makedirs(CSV_DIR, exist_ok=True)

# Configuration

TXT_FILE = "words.txt"

MASTER_DBS = {
    "nouns": r"MasterDB\german_nouns.db",
    "verbs": r"MasterDB\german_verbs.db",
    "adjectives": r"MasterDB\german_adjectives.db",
    "adverbs": r"MasterDB\german_adverbs.db",
}

ORACLE_CSV_FILES = {
    "nouns": r"CSVS\oracle_nouns.csv",
    "verbs": r"CSVS\oracle_verbs.csv",
    "adjectives": r"CSVS\oracle_adjectives.csv",
    "adverbs": r"CSVS\oracle_adverbs.csv"
}

# Helpers

def load_words(txt_file):
    with open(txt_file, encoding="utf-8-sig") as f:
        return {
            line.strip()
            for line in f
            if line.strip()
        }

def existing_words(csv_file):
    """
    Returns words already stored in oracle csv.
    """

    if not os.path.exists(csv_file):
        return set()

    words = set()

    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            words.add(row["word"])

    return words

def append_rows(csv_file, fieldnames, rows):

    file_exists = os.path.exists(csv_file)

    with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(rows)

# Nouns
def process_nouns(words):

    conn = sqlite3.connect(MASTER_DBS["nouns"])
    cur = conn.cursor()

    oracle_words = existing_words(
        ORACLE_CSV_FILES["nouns"]
    )

    rows = []

    for word in words:

        cur.execute("""
            SELECT word,
                   article,
                   plural,
                   meaning
            FROM nouns
            WHERE word = ?
        """, (word,))

        result = cur.fetchone()

        if result and result[0] not in oracle_words:

            rows.append({
                "word": result[0],
                "article": result[1],
                "plural": result[2],
                "meaning": result[3]
            })

    conn.close()

    append_rows(
        ORACLE_CSV_FILES["nouns"],
        ["word", "article", "plural", "meaning"],
        rows
    )

    return len(rows)

# Verbs
def process_verbs(words):

    conn = sqlite3.connect(MASTER_DBS["verbs"])
    cur = conn.cursor()

    oracle_words = existing_words(
        ORACLE_CSV_FILES["verbs"]
    )

    rows = []

    for word in words:

        cur.execute("""
            SELECT *
            FROM verbs
            WHERE word = ?
        """, (word,))

        result = cur.fetchone()

        if result and result[0] not in oracle_words:

            rows.append({
                "word": result[0],
                "meaning": result[2],
                "preterite": result[3],
                "participle": result[4],
                "auxiliary": result[5],
                "regularity": result[6],
                "separable": result[7],
                "example_de": result[8],
                "example_en": result[9]
            })

    conn.close()

    append_rows(
        ORACLE_CSV_FILES["verbs"],
        [
            "word",
            "meaning",
            "preterite",
            "participle",
            "auxiliary",
            "regularity",
            "separable",
            "example_de",
            "example_en"
        ],
        rows
    )

    return len(rows)

# Adjectives
def process_adjectives(words):

    conn = sqlite3.connect(MASTER_DBS["adjectives"])
    cur = conn.cursor()

    oracle_words = existing_words(
        ORACLE_CSV_FILES["adjectives"]
    )

    rows = []

    for word in words:

        cur.execute("""
            SELECT *
            FROM adjectives
            WHERE word = ?
        """, (word,))

        result = cur.fetchone()

        if result and result[0] not in oracle_words:

            rows.append({
                "word": result[0],
                "meaning": result[2],
                "comparative": result[3],
                "superlative": result[4],
                "example_de": result[5],
                "example_en": result[6]
            })

    conn.close()

    append_rows(
        ORACLE_CSV_FILES["adjectives"],
        [
            "word",
            "meaning",
            "comparative",
            "superlative",
            "example_de",
            "example_en"
        ],
        rows
    )

    return len(rows)

# Adverbs
def process_adverbs(words):

    conn = sqlite3.connect(MASTER_DBS["adverbs"])
    cur = conn.cursor()

    oracle_words = existing_words(
        ORACLE_CSV_FILES["adverbs"]
    )

    rows = []

    for word in words:

        cur.execute("""
            SELECT *
            FROM adverbs
            WHERE word = ?
        """, (word,))

        result = cur.fetchone()

        if result and result[0] not in oracle_words:

            rows.append({
                "word": result[0],
                "meaning": result[2],
                "example_de": result[3],
                "example_en": result[4]
            })

    conn.close()

    append_rows(
        ORACLE_CSV_FILES["adverbs"],
        [
            "word",
            "meaning",
            "example_de",
            "example_en"
        ],
        rows
    )

    return len(rows)


# Main
def main():

    words = load_words(TXT_FILE)

    nouns_added = process_nouns(words)
    verbs_added = process_verbs(words)
    adjectives_added = process_adjectives(words)
    adverbs_added = process_adverbs(words)

    print(f"Nouns added: {nouns_added}")
    print(f"Verbs added: {verbs_added}")
    print(f"Adjectives added: {adjectives_added}")
    print(f"Adverbs added: {adverbs_added}")

if __name__ == "__main__":
    main()