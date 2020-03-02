def operation(x,y):
    return x/y
num_one=float(input("Enter value of x: "))
num_two=float(input("Enter value of y: "))
division=operation
try:
    print(division(num_one,num_two))
except ZeroDivisionError:
    print("An error occurred due to zero division")
