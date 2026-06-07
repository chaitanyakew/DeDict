import sqlite3
import os

DB_DIR = "OracleDB"
ORACLE_DB = "oracle.db"

os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.join(DB_DIR, ORACLE_DB)

def create_oracle_db_schema():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # --------------------
    # Nouns
    # --------------------

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

    # --------------------
    # Verbs
    # --------------------

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

    # --------------------
    # Adjectives
    # --------------------

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

    # --------------------
    # Adverbs
    # --------------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS adverbs (
        word TEXT PRIMARY KEY,
        pos TEXT,
        meaning TEXT,
        example_de TEXT,
        example_en TEXT,
        audio_file TEXT,
        audio_url TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("oracle.db created.")


if __name__ == "__main__":
    create_oracle_db_schema()