from bs4.diagnose import diagnose



testStrings = [
    "<a><b></b></a>",
    "<a><b></b>    ",
    "<a><b>    </a>",
    "<a>   </b></a>",
    "   <b></b></a>",
]
f_string = open('test3.html').read()
testStrings.append(f_string)
f_string = open('test4.html').read()
testStrings.append(f_string)

f_string = open('test5.html').read()
testStrings.append(f_string)
for test in testStrings:
    print("\n\ndiagnosing " + test)
    diagnose(test)