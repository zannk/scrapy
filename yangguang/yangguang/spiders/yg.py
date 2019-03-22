# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/html/top/report.shtml']

    def parse(self, response):
        # 分组
        tr_list = response.xpath("//div[@class='newshead']/table[2]/tr/td")
        for tr in tr_list:
            item = YangguangItem()

            item["title"] = tr.xpath("./tr/td[3]/a[1]/@title").extract_first()
            item["href"] = tr.xpath("./tr/td[3]/a[1]/@href").extract_first()
            item["publish_data"] = tr.xpath("./td[last()]/text()").extract_first()

            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
            )
            
    def parse_detail(self, response):
        item = response.meta["item"]
        item["content"] = response.xpath("//div[@class='wzyl']/table[1]//text()").extract()
        item["content_img"] = response.xpath(".//div[@class='wzyl']/div[@class='textpic']//img/@src").extract()
        item["content_img"] = ["http://wz.sun0769.com" + i for i in item["content_img"]]
        print(item)
