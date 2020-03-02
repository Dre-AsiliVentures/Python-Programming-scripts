def longest_string(x,y):
    if len(x)>=len(y):
        print("The longest string is x")
        return x
    else:
        print("The longest string is y")
        return y
x=str(input("Enter the string of x: "))
y=str(input("Enter the string of y: "))
print(longest_string(x,y))
