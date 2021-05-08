#!/usr/bin/env python
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from Crypto.Hash import SHA256
from simhash import Simhash
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

@dataclass
class Node:
    name: str = field(default="")
    attributes: list[str] = field(default_factory=list)
    isCloseTag: bool = field(default=True)
    depth: int = field(default=0)
    #representationDepth: int = field(default=0)


class HtmlStruct:

    def __init__(self):
        self.structure = []
        self.nodes = []
        self.originalDoc = None
        self.soup = None
        self.__keptAttr = None
    
    def parseHtml(self, htmlString, leadingSpaces=False, spacesMultiplier=2, keepAttributes=False):
        self.originalDoc = htmlString
        self.soup = BeautifulSoup(htmlString, 'lxml')
        self.structure = []
        self.__keptAttr = keepAttributes
        self.__recursion(self.getSoup().html, leadingSpaces=leadingSpaces, spacesMultiplier=spacesMultiplier, keepAttributes=keepAttributes)

    def getSoup(self):
        return self.soup

    def keptAttr(self):
        return self.__keptAttr
    
    # private function for geting the structure
    def __recursion(self, tag, depth=0, spacesMultiplier = 2, leadingSpaces=False, keepAttributes=False):
        if tag.name:
            spaces = ""
            if leadingSpaces:
                spaces = " " * spacesMultiplier * depth
            
            attributes = ""
            if keepAttributes:
                for att in sorted(tag.attrs):
                    extra = ""
                    if tag.attrs[att] != '':
                        extra = "=\"\""
                    attributes += " " + att + extra
            
            self.structure.append(spaces + "<" + tag.name + attributes +">")
            
            for child in tag.children:
                self.__recursion(child, depth + 1, leadingSpaces=leadingSpaces, keepAttributes=keepAttributes)
            self.structure.append(spaces + "</" + tag.name + ">")

    # private function that creates a list of nodes where each node is a dictionary that contains the tag's name, atributes, depth...
    def __createNodes(self):
        if self.soup != None:
            self.nodes = list()
            depth = 0
            for tag in self.getStrucAsStr().split("> <"):
                if tag[0] == "<":
                    tag = tag[1:]
                if tag[-1] == ">":
                    tag = tag[:-1]
                
                node = Node()

                node.isCloseTag = (tag[0] == "/")

                if node.isCloseTag:
                    depth -= 1
                node.depth = depth
                
                node.name = tag.split(" ")[0]
                if node.name[0] == "/":
                    node.name = node.name[1:]
                
                words = tag.split()
                if len(words) > 1:
                    for word in words:
                        if word == node.name:
                            continue
                        if len(word) > 3:
                            if word[-3] == "=":
                                word = word[:-3]
                        node.attributes.append(word)
                                
                
                if not node.isCloseTag:
                    depth += 1

                self.nodes.append(node)
        else:
            raise Exception("__createNodes(), must parse a document first")

    # returns list
    def getStrucList(self):
        if self.soup != None:
            return self.structure
        else:
            raise Exception("getStrucList(), must parse a document first")

    # returns string
    def getStrucAsStr(self, end=" "):
        if self.soup != None:
            if len(end) == 1:
                result = ""
                for line in self.structure:
                    result += line.lstrip() + end
                return result[:-1]
            else:
                raise Exception("getStrucAsStr(): end parameter has to be of length 1, got length " + str(len(end)))
        else:
            raise Exception("getStrucAsStr(), must parse a document first")

    # get SHA256 hash or simhash
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

    def getNodes(self):
        self.__createNodes()
        return self.nodes

    def structDiff(self, newStruc):
        if self.soup != None:
            if self.keptAttr() != newStruc.keptAttr():
                raise Exception("2 structures that are compared must have either both kept attributes or both not kept attributes during parsing")
            if isinstance(newStruc, HtmlStruct):
                self.__createNodes()
                newNodes = newStruc.getNodes()

                i = 0
                j = 0

                imax = len(self.nodes)
                jmax = len(newNodes)

                result = []
                insertedStruct = []

                state = 0
                while i < imax and j < jmax:
                    iNode = self.nodes[i]
                    jNode = newNodes[j]
                    if state == 0:
                        if iNode == jNode:
                            state = 0
                            i += 1
                            j += 1
                            continue
                        else:
                            state = 1
                            continue
                    elif state == 1:
                        if jNode == iNode:
                            result.append(insertedStruct)
                            insertedStruct = []
                            
                            state = 0
                            i += 1
                            j += 1
                            continue
                        else:
                            insertedStruct.append(jNode)
                            
                            state = 1
                            j += 1
                            continue
                
                if i == imax and j == jmax:
                    return result
                else:
                    return None
            else:
                raise Exception("structDiff(), must pass an HtmlStruc object, got " + str(type(newStruc)))
        else:
            raise Exception("structDiff(), must parse a document first")

    @staticmethod
    def presentNodes(nodes, spacesMultiplier=2):
        # find min depth first
        minDepth = None
        for node in nodes:
            if minDepth == None or minDepth > node.depth:
                minDepth = node.depth
        
        result = ""
        for node in nodes:
            representationDepth = node.depth - minDepth
            spaces = " " * spacesMultiplier * representationDepth
            name = node.name
            if node.isCloseTag:
                name = "/" + name
            for att in node.attributes:
                name = name + " " + att + "=\"\""
            name = "<" + name + ">"
            result = result + spaces + name + "\n"
        
        return result
            

if __name__ == '__main__':

    tests = []
    tests.append(("test1.1.html", "test1.2.html"))
    tests.append(("test2.1.html", "test2.2.html"))
    tests.append(("test3.1.html", "test3.2.html"))
    tests.append(("test4.1.html", "test4.2.html"))
    tests.append(("test5.1.html", "test5.2.html"))
    tests.append(("test6.1.html", "test6.2.html"))
    tests.append(("test7.1.html", "test7.1.html"))

    for old, new in tests:
        oldfn = Path("./tests/" + old)
        newfn = Path("./tests/" + new)

        with open(oldfn, "r", encoding="utf-8") as oldf:
            with open(newfn, "r", encoding="utf-8") as newf:
                oldStr = oldf.read()
                newStr = newf.read()
                #diagnose(newStr)
                oldStruc = HtmlStruct()
                oldStruc.parseHtml(oldStr, keepAttributes=True)

                newStruc = HtmlStruct()
                newStruc.parseHtml(newStr, keepAttributes=True)

                diff = oldStruc.structDiff(newStruc)

                print ("===============================================\n")
                print("    ---------- old document ----------")
                print(HtmlStruct.presentNodes(oldStruc.getNodes()))
                print("\n    ---------- new document ----------")
                print(HtmlStruct.presentNodes(newStruc.getNodes()))
                if diff != None:
                    print("\n    ---------- number of injected structures: {} ----------\n".format(len(diff)))
                else:
                    print("    ---------- document changed beyond simple injections ----------\n")
                i = 1
                if diff:
                    for insertedStruct in diff:
                        print("    ---------- injected structure {} ----------\n".format(i))
                        i += 1
                        print (HtmlStruct.presentNodes(insertedStruct))
                        print("\n")



    
    


    

