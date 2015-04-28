import webbrowser
import time

counter = 1
name = "http://www.vitoshacademy.com"

while (counter < 100):
    webbrowser.open_new_tab(name)
    counter += 1
    time.sleep(5)
    print(counter)

