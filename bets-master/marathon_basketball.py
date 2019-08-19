#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import json
import os
import re
import sys
import string
import re

from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import util

BOOKIE_NAME = "Marathonbet"
# BOOKIE_URL = "https://www.marathonbet.com/hr/betting/Basketball/NBA/"
BOOKIE_URL = "https://www.marathonbet.es/es/popular/Basketball/"
#BOOKIE_URL = "file:///" + os.getcwd() + "/marathonbet_popular_Basketball.html"


def main():
    htmls = util.getHtml(sys.argv, selenium, BOOKIE_NAME)
    print("*************MAIN print htmls**********")
    # print (htmls[0])
    players = []
    try:
        fd = open("marathonbet_basket.csv","w")
    except:
        print ("Error while file creation")
    print("----------------------------------------")
    header = "ID,Local, Visitor, Date, 1., 2.\n"
    fd.write(header)
    counter = 1
    for html in htmls:
        print("+++++++++++++++++++++++++++++++++++++++")
        print(html)
        line = ""
        players.extend(getTeams(html))
        players.extend(getDate(html))
        players.extend(getBets(html))
        printable = set(string.printable)
        line = str(counter) + ',' + str(getTeams(html)[0]) + ',' + str(getTeams(html)[1]) + ',' + str(getDate(html)[0].replace('\n','')) + ',' + str(getBets(html)[0]) + ',' +  str(getBets(html)[1]) + '\n'
        fd.write(line)
        counter = counter + 1
        print("+++++++++++++++++++++++++++++++++++++++")
    #util.output(sys.argv, players)
    fd.close()
    print(players)


def selenium():
    with closing(Firefox()) as browser:
        browser.get(BOOKIE_URL)
        # WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='today-member-name nowrap ']")))
        WebDriverWait(browser, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='bg coupon-row']")))
        # dates = getDates(browser.page_source)
        # elements = browser.find_elements_by_xpath("//div[@class='today-member-name nowrap ']")
        elements = browser.find_elements_by_xpath("//div[@class=' coupon-row']")

        htmls = []
        # for e in elements[::2]:
        iteration = 0
        for e in elements[:]:
            iteration = iteration + 1
            # print("Element HTML - " + str(iteration))
            # print (e.get_attribute('innerHTML'))
            # print("****************************************")
            htmls.append(e.get_attribute('innerHTML'))
            # print("-----------------------------------------")
            # e.click()

        return htmls


def getDates(html):
    soup = BeautifulSoup(html, "html.parser")
    pl = soup.findAll("td", "date")
    out = []
    for p in pl:
        out.append(p.find(text=True))
    return out


def getDate(html):
    soup = BeautifulSoup(html, "html.parser")
    pl = soup.find_all("td", {"class": "date"})
    out = []
    for p in pl:
        out.append(p.find(text=True))
    return out

def getTeams(html):
    soup = BeautifulSoup(html, "html.parser")
    players = []
    # pl = soup.findAll("span data-member-link=\"true\"")
    pl = soup.find_all("span", {"data-member-link": "true"})
    print("¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
    print(pl)
    print("?????????????????????????")
    for a, b in util.pairwise(pl):
        print("->a")
        print(a.contents[0])
        print("----")
        print(b.contents[0])
        #respA = json.loads(a.contents[0])
        # name, surname = cleanName(respA["mn"])
        # points = cleanPoints(respA["sn"])
        # under = "%.2f" % float(respA["epr"])
        #respB = json.loads(b.contents[0])
        # over = "%.2f" % float(respB["epr"])
        # player = util.getPlayer(name, surname, points, under, over, BOOKIE_NAME, BOOKIE_URL)
        # players.append(player)
        players.append(a.contents[0])
        players.append(b.contents[0])
    return players

def getBets(html):
    soup = BeautifulSoup(html, "html.parser")
    players = []
    # pl = soup.findAll("span data-member-link=\"true\"")
    pl = soup.find_all("span", {"data-prt" : "CP"})
    print("¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
    print(pl)
    print("?????????????????????????")
    for a, b in util.pairwise(pl):
        print("->a")
        print(a.contents[0])
        print("----")
        print(b.contents[0])
        #respA = json.loads(a.contents[0])
        # name, surname = cleanName(respA["mn"])
        # points = cleanPoints(respA["sn"])
        # under = "%.2f" % float(respA["epr"])
        #respB = json.loads(b.contents[0])
        # over = "%.2f" % float(respB["epr"])
        # player = util.getPlayer(name, surname, points, under, over, BOOKIE_NAME, BOOKIE_URL)
        # players.append(player)
        players.append(a.contents[0])
        players.append(b.contents[0])
    return players


def cleanName(name):
    name = re.sub("Points \(", "", name)
    name = re.sub("[,)]", "", name)
    names = name.split(' ')
    # McCollum Christian James -> C.J. McCollum
    if len(names) == 3:
        return names[1][0] + "." + names[2][0] + ".", names[0]
    else:
        return names[1], names[0]


def cleanPoints(points):
    return re.sub("^[^0-9]*", "", points)


if __name__ == '__main__':
    main()
