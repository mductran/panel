from urllib.parse import urlencode, parse_qs

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
import scrapy

class AllMangaDexSpider(CrawlSpider):
    name = "all_manga_dex"
    allowed_domains = ["rmanga.app", "readmanga.app"]
    # start_urls = ["https://www.nettruyenus.com/truyen-tranh/moi-nguoi-deu-den-tu-the-gioi-khac-ngoai-tru-toi-96820"]
    start_urls = ["https://rmanga.app/ranking/new/1"]

    # rules = (Rule(LinkExtractor(allow=r"tim-truyen\?[A-Za-z]+=\d")),
    #          Rule(LinkExtractor(allow="truyen-tranh"), callback="parse_item"),)

    # rules = (Rule(LinkExtractor(allow=r"truyen-tranh/moi-nguoi-deu-den-tu-the-gioi-khac-ngoai-tru-toi/([A-Za-z0-9]+(-[A-Za-z0-9]+)+)/[0-9]+"), callback="parse_item", follow=False), )

    # def process_links(self, links):
    #     for link in links:
    #         if "http://localhost:8050/render.html?&" not in link.url:
    #             link.url = "http://localhost:8050/render.html?&" + urlencode({'url': link.url,
    #                                                                           'wait': 2.0})
    #     return links

    rules = (Rule(LinkExtractor(allow="berserk-of-gluttony/chapter-52/all-pages"), callback="parse_item"),)

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url, self.parse_item, meta={
    #             'splash': {
    #                 'endpoint': 'render.html',
    #                 'args': {'wait': 0.5}
    #             }
    #         })

    def parse_item(self, response):
        raw_images = response.css(".text-center img ::attr(src)").extract()
        clean_images = []
        for img_url in raw_images:
            clean_images.append(response.urljoin(img_url))

        yield {
            "image_urls": clean_images,
        }


    # def parse_item(self, response):
    #     raw_images = response.css(".page-chapter img ::attr(src)")
    #     clean_images = []
    #     for img_url in raw_images:
    #         clean_images.append("https:" + img_url.get())
    #
    #     yield {
    #         "image_urls": clean_images,
    #     }
