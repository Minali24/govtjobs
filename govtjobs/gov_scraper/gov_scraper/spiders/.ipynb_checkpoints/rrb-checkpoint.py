import scrapy
from gov_scraper.items import GovScraperItem
class RRBSpider(scrapy.Spider):
    name = "rrb"

    def start_requests(self):
        urls = [
            'http://rrbcdg.gov.in/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        rrb_fields = GovScraperItem()
        ls= []
        extracted_links = response.css("a::attr('href')").extract()
        for x in extracted_links:
            if 'pdf' in x:
                ls.append('http://rrbcdg.gov.in/'+x)
                
        rrb_fields['file_urls'] = ls
        yield rrb_fields
                
        
        
        