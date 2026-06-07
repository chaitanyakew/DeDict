import sqlite3
import os

oracle_path = "OracleDB/oracle.db"

WORDS_FILE = "words.txt"

MasterDB = "MasterDB"
os.makedirs(MasterDB, exist_ok=True)

MASTER_DBS = {
    "nouns": r"MasterDB\german_nouns.db",
    "verbs": r"MasterDB\german_verbs.db",
    "adjectives": r"MasterDB\german_adjectives.db",
    "adverbs": r"MasterDB\german_adverbs.db",
}


def load_words():

    with open(WORDS_FILE, encoding="utf-8") as f:
        return {
            line.strip()
            for line in f
            if line.strip()
        }


def copy_word_to_oracle(word, table):

    master_conn = sqlite3.connect(MASTER_DBS[table])
    master_cur = master_conn.cursor()

    oracle_conn = sqlite3.connect(oracle_path)
    oracle_cur = oracle_conn.cursor()

    # Get full row
    master_cur.execute(
        f"SELECT * FROM {table} WHERE word = ?",
        (word,)
    )

    row = master_cur.fetchone()

    if row:

        placeholders = ",".join(
            ["?"] * len(row)
        )

        oracle_cur.execute(
            f"""
            INSERT OR IGNORE INTO {table}
            VALUES ({placeholders})
            """,
            row
        )

        oracle_conn.commit()

        print(f"Added {word} -> {table}")

        added = True

    else:
        added = False

    master_conn.close()
    oracle_conn.close()

    return added


def main():

    words = load_words()

    found = 0
    not_found = []

    for word in words:

        inserted = False

        for table in [
            "nouns",
            "verbs",
            "adjectives",
            "adverbs"
        ]:

            if copy_word_to_oracle(word, table):
                found += 1
                inserted = True

        if not inserted:
            not_found.append(word)

    print("\nDone")
    print(f"Found: {found}")
    print(f"Not found: {len(not_found)}")

    if not_found:
        print("\nMissing words:")
        for word in not_found:
            print(word)


if __name__ == "__main__":
    main()

