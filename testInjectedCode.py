from pathlib import Path
from htmlStruct import HtmlStruct

def main():

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



if __name__ == '__main__':
    main()