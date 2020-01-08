import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SteamSpider(scrapy.Spider):
    name = 'gametest'
    allowed_domains = ['steampowered.com']
    start_urls = ['https://store.steampowered.com/app/464920/Surviving_Mars/',
                  'https://store.steampowered.com/app/255710/Cities_Skylines/',
                  'https://store.steampowered.com/app/453480/Shadowverse_CCG/',
                  'https://store.steampowered.com/app/493340/Planet_Coaster/',
				  'https://store.steampowered.com/app/359320/Elite_Dangerous/',
                  'https://store.steampowered.com/app/453090/Parkitect/',
                  'https://store.steampowered.com/app/675010/MudRunner/',
                  'https://store.steampowered.com/app/517710/Redout_Enhanced_Edition/',
                  'https://store.steampowered.com/app/1070580/Drift86/',
                  'https://store.steampowered.com/app/863570/Super_Seducer_2__Advanced_Seduction_Tactics/'
    ]

    rules = [
    ]

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        game = {
            'title' : response.xpath('//title/text()').get(),
            'recentreviews' : response.xpath('//span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').get(), # needs to be parsed for first two characters
            'allreviews' : response.xpath('//span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()')[1].get(),
            'nreviews' : response.xpath('//span[@class="responsive_hidden"]/text()')[1].get(),
            'date' : response.xpath('//div[@class="date"]/text()').get(),
            'dev' : response.css('.dev_row a::text').get(),
            'pub' : response.css('.dev_row a::text')[1].get(),
            'price' : response.css('.game_purchase_price::text').get(),
            'gamedetails' : response.css('.game_area_details_specs a ::text').getall(),
            'genre' : response.css('.details_block  a ::text').getall(), #needs to be cleaned. Only the first section of this returns the needed data
            'metacritic' : response.xpath('//div[@class="score high"]/text()').get(),
		}
        yield game