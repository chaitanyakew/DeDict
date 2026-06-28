import sqlite3
import csv
import os

CSV_DIR = "CSVS"
os.makedirs(CSV_DIR, exist_ok=True)

ORACLE_DB = r"OracleDB\oracle.db"

CSV_FILES = {
    "nouns": r"CSVS\oracle_nouns.csv",
    "verbs": r"CSVS\oracle_verbs.csv",
    "adjectives": r"CSVS\oracle_adjectives.csv",
    "adverbs": r"CSVS\oracle_adverbs.csv",
}

FIELDNAMES = {
    "nouns": ["word", "article", "plural", "meaning"],
    "verbs": ["word", "meaning", "preterite", "participle", "auxiliary", "regularity", "separable", "example_de", "example_en"],
    "adjectives": ["word", "meaning", "comparative", "superlative", "example_de", "example_en"],
    "adverbs": ["word", "meaning", "example_de", "example_en"],
}

ORACLE_CSV_FILES = {
    "nouns": r"CSVS\oracle_nouns.csv",
    "verbs": r"CSVS\oracle_verbs.csv",
    "adjectives": r"CSVS\oracle_adjectives.csv",
    "adverbs": r"CSVS\oracle_adverbs.csv"
}

QUERIES = {
    "nouns":      "SELECT word, article, plural, meaning FROM nouns",
    "verbs":      "SELECT word, meaning, preterite, participle, auxiliary, regularity, separable, example_de, example_en FROM verbs",
    "adjectives": "SELECT word, meaning, comparative, superlative, example_de, example_en FROM adjectives",
    "adverbs":    "SELECT word, meaning, example_de, example_en FROM adverbs",
}


def export_table_to_csv(table):

    conn = sqlite3.connect(ORACLE_DB)
    cur = conn.cursor()

    cur.execute(QUERIES[table])
    rows = cur.fetchall()
    conn.close()

    csv_file = CSV_FILES[table]
    fieldnames = FIELDNAMES[table]

    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow(dict(zip(fieldnames, row)))

    return len(rows)

def export_nouns_to_csv():

    conn = sqlite3.connect(ORACLE_DB)
    cur = conn.cursor()

    cur.execute("SELECT word, article, plural, meaning FROM nouns")
    rows = cur.fetchall()
    conn.close()

    csv_file = CSV_FILES["nouns"]
    fieldnames = ["article", "singular", "plural", "meaning"]

    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            word, article, plural, meaning = row

            writer.writerow({
                "article": article,
                "singular": word,
                "plural": f"die {plural}" if plural else "",
                "meaning": meaning
            })

    return len(rows)


def main():

    export_nouns_to_csv()
    print(f"Nouns csv created.")
    for table in ["verbs", "adjectives", "adverbs"]:
        count = export_table_to_csv(table)
        print(f"{table.capitalize()} csv created.")


if __name__ == "__main__":
    main()