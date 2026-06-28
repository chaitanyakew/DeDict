from masterdb_helper_nouns import create_database as create_nouns
from masterdb_helper_verbs import create_database as create_verbs
from masterdb_helper_adjectives_ import create_database as create_adjectives
from masterdb_helper_adverbs import create_database as create_adverbs

def main():
    print("Creating noun database...")
    create_nouns()

    print("Creating verb database...")
    create_verbs()

    print("Creating adjective database...")
    create_adjectives()

    print("Creating adverb database...")
    create_adverbs()

    print("All master databases created successfully.")

if __name__ == "__main__":
    main()