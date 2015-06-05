males = [
    {
        "name": "A",
        "is_free": True,
        "gender": "male",
        "preferences": ["10", "20", "30", "40", "50", "60"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "B",
        "is_free": True,
        "gender": "male",
        "preferences": ["20", "30", "50", "10", "40", "60"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "C",
        "is_free": True,
        "gender": "male",
        "preferences": ["20", "30", "10", "50", "40", "60"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "D",
        "is_free": True,
        "gender": "male",
        "preferences": ["20", "30", "10", "50", "40", "60"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "E",
        "is_free": True,
        "gender": "male",
        "preferences": ["10", "30", "20", "50", "40", "60"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "F",
        "is_free": True,
        "gender": "male",
        "preferences": ["20", "30", "10", "50", "40", "60"],
        "engaged_to": "",
        "proposed_to":[],
    },
]

females = [
    {
        "name": "10",
        "is_free": True,
        "gender": "female",
        "preferences": ["A", "B", "C", "E", "D", "F"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "20",
        "is_free": True,
        "gender": "female",
        "preferences": ["C", "A", "B", "D", "E", "F"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "30",
        "is_free": True,
        "gender": "female",
        "preferences": ["C", "A", "B", "D", "E", "F"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "40",
        "is_free": True,
        "gender": "female",
        "preferences": ["A", "B", "C", "E", "D", "F"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "50",
        "is_free": True,
        "gender": "female",
        "preferences": ["A", "B", "C", "E", "D", "F"],
        "engaged_to": "",
        "proposed_to":[],
    },
    {
        "name": "60",
        "is_free": True,
        "gender": "female",
        "preferences": ["B", "A", "C", "D", "F", "E"],
        "engaged_to": "",
        "proposed_to":[],
    },
]


def break_engagement(person):
    breakingWith = is_engaged_to(person)
    for m in males:
        if m["name"] == person:
            if m["engaged_to"] != "":
                m["engaged_to"] = ""
                m["is_free"] = True
                print("{} is breaking with {}.".format(person, breakingWith))

    for f in females:
        if f["name"] == person:
            if f["engaged_to"] != "":
                f["engaged_to"] = ""
                m["is_free"] = True
                print("{} is breaking with {}.".format(person, breakingWith))


def is_engaged_to(person):
    for m in males:
        if m["name"] == person:
            return m["engaged_to"]

    for f in females:
        if f["name"] == person:
            return f["engaged_to"]

    return False


def is_engaged(person):
    for m in males:
        if m["name"] == person:
            if m["engaged_to"] != "":
                return True

    for f in females:
        if f["name"] == person:
            if f["engaged_to"] != "":
                return True

    return False


def who_do_you_love_more(person, candidate1, candidate2):
    for m in males:
        if m["name"] == person:
            for x in range(0, len(males)):
                if candidate1 == m["preferences"][x]:
                    return candidate1
                if candidate2 == m["preferences"][x]:
                    return candidate2

    for f in females:
        if f["name"] == person:
            for x in range(0, len(males)):
                if candidate1 == f["preferences"][x]:
                    return candidate1
                if candidate2 == f["preferences"][x]:
                    return candidate2


def engage(dramaKing, dramaQueen):
    for m in males:
        if m["name"] == dramaKing:
            m["engaged_to"] = dramaQueen
            m["is_free"] = False

    for f in females:
        if f["name"] == dramaQueen:
            f["engaged_to"] = dramaKing
            f["is_free"] = False


def get_name_from_ranking(dramaKing, rank):
    for m in males:
        if m["name"] == dramaKing:
            return m["preferences"][rank]


def main():
    while (True):
        numberOfPairs = len(males)
        good = 1
        for m in males:
            dramaKing = m["name"]
            if (m["is_free"] == False) and (len(m["proposed_to"]) != numberOfPairs):
                good += 1
                if good == numberOfPairs:
                    print("\n\n\nSuccess!")
                    return

            for x in range(0, numberOfPairs):
                if not is_engaged(dramaKing):
                    if x not in m["proposed_to"]:
                        m["proposed_to"].append(x)

                        woman = get_name_from_ranking(dramaKing, x)

                        if is_engaged(woman):
                            currentManOfTheEngaged = is_engaged_to(woman)

                            betterLover = who_do_you_love_more(
                                woman, currentManOfTheEngaged, dramaKing)

                            engage(betterLover, woman)

                            if betterLover != currentManOfTheEngaged:
                                break_engagement(currentManOfTheEngaged)
                        else:
                            engage(dramaKing, woman)


def happyend():
    print("Resolution:\n")
    for m in males:
        dramaKing = m["name"]
        dramaQueen = m["engaged_to"]

        print("{} <---> {}".format(dramaKing, dramaQueen))


main()
happyend()
