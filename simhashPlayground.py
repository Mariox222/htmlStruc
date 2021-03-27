import re
from simhash import Simhash
def get_features(s):
    width = 6
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

h1 = Simhash('ćHow are you? I am fine. Thanks1.')
h2 = Simhash('ćHow are you? I am fine. Thanks2.')

str1 = 'ćHow are you? I am fine. Thanks1.'
str2 = 'ćHow are you? I am fine. Thanks2.'
h1 = Simhash(str1)
h2 = Simhash(str2)

print ("hash for " + str1 + " : ")
print(h1.value)
print ("hash for " + str2 + " : ")
print(h2.value)

print ("distance:")
print(h1.distance(h2))
print("\n")




str1 = 'a'
str2 = 'b'
h1 = Simhash(str1)
h2 = Simhash(str2)

print ("hash for " + str1 + " : ")
print(h1.value)
print ("hash for " + str2 + " : ")
print(h2.value)

print ("distance:")
print(h1.distance(h2))
print("\n")



str1 = '1'
str2 = '2'
h1 = Simhash(str1)
h2 = Simhash(str2)

print ("hash for " + str1 + " : ")
print(h1.value)
print ("hash for " + str2 + " : ")
print(h2.value)

print ("distance:")
print(h1.distance(h2))
print("\n")



str1 = '111111111111111'
str2 = '111111111111112'
h1 = Simhash(str1)
h2 = Simhash(str2)

print ("hash for " + str1 + " : ")
print(h1.value)
print ("hash for " + str2 + " : ")
print(h2.value)

print ("distance:")
print(h1.distance(h2))
print("\n")
