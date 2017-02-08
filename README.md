# flightscraper
A scrapy script to scrape flight information.

1. Get pending items from dynamodb.
2. Scrape items for flight info from two websites jetstar and airasia (using 2 crawlers).
3. Save the extracted flight info to postgres database in Redshift. Mark the queue items in dynamodb as completed.
