x = list(range(0, 100, 5))
y = ["A", "B", "C", "D"]
z = ["Vitosh", "Academy", "Dot", "Com"]

print(list(zip(x, y, z)))
print([number * number for number in x if (number * number) % 2 != 1])
