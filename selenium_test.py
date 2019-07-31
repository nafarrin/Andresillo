#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SAUCE_USERNAME = 'nafarrin2'
SAUCE_ACCESS_KEY = '564fb56c-2c5b-4b0c-a092-50b787deeb48'
#print ('https://%s:%s@ondemand.saucelabs.com:443/wd/hub' % (SAUCE_USERNAME, SAUCE_ACCESS_KEY))
print ('https://%s:%s@ondemand.eu-central-1.saucelabs.com/wd/hub' % (SAUCE_USERNAME, SAUCE_ACCESS_KEY))

driver = webdriver.Remote(
    desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
    command_executor= 'https://%s:%s@ondemand.eu-central-1.saucelabs.com/wd/hub' % (SAUCE_USERNAME, SAUCE_ACCESS_KEY)
)
driver.get('https://www.betfair.es/sport/basketball')
WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'com-coupon-line-new-layout')]")))
elements = driver.find_elements_by_xpath("//li[contains(@class, 'com-coupon-line-new-layout')]")
#body = driver.find_element_by_css_selector('body')
#print (body.get_attribute('innerHTML'))
print(elements)

driver.quit()
