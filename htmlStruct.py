import re


def getTag (line, startFrom = 0):
    mode = 0
    
    result = ""
    for c in line[startFrom:]:
        
        #prije "<"
        if mode == 0:
            if c == "<":
                mode = 1
                result += c
                continue
            else:
                continue
        
        #poslije "<" moze doci "/"
        if mode == 1:
            if c == " ":
                mode = 0
                result = ""
                continue
            if c == "/":
                mode = 4
                result += c
                continue
            else:
                mode = 2
                result += c
                continue

        #poslije "/"
        if mode == 4:
            if c == " ":
                continue
            else:
                mode = 2
                result += c
                continue
        
        #parsiranje imena elementa
        elif mode == 2:
            if c == ">":
                result += c
                break
            elif c != " ":
                result += c
                continue
            else:
                mode = 3
                continue

        #parsiranje do ">"
        elif mode == 3:
            if c != ">":
                continue
            else:
                #print ("over: " + result + " + " + c)
                result += c
                break
    
    return result


#main
#print (getTag ("<a      >", 0))
#print (getTag ("</    a  >", 0))
#print (getTag ("<a> </a>", 0))

tag_re = re.compile("<(/{1})?( )*[^>]*()*>", re.IGNORECASE)

alltags = []

for line in open("test.html", 'r'):
    
    tags = []
    
    while line:
        tag = getTag(line)
        if tag == "":
            break
        tags.append(tag)
        m = tag_re.search(line)
        if m.end() < len(line):
            line = line[m.end():]
        else:
            break
    
    alltags.append(tags)

print (alltags)