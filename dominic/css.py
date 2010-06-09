# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <dominic - python-pure implementation of CSS Selectors>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import re

class XPathTranslator(object):
    def __init__(self, selector):
        self.selector = selector

    def get_selector(self):
        sel = self.selector

        sel = self.do_translations(sel)
        sel = self.do_fixes(sel)
        return sel

    def do_translations(self, sel):
        sel = self._translate_attrs(sel)
        sel = self._translate_ids(sel)
        sel = self._translate_classes(sel)
        sel = self._translate_parents(sel)
        return sel

    def do_fixes(self, sel):
        sel = self._fix_asterisks(sel)
        sel = self._fix_bars(sel)
        sel = self._fix_attrs(sel)
        sel = self._fix_direct_childs(sel)
        return sel

    def _translate_attrs(self, selector):
        regex = re.compile(r'\[(\S+)=(\S+)\]')
        sel = regex.sub("[@\g<1>='\g<2>']", selector)
        return sel

    def _translate_ids(self, selector):
        regex = re.compile(r'[#]([^ \[]+)')
        return regex.sub("[@id='\g<1>']", selector)

    def _translate_classes(self, selector):
        regex = re.compile(r'[.]([^ .\[]+)')
        sel = regex.sub("[contains(@class, '\g<1>')]", selector)
        return sel

    def _translate_parents(self, selector):
        return "//%s" % ("//".join(selector.split()))

    def _fix_asterisks(self, selector):
        regex = re.compile(r'[/]{2}\[')
        return regex.sub("//*[", selector)

    def _fix_bars(self, selector):
        return selector.replace("//'", "'")

    def _fix_attrs(self, selector):
        sel = selector.replace("][", " and ")
        return sel

    def _fix_direct_childs(self, selector):
        sel = selector.replace("//>//", "/")
        return sel

    @property
    def path(self):
        return self.get_selector()
