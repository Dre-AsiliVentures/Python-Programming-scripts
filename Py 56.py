try:
    print("Hello")
    print(1/0)
except ZeroDivisionError:
    print("Error due to division by zero")
finally:
    print("Programming is exciting")
