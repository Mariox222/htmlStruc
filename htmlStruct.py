#!/usr/bin/env python
from bs4 import BeautifulSoup
from Crypto.Hash import SHA256
from simhash import Simhash


class HtmlStruct:

    def __init__(self, html):
        self.structNoAtt = []
        self.originalDoc = html
    
    def parseHtml(self, htmlString, leadingSpaces=False, spacesMultiplier=2):
        self.soup = BeautifulSoup(htmlString, 'html5lib')
        self.structNoAtt = []
        self.__recursion(self.getAll().html, leadingSpaces=leadingSpaces, spacesMultiplier=spacesMultiplier)

    
    def getAll(self):
        return self.soup

    def __recursion(self, tag, depth=0, spacesMultiplier = 2, leadingSpaces=False):
        if tag.name:
            spaces = ""
            
            if leadingSpaces:
                for x in range(depth * spacesMultiplier):
                    spaces += " "
            self.structNoAtt.append(spaces + "<" + tag.name + ">")
            for child in tag.children:
                self.__recursion(child, depth + 1, leadingSpaces=leadingSpaces)
            self.structNoAtt.append(spaces + "</" + tag.name + ">")

    def getStruc(self):
        return self.structNoAtt

    def getStrucBeautify(self, spacesMultiplier=2):
        self.parseHtml(self.originalDoc, leadingSpaces=True, spacesMultiplier=spacesMultiplier)
        result = ""
        for line in self.structNoAtt:
            result += line
            result += "\n"
        return result[:-1]

    def getStrucAsStr(self):
        self.parseHtml(self.originalDoc, leadingSpaces=False)
        result = ""
        for line in self.structNoAtt:
            result += line.lstrip() + " "
        return result[:-1]
    
    def getHash(self, simHash=False, hashStructureOnly=True, hexDigest=True):
        toHash = ""
        if hashStructureOnly:
            toHash = self.getStrucAsStr()
        else:
            toHash = self.originalDoc
        
        if simHash:
            sh = Simhash(toHash)
            return sh.value
        else:
            hash_object = SHA256.new(toHash.encode())
            if hexDigest:    
                return hash_object.hexdigest()
            else:
                return hash_object.digest()
        


if __name__ == '__main__':

    f_string = open('test3.html').read()

    o = HtmlStruct(f_string)
    

    print (o.getStrucBeautify(spacesMultiplier=4))
    print (o.getStrucAsStr())

    print("Crypto hash of original is:  " + str(o.getHash(simHash=False, hashStructureOnly=False, hexDigest=True)))
    print("Crypto hash of structure is: " + str(o.getHash(simHash=False, hashStructureOnly=True, hexDigest=True)))

    print("sim hash of original is:  " + str(o.getHash(simHash=True, hashStructureOnly=False)))
    print("sim hash of structure is: " + str(o.getHash(simHash=True, hashStructureOnly=True)))

    


