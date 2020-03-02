try:
    f=open("filename.txt")
    print(f.read())
finally:
    f.close()
