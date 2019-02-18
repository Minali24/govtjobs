# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import os
from tika import parser
import logging
import re
# class GovScraperPipeline(object):
#     def process_item(self, item, spider):
#         logging.error(item)
#         return item
class MyImagesPipeline(FilesPipeline):    
    def get_media_requests(self, item, info):
        for image_url in item['file_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        path = '/home/urmi/Documents/govtjobs/govtjobs/downloaded_pdfs/'
        path_txt = '/home/urmi/Documents/govtjobs/govtjobs/downloaded_text/'
        file_cen = open("cen.csv", "w+")
        for x in results:
            if(x[0]):
                raw = parser.from_file(path+x[1]['path'])
                text = raw['content']

                # extracting out the CEN id from the text
                try:
                    result = re.search(r"CEN(\s|-)[0-9]{2}\/[0-9]{4}", text)
                    print (">>>>>>>>>>>>" + result.group(0))
                    # print (">>>>>>>>>>>>" + x[1]['path'])
                    file_cen.write(path+x[1]['path'] + ", " + result.group(0) + "\n")
                except:
                    print(">>>>>>>>>>>> Pattern not found in text.")
                fl = open( path_txt+x[1]['path']+'.txt' ,'w+')
                if text:
                    fl.write(text)
                fl.close()
        file_cen.close()
