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
        file_csv = open("cen.csv", "w+")
        file_no_pattern = open("no_patterns.txt", "w+")
        for x in results:
            if(x[0]):
                raw = parser.from_file(path+x[1]['path'])
                text = raw['content']
                
                fl = open( path_txt+x[1]['path']+'.txt' ,'w+')
                if text:
                    fl.write(text)
                fl.close()
                
                file_csv.write(x[1]['path'] + ", ")


                try:
                    # extracting out the CEN id from the text
                    pattern_result_cen = re.search(r"(\(CEN\)|CEN)(\s(No.\s?)?|-|\.)[0-9]{2}\/[0-9]{4}", text)
                    if pattern_result_cen:
                        file_csv.write(pattern_result_cen.group(0) + ", ")
                        print (">>>>>>>>>>>>" + pattern_result_cen.group(0))
                    else:
                        print(">>>>>>>>>>>> CEN Pattern not found in text.")
                        file_csv.write(", ")

                    # extracting out the Date from the text
                    pattern_result_date = re.compile('Date:\s?\d{2}.\d{2}.\d{4}')
                    pattern_result_date_list = pattern_result_date.findall(text)
                    print ("pattern_result_date_list >>>>>>>>>> ")
                    print (pattern_result_date_list)
                    result_date = pattern_result_date_list[-1]

                    if pattern_result_date:
                        file_csv.write(result_date)
                        print (">>>>>>>>>>>>" + result_date)
                    else:
                        print(">>>>>>>>>>>> Date Pattern not found in text.")

                except:
                    print("Something wrong happened!")
                file_csv.write("\n")
                
        file_no_pattern.close()
        file_csv.close()
