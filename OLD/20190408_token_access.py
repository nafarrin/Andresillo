#!/usr/bin/env python
 
from urllib import request, parse
import requests
#import requests
import json
import datetime
import sys 

#openssl x509 -x509toreq -in certificate.crt -out CSR.csr -signkey privateKey.key
 
url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
 
payload = 'username=juan@navarro-zunzarren.com&password=Zeporro12!'
headers = {'X-Application': '07Z9ENOdKUrkC8bF', 'Content-Type': 'application/x-www-form-urlencoded'}
 
resp = requests.post('https://identitysso-cert.betfair.es/api/certlogin', data=payload, cert=('client-2048.crt', 'client-2048.key'), headers=headers)

"""
make a call API-NG
"""

def callAping(jsonrpc_req):
    try:
        req = request.Request(url, jsonrpc_req.encode(), headers2)
        #print (req)
        response = request.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse
    except request.URLError:
        print ('Oops no service available at ' + str(url))
        exit()
    except request.HTTPError:
        print ('Oops not a valid operation from the service ' + str(url))
        exit()


"""
calling getEventTypes operation
"""

def getEventTypes():
    event_type_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
    print ('Calling listEventTypes to get event Type ID')
    eventTypesResponse = callAping(event_type_req)
    eventTypeLoads = json.loads(eventTypesResponse)
    """
    print eventTypeLoads
    """

    try:
        eventTypeResults = eventTypeLoads['result']
        return eventTypeResults
    except:
        print ('Exception from API-NG' + str(eventTypeLoads['error']))
        exit()


"""
Extraction eventypeId for eventTypeName from evetypeResults
"""

def getEventTypeIDForEventTypeName(eventTypesResult, requestedEventTypeName):
    if(eventTypesResult is not None):
        for event in eventTypesResult:
            eventTypeName = event['eventType']['name']
            if( eventTypeName == requestedEventTypeName):
                return  event['eventType']['id']
    else:
        print ('Oops there is an issue with the input')
        exit()


"""
Calling marketCatalouge to get marketDetails
"""

def getMarketCatalogueForNextGBWin(eventTypeID):
    if (eventTypeID is not None):
        print ('Calling listMarketCatalouge Operation to get MarketID and selectionId')
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        market_catalogue_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventTypeIds":["' + eventTypeID + '"],' \
                                 '"marketStartTime":{"from":"' + now + '", "to":"' + (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ') + '"}},"sort":"FIRST_TO_START","maxResults":"1000",' \
                                 '"marketProjection":["COMPETITION","EVENT","EVENT_TYPE","RUNNER_DESCRIPTION","RUNNER_METADATA","MARKET_START_TIME"]}, "id": 1}'
        #"""
        print  (market_catalogue_req)
        #"""
        market_catalogue_response = callAping(market_catalogue_req)
        """
        print market_catalogue_response
        """
        market_catalouge_loads = json.loads(market_catalogue_response)
        try:
            market_catalouge_results = market_catalouge_loads['result']

            fd = open(datetime.datetime.now().strftime('%Y-%m-%dT%H_%M_%SZ') + "_marketCatalogue.log", "w")
            fd.write('marketId#market_name#marketStartTime#totalMatched#selectionId_1#runnerName_1#selectionId_2#runnerName_2#competition#event_id#event_name\n')
            for item in market_catalouge_loads['result']:
                entry = item['marketId'] + '#' + item['marketName'] + '#' + item['marketStartTime']+ '#'+ str(item['totalMatched'])+ '#'
                for runner in item['runners']:
                    entry += str(runner['selectionId'])+'#'+runner['runnerName']+'#'
                entry += item['competition']['name']+'#'+item['event']['id']+'#'+item['event']['name']+'#'
                fd.write(entry + "\n")
            fd.close()
            return market_catalouge_results
        except:
            print  ('Exception from API-NG' + str(market_catalouge_results['error']))
            exit()


def getMarketId(marketCatalogueResult):
    if( marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            print (market)
            return market['marketId']


def getSelectionId(marketCatalogueResult):
    if(marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            return market['runners'][0]['selectionId']


def getMarketBookBestOffers(marketId):
    print ('Calling listMarketBook to read prices for the Market with ID :' + marketId)
    market_book_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":["' + marketId + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS", "EX_TRADED"]}}, "id": 1}'
    """
    print  market_book_req
    """
    market_book_response = callAping(market_book_req)
    """
    print market_book_response
    """
    market_book_loads = json.loads(market_book_response)
    try:
        market_book_result = market_book_loads['result']
        return market_book_result
    except:
        print  ('Exception from API-NG' + str(market_book_result['error']))
        exit()


def printPriceInfo(market_book_result):
    if(market_book_result is not None):
        print ('Please find Best three available prices for the runners')
        for marketBook in market_book_result:
            runners = marketBook['runners']
            for runner in runners:
                print ('Selection id is ' + str(runner['selectionId']))
                if (runner['status'] == 'ACTIVE'):
                    print ('Available to back price :' + str(runner['ex']['availableToBack']))
                    print ('Available to lay price :' + str(runner['ex']['availableToLay']))
                else:
                    print ('This runner is not active')


def placeFailingBet(marketId, selectionId):
    if( marketId is not None and selectionId is not None):
        print ('Calling placeOrder for marketId :' + marketId + ' with selection id :' + str(selectionId))
        place_order_Req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/placeOrders", "params": {"marketId":"' + marketId + '","instructions":'\
                                                                                                                              '[{"selectionId":"' + str(
            selectionId) + '","handicap":"0","side":"BACK","orderType":"LIMIT","limitOrder":{"size":"0.01","price":"1.50","persistenceType":"LAPSE"}}],"customerRef":"test12121212121"}, "id": 1}'
        """
        print place_order_Req
        """
        place_order_Response = callAping(place_order_Req)
        place_order_load = json.loads(place_order_Response)
        try:
            place_order_result = place_order_load['result']
            print ('Place order status is ' + place_order_result['status'])
            """
            print 'Place order error status is ' + place_order_result['errorCode']
            """
            print ('Reason for Place order failure is ' + place_order_result['instructionReports'][0]['errorCode'])
        except:
            print  ('Exception from API-NG' + str(place_order_load['error']))
        """
        print place_order_Response
        """

if resp.status_code == 200:
  resp_json = resp.json()
  print (resp_json)
  if resp_json['loginStatus'] == 'SUCCESS':
      fd = open('serendipity.txt','w')
      fd.write( resp_json['sessionToken'] )
      fd.close()
  #print (resp_json['loginStatus'])
  #print (resp_json['sessionToken'])
else:
  print ("Request failed.")
  exit(0)

headers2 = {'X-Application': '07Z9ENOdKUrkC8bF','X-Authentication': resp_json['sessionToken'], 'Content-Type': 'application/x-www-form-urlencoded'}

eventTypesResult = getEventTypes()
print ("->")
print (eventTypesResult)
print("****************************")
BasketballEventTypeID = getEventTypeIDForEventTypeName(eventTypesResult, 'Basketball')

print ('Eventype Id for Basketball is :' + str(BasketballEventTypeID))

marketCatalogueResult = getMarketCatalogueForNextGBWin(BasketballEventTypeID)
print ("->    marquetCatalogueResult")
print(marketCatalogueResult)
print("***************marquetCatalogueResult")
marketid = getMarketId(marketCatalogueResult)
runnerId = getSelectionId(marketCatalogueResult)
"""
print marketid
print runnerId
"""
market_book_result = getMarketBookBestOffers(marketid)
print ("------begining market_book_result -----------")
print (market_book_result)
print ("------end of market_book_result -----------")
printPriceInfo(market_book_result)

placeFailingBet(marketid, runnerId)
