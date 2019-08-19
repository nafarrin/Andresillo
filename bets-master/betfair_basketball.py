#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import datetime
import re
from contextlib import closing

import pendulum
import util
from bs4 import BeautifulSoup
from date_management import *
from selenium.webdriver import Firefox  # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
  try:
    fd = open("betfair_basket.csv", "w")
  except:
    print("Error while file creation")
  print("----------------------------------------")
  header = "ID,Local, Visitor, Date, 1., 2.\n"
  fd.write(header)
  htmls = selenium()
  for html in htmls:
    line = parse(html)
    print (",".join(line))
    fd.write((",").join(line) + "\n")

  fd.close()
def selenium():
  with closing(Firefox()) as browser:
    browser.get('https://www.betfair.com/sport/basketball')
    #browser.get("file:///" + os.getcwd() + "/Cuotas de Baloncesto _ ¡Apuestas en Baloncesto!_ Betfair.html")
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
    aux_list.append(cleanBothEnds(a.contents[0]))
    print (b.contents[0])
    aux_list.append(cleanBothEnds(b.contents[0]))
    print("+++++++++++++++")
    #find date
    try:
      date = soup.find_all("span", {"class":"date ui-countdown"})
    except:
      date = []
    if date != []:
        date = date[0].contents[0]
    else:
      date = "En Juego"

    aux_list.append(cleanDate(date))

    #print (soup.find_all("span", {"class":"date ui-countdown"}))
    print("---------------")
    #find bets
    try:
      runner_list = soup.find_all("ul", {"class":"runner-list-selections"})[-1]
      #print(runner_list)

    except:
      runner_list = "except"

    money_line_first = runner_list.find_all("li", {"class": "selection sel-0"})
    money_line_first_bet = money_line_first[0].find_all("span", {"class":"ui-runner-price"})
    money_line_second = runner_list.find_all("li", {"class": "selection sel-1"})
    money_line_second_bet= money_line_second[0].find_all("span", {"class":"ui-runner-price"})
    print (money_line_first_bet[0].contents[0] + "++++++++++" + money_line_second_bet[0].contents[0])
    """for a,b in util.pairwise(money_line_first):
      print("->")
      print (a)
      #print (b)
      #if bet != :
      #  aux_list.append(bet.content[0])"""

    aux_list.append(cleanBothEnds(money_line_first_bet[0].contents[0]))
    aux_list.append(cleanBothEnds(money_line_second_bet[0].contents[0]))
    print(aux_list)
    print("*************************************")
    return aux_list
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

def cleanDate(date):
  #date contains a date in string, we will remove whitespaces and non-printable chars
  pattern_hour = re.compile("[0-9][0-9]:[0-9][0-9]")
  pattern_manana = re.compile("Mañana [0-9][0-9]:[0-9][0-9]")
  pattern_comienza = re.compile("Comienza en [0-9][0-9]")
  pattern_date = re.compile("[0-9][0-9] [a-z][a-z][a-z] [0-9][0-9]:[0-9][0-9]")
  if not date.isprintable():
    date = cleanBothEnds(date)
    today = datetime.datetime.now()
    #If only game time appears
    if pattern_hour.match(date) :
      hour , minute = date.split(":")
      date = str(pendulum.local(today.year, today.month, today.day, int(hour), int(minute)))
    elif pattern_comienza.match(date):
      date = str(pendulum.local(today.year, today.month, today.day))
    elif pattern_manana.match(date):
      hour, minute = date.split(" ")[-1].split(":")
      date = str(pendulum.local(today.year, today.month, today.day + 1, int(hour), int(minute)))
    elif pattern_date.match(date):
      day , month, game_time = date.split(" ")
      hour, minute = game_time.split(":")

      date = str(pendulum.local(today.year, int(aliases[month][0]), int(day), int(hour), int(minute)))
      #date = "Hoy a las " + date
  else:
    date = str(pendulum.now())
  return date

if __name__ == '__main__':
  main()
