#!/usr/bin/env python

from selenium import webdriver

SAUCE_USERNAME = 'nafarrin2'
SAUCE_ACCESS_KEY = '564fb56c-2c5b-4b0c-a092-50b787deeb48'
#print ('https://%s:%s@ondemand.saucelabs.com:443/wd/hub' % (SAUCE_USERNAME, SAUCE_ACCESS_KEY))
print ('https://%s:%s@ondemand.eu-central-1.saucelabs.com/wd/hub' % (SAUCE_USERNAME, SAUCE_ACCESS_KEY))

driver = webdriver.Remote(
    desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
    command_executor= 'https://%s:%s@ondemand.eu-central-1.saucelabs.com/wd/hub' % (SAUCE_USERNAME, SAUCE_ACCESS_KEY)
)
driver.get('https://www.betfair.com/sport/basketball')
elements = driver.find_elements_by_xpath("//li[contains(@class, 'com-coupon-line-new-layout')]")
body = driver.find_element_by_css_selector('body')
print (body.get_attribute('innerHTML'))
print(driver)

driver.quit()
