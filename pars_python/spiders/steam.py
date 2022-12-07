import scrapy


class SteamSpider(scrapy.Spider):
    name = 'steam'
    start_urls = [
        'https://store.steampowered.com/search?term=%D0%B8%D0%BD%D0%B4%D0%B8&supportedlang=russian&page=1&ndl=1',
        'https://store.steampowered.com/search?term=%D0%B8%D0%BD%D0%B4%D0%B8&supportedlang=russian&page=2&ndl=1',
        'https://store.steampowered.com/search?term=minecraft&supportedlang=russian&page=1&ndl=1',
        'https://store.steampowered.com/search?term=minecraft&supportedlang=russian&page=2&ndl=1',
        'https://store.steampowered.com/search?term=%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B5%D0%B3%D0%B8%D0%B8&supportedlang=russian&page=1&ndl=1',
        'https://store.steampowered.com/search?term=%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B5%D0%B3%D0%B8%D0%B8&supportedlang=russian&page=2&ndl=1',
        'https://store.steampowered.com/search?term=%D0%B8%D0%BD%D0%B4%D0%B8&supportedlang=russian&page=1&ndl=1',
    ]

    def parse(self, response):
        for url in self.start_urls:
            for link in response.css('a.search_result_row::attr(href)').getall():
                yield response.follow(link, callback=self.parse_games)

    def parse_games(self, response):
        if response.css('div.apphub_AppName::text').get() is None or response.css(
                'div.apphub_AppName::text').get() == "":
            return

        lst_tags = response.css('div.glance_tags.popular_tags a::text').getall()
        for i in range(len(lst_tags)):
            lst_tags[i] = lst_tags[i].strip()

        yield {
            'name': response.css('div.apphub_AppName::text').get(),
            'types': response.css('div.blockbg a::text').getall()[1:],
            'count_review': response.css('div.summary_section span::text')[1].getall(),
            'grade': response.css('span.game_review_summary.positive::text').get(),
            'price': response.css('div.discount_final_price::text').get(),
            'platforms': 'хз',
            'developer': response.css('div.summary.column a::text').get(),
            'tags': lst_tags,
            'date_release': response.css('div.date::text').get()
        }
