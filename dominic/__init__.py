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

version = '0.1-unreleased'

import re
import xpath
from xml.dom import minidom

class CSSSelect(object):
    def __init__(self, selector):
        self.selector = selector

    def get_selector(self):
        sel = self.selector

        sel = self._translate_attrs(sel)
        sel = self._translate_ids(sel)
        sel = self._translate_classes(sel)

        sel = self._translate_parents(sel)
        sel = self._put_asterisks(sel)
        sel = self._fix_bars(sel)
        sel = self._fix_attrs(sel)
        return sel

    def _put_asterisks(self, selector):
        regex = re.compile(r'[/]{2}\[')
        return regex.sub("//*[", selector)

    def _translate_attrs(self, selector):
        regex = re.compile(r'\[(\S+)=(\S+)\]')
        sel = regex.sub("[@\g<1>='\g<2>']", selector)
        return sel

    def _translate_ids(self, selector):
        regex = re.compile(r'[#](\S+)')
        return regex.sub("[@id='\g<1>']", selector)

    def _translate_classes(self, selector):
        regex = re.compile(r'[.]([^ \[]+)')
        sel = regex.sub("[contains(@class, '\g<1>')]", selector)
        return sel

    def _translate_parents(self, selector):
        return "//%s" % ("//".join(selector.split()))

    def _fix_bars(self, selector):
        return selector.replace("//'", "'")

    def _fix_attrs(self, selector):
        sel = selector.replace("][", " and ")
        return sel

    @property
    def path(self):
        return self.get_selector()

class BaseHandler(object):
    def xpath(self, path):
        finder = xpath.XPath(path)
        return ElementSet(finder.find(self.document))

    def find(self, selector):
        xpather = CSSSelect(selector)
        return self.xpath(xpather.path)

    def get(self, selector):
        return self.find(selector)[0]

class ElementSet(list):
    def __init__(self, items):
        super(ElementSet, self).__init__(map(Element, items))

    def get(self):
        return self[0]

class Element(BaseHandler):
    def __init__(self, element):
        self.element = element
        self.attribute = self._fetch_attributes(element)
        self.tag = element.tagName

    def text(self):
        only_text = lambda x: hasattr(x, 'wholeText')
        get_text = lambda x: x.wholeText
        return " ".join(map(get_text, filter(only_text, self.element.childNodes)))

    def html(self):
        return self.element.toxml()

    def _fetch_attributes(self, element):
        keys = element.attributes.keys()
        return dict([(k, element.getAttribute(k)) for k in keys])

class DOM(BaseHandler):
    def __init__(self, raw):
        self.raw = raw
        self.document = minidom.parseString(raw)
