#!/usr/bin/env python

from bs4 import BeautifulSoup



class HtmlStruct:

    def __init__(self):
        self.structNoAtt = []
    
    def parseHtml(self, htmlString):
        self.soup = BeautifulSoup(htmlString, 'html.parser')
        self.__recursion(self.getAll().html)

    
    def getAll(self):
        return self.soup

    def __recursion(self, tag, depth=0, spacesMultiplier = 2):
        if tag.name:
            spaces = ""
            for x in range(depth * spacesMultiplier):
                spaces += " "
            self.structNoAtt.append(spaces + "<" + tag.name + ">")
            for child in tag.children:
                self.__recursion(child, depth + 1)
            self.structNoAtt.append(spaces + "</" + tag.name + ">")

    def getStruc(self):
        return self.structNoAtt

    def getStrucAsStr(self):
        result = ""
        for line in self.structNoAtt:
            result += line
            result += "\n"
        return result[:-1]
    

if __name__ == '__main__':

    f_string = open('test.html').read()

    o = HtmlStruct()
    o.parseHtml(f_string)

    print (o.getStrucAsStr())

