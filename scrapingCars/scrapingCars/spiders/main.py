import scrapy
from scrapingCars.items import CarItem
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader


class MainSpider(scrapy.Spider):
    name = "main"

    def start_requests(self):

        url = 'https://www.gaaclassiccars.com/vehicles?q%5Bbranch_id_eq%5D=53'

        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-419,es;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'vehicles={%22action_name%22:%22index%22%2C%22params%22:{%22q%22:{%22branch_id_eq%22:%2253%22}}%2C%22request_fullpath%22:%22/vehicles?q%255Bbranch_id_eq%255D=53%22}',
        'If-Modified-Since': 'Tue, 06 Aug 2024 14:10:38 GMT',
        'If-None-Match': 'W/"82106878b7e953942ac9be2c4921122b"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
        yield scrapy.Request(url, callback = self.get_cars_urls, headers = self.headers)

    def get_cars_urls(self, response):
        urls = response.css('div.gaa-inventory-container a.gaa-vehicle-item::attr(href)').getall()

        for u in urls:
            yield scrapy.Request(response.urljoin(u), callback=self.parseCarPage, headers = self.headers)

        next_page_element = response.css('a.next::attr(href)').get()
        if next_page_element is not None:
            next_page = response.urljoin(next_page_element)
            scrapy.Request(next_page, callback = self.get_cars_urls, headers = self.headers)

    def parseCarPage(self, response):

        item = CarItem()
        carData = response.css('div.gaa-spec-row dd::text').getall()

        item['carUrl'] = str(response.url)
        item['carName'] = str(response.css('h1.vehicle-name::text').get().strip())
        item['year'] = str(carData[0].strip())
        item['brand'] = str(carData[1].strip())
        item['model'] = str(carData[2].strip())
        item['doors'] = str(carData[3].strip())
        item['color'] = str(carData[4].strip())
        item['style'] = str(carData[-1].strip())
        item['lot'] = str(response.css('div.gaa-lot-number h5 span::text').get().strip())
        item['vinCode'] = str(response.css('div.vin::text').get())
        item['views'] = str(response.css('div.gaa-view-counter::text').get())
        item['description'] = str(response.css('div.gaa-about-vehicle h2::text').get())
        item['carHL'] = response.css('ul.gaa-vehicle-highlights li::text').getall()

        yield item
