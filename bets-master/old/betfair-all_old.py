#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import json
import os
import re
import sys
import util

from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver import Chrome # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def main():
  htmls = selenium()
  for html in htmls:
    parse(html)

def selenium():
  with closing(Firefox()) as browser:
    browser.get('https://www.betfair.com/sport/basketball')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'com-coupon-line-new-layout')]")))
    #element = browser.find_element_by_xpath("//*[contains(text(), 'NBA 2015-2016')]")
    #Funciona pero lo utilizaremos más adelante
    #element = browser.find_element_by_xpath("//div[@class='teams-container']")
    elements = browser.find_elements_by_xpath("//li[contains(@class, 'com-coupon-line-new-layout')]")
    #element.click()
    #WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
    #elementsA = browser.find_elements_by_xpath("//li[@class='com-coupon-line avb-row market-avb large ']")
    #numOfElements = len(elementsA)

    htmls = []
    #for i in range(0, numOfElements):
    for i in elements[:]:
      #element = browser.find_element_by_xpath("//*[contains(text(), 'NBA 2015-2016')]")
      #element.click()
      #WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='away-team-name']")))
      # elements = browser.find_elements_by_xpath("//li[@class='com-coupon-line avb-row market-avb large ']")
      #elements = browser.find_elements_by_xpath("//div[@class='details-event']")
      #print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
      #print(i.get_attribute('innerHTML'))
      #elements[i].click()
      #WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ui-expandable ui-expandable-selected com-expandable-header-anchor has-deeplink']")))
      #htmls.append(browser.page_source)
      htmls.append(i.get_attribute('innerHTML'))
      #browser.back()
      #WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
    return htmls 


#   numOfElements = getNumberOfElements()
#   # print(numOfElements)
#   htmls = []
#   for i in range(0, numOfElements):
#     htmls.append(getHtmlFromElementIndex(i))
#   return htmls

# def getNumberOfElements():
#   with closing(Firefox()) as browser:
#     browser.get('https://www.betfair.com/sport/basketball')
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
#     element = browser.find_element_by_xpath("//*[contains(text(), 'NBA 2015-2016')]")
#     element.click()
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
#     elements = browser.find_elements_by_xpath("//li[@class='com-coupon-line avb-row market-avb large ']")
#     return len(elements)

# def getHtmlFromElementIndex(index):
#   with closing(Firefox()) as browser:
#     browser.get('https://www.betfair.com/sport/basketball')
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
#     element = browser.find_element_by_xpath("//*[contains(text(), 'NBA 2015-2016')]")
#     element.click()
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='section-header-label']")))
#     elements = browser.find_elements_by_xpath("//li[@class='com-coupon-line avb-row market-avb large ']")
#     elements[index].click()
#     WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ui-expandable ui-expandable-selected com-expandable-header-anchor has-deeplink']")))
#     return browser.page_source

def parse(html):
  soup = BeautifulSoup(html, "html.parser")
  #find teams
  pll = soup.findAll("span", "team-name")

  #for p in pll:
  for a, b in util.pairwise(pll):
    line = ""
    aux_list = []
    print (a.contents[0])
    aux_list.append(a.contents[0])
    print (b.contents[0])
    aux_list.append(b.contents[0])
    print("+++++++++++++++")
    #find date
    try:
      date = soup.find_all("span", {"class":"date ui-countdown"})
    except:
      date = ''
    if date != []:
        date = date[0].contents[0]
    else:
      date = ""
    aux_list.append(date)

    #print (soup.find_all("span", {"class":"date ui-countdown"}))
    print("---------------")
    #find bets
    try:
      runner_list = soup.find_all("div", {"class":"runner-list"})[-1]
    except:
      runner_list = ""
    money_line_first = BeautifulSoup(runner_list, "html.parser").find_all("li",{"class":"selection sel-0 "})
    #bets = soup.find_all("span",{"class":"ui-runner-price"})
    print(runner_list)
    print (money_line_first)
    """for a,b in bets:
      print("->")
      print (a)
      print (b)
      #if bet != :
      #  aux_list.append(bet.content[0])"""


    print(aux_list)
    print("*************************************")
    #player = p.find("span", text = re.compile(".*Total Points $"), attrs =  {"class": "title"})
    #if player:
      #printSoup(player)
      #printOther(p)



def printOther(p):
  pp = p.findAll("li", attrs={'class': "runner-item"})
  for bla in pp:
    printOdd(bla)

def printOdd(bla):
  spans = bla.findAll("span")
  points = spans[2].find(text=True)
  odd = spans[1].find(text=True)
  print(points)
  print(odd)

def printSoup(soup):
  for a in soup:
    print(a)
    print()

if __name__ == '__main__':
  main()
