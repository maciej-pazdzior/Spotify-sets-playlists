import scrapy
from ..items import ScrapysongsItem
from scrapy.loader import ItemLoader

class SongsSpider(scrapy.Spider):
    name = 'songs'
    allowed_domains = ['setlist.fm']
    start_urls = [input('Podaj link:')]

    def __init__(self):
        self.pages = int(input('Podaj liczbę stron:'))

    def parse(self, response):
        il = ItemLoader(item=ScrapysongsItem(), selector=response.css('div.transparentBox.border.visiblePrint h1')) 
        il.add_css('band', 'h1::text')
        yield il.load_item()

        links = response.css("div.col-xs-12.setlistPreview.vevent > div > h2 > a::attr(href)")
        for link in links:
            setlist_link = 'https://www.setlist.fm/' + link.extract()[2:]
            yield scrapy.Request(setlist_link, self.parse_setlist)

        self.pages -= 1
        while self.pages>0:
            link = 'https://www.setlist.fm' + response.css('ul.listPagingNavigator.text-center.hidden-print li a::attr(href)').extract()[-1][2:]
            yield scrapy.Request(link, self.parse)

    def parse_setlist(self, response):
        for song in response.css('a.songLabel'):
            il = ItemLoader(item=ScrapysongsItem(), selector=song)
            il.add_css('song', 'a::text')
            yield il.load_item()
        
        

