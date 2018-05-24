from scrapy.spiders import Spider


class BlogSpider(Spider):
    name = 'woodenrobot'
    start_urls = ['http://woodenrobot.me']

    def parse(self, response):
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            print title.strip()