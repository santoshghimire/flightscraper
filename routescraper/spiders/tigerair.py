# -*- coding: utf-8 -*-
import scrapy
import sys
import codecs
import locale
# import selenium
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from routescraper.items import RouteItem


class TigerAirSpider(scrapy.Spider):
    name = "tigerair"
    allowed_domains = ["tigerair.com"]
    start_urls = [
        # "https://booking.tigerair.com/Search.aspx",
        'http://www.tigerair.com/sg/en/'
    ]

    def __init__(self):
        sys.stdout = codecs.getwriter(
            locale.getpreferredencoding())(sys.stdout)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        super(TigerAirSpider, self).__init__()
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            executable_path='browsers/chromedriver',
            chrome_options=chrome_options
        )

        # self.driver = webdriver.Chrome('browsers/chromedriver')

    # def closed(self, reason):
    #     self.driver.quit()

    def parse(self, response):
        self.origin = 'SIN'
        self.destination = 'DPS'
        self.depart = '2017-01-09'
        self.adult = '1'
        self.child = '0'
        self.infant = '0'
        self.driver.get(response.url)

        item = RouteItem()
        item['origin'] = self.origin
        item['destination'] = self.destination
        item['num_adult'] = self.adult
        item['num_child'] = self.child
        item['num_infant'] = self.infant
        item['departure_date'] = self.depart
        depart_date_obj = datetime.strptime(self.depart, "%Y-%m-%d")
        item['days_to_flight'] = (depart_date_obj - datetime.today()).days

        body = self.driver.page_source
        with open('tigerair.html', 'wb') as htmlfile:
            htmlfile.write(body)

        self.driver.find_element_by_id("radioOneWay").click()
        origin = self.driver.find_element_by_id("selOriginPicker")
        destination = self.driver.find_element_by_id("selDestPicker")
        origin.send_keys("SIN")
        destination.send_keys("DPS")

        self.driver.find_element_by_id("dateDepart").click()
        # self.driver.find_element_by_xpath(
        #     "//select[@class='ui-datepicker-year']/option[@value='2017']"
        # ).click()
        # self.driver.find_element_by_xpath(
        #     "//select[@class='ui-datepicker-month']/option[@value='0']"
        # ).click()

        # ui-datepicker-unselectable ui-state-disabled
        # if self.is_visible('table.ui-datepicker-calendar', timeout=10):
        #     depart_table = self.driver.find_element_by_xpath(
        #         "//div[@class='ui-datepicker-group ui-datepicker-group-first']/table"
        #     )
        #     depart_table.find_element_by_xpath(".//a[text()[contains(.,'12')]]").click()
        # else:
        #     print('exception')

        # self.driver.find_element_by_id("submitSearch").click()
        self.driver.save_screenshot("capture.jpeg")
        self.driver.get_screenshot_as_file('google.png')
        # b.find_element_by_xpath("//select[@name='element_name']/option[text()='option_text']").click()
        yield item

    def parse_results(self, response):
        print('parse results')
        print(response)
        item = RouteItem()
        yield item

    def is_visible(self, locator, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, locator))
            )
            return True
        except TimeoutException:
            return False
