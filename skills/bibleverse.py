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

    verse_text = bible.get_verse_text(rand_verse_id, version=VERSION)

    verse_info = bible.get_book_chapter_verse(rand_verse_id)

    return f'{verse_info[0].title} {verse_info[1]}:{verse_info[2]} "{verse_text}"'

if __name__ == "__main__":
   print(get_random_verse())
