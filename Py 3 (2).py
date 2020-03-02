class country:
    def __init__(self,continent,name):
        self.continent=continent
        self.name = name


class details(country):
    def city(self,name):
        print("Country name:")


KEN = details("Africa", "Kenya")
print(KEN.continent)
