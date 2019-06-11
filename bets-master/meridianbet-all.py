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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import util

BOOKIE_NAME = "Meridianbet"
BOOKIE_URL = "https://meridianbet.com/#!standard_betting;leagueIDs=593"

def main():
  htmls = util.getHtml(sys.argv, selenium, BOOKIE_NAME)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.output(sys.argv, players)

def selenium():
  with closing(Firefox()) as browser:
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='gwt-Label home']")))
    return [browser.page_source]

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  dates = soup.findAll("div", "gwt-Label date")
  times = soup.findAll("div", "gwt-Label time")
  pl = soup.findAll("div", "rivals")
  pa = soup.findAll("div", "selections three four")
  players = []
  for date, time, a, b in zip(dates, times, pl, pa):
    players.append(getPlayer(date, time, a, b))
  return players

def getPlayer(date, time, a, b):
  odds = b.findAll("div", "gwt-Label")
  name, surname = getNameAndSurname(a.find("div", "gwt-Label away").find(text=True))
  points = odds[7].find(text=True)
  under = odds[1].find(text=True)
  over = odds[5].find(text=True)
  return util.getPlayer(name, surname, points, under, over, BOOKIE_NAME, BOOKIE_URL)

def getNameAndSurname(partialName):
  partialName = re.sub(" \(.*\)$", "", partialName)
  partialName = re.sub("\..*$", "", partialName)
  names = partialName.split(' ')
  return names[1], names[0]

if __name__ == '__main__':
  main()
