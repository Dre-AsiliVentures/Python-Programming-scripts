message="Programming is exciting"
file=open("newfile.txt","w")
bytes_written=file.write(message)
print(bytes_written)
file.close()
