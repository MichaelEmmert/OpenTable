import scrapy
from OpenTable.items import OpentableItem

class OpentableSpider(scrapy.Spider):
    name = 'opentable_spider'
    allowed_urls = ['https://www.opentable.com']
    start_urls = ['https://www.opentable.com/new-york-restaurant-listings?covers=2&currentview=list&datetime=2020-01-22+19%3A00&latitude=40.802092&longitude=-73.981569&metroid=8&size=100&sort=Popularity&from=0']

    def parse(self, response):
        #Date is currently in the URL so maybe make it update with the current day
        last_page = int(response.xpath('//span[@class="js-pagination-page pagination-link  "]/span[@class="underline-hover"]/text()').extract()[-1])
        urls = [f'https://www.opentable.com/new-york-restaurant-listings?covers=2&currentview=list&datetime=2020-01-22+19%3A00&latitude=40.802092&longitude=-73.981569&metroid=8&size=100&sort=Popularity&from={i}' for i in range(0,100*last_page,100)]
        # print(urls)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        rows = response.xpath('//ul[@class="content-section-list infinite-results-list analytics-results-list"]/li[@class="result content-section-list-row cf with-times"]')
        for row in rows:

            name = row.xpath('.//span[@class="rest-row-name-text"]/text()').extract_first()
            location = row.xpath('.//span[@class="rest-row-meta--location rest-row-meta-text sfx1388addContent"]//text()').extract_first()
            cuisine = row.xpath('.//span[@class="rest-row-meta--cuisine rest-row-meta-text sfx1388addContent"]//text()').extract_first()
            review_count = row.xpath('.//a[@class="review-link"]//span[@class="underline-hover"]//text()').extract_first()
            review_link = row.xpath('.//a[@class="review-link"]//@href').extract_first()
            link = row.xpath('.//div[@class="rest-row-header flex-row-justify"]/a/@href').extract_first()
            cost = row.xpath('.//i[@class="pricing--the-price"]//text()').extract_first().strip()
            rating = row.xpath('.//*[@class="star-rating-score"]//@aria-label').extract_first()
            promoted = row.xpath('.//span[@class="promoted-badge"]//text()').extract_first()

            item = OpentableItem()
            item['name'] = name
            item['location'] = location
            item['cuisine'] = cuisine
            item['review_count'] = review_count
            item['review_link'] = review_link
            item['link'] = link
            item['cost'] = cost
            item['rating'] = rating
            item['promoted'] = promoted

            yield item