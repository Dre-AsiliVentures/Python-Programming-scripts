class Vector_2D:
    def __init_subclass__(self,x,y):
        self.x=5
        self.y=7

    def __add__(self,other):
        return Vector_2D(self.x+other.x,self.y+other.y)


first=Vector_2D(5,7)
second=Vector_2D(3,9)
result=first+second
print(result.x)
print(result.y)