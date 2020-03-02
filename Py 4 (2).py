class Country:
    def method_one(self):
        print("Country: Kenya")


class Capital(Country):
    def method_two(self):
        print("Capital city: Nairobi")


class population(Capital):
    def method_three(self):
        print("Population : 3 million")


x = population()
x.method_one()
x.method_two()
x.method_three()