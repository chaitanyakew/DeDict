# DeDict: Your Own Oracle

## Purpose

A language teacher once told me that creating your own vocabulary deck is far more effective than downloading someone else's. The words you personally encounter in class, books, conversations, and exercises are the words most relevant to your learning journey. Having a curated collection of these words significantly improves retention and long-term recall.

The problem is that maintaining such a collection manually is tedious and time-consuming.

**DeDict** aims to automate this process. Given a simple list of words, it can build and maintain your personal language oracle, generate structured databases, and create exports that can later be used for Anki decks, CSV files, or direct searching and reference.

## Current Status

Implemented:

* ✅ MasterDB generation scripts
* ✅ OracleDB generation scripts
* ✅ CSV generation from `words.txt`

## Project Structure

```text
masterdb_helper_adjectives.py
masterdb_helper_adverbs.py
create_all_master_dbs.py
create_csvs_from_oracle.py
masterdb_helper_nouns.py
create_oracledb_schema.py
masterdb_helper_verbs.py
```

### Script Overview

| Script                          | Purpose                             |
| ------------------------------- | ----------------------------------- |
| `masterdb_helper_adjectives.py` | Build adjective master database     |
| `masterdb_helper_adverbs.py`    | Build adverb master database        |
| `masterdb_helper_nouns.py`      | Build noun master database          |
| `masterdb_helper_verbs.py`      | Build verb master database          |
| `create_all_master_dbs.py`      | Generate all master databases       |
| `create_oracledb_schema.py`     | Create and populate OracleDB schema |
| `create_csvs_from_oracle.py`    | Export data from OracleDB to CSV    |

## Workflow

```text
kaikki.org-dictionary-German.jsonl
    ↓
MasterDB Generation

-----------------------------------

words.txt
    ↓
OracleDB Creation
    ↓
CSV Export
    ↓
(Upcoming) Anki Deck Generation
```

## Roadmap

* [ ] Anki deck generation script
* [ ] Audio download and integration for Anki cards
* [ ] Improved error handling and validation for `words.txt`
* [ ] Better parsing and reporting of malformed entries

## Motivation

The goal of this project is not just to store vocabulary, but to help language learners build a personalized knowledge base containing the exact words they encounter during their studies.

Instead of relying on generic vocabulary lists, DeDict allows learners to create and maintain their own evolving dictionary—their own oracle.

## Setup & Usage

### Step 1 — Add the dictionary file

Download the German dictionary from [kaikki.org](https://kaikki.org/dictionary/German/) and place it in the root project directory:

```
kaikki.org-dictionary-German.jsonl
```

---

### Step 2 — Create the Master Databases

Run this **once** to parse the JSONL file and build the 4 MasterDBs.

```bash
python create_all_master_dbs.py
```

This creates the `MasterDB/` folder with:

- `german_nouns.db`
- `german_verbs.db`
- `german_adjectives.db`
- `german_adverbs.db`

> This step can take a few minutes depending on your machine, as it processes the full dictionary file.

---

### Step 3 — Create the Oracle DB

Run this **once** to set up the empty Oracle database schema.

```bash
python create_oracledb_schema.py
```

This creates `OracleDB/oracle.db` with empty tables for nouns, verbs, adjectives, and adverbs.

---

### Step 4 — Add your words

Add the German words you want to track into `words.txt`, one word per line:

```
Haus
gehen
schnell
leider
```

---

### Step 5 — Populate the Oracle DB

Run this to look up your words in the MasterDBs and copy them into `oracle.db`.

```bash
python update_oracledb_from_txt.py
```

- Words already in `oracle.db` are skipped automatically.
- Any words not found in any MasterDB are printed at the end.

---

### Step 6 — Export to CSV

Run this to generate CSV files from everything currently in `oracle.db`.

```bash
python create_csvs_from_oracle.py
```

This creates the `CSVS/` folder with:

| File | Columns |
|------|---------|
| `oracle_nouns.csv` | word, article, plural, meaning |
| `oracle_verbs.csv` | word, meaning, preterite, participle, auxiliary, regularity, separable, example_de, example_en |
| `oracle_adjectives.csv` | word, meaning, comparative, superlative, example_de, example_en |
| `oracle_adverbs.csv` | word, meaning, example_de, example_en |

> The CSV files are fully overwritten on each run, reflecting the current state of `oracle.db`.

---

## Adding New Words Later

Steps 2 `create_all_master_dbs.py` and 3 `create_oracledb_schema.py` only need to be run once. For adding new words:

1. Add new words to `words.txt`
2. Run `python update_oracledb_from_txt.py`
3. Run `python create_csvs_from_oracle.py`