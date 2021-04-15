#!/usr/bin/env python
from bs4 import BeautifulSoup
from Crypto.Hash import SHA256
from simhash import Simhash


class HtmlStruct:

    def __init__(self):
        self.structNoAtt = []
        self.originalDoc = None
        self.soup = None
    
    def parseHtml(self, htmlString, leadingSpaces=False, spacesMultiplier=2, keepAttributes=False):
        self.originalDoc = htmlString
        self.soup = BeautifulSoup(htmlString, 'html5lib')
        self.structNoAtt = []
        self.__recursion(self.getAll().html, leadingSpaces=leadingSpaces, spacesMultiplier=spacesMultiplier, keepAttributes=keepAttributes)

    def getAll(self):
        return self.soup

    def __recursion(self, tag, depth=0, spacesMultiplier = 2, leadingSpaces=False, keepAttributes=False):
        if tag.name:
            spaces = ""
            if leadingSpaces:
                for x in range(depth * spacesMultiplier):
                    spaces += " "
            
            attributes = ""
            if keepAttributes:
                for att in sorted(tag.attrs):
                    extra = ""
                    if tag.attrs[att] != '':
                        extra = "=\"\""
                    attributes += " " + att + extra
            
            self.structNoAtt.append(spaces + "<" + tag.name + attributes +">")
            
            for child in tag.children:
                self.__recursion(child, depth + 1, leadingSpaces=leadingSpaces, keepAttributes=keepAttributes)
            self.structNoAtt.append(spaces + "</" + tag.name + ">")

    def getStruc(self):
        return self.structNoAtt

    def getStrucBeautify(self):
        if self.soup != None:
            result = ""
            for line in self.structNoAtt:
                result += line
                result += "\n"
            return result[:-1]
        else:
            return None

    def getStrucAsStr(self):
        if self.soup != None:
            result = ""
            for line in self.structNoAtt:
                result += line.lstrip() + " "
            return result[:-1]
        else:
            return None
    
    def getHash(self, simHash=False, hashStructureOnly=True):
        toHash = ""
        if hashStructureOnly:
            toHash = self.getStrucAsStr()
        else:
            toHash = self.originalDoc
        
        if toHash == None:
            return None

        if simHash:
            return Simhash(toHash)
        else:
            return SHA256.new(toHash.encode())
        


if __name__ == '__main__':

    f_string = open('test.html').read()

    o1 = HtmlStruct()
    o2 = HtmlStruct()

    o1.parseHtml(f_string, keepAttributes=False)
    o2.parseHtml(f_string, keepAttributes=True)
    
    print (o1.getStrucAsStr())
    print (o2.getStrucAsStr())

    s1 = o1.getHash(simHash=True, hashStructureOnly=True)
    s2 = o2.getHash(simHash=True, hashStructureOnly=True)
    
    print("simhash1: " + str(s1.value))
    print("simhash2: " + str(s2.value))

    print("sim hash distance:  " + str(s1.distance(s2)))
    


    

