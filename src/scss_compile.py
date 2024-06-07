import sass
import os
#os.mkdir('css')
#os.mkdir('sass')

#compile sass
sass.compile(dirname=('scss','.'),
             output_style='expanded')
