from bs4 import BeautifulSoup
import requests

myHeaders = {}
ua1 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
myHeaders["User-Agent"] = ua1

webSite = 'http://vitoshacademy.com'
myExternalLinks = []
myInternalLinks = []
myList = []
myImporvedList = []
myDictionary = {}


def generateLinkSites(webSite):
    r = requests.get(webSite, headers=myHeaders)

    mySoup = BeautifulSoup(r.text)

    for link in mySoup.find_all('a'):
        myUrl = link.get('href')
        if (myUrl is not None
                and len(myUrl) > 5
                and "javascript" not in myUrl):

            if "vitosh" not in myUrl:
                myExternalLinks.append(myUrl)
            else:
                myInternalLinks.append(myUrl)

myFileInternalLinks = open("internals", 'w')
myFileInternalLinks.write(myInternalLinks)
myFileInternalLinks.close()

myFileExternalLinks = open("internals", 'w')
myFileExternalLinks.write(myExternalLinks)
myFileExternalLinks.close()

#         myList.append(link.get('href'))

# for line in myList:
#     if (line[:12] == "link.php?id="):
#         line = webSite + "/" + line
#     myImporvedList.append(line)

# myFile = open('myFile', 'w')
# myFile.write('\n'.join(myImporvedList))
# myFile.close()

# for line in myImporvedList:
#     if "apache" in line.lower():


# for line in myImporvedList:
#     try:
#         r = requests.head(line, headers=myHeaders, timeout=0.2)
#         serverType = r.headers["Server"]

# if "apache" in serverType.lower():
# serverType = "apache"

# elif "nginx" in serverType.lower():
# serverType = "nginx"

#         if serverType not in myDictionary:
#             myDictionary[serverType] = 1
#         else:
#             myDictionary[serverType] += 1

#     except Exception as e:
#         pass

# myFile = open('myFile', 'w')

# for item in sorted(myDictionary):
#     myFile.write("{} {}\n".format(item, myDictionary[item]))
# myFile.close()
