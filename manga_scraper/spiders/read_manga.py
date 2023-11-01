import scrapy
from manga_scraper.items import MangaItem


def valid_folder_name(input_string):
    list_str = input_string.split(" ")
    result = []
    for string in list_str:
        result.append("".join(ch.lower() for ch in string if ch.isalnum() or ch == "-" or ch == "."))
    return "-".join(result)


class ReadMangaSpider(scrapy.Spider):
    name = "read_manga"
    allowed_domains = ["rmanga.app", "readmanga.app", "readm.org"]
    start_urls = ["https://rmanga.app/ari-no-su-dungeon-e-youkoso"]

    def parse(self, response):
        manga_urls = response.css(".category-name a ::attr(href)").extract()
        for manga_url in manga_urls:
            yield response.follow(response.urljoin(manga_url), callback=self.parse_manga)

        nav_pages = response.css('.pagination__item')
        next_page = nav_pages[len(nav_pages) - 2]
        if next_page.css('::text').get() == "»":
            next_page_url = next_page.css('::attr(href)').get()
            yield response.follow(next_page_url, callback=self.parse)

    def parse_manga(self, response):
        chapter_urls = response.css(
            ".col-md-12.mt-2.mb-2 .cm-tabs-content.novels-detail-chapters a ::attr(href)").extract()
        manga_type = response.css('li:nth-child(4) .red-color strong::text').get().strip().lower()
        if manga_type == "japanese":
            for chapter_url in chapter_urls:
                yield response.follow(chapter_url, callback=self.parse_chapter)

    def parse_chapter(self, response):
        item = MangaItem()
        raw_images = response.css(".chapter-detail-novel-big-image img ::attr(src)").extract()
        raw_manga = response.css(".max-caracter-2::text").get()
        raw_chapter = response.css(".me-auto span::text").get()

        item["image_urls"] = raw_images
        item["manga"] = valid_folder_name(raw_manga)
        item["chapter"] = valid_folder_name(raw_chapter)
        yield item
