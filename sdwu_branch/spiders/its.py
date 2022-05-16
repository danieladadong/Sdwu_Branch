import scrapy
import re
from scrapy.spiders import Spider
from sdwu_branch.items import SdwuBranchItem
class WYXYSpider(Spider):
    name = 'its'
    start_urls = ['https://its.sdwu.edu.cn/list.jsp?a250844t=21&a250844p={}&a250844c=8&urltype=tree.TreeTempUrl&wbtreeid=1089'.format(str(i)) for i in range(1, 22, 1)]
    def parse(self, response):
        selector_list = response.xpath("//div[@class='c1_con']/div")
        for one_selector in selector_list:
            item = SdwuBranchItem()
            item['title']=one_selector.xpath("div/a/h1/text()").extract()
            item['times']=one_selector.xpath("div/div/span/text()").extract()
            content_url = one_selector.xpath('div/a/@href').extract()[0].strip('../')
            if'https' in content_url:
                continue
            else:
                content_url = 'http://its.sdwu.edu.cn/'+content_url
                yield scrapy.Request(content_url, meta={"item": item},callback=self.parse_content)



    def parse_content(self,response):
        content = response.xpath("//div[@id='vsb_content']//text()").extract()
        item = response.meta['item']
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        item['content'] = pattern.findall(str(content))
        yield item
