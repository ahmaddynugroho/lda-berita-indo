# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from calendar import monthrange

import scrapy


class Detik(scrapy.Spider):
    name = 'detik'
    dates = [(day + 1, 12, 2022) for day in range(0, monthrange(2022, 12)[1])]
    start_urls = [
        f'https://news.detik.com/indeks/1?date={month:02}/{day:02}/{year}' for day, month, year in dates]

    def parse(self, response):
        headlines = response.css('h3 a.media__link::text').getall()
        date = response.css('.media__date span::text').get().split(' ')
        for headline in headlines:
            yield {
                'date': f'{date[1]} {date[2]} {date[3]}',
                'headline': headline
            }

        next_links = response.css('.pagination__item')
        for a in next_links:
            if 'Next' in a.get():
                yield response.follow(a, callback=self.parse)


class Kompas(scrapy.Spider):
    name = 'kompas'
    dates = [(day + 1, 12, 2022) for day in range(0, monthrange(2022, 12)[1])]
    start_urls = [
        f'https://indeks.kompas.com/?site=all&date={year}-{month:02}-{day:02}&page=1' for day, month, year in dates]

    def parse(self, response):
        headlines = response.css('a.article__link::text').getall()
        headlines_date = response.css('div.article__date::text').getall()
        for headline, date in zip(headlines, headlines_date):
            yield {
                'date': date.split(',')[0],
                'headline': headline
            }

        next_links = response.css('a.paging__link--next')
        for a in next_links:
            if 'Next' in a.get():
                yield response.follow(a, callback=self.parse)
