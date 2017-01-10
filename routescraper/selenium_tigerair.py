# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from datetime import datetime
import random
from selenium.webdriver.common.proxy import Proxy, ProxyType
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec


def tigerair_scraper(item):
    # CHROME
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = rand_proxy()
    # prox.socks_proxy = "ip_addr:port"
    # prox.ssl_proxy = "ip_addr:port"

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        executable_path='../browsers/chromedriver',
        desired_capabilities=capabilities
        # chrome_options=chrome_options
    )

    # binary = FirefoxBinary('../browsers/geckodriver')
    # driver = webdriver.Firefox(firefox_binary=binary)
    driver.maximize_window()

    # wait = WebDriverWait(driver, 10)

    url = 'http://www.tigerair.com/sg/en/'
    driver.get(url)

    # click on one way
    time.sleep(rand_time())
    driver.find_element_by_id("radioOneWay").click()
    # find origin and destination inputs
    origin = driver.find_element_by_id("selOriginPicker")
    destination = driver.find_element_by_id("selDestPicker")
    # send text to origin and destination inputs
    time.sleep(rand_time())
    origin.send_keys(item['origin'])
    time.sleep(rand_time())
    destination.send_keys(item['destination'])

    # click the depart date input to open a calendar
    time.sleep(rand_time())
    driver.find_element_by_id("dateDepart").click()
    calendar = driver.find_element_by_xpath("//div[@id='ui-datepicker-div']")
    depart_date = datetime.strptime(
        item['departure_date'], "%Y-%m-%d")
    # select month
    time.sleep(rand_time())
    calendar.find_element_by_xpath(
        ".//select[@class='ui-datepicker-month']"
        "/option[@value='{0}']".format(depart_date.month - 1)
    ).click()
    # select year
    time.sleep(rand_time())
    calendar.find_element_by_xpath(
        ".//select[@class='ui-datepicker-year']/"
        "option[@value='{0}']".format(depart_date.year)
    ).click()
    time.sleep(rand_time())
    calendar.find_element_by_xpath(
        ".//a[@class='ui-state-default']"
        "[contains(text(), '{0}')]".format(depart_date.day)
    ).click()

    time.sleep(rand_time())
    driver.find_element_by_id("submitSearch").click()

    time.sleep(rand_time())
    body = driver.page_source.encode('utf-8')
    if 'Pardon Our Interruption' in body:
        print('Got Captcha... exiting')
        with open('../tigerair.html', 'wb') as htmlfile:
            htmlfile.write(body)
        quit(driver)
        return

    flights = driver.find_elements_by_xpath("//tbody[@id='tableMarket1']/tr")
    prices = []
    currencies = []
    for flight in flights:
        price = flight.find_element_by_xpath(
            ".//td[@class='light prices']/label/span[@class='price']"
        ).text
        currency = flight.find_element_by_xpath(
            ".//td[@class='light prices']/label/span[@class='price']/"
            "span[@class='currency']"
        ).text
        prices.append(float(price.strip()))
        currencies.append(currency)
        # print('price', price.strip(), currency.strip())
    price = min(prices)
    item['price'] = price
    min_index = prices.index(price)
    currency = currencies[min_index]
    item['currency'] = currency
    min_flight = flights[min_index]

    # flight info
    depart_time = min_flight.find_element_by_xpath(
        ".//li[@class='depart']/strong/span[@class='time']"
    ).text
    depart_am_pm = min_flight.find_element_by_xpath(
        ".//li[@class='depart']/strong"
    ).text
    depart_am_pm = depart_am_pm.split('-')[0].strip()

    full_depart_datetime = item['departure_date'] + ' ' + depart_time +\
        ' ' + depart_am_pm.upper()
    depart_date_obj = datetime.strptime(
        full_depart_datetime, "%Y-%m-%d %I:%M %p")
    item['departure_date'] = depart_date_obj.strftime('%Y-%m-%d %H:%M')

    # arrival
    arrive_time = min_flight.find_element_by_xpath(
        ".//li[@class='arrive']/strong/span[@class='time']"
    ).text
    arrive_am_pm = min_flight.find_element_by_xpath(
        ".//li[@class='arrive']/strong"
    ).text
    arrive_am_pm = arrive_am_pm.split('-')[0].strip()
    arrive_date = min_flight.find_element_by_xpath(
        ".//li[@class='arrive']"
    ).text.strip()
    arrive_date = datetime.strptime(
        arrive_date, "%a, %b %d, %Y").strftime("%Y-%m-%d")
    full_arrive_datetime = arrive_date + ' ' + arrive_time +\
        ' ' + arrive_am_pm.upper()
    arrive_date_obj = datetime.strptime(
        full_arrive_datetime, "%Y-%m-%d %I:%M %p")
    item['arrival_date'] = arrive_date_obj.strftime('%Y-%m-%d %H:%M')

    # flight number
    flight_number = min_flight.find_element_by_xpath(
        ".//span[@class='flight-designation']"
    ).text.replace('Flight: ', '')
    item['flight_number'] = flight_number

    airline_name = min_flight.find_element_by_xpath(
        ".//span[@class='flight-designation']/ul/li[@class='key-tr']"
    ).text
    item['airline_name'] = airline_name

    item['fare_class'] = ""
    item['price_date'] = datetime.now().strftime('%Y-%m-%d')
    item['days_to_flight'] = (depart_date_obj - datetime.today()).days
    print(item)
    time.sleep(rand_time)
    quit(driver)
    return item


def rand_time():
    return round(random.uniform(1.0, 5.0), 1)


def rand_proxy():
    return '202.106.16.36:3128'


def quit(driver):
    driver.save_screenshot("../capture.jpeg")
    driver.close()

if __name__ == '__main__':
    item = {
        'origin': 'SIN', 'destination': 'DPS',
        'departure_date': '2017-01-12', 'num_adult': '1',
        'num_child': '0', 'num_infant': '0'
    }
    tigerair_scraper(item)
