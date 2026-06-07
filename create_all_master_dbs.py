from create_nouns_masterdb import create_database as create_nouns
from create_verbs_masterdb import create_database as create_verbs
from create_adjectives_masterdb import create_database as create_adjectives
from create_adverbs_masterdb import create_database as create_adverbs

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