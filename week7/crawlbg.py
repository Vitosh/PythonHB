from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

myHeaders = {}
ua1 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
ua2 = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"
ua3 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
ua4 = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36"
ua5 = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36"
ua6 = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"
ua7 = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36"
ua8 = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36"

myHeaders["User-Agent"] = ua1

webSite = 'http://register.start.bg'
r = requests.get(webSite, headers=myHeaders)


mySoup = BeautifulSoup(r.text)
myList = []
myImporvedList = []
myDictionary = {}

for link in mySoup.find_all('a'):
    if (link.get('href') is not None
            and len(link.get('href')) > 8
            and link.get('href')[:1] != "/"
            and "javascript" not in link.get('href')):

        myList.append(link.get('href'))

for line in myList:
    if (line[:12] == "link.php?id="):
        line = webSite + "/" + line
    myImporvedList.append(line)

# myFile = open('myFile', 'w')
# myFile.write('\n'.join(myImporvedList))
# myFile.close()

# for line in myImporvedList:
#     if "apache" in line.lower():


for line in myImporvedList:
    try:
        r = requests.head(line, headers=myHeaders, timeout=0.1)
        serverType = r.headers["server"]

        if "apache" in serverType.lower():
            serverType = "apache"

        elif "nginx" in serverType.lower():
            serverType = "nginx"

        if serverType not in myDictionary:
            myDictionary[serverType] = 1
        else:
            myDictionary[serverType] += 1

    except Exception as e:
        pass

myFile = open('myFile', 'w')

for item in sorted(myDictionary):
    myFile.write("{} {}\n".format(item, myDictionary[item]))
myFile.close()

keys = list(myDictionary.keys())
values = list(myDictionary.values())

X = list(range(len(keys)))

plt.bar(X, list(myDictionary.values()), align="center")
plt.xticks(X, keys)

plt.title(".bg servers")
plt.xlabel("Server")
plt.ylabel("Count")
plt.savefig("histogram.png")
