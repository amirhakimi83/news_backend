import scrapy
from twisted.spread.jelly import reference_atom
import requests

class ZoomitSpider(scrapy.Spider):
    name = "zoomit"
    start_urls = ["https://www.zoomit.ir/archive"]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 60000,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse,
            )

    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]
        await page.close()
        all_news_link =  response.css('div.scroll-m-16 a::attr(href)').getall()
        for link in all_news_link:
            one_news_link = response.urljoin(link)
            yield scrapy.Request(
                one_news_link,
                meta={'playwright': True, 'playwright_include_page': True},
                callback=self.parse_news
            )

    async def parse_news(self, response, **kwargs):
        page = response.meta['playwright_page']
        await page.close()

        title = response.css('article header.sc-6a819410-5.eUacdC div.sc-481293f7-0.iUFaKx div.sc-481293f7-1.fjdwzl h1.sc-9996cfc-0.ieMlRF::text').get()
        tags = response.css('span.sc-9996cfc-0.NawFH::text').getall()
        content1 = response.css('span.sc-9996cfc-0.kFMLTe::text').get()
        content2 = response.css('p.sc-9996cfc-0.gAFslo.sc-b2ef6c17-0.joXpaW::text').getall()
        content_str = ''
        content_str += content1
        for c in content2:
            content_str += c
        reference = response.css("p.sc-9996cfc-0.gAFslo.sc-b2ef6c17-0.joXpaW a::attr(href)").get()

        data = {
            "title": title.strip(),
            "content_news": content_str,
            "tags": tags,
            "reference": reference
        }
        save_news_url = 'http://127.0.0.1:8000/api/news/insert/'
        insert_response = requests.post(save_news_url, json=data)
        print(f"\n\n\n\n\n\n\n\n{insert_response.status_code}\n{insert_response.text}\n\n\n\n\n\n\n\n")

        yield {"news_data": data}
