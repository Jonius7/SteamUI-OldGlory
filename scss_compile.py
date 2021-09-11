'''
scss_compile.py
Simple script that compiles the .scss files into libraryroot.custom.css
'''

import sass
import os
#os.mkdir('css')
#os.mkdir('sass')

#compile sass
sass.compile(dirname=('scss','.'),
             output_style='expanded')
