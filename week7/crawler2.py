from bs4 import BeautifulSoup
import requests

myHeaders = {}
ua1 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
myHeaders["User-Agent"] = ua1

webSite = 'http://vitoshacademy.com'
webSitePart = webSite.split("//", 1)[1]
myExternalLinks = []
myInternalLinks = []


def generateLinkSites(webSite):
    try:
        r = requests.get(webSite, headers=myHeaders, timeout=4)

        mySoup = BeautifulSoup(r.text)

        for link in mySoup.find_all('a'):
            myUrl = link.get('href')

            if (myUrl is not None
                    and len(myUrl) > 5
                    and "javascript" not in myUrl):

                if myUrl[:1] == "/":
                    myUrl = webSite + myUrl
                    myUrl = myUrl.replace("com//", "com/")

                if (webSitePart in myUrl):
                    if myUrl not in myInternalLinks:
                        myInternalLinks.append(myUrl)

                else:
                    if myUrl not in myExternalLinks:
                        myExternalLinks.append(myUrl)
                        extLinks.write("{}\n".format(myUrl))
                        print("{}\n".format(myUrl))
                        # extLinks.flush()

                        if len(myExternalLinks) == 1000:
                            extLinks.close()
                            return

    except Exception:
        pass

    while len(myInternalLinks) > 0:
        currentFile = myInternalLinks.pop(0)
        # print(currentFile)

        generateLinkSites(currentFile)

with open("externals", 'w') as extLinks:
    generateLinkSites(webSite)

extLinks.close()
