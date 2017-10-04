#The basic outline of this problem is to read the file, look for integers using the re.findall(),
#looking for a regular expression of '[0-9]+' and then converting the extracted strings to integers and summing up the integers.
import re

file = open(input('Enter filename: '))
l = list()
sum_num = 0
a = list()
for line in file:
    x = re.findall('[0-9]+', line)
    if len(x) > 0:
        for list in x:
            # a.append(list)
            sum_num += int(list)
# print (len(a))
print (sum_num)
