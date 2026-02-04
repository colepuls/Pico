import pythonbible as bible
import random


def run_verse():
    
    VERSION = bible.Version.KING_JAMES
    
    while True:
        try:
            rand_verse_id = random.randint(1001001, 66022013) # genesis 1:1 to revelation 22:13
            # check if valid
            if bible.is_valid_verse_id(rand_verse_id):
                break
        except Exception:
            continue # try again

    # extract
    verse_text = bible.get_verse_text(rand_verse_id, version=VERSION)
    verse_info = bible.get_book_chapter_verse(rand_verse_id)
    return f'{verse_info[0].title} {verse_info[1]}:{verse_info[2]} "{verse_text}"'
