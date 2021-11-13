import unittest
import sys
import os
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
import backend
import js_tweaker
import datetime
import re
import shutil
from timeit import timeit

#CSS Line Parser
class TestCopyFilesFromSteam(unittest.TestCase):

    def test_reset1(self):
        js_tweaker.copy_files_from_steam(reset=1)

    def test_run_fixes_modify(self):
        a, b = backend.load_js_fixes_OLD()
        backend.write_js_fixes_OLD(a, b)

    def test_find_fixes_variables(self):
        js_tweaker.find_fix_with_variable("$^: $^ * $^", "\\1: (\\3 - 10) * $^")

class TestYaml(unittest.TestCase):
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

class TestRegex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ac = js_tweaker.RegexHandler()
    
    def test_semantic_1(self):
        print(js_tweaker.semantic_find_str('onContextMenu: this.OnContextMenu,~~hoverDelay: 300,'))

    def test_semantic_2(self):
        print(js_tweaker.semantic_find_str('onContextMenu: this.OnContextMenu,hoverDelay: 300,'))

    def test_regex_cap_groups(self):
        print(re.sub('\\\\([0-9])+', '\\(\\1)', 'Object\\(\\\\1\\.\\\\2\\)\\(\\[\\\\3\\.\\\\4\\]'))


    def test_sub_vars(self):
        print(self.ac.sub_find_with_regex("Object(%1%.%1%)([%2%, %3%], %4%)"))

    def test_combined_regex1(self):
        bb = self.ac.sub_find_with_regex('.apply(console, Object(%1%.%2%)([%3%, %4%], %5%))')
        bc = self.ac.sub_repl_with_regex('.apply(console, Object(%1%.%2%)([%3%, %4%], %5%))*/')

        print(js_tweaker.unescape(re.sub(bb, bc, '.apply(console, Object(p.g)([e, t], n))')))

    def test_combined_regex2(self):
        #start_time = datetime.datetime.now()
        bb = self.ac.sub_find_with_regex('y: %1% * %2%')
        bc = self.ac.sub_repl_with_regex('y: %1% * (%2% - 10)')

        print(js_tweaker.unescape(re.sub(bb, bc, 'y: dd * ac')))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)

    def test_combined_regex_func1(self):
        #start_time = datetime.datetime.now()
        cd = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null),'
        ce = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null), Object(%1%.%2%)([%3%.%4%], e.prototype, "OnRemoveHero", null),'

        #print(self.ac.find_and_repl(cd, ce, 'Object(a.c)([E.a], e.prototype, "OnChangeHero", null),'))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)

    def test_combined_regex_func2(self):
        #start_time = datetime.datetime.now()
        cd = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null),'
        ce = 'Object(%1%.%2%)([%3%.%4%], e.prototype, "OnChangeHero", null), Object(%1%.%2%)([%3%.%4%], e.prototype, "OnRemoveHero", null),'

        print("PROTO")
        print(self.ac.find("gesgas", 'segesgesgasegase'))
        #end_time = datetime.datetime.now()
        #print(end_time - start_time)

    def test_semantic(self):
        print(js_tweaker.semantic_find_str('switch (t) {~~case 38:'))


class TestRegOptimise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ac = js_tweaker.RegexHandler()
    
    def test_performance_whitespace1(self):
        f = self.ac.sub_find_with_regex('Object(%1%.%2%)([%3%.%4%], %5%.prototype, "OnChangeHero", null),')
        r = 'Object(%a%.%b%)([%c%.%d%], %e%.prototype, "OnChangeHero", null), Object(%a%.%b%)([%c%.%d%], %e%.prototype, "OnRemoveHero", null),'
        h = re.compile(f)
        line = '                                return (null == t ? void 0 : t[1]) && (n += 3600 * parseInt(t[1])), (null == t ? void 0 : t[2]) && (n += 60 * parseInt(t[2])), (null == t ? void 0 : t[3]) && (n += parseInt(t[3])), n'
        self.ac.find_and_repl(f, r, line, 1)
        
    def test_performance_whitespace2(self):
        f = self.ac.sub_find_with_regex('Object(%1%.%2%)([%3%.%4%], %5%.prototype, "OnChangeHero", null),')
        r = 'Object(%a%.%b%)([%c%.%d%], %e%.prototype, "OnChangeHero", null), Object(%a%.%b%)([%c%.%d%], %e%.prototype, "OnRemoveHero", null),'
        h = re.compile(f)
        line = '                                return (null == t ? void 0 : t[1]) && (n += 3600 * parseInt(t[1])), (null == t ? void 0 : t[2]) && (n += 60 * parseInt(t[2])), (null == t ? void 0 : t[3]) && (n += parseInt(t[3])), n'
        self.ac.find_and_repl(f, r, line.lstrip(), 1)
    
        
class TestMinify(unittest.TestCase):
    def test_re_minify(self):
        #shutil.copy2(os.path.join(os.getcwd(), "libraryroot.beaut.js"),
        #             os.path.join(os.getcwd(), "libraryroot.modif.js"))
        js_tweaker.re_minify_file(2)

class TestBeautify(unittest.TestCase):
    def test_beautify_files(self):
        js_tweaker.beautify_js_files(["libraryroot.js", "library.js"])
        
if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    #unittest.TextTestRunner(verbosity=3).run(suite)
    #unittest.main(argv=['ignored', '-v', 'TestBeautify.test_beautify_files'], exit=False)
    a = timeit("unittest.main(argv=['ignored', 'TestRegOptimise.test_performance_whitespace1'], exit=False)", 
           setup="import unittest",
           number=500)
    b = timeit("unittest.main(argv=['ignored', 'TestRegOptimise.test_performance_whitespace2'], exit=False)", 
           setup="import unittest",
           number=500)
    print("1: " + str(a) + "2: " + str(b))