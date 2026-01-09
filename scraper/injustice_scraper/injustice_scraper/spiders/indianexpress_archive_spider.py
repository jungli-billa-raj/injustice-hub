import scrapy


class IndianExpressArchiveSpider(scrapy.Spider):
    """
    Scrapes ALL articles from Indian Express archive
    for a specific day, across all paginated pages.

    Flow:
    1. Start from archive page (page 1)
    2. Extract article URLs
    3. Follow pagination via "Next" button
    4. Open each article page
    5. Extract raw article data
    """

    name = "indianexpress_archive"
    allowed_domains = ["indianexpress.com"]

    # Archive start URL (page 1 of the day)
    start_urls = ["https://indianexpress.com/archive/2024/04/01/"]

    def parse(self, response):
        """
        Handles ARCHIVE pages.

        - Extracts article links
        - Schedules article pages for parsing
        - Finds and follows the 'Next' pagination link
        """

        # ✅ Extract article URLs from the archive list
        article_links = response.xpath(
            "//div[contains(@class,'article-list')]//p/a/@href"
        ).getall()

        for link in article_links:
            # Schedule article page for parsing
            yield response.follow(link, self.parse_article)

        # ✅ Find "Next" page link for pagination
        next_page = response.xpath(
            "//div[contains(@class,'pagination')]//a[contains(@class,'next')]/@href"
        ).get()

        if next_page:
            # Recursively schedule the next archive page
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        """
        Handles INDIVIDUAL ARTICLE pages.

        Extracts raw article content and yields it
        to the SQLite pipeline.
        """

        # Extract headline
        headline = response.xpath("//h1/text()").get()

        # Extract published timestamp from meta tag
        published_at = response.xpath(
            "//meta[@property='article:published_time']/@content"
        ).get()

        # Extract article body text (main readable content)
        paragraphs = response.xpath(
            "//div[contains(@class,'full-details')]//p/text()"
        ).getall()

        full_text = " ".join(p.strip() for p in paragraphs if p.strip())

        # Guard clause: skip pages with missing data
        if not headline or not full_text:
            return

        # Yield item → sent directly to SQLite pipeline
        yield {
            "source": "Indian Express",
            "url": response.url,
            "headline": headline.strip(),
            "published_at": published_at,
            "full_text": full_text,
        }
