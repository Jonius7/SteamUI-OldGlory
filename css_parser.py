'''
css_parser.py
Test script for reading the css file as css properties, and not just a text file
'''

import tinycss2

f = open("libraryroot.custom.css", "rb")
stylesheet = tinycss2.parse_stylesheet_bytes(f.read())
print(stylesheet)

print("=====")
#print(stylesheet[0])
#for style in stylesheet[0]:
    #print(style)
#    pass

print(stylesheet[0][6].content)

f.close()
