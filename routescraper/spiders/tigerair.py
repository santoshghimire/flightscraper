# -*- coding: utf-8 -*-
import scrapy
import time
import sys
import codecs
import locale
# import selenium

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException, WebDriverException

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
        self.driver.get(response.url)
        body = self.driver.page_source
        with open('tigerair.html', 'wb') as htmlfile:
            htmlfile.write(body)
        print('first response', response)
        # div_selectors = self.driver.find_elements_by_xpath("//div[@class='_nljxa']")[1]
        self.driver.find_element_by_id("radioOneWay").click()
        origin = self.driver.find_element_by_id("selOriginPicker")
        destination = self.driver.find_element_by_id("selDestPicker")
        self.driver.find_element_by_id("dateDepart").click()
        origin.send_keys("SIN")
        destination.send_keys("DPS")

        # self.driver.find_element_by_xpath(
        #     "//select[@class='ui-datepicker-year']/option[@value='2017']"
        # ).click()
        # self.driver.find_element_by_xpath(
        #     "//select[@class='ui-datepicker-month']/option[@value='0']"
        # ).click()

        # ui-datepicker-unselectable ui-state-disabled
        if self.is_visible('table.ui-datepicker-calendar', timeout=10):
            depart_table = self.driver.find_element_by_xpath(
                "//div[@class='ui-datepicker-group ui-datepicker-group-first']/table"
            )
            depart_table.find_element_by_xpath(".//a[text()[contains(.,'12')]]").click()
        else:
            print('exception')
        # depart.send_keys("12 Jan 2017")
        # time.sleep(10)
        # self.driver.find_element_by_class_name('ui-state-default ui-state-active ui-state-hover').click()
        time.sleep(10)
        self.driver.find_element_by_id("submitSearch").click()
        self.driver.save_screenshot("capture.jpeg")
        self.driver.get_screenshot_as_file('google.png')
        time.sleep(1000)

        # b.find_element_by_xpath("//select[@name='element_name']/option[text()='option_text']").click()
        item = RouteItem()
        yield item
        # form_data = {
        #     'MarketStructure': 'OneWay',
        #     'TripKind': 'oneWay',
        #     'selOrigin': 'SIN',
        #     'Origin': 'SIN',
        #     'selDest': 'DPS',
        #     'Destination': 'DPS',
        #     'DepartureDate': '12 Jan 2017',
        #     'ReturnDate': '12 Jan 2017',
        #     'AdultCount': '1',
        #     'ChildCount': '0',
        #     'InfantCount': '0',
        #     'PromoCode': "",
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListMarketDateRange1': '1|1',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListMarketDateRange2': '1|1',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListMarketDay1': '12',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListMarketDay2': '12',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListMarketMonth1': '2017-01',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListMarketMonth2': '2017-01',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListPassengerType_ADT': '1',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListPassengerType_CHD': '0',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$DropDownListPassengerType_INFANT': '0',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$RadioButtonMarketStructure': 'OneWay',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$TextBoxMarketDestination1': 'DPS',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$TextBoxMarketDestination2': '',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$TextBoxMarketOrigin1': 'SIN',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$TextBoxMarketOrigin2': '',
        #     'ControlGroupSearchView$ButtonSubmit': 'Get Flights',
        #     'ControlGroupSearchView_AvailabilitySearchInputSearchViewdestinationStation1': 'DPS',
        #     'ControlGroupSearchView_AvailabilitySearchInputSearchViewdestinationStation2': '',
        #     'ControlGroupSearchView_AvailabilitySearchInputSearchVieworiginStation1': 'SIN',
        #     'ControlGroupSearchView_AvailabilitySearchInputSearchVieworiginStation2': '',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$HIDDENPROMOCODE': '',
        #     'ControlGroupSearchView$AvailabilitySearchInputSearchView$HiddenFieldExternalRateId': '',
        #     '__EVENTARGUMENT': '',
        #     '__EVENTTARGET': '',
        #     '__VIEWSTATE': '/wEPDwUBMGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFR0NvbnRyb2xHcm91cEhlYWRlclNlYXJjaFZpZXckTG9naW5IZWFkZXJWaWV3U2VhcmNoVmlldyRjaGtCb3hSZW1lbWJlck1lbtVz7QBIFPTiVa3d9L4eCU/DdvQ=',
        #     'date_picker': '2017-01-12',
        #     'hiddendAdultSelection': '1',
        #     'hiddendChildSelection': '0',
        #     'pageToken': ''
        # }
        # # return scrapy.FormRequest.from_response(
        # #     response,
        # #     formdata=form_data,
        # #     callback=self.parse_results,
        # # )
        # return [scrapy.FormRequest(url="https://booking.tigerair.com/Search.aspx?culture=en-GB&gaculture=SGEN",
        #                     formdata=form_data,
        #                     callback=self.parse_results)]

    def parse_results(self, response):
        print('parse results')
        print(response)
        item = RouteItem()
        yield item

    def is_visible(self, locator, timeout=2):
        try:
            # WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, locator))
            )
            return True
        except TimeoutException:
            return False
