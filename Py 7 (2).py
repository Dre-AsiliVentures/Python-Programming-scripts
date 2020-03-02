class Rectangle(object):
    def __init__(self,length,width):
        self.length=length
        self.width=width

    def getwidth(self):
        return self.width

    def setwidth(self,width):
        self.width=width

    def getheight(self):
        return self.height
    
    def setheight(self,height):
        self.height=height

    def area(self):
        return self.getheight()*self.getwidth
rect=Rectangle(30,50)
print.rect.area()
rect.setwidth()