import csv

kkk=raw_input("kkk:")

korrer = open('korrer.csv', "a")
korrer.write("\n")
korrer.write(kkk,str(";"))
korrer.close()

