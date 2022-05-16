import scrapy
import re
from scrapy.spiders import Spider
from sdwu_branch.items import SdwuBranchItem
class WYXYSpider(Spider):
    name = 'kjxy'
    start_urls = ['https://kjxy.sdwu.edu.cn/index/zxdt/{}.htm'.format(str(i)) for i in range(9, 1, -1)]
    start_urls.insert(0,'https://kjxy.sdwu.edu.cn/index/zxdt.htm')
    def parse(self, response):
        selector_list = response.xpath("//div[@class='vsb-space n_right']/ul/li")
        for one_selector in selector_list:
            item = SdwuBranchItem()
            item['title']=one_selector.xpath("div/a[@class='tit']/text()").extract()
            item['times']=one_selector.xpath("div[@class='list_time fl']/p/text()").extract()
            content_url = one_selector.xpath("div/a[@class='tit']/@href").extract()[0].strip('../')
            if'https' in content_url:
                continue
            else:
                content_url = 'http://kjxy.sdwu.edu.cn/'+content_url
                yield scrapy.Request(content_url, meta={"item": item},callback=self.parse_content)



    def parse_content(self,response):
        content = response.xpath("//div[contains(@id,'vsb_content') or contains(@class,'c250981_content')]//text()").extract()
        item = response.meta['item']
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        item['content'] = pattern.findall(str(content))
        yield item
