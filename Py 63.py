default_pin=0000
try:
    pin=float(input("Enter pin to open:"))
    if pin==default_pin:
        myfile=open("songs.txt")
    else:
        print("Incorrect pin entered")
except(ValueError,TypeError):
    print("An error occured due to input")
    
