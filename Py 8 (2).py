class County:
    def __init__(self,name,country):
        self.name=name
        self.country=country

    def welcome(self):
        print("Welcome")

    def county_name(self):
        print("County name")


Kiambu=County("Kiambu","Kenya")
Kiambu.welcome()
Kiambu.county_name()

