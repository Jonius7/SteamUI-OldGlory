import sass
import os
#os.mkdir('css')
#os.mkdir('sass')

'''
scss = """\
$theme_color: #cc0000;
body {
    background-color: $theme_color;
}
"""
'''
#with open('sass/example.scss', 'w') as example_scss:
#     example_scss.write(scss)


#compile sass
sass.compile(dirname=('scss','.'),
             output_style='expanded')
#with open('libraryroot.custom.css') as example_css:
#    print(example_css.read())

#body{background-color:#c00}
