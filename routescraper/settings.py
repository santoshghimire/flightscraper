# -*- coding: utf-8 -*-

# Scrapy settings for routescraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'routescraper'

SPIDER_MODULES = ['routescraper.spiders']
NEWSPIDER_MODULE = 'routescraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'routescraper (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.8,ne;q=0.6,it;q=0.4',
#     'Accept-Encoding': 'gzip, deflate, sdch, br',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     # Cookie:ASP.NET_SessionId=qxrzpn3ffnktfeiv30socmes; skysales=528146954.20480.0000; TigerBookingCulture=CultureCode=en-GB; jumpseat_uid=TSRW6KCwWwk7Y7kHoTkugw; D_SID=110.34.8.13:rTK/hCgrlnqIOFwF48qvF9m3qN4+ESgRvStmBQCY7vs; viewedOuibounceModal=true; _vwo_uuid_v2=6A5A6B83211018FD758CE3957ECDA5D8|ab5cf272658825e13ccacadc68fc47e1; _ga=GA1.2.767427501.1482842195; _ga=GA1.3.767427501.1482842195; _gat_UA-29652265-4=1; __utmt=1; __utma=33480891.767427501.1482842195.1483410394.1483580022.3; __utmb=33480891.2.10.1483580022; __utmc=33480891; __utmz=33480891.1482842196.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=33480891.|5=BID=c0dc0478-2e3c-47fc-a42d-551e466a4c5c=1; __utmli=ControlGroupSearchView_AvailabilitySearchInputSearchView_RoundTrip; D_PID=56ADA3AF-841F-36E3-A882-42EF9CB59ED6; D_IID=5E6BD877-0FEA-3993-965B-926A0AD381A7; D_UID=EA2553F8-AAA5-3354-916B-303D7C374051; D_HID=mw6aeAjQVSknrsJ6fcVvJnEZ/jnB9BQf+beE6NIC+CU; D_ZID=26E2F249-A655-339C-9FB0-4D8FC1F3B164; D_ZUID=D4B39FD1-E2CD-3316-AEFC-E4355F41D72E; gsScrollPos=; bid_mz5gfrJyaUcG4Pc2uugPhupj3KRV5kMt=c0dc0478-2e3c-47fc-a42d-551e466a4c5c
#     'Host': 'booking.tigerair.com',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
# }
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'routescraper.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'routescraper.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'routescraper.pipelines.RoutescraperPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

import time
import os
if not os.path.exists('logs'):
    os.mkdir('logs')
LOG_STDOUT = True
LOG_FILE = "%s/%s.txt" % ('logs', time.strftime('%Y-%m-%d'))
