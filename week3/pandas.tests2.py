from pandas import *

network = PandaSocialNetwork()

ivo = Panda("Ivo", "ivo@pandamail.com", "male")
rado = Panda("Rado", "rado@pandamail.com", "male")
monika = Panda("Monika", "tony@pandamail.com", "female")
petko = Panda("Petko", "tony@pandamail.com", "female")
ivanka = Panda("Ivanka", "tony@pandamail.com", "female")


print(ivo)
print(rado)
print(monika)
print(petko)
print(ivanka)

for panda in [ivo, rado, monika, petko, ivanka]:
    network.add_panda(panda)

print()
print(network)
print()

network.make_friends(ivo, rado)
network.make_friends(rado, monika)
network.make_friends(monika, petko)
network.make_friends(monika, ivanka)

print(network.conection_level(ivo, rado))
