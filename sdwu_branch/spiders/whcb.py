import scrapy
import re
from scrapy.spiders import Spider
from sdwu_branch.items import SdwuBranchItem
class WYXYSpider(Spider):
    name = 'whcb'
    start_urls = ['https://whcb.sdwu.edu.cn/index/xydt/{}.htm'.format(str(i)) for i in range(38, 1, -1)]
    start_urls.insert(0,'https://whcb.sdwu.edu.cn/index/xydt.htm')
    def parse(self, response):
        selector_list = response.xpath("//div[@class='wape-right']/ul/li")
        for one_selector in selector_list:
            item = SdwuBranchItem()
            item['title']=one_selector.xpath("a/text()").extract()
            item['times']=one_selector.xpath("span/text()").extract()
            content_url = one_selector.xpath('a/@href').extract()[0].strip('../')
            if'https' in content_url:
                continue
            else:
                content_url = 'http://whcb.sdwu.edu.cn/'+content_url
                yield scrapy.Request(content_url, meta={"item": item},callback=self.parse_content)



    def parse_content(self,response):
        content = response.xpath("//div[contains(@id,'vsb_content') or contains(@class,'c250981_content')]//text()").extract()
        item = response.meta['item']
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        item['content'] = pattern.findall(str(content))
        yield item
