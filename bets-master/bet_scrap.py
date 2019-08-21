import db_connection
import betfair_basketball
import marathon_basketball

#Get bets from web bookies
def get_web_bookies ():
    """get all the web url of our bookies in order to start scrapping
    web_bookies will be a dictionay with name as index and url as its related value"""
    web_bookies = {}
    mydb = db_connection.get_connection()

    if mydb != 1:
        cursor = mydb.cursor()
        cursor.execute("select name, url from `bookie_web`;")
        records = cursor.fetchall()
        for record in records:
            name = record[0]
            url = record[1]
            web_bookies[name] = url
         #   web_bookies[record]

    return web_bookies
def get_module_names():
    """get all the to import for starting the scrapping
      module_names will be a list of modules to import """
    modules = []
    mydb = db_connection.get_connection()
    if mydb != 1:
        cursor = mydb.cursor()
        cursor.execute("select scrap from `bookie_web`;")
        records = cursor.fetchall()
        for record in records:
           modules.append(record[0])
        #   web_bookies[record]

    return modules

if __name__ == "__main__":
    """1.- Get the list of bookies and their webpages, web_bookies is a dictionary with name of the bookie house and their value will be the url related"""
    web_bookies = get_web_bookies()
    """2.- import modules"""
   #TBD
    """3.- Scrap bets"""
    try:
        betfair_basketball.main()
    except:
        print ("Error betfair")
    try:
        marathon_basketball.main()
    except:
        print ("Error Marathon")


