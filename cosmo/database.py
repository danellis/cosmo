import sqlite3

class Database(object):
    page_link_type = "page"
    image_link_type = "image"

    def __init__(self, db_filename, flush=False):
        """Initialize the database file, creating tables and indices as necessary.

        :param db_filename: The name of a new or existing SQLite database file
        :param flush: If True, delete the existing triples
        """
        self.db = sqlite3.connect(db_filename)
        cursor = self.db.cursor()

        # Create a table for the triples, but only if it doesn't already exist
        # Put an index on the page_url column for checking whether we already
        # crawled a URL
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS triples (
                page_url TEXT NOT NULL,
                link_type TEXT NOT NULL,
                link_url TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS triples_page_url_index ON triples(page_url);
        """)
        self.db.commit()
        if flush:
            self.flush()

    def flush(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM triples")
        self.db.commit()

    def close(self):
        """Commit any outstanding inserts and then close cleanly

        :returns: None
        """
        self.db.commit()
        self.db.close()

    def is_page_stored(self, page_url):
        """Check whether any triples for a given URL have already been stored

        :param page_url:
        :returns: True if the given page_url already exists in the database, otherwise False
        """
        cursor = self.db.cursor()
        cursor.execute("SELECT 1 FROM triples WHERE page_url = ? LIMIT 1", (page_url,))
        return len(cursor.fetchall()) > 0

    def store_triples(self, triples):
        """Store (page URL, link type, link URL) triples in the database

        :param triples: Iterable of (page URL, link type, link URL) tuples
        :returns: None
        """
        cursor = self.db.cursor()
        cursor.executemany("INSERT INTO triples VALUES (?, ?, ?)", triples)
        self.db.commit()

    def get_triples(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT page_url, link_type, link_url FROM triples ORDER BY page_url, link_type")
        return cursor.fetchall()
