from itemadapter import ItemAdapter
from scrapingCars.items import CarItem
from scrapy.loader.processors import MapCompose, TakeFirst
import re

class ScrapingcarsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.serialize_str_columns(adapter)
        self.clean_carHL(adapter)

        return item

    def serialize_str_columns(self, adapter):
        for field in adapter.keys():
            value = adapter.get(field)
            if value:
                adapter[field] = re.sub(r'\n+', '', str(value)).strip()

    def clean_carHL(self, adapter):
        value = adapter.get('carHL')
        if isinstance(value, list):
            cleaned_values = [re.sub(r'[\\n\\r]+', ' ', str(x)).strip() for x in value]
            adapter['carHL'] = cleaned_values