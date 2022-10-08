import sys
import csv
import re


def main():
    if len(sys.argv) != 3:
        sys.exit("python dna.py data.csv sequence.txt")
    with open(sys.argv[1], "r") as datafile:
        datareader = csv.DictReader(datafile)
        database = list(datareader)
    with open(sys.argv[2], "r") as seqfile:
        seqreader = seqfile.read()
    strlist = []
    strcountlist = []
    for i in range(1, len(database[0].keys())):
        strlist.append(datareader.fieldnames[i])
    for i in range(len(strlist)):
        strcountlist.append(str_count(strlist[i], seqreader))
    for i in range(len(database)):
        matches = 0
        for j in range(1, len(datareader.fieldnames)):
            if int(strcountlist[j - 1]) == int(database[i][datareader.fieldnames[j]]):
                matches += 1
            if matches == (len(datareader.fieldnames) - 1):
                print(database[i]['name'])
                exit(0)
    print('No match')
    
    
def str_count(STR, seqreader):
    strgroups = re.findall(rf'(?:{STR})+', seqreader)
    longest = 0
    try:
        longest = max(strgroups, key=len)
    except ValueError:
        pass
    strcount = len(str(longest))//len(str(STR))
    return strcount
   
   
if __name__ == "__main__":
    main()