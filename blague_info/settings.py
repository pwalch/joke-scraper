# Scrapy settings for blague_info project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'blague_info'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['blague_info.spiders']
NEWSPIDER_MODULE = 'blague_info.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

