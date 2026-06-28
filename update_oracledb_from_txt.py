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

# loads words from .txt file
def load_words():

    with open(WORDS_FILE, encoding="utf-8") as f:
        return {
            line.strip()
            for line in f
            if line.strip()
        }

# Check for already existing words in oracle
def load_existing_oracle_words(table):
    """Returns words already present in oracle.db for a given table."""
    oracle_conn = sqlite3.connect(oracle_path)
    oracle_cur = oracle_conn.cursor()
    oracle_cur.execute(f"SELECT word FROM {table}")
    words = {row[0] for row in oracle_cur.fetchall()}
    oracle_conn.close()
    return words

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

    words = load_words() # loads words from .txt file

    found = 0
    not_found = []
    already_present = 0

    # Pre-load existing words from oracle.db per table
    existing = {
        table: load_existing_oracle_words(table)
        for table in ["nouns", "verbs", "adjectives", "adverbs"]
    }

    for word in words:

        inserted = False

        for table in [
            "nouns",
            "verbs",
            "adjectives",
            "adverbs"
        ]:
            # Skip if already in oracle.db
            if word in existing[table]:
                inserted = True
                already_present+= 1
                continue

            if copy_word_to_oracle(word, table):
                found += 1
                inserted = True

        if not inserted:
            not_found.append(word)

    print("\nDone")
    print(f"Already Present: {already_present}")
    print(f"Newly Added: {found}")
    print(f"Not found: {len(not_found)}")

    if not_found:
        print("\nMissing words:")
        for word in not_found:
            print(word)
    print("\n")

if __name__ == "__main__":
    main()

