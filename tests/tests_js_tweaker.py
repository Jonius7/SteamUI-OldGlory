import unittest
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
import backend
import js_tweaker
import datetime
import re

#CSS Line Parser
class TestCopyFilesFromSteam(unittest.TestCase):

    def test_reset1(self):
        js_tweaker.copy_files_from_steam(reset=1)

    def test_run_fixes_modify(self):
        a, b = backend.load_js_fixes()
        backend.write_js_fixes(a, b)

    def test_find_fixes_variables(self):
        js_tweaker.find_fix_with_variable("$^: $^ * $^", "\\1: (\\3 - 10) * $^")

    ###
    def test_parse_yaml(self):
        yaml = js_tweaker.YamlHandler(sys.path[0] + "/../js_tweaks.yml")
        return yaml

    def test_retrieve_find(self):
        yaml = self.test_parse_yaml()
        start_time = datetime.datetime.now()
        for fix in yaml.data:
            for find in yaml.data[fix]["strings"]:
                    #print(find)
                    pass
        end_time = datetime.datetime.now()
        print(end_time - start_time)

    def test_parse_old_fixes(self):
        start_time = datetime.datetime.now()
        js_tweaker.parse_fixes_file_OLD('fixes.txt')
        end_time = datetime.datetime.now()
        print(end_time - start_time)

    #def test_write_modif(self):
    #    yaml = self.test_parse_yaml()
    #    js_tweaker.write_modif_file(yaml.data)

    def test_semantic_1(self):
        print(js_tweaker.semantic_find_str('onContextMenu: this.OnContextMenu,~~hoverDelay: 300,'))

    def test_semantic_2(self):
        print(js_tweaker.semantic_find_str('onContextMenu: this.OnContextMenu,hoverDelay: 300,'))

    def test_regex_cap_groups(self):
        print(re.sub('\\\\([0-9])+', '\\(\\1)', 'Object\\(\\\\1\\.\\\\2\\)\\(\\[\\\\3\\.\\\\4\\]'))


    def test_sub_vars(self):
        ac = js_tweaker.RegexHandler()
        print(ac.sub_find_with_regex("Object(%1%.%1%)([%2%, %3%], %4%)"))

    def test_combined_regex1(self):
        ad = js_tweaker.RegexHandler()
        bb = ad.sub_find_with_regex('.apply(console, Object(%1%.%2%)([%3%, %4%], %5%))')
        bc = ad.sub_repl_with_regex('.apply(console, Object(%1%.%2%)([%3%, %4%], %5%))*/')

        print(js_tweaker.unescape(re.sub(bb, bc, '.apply(console, Object(p.g)([e, t], n))')))

    def test_combined_regex2(self):
        #start_time = datetime.datetime.now()
        ad = js_tweaker.RegexHandler()
        bb = ad.sub_find_with_regex('y: %1% * %2%')
        bc = ad.sub_repl_with_regex('y: %1% * (%2% - 10)')

        print(js_tweaker.unescape(re.sub(bb, bc, 'y: dd * ac')))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)

    def test_combined_regex_func1(self):
        #start_time = datetime.datetime.now()
        ad = js_tweaker.RegexHandler()
        cd = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null),'
        ce = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null), Object(%1%.%2%)([%3%.%4%], e.prototype, "OnRemoveHero", null),'

        print(ad.find_and_repl(cd, ce, 'Object(a.c)([E.a], e.prototype, "OnChangeHero", null),'))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)

    def test_combined_regex_func2(self):
        #start_time = datetime.datetime.now()
        ad = js_tweaker.RegexHandler()
        cd = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null),'
        ce = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null), Object(%1%.%2%)([%3%.%4%], e.prototype, "OnRemoveHero", null),'

        print("PROTO")
        print(ad.find("gesgas", 'segesgesgasegase'))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)
        
if __name__ == '__main__':
    unittest.main()
