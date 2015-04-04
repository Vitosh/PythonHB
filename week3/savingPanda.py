from just2 import *

if __name__ == '__main__':
    pandaton = Panda(
        "Pandaton",
        "pandaton@gmail.com",
        "male"
    )
    with open('data.txt', 'w') as outfile:
        json.dump(pandaton.__dict__, outfile)
