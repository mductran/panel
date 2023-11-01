import hashlib

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class MangaScraperPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{item['manga']}/{item['chapter']}/{image_guid}.jpg"

    # def item_completed(self, results, item, info):
    #     image_paths = [x["path"] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     adapter = ItemAdapter(item)
    #     adapter["image_paths"] = image_paths
    #     return item