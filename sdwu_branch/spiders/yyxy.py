import scrapy
import re
from scrapy.spiders import Spider
from sdwu_branch.items import SdwuBranchItem
class WYXYSpider(Spider):
    name = 'yyxy'
    start_urls = ['https://yyxy.sdwu.edu.cn/xwsd/{}.htm'.format(str(i)) for i in range(8, 1, -1)]
    start_urls.insert(0,'https://yyxy.sdwu.edu.cn/xwsd.htm')
    def parse(self, response):
        selector_list = response.xpath("//div[@class='main intro_R_sj']/ul/li")
        for one_selector in selector_list:
            item = SdwuBranchItem()
            item['title']=one_selector.xpath("div/a/text()").extract()
            item['times']=one_selector.xpath("div/text()").extract()
            content_url = one_selector.xpath('div/a/@href').extract()[0].strip('../')
            if'https' in content_url:
                continue
            else:
                content_url = 'http://yyxy.sdwu.edu.cn/'+content_url
                yield scrapy.Request(content_url, meta={"item": item},callback=self.parse_content)



    def parse_content(self,response):
        content = response.xpath("//div[contains(@id,'vsb_content') or contains(@id,'vsb_content_4')]//text()").extract()
        item = response.meta['item']
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        item['content'] = pattern.findall(str(content))
        yield item
