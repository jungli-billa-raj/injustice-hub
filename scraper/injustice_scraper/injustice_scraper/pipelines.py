# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SQLitePipeline:
    """
    Pipeline responsible for inserting scraped articles
    into the SQLite database.
    """

    def open_spider(self, spider):
        """
        Runs once when the spider starts.
        Establishes DB connection.
        """
        self.conn = sqlite3.connect("../../data/injustice.db")
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """
        Runs once when the spider finishes.
        Closes DB connection safely.
        """
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        """
        Inserts a single scraped article into raw_articles.
        """
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO raw_articles
            (source, url, headline, published_at, full_text)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                item["source"],
                item["url"],
                item["headline"],
                item["published_at"],
                item["full_text"],
            ),
        )

        return item
