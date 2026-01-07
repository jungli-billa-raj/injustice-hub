import scrapy


class NewsSpider(scrapy.Spider):
    """
    Spider that scrapes raw news articles
    and stores them WITHOUT interpretation.
    """

    name = "news"
    allowed_domains = ["thehindu.com"]

    # Start with a small, controlled set of URLs
    start_urls = ["https://www.thehindu.com/news/national/"]

    def parse(self, response):
        """
        Extract article links from listing pages.
        """
        article_links = response.xpath("//a[contains(@href, '/news/')]/@href").getall()

        for link in article_links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        """
        Extract raw article data.
        """

        headline = response.xpath("//h1/text()").get()
        published_at = response.xpath(
            "//meta[@property='article:published_time']/@content"
        ).get()

        paragraphs = response.xpath(
            "//div[contains(@class,'articlebodycontent')]//p/text()"
        ).getall()
        self.logger.info("Parsed article: {response.url}")
        full_text = " ".join(paragraphs)

        # Guard clause: skip broken pages
        if not headline or not full_text:
            return

        yield {
            "source": "The Hindu",
            "url": response.url,
            "headline": headline.strip(),
            "published_at": published_at,
            "full_text": full_text.strip(),
        }
