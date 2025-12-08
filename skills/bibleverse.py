"""
Get a random bible verse - "tell me a bible verse"
"""

import pythonbible as bible
import random

def get_random_verse():
    VERSION = bible.Version.KING_JAMES

    while True:
        try:
            rand_verse_id = random.randint(1001001, 66022013)
            if bible.is_valid_verse_id(rand_verse_id):
                break
        except Exception:
            continue

    verse = bible.get_verse_text(rand_verse_id, version=VERSION)

    return verse

if __name__ == "__main__":
    verse = get_random_verse()
    print(verse)
