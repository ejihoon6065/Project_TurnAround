import scrapy
import json


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://hk.carousell.com/categories/men-s-fashion-3/mens-bags-wallets-476/']

    def parse(self, response):
        jsonStr = response.css('script:nth-child(2)::text').get()

        jsonStr = jsonStr[20:]
        jsonStr = json.loads(jsonStr)
        itemList = jsonStr["SearchListing"]["listingCards"]
        resultList = []
        for item in itemList:
            vo = {}
            tmpJson = item['belowFold']
            name = tmpJson[0]['stringContent']
            price = tmpJson[1]['stringContent']
            desc = tmpJson[2]['stringContent']
            status = tmpJson[3]['stringContent']
            imgUrl = item['thumbnailURL']
            url = 'https://hk.carousell.com/p/' + str(item['listingID'])
            vo['name'] = name
            vo['price'] = price
            vo['desc'] = desc
            vo['status'] = status
            vo['imgUrl'] = imgUrl
            vo['url'] = url
            resultList.append(vo)
            yield vo

        # for title in response.css('.post-header>h2'):
        #     yield {'title': title.css('a ::text').get()}

        buttonList = response.css('button')
        loadMore = buttonList[len(buttonList) - 1]
        print('##################')
        print(loadMore.extract())
        loadMore

        # yield response.follow(buttonList[len(buttonList) - 1], self.parse)

        # for next_page in response.css('a.next-posts-link'):
        #     yield response.follow(next_page, se
        # loadMore.click()

        # yield response.follow(buttonList[len(buttonList) - 1], self.parse)

        # for next_page in response.css('a.next-posts-link'):
        #     yield response.follow(next_page, self)
