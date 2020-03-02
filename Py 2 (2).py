class Animal:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class Zebra(Animal):
    def wild(self):
        print("Wild animal")


class Dog(Animal):
    def domestic(self):
        print("Domestic animal")


stripes=Zebra("Stripes", "brown")
print(stripes.color)

