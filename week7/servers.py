import requests
import matplotlib.pyplot as plt
 
 
class SomeStrings:
    myHeaders = {}
    ua1 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    myHeaders["User-Agent"] = ua1
    servApache = "apache"
    servNginx = "nginx"
    csvName = "Top 50 BG Websites.csv"
 
 
class TopSitesServer():
 
    def __init__(self):
        self.topSites = []
        self.serverDict = {}
 
    def generate_dictionary(self):
        # First part of the cralwer
        with open(SomeStrings.csvName, 'r') as mySource:
            for line in mySource:
                myAddress = line.split(",")
                myWWW = "http://www." + str(myAddress[1])
                self.topSites.append(myWWW)
        mySource.close()
 
        # Second part of the cralwer
        for site in self.topSites:
            try:
                r = requests.get(
                    site, headers=SomeStrings.myHeaders, timeout=2)
                serverType = r.headers["server"]
 
                if SomeStrings.servApache in serverType.lower():
                    serverType = SomeStrings.servApache
 
                elif SomeStrings.servNginx in serverType.lower():
                    serverType = SomeStrings.servNginx
 
                if serverType not in self.serverDict:
                    self.serverDict[serverType] = 1
                else:
                    self.serverDict[serverType] += 1
 
            except Exception:
                pass
 
    def printChart(self, values=2):
 
        myDict = self.serverDict
        myLabels = list(myDict.keys())
        mySizes = list(myDict.values())
 
        if values > len(myLabels):
            values = len(myLabels)
 
        explode = tuple(
            [0 if i > values else 0.2 for i in range(len(myLabels))])
 
        myColors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral',
                  'green', 'blue', 'yellow',
                  'silver', 'whitesmoke', 'navajowhite', 'ivory',
                  'mintcream', 'linen', 'tan', 'sienna', 'c', 'g']
 
        plt.pie([float(v) for v in mySizes],
                labels=myLabels,
                explode=explode,
                colors=myColors,
                autopct='%1.1f%%',
                startangle=20)
 
        plt.axis('equal')
        plt.show()
 
 
checkServers = TopSitesServer()
checkServers.generate_dictionary()
checkServers.printChart(50000)