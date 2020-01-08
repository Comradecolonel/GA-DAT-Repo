import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


def parse_game(response):
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
		
    return game


class SteamSpider(CrawlSpider):
    name = 'games'
    allowed_domains = ['steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998']

    rules = [
        Rule(LinkExtractor(
             allow='/app/(.+)/',
             restrict_css='#search_result_container'),
             callback='parse_game'),
        Rule(LinkExtractor(
             allow='page=(\d+)',
             restrict_css='.search_pagination_right'))
    ]
	
    def __init__(self, steam_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.steam_id = steam_id

    def start_requests(self):
        if self.steam_id:
            yield Request(f'http://store.steampowered.com/app/{self.steam_id}/',
                          callback=self.parse_product)
        else:
            yield from super().start_requests()

    def parse(self, response):
        # Circumvent age selection form.
        if '/agecheck/app' in response.url:
            logger.debug(f'Form-type age check triggered for {response.url}.')

            form = response.css('#agegate_box form')

            action = form.xpath('@action').extract_first()
            name = form.xpath('input/@name').extract_first()
            value = form.xpath('input/@value').extract_first()

            formdata = {
                name: value,
                'ageDay': '1',
                'ageMonth': '1',
                'ageYear': '1955'
            }

            yield FormRequest(
                url=action,
                method='POST',
                formdata=formdata,
                callback=self.parse_product
            )

        else:
             yield parse_game(response)

