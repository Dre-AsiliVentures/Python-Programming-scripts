class Games:
    def sports(self):
        print("Games are sports")


class Football(Games):
    def sports(self):
        print("Game: Football")
        super().sports()


Football().sports()