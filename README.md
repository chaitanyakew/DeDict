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
