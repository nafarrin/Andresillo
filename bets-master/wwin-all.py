#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import json
import os
import re
import sys

from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver import PhantomJS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import util

BOOKIE_NAME = "Wwin"
BOOKIE_URL = "https://wwin.com/sports/default.aspx?t=-60#f/0/110/0/"

def main():
  htmls = util.getHtml(sys.argv, selenium, BOOKIE_NAME)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.output(sys.argv, players)

def selenium():
  with closing(Firefox()) as browser:
  # with closing(PhantomJS()) as browser:
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item'][@fullok='430']")))
    element = browser.find_element_by_xpath("//div[@class='item'][@fullok='430']")
    element.click()
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='ex1 ex22']")))
    return [browser.page_source]

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  parovi = soup.findAll("table", "parovi extra")[-1]
  pl = parovi.findAll("tr", {"ot" : re.compile("[0-9]*")})
  players = []
  for a in pl:
    players.append(getPlayer(a))
  return players

def getPlayer(a):
  nameAndPoints = a.find("td", "parPar").find(text=True)
  odds = a.findAll("td", "tgp")
  name, surname = cleanName(nameAndPoints)
  points = cleanPoints(nameAndPoints)
  under = re.sub(",", ".", odds[1].find(text=True))
  over = re.sub(",", ".", odds[0].find(text=True))
  return util.getPlayer(name, surname, points, under, over, BOOKIE_NAME, BOOKIE_URL)

def cleanName(nameAndPoints):
  name = re.sub("^.*/", "", nameAndPoints)
  name = re.sub(" [().0-9]*$", "", name)
  names = name.split('.')
  if len(names) > 1:
    # Must remove spaces form surname because of "D.De Rozan"
    return names[0], re.sub(' ', '', names[-1])
  else:
    names = name.split(' ')
    return names[0], names[1]

def cleanPoints(nameAndPoints):
  points = re.sub("^.*\(", "", nameAndPoints)
  return re.sub("\)$", "", points)

if __name__ == '__main__':
  main()
