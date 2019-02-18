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
        for x in results:
            if(x[0]):
                raw = parser.from_file(path+x[1]['path'])
                text = raw['content']
                
                fl = open( path_txt+x[1]['path']+'.txt' ,'w+')
                if text:
                    fl.write(text)
                fl.close
