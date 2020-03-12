import random

String1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
String2 = 'abcdefghijklmnopqrstuvwxyz'
String3 = '1234567890'
String4 = '@#$&!'

def getRandomString():
    length = random.randint(5,10)
    string = ''
    while(len(string) != length):
        x = random.randint(1,4)
        if x == 1:
            string = string + String1[random.randint(0,25)]
        elif x == 2:
            string = string + String2[random.randint(0,25)]
        elif x == 3:
            string = string + String3[random.randint(0,9)]
        else:
            string = string + String4[random.randint(0,len(String4)-1)]
    return string


def getRandomNumber(start=0, end=1000):
    return random.randint(start,end)
