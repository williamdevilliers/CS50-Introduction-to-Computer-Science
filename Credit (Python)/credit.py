import cs50

while True:
    cardnum = cs50.get_int("Number: ")
    if cardnum > 1:
        numstring = str(cardnum)
        ndigits = int(len(numstring))
        firstnumber = int(str(cardnum)[:1])
        firsttwonumbers = int(str(cardnum)[:2])
        checksum = 0
        for i in range(ndigits, -1, -2):
            thedouble = int(int((cardnum % 100) / 10) * 2)
            checksum += int((thedouble % 100) / 10) + int(thedouble % 10)
            checksum += int(cardnum % 10)
            cardnum /= 100
        if ndigits == 15 and (firsttwonumbers == 34 or firsttwonumbers == 37) and checksum % 10 == 0:
            print("AMEX")
        elif ndigits == 16 and (51 <= firsttwonumbers and firsttwonumbers <= 55) and checksum % 10 == 0:
            print("MASTERCARD")
        elif (ndigits == 16 or ndigits == 13) and firstnumber == 4 and checksum % 10 == 0:
            print("VISA")
        else:
            print("INVALID")
        break