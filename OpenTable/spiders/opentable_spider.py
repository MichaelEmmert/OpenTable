import scrapy
from OpenTable.items import OpentableItem

class OpentableSpider(scrapy.Spider):
    name = 'opentable_spider'
    allowed_urls = ['https://www.opentable.com']
    start_urls = ['https://www.opentable.com/chicago-illinois-restaurant-listings?covers=2&currentview=list&datetime=2020-01-28+19%3A00&latitude=41.879016&longitude=-87.85132&metroid=3&size=100&sort=Popularity&from=100']

    def parse(self, response):
        full_path = 'https://www.opentable.com/chicago-illinois-restaurant-listings?covers=2&currentview=list&datetime=2020-01-28+19%3A00&latitude=41.879016&longitude=-87.85132&metroid=3&size=100&sort=Popularity&from=00'
        last_page = int(response.xpath('//span[@class="js-pagination-page pagination-link  "]/span[@class="underline-hover"]/text()').extract()[-1])
        urls = [full_path[:-2] + str(i) for i in range(0,100*last_page,100)]
        for page_num, url in enumerate(urls):
            yield scrapy.Request(url, self.parse_list_page, meta = {'page_num':page_num})

    def parse_list_page(self, response):
        page_num = response.meta['page_num']
        rows = response.xpath('//ul[@class="content-section-list infinite-results-list analytics-results-list"]/li[@class="result content-section-list-row cf with-times"]')
        area = response.xpath('//*[@id="header"]/ol/li[3]/a/span//text()').extract_first()
        for index, row in enumerate(rows):
            location_on_page = [page_num, index]
            name = row.xpath('.//span[@class="rest-row-name-text"]/text()').extract_first()
            location = row.xpath('.//span[@class="rest-row-meta--location rest-row-meta-text sfx1388addContent"]//text()').extract_first()
            cuisine = row.xpath('.//span[@class="rest-row-meta--cuisine rest-row-meta-text sfx1388addContent"]//text()').extract_first()
            review_count = row.xpath('.//a//span[@class="underline-hover"]//text()').extract_first()
            review_link = row.xpath('.//a//@href').extract_first()
            link = row.xpath('.//div//@href').extract_first()
            cost = row.xpath('.//i//text()').extract_first()
            rating = row.xpath('.//*[@class="star-rating-score"]//@aria-label').extract_first()
            promoted = row.xpath('.//span[@class="promoted-badge"]//text()').extract_first()

            yield scrapy.Request(link, self.parse_each_link, 
                meta = {
                'location_on_page': location_on_page,
                'name': name,
                'area': area,
                'location': location,
                'cuisine': cuisine,
                'review_count':review_count,
                'review_link': review_link,
                'link': link,
                'cost': cost,
                'rating' : rating,
                'promoted': promoted
                })
    
    def parse_each_link(self, response):
        bookings_today =  response.xpath('//*[@id="js-page"]/div[2]/aside/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/span//text()').extract_first()
        address = response.xpath('//*[@id="js-page"]//a[@target="_blank"]//@href').extract_first()
        item = OpentableItem()
        item['location_on_page'] = response.meta['location_on_page']
        item['name'] = response.meta['name']
        item['area'] = response.meta['area']
        item['location'] = response.meta['location']
        item['cuisine'] = response.meta['cuisine']
        item['review_count'] = response.meta['review_count']
        item['review_link'] = response.meta['review_link']
        item['link'] = response.meta['link']
        item['cost'] = response.meta['cost']
        item['rating'] = response.meta['rating']
        item['promoted'] = response.meta['promoted']
        item['bookings_today'] = bookings_today
        item['address'] = address
        
        yield item
