# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy


class Headlines(scrapy.Spider):
    name = 'headlines'
    start_urls = ['https://indeks.kompas.com/?site=all&date=2023-01-01&page=1']
    # start_urls = [f'https://indeks.kompas.com/?site=all&date=2022-12-{day:02}&page=1' for day in range (1, 32)]

    def parse(self, response):
        headlines = response.css('a.article__link::text').getall()
        headlines_date = response.css('div.article__date::text').getall()
        for headline, date in zip(headlines, headlines_date):
            yield {'headline': headline,
                   'date': date.split(',')[0]
                   }

        next_links = response.css('a.paging__link--next')
        for a in next_links:
            if 'Next' in a.get():
                yield response.follow(a, callback=self.parse)
