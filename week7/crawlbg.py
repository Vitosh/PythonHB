from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import sqlite3
import os.path


def generate_table():

    connection = sqlite3.connect("servers.db")
    cursor = connection.cursor()

    create_users_table = """CREATE TABLE IF NOT EXISTS
                        server100 (id INTEGER PRIMARY KEY, webAddress TEXT, serverType TEXT, headers TEXT, accessedFrom TEXT);
                        """
    delete_data = """DELETE FROM server100;"""

    cursor.execute(create_users_table)
    cursor.execute(delete_data)
    connection.commit()

    myHeaders = {}
    ua1 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

    myHeaders["User-Agent"] = ua1

    webSite = "http://register.start.bg"
    r = requests.get(webSite, headers=myHeaders)

    mySoup = BeautifulSoup(r.text)
    myList = []
    myImporvedList = []

    for link in mySoup.find_all('a'):
        if (link.get('href') is not None
                and len(link.get('href')) > 8
                and link.get('href')[:1] != "/"
                and "javascript" not in link.get('href')):

            myList.append(link.get('href'))

    for line in myList:
        ok = True
        if (line[:12] == "link.php?id="):
            line = webSite + "/" + line
        try:
            r = requests.head(line, headers=myHeaders, timeout=3)

            if (r.status_code != 200):
                line = r.headers["location"]

            line = urlparse(line)
            line = line.netloc

        except Exception:
            ok = False

        if line not in myImporvedList and len(line) > 6 and ok:
            myImporvedList.append(line)

    for line in myImporvedList:
        ok = True
        try:

            if (line[:4] != "http"):
                line = "http://" + line

            print("Writing {}".format(line))

            r = requests.head(line, headers=myHeaders, timeout=3)

            myAccessedFrom = webSite
            headers1 = str(r.headers)

            serverType = r.headers["server"]

            if (r.status_code == 200):
                serverSite = line
            else:
                serverSite = r.headers["location"]

        except Exception:
            ok = False

        if ok:
            sqlText = """INSERT INTO server100 (webAddress,serverType,headers, accessedFrom)
                     VALUES (?,?,?,?);"""
            cursor.execute(
                sqlText, (serverSite, serverType, headers1, myAccessedFrom))
            connection.commit()

    cursor.close()
    connection.close()
    print("SUCCESS")


def Read_Table(db_name, table_name, column_name):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, db_name)
    connection = sqlite3.connect(db_path)
    myList = []
    cursor = connection.cursor()
    sql = """SELECT {} FROM {};"""
    cursor.execute(sql.format(column_name, table_name))

    for row in cursor:
        myList.append(row[0])
    print(myList)


var_db_name = "servers.db"
var_table_name = "server100"
var_column_name = "webAddress"

Read_Table(var_db_name, var_table_name, var_column_name)
