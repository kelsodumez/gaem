import datetime
x = datetime.datetime.now()
x = str(x)
x = x.split (" ")
x.pop(1)
x = str(x)
print(x)