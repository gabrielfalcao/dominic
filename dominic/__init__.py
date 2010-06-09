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

version = '0.1.3-unreleased'

import xpath
from xml.dom import minidom
from dominic.css import XPathTranslator

class BaseHandler(object):
    def xpath(self, path):
        finder = xpath.XPath(path)
        return ElementSet(finder.find(self.element))

    def find(self, selector):
        xpather = XPathTranslator(selector)
        return self.xpath(xpather.path)

    def get(self, selector):
        return self.find(selector)[0]

    def _get_element_text(self):
        ret = self.element.childNodes[0].wholeText
        return ret.encode('utf-8')

    def text(self, new=None):
        if isinstance(new, basestring):
            self.element.childNodes[0].replaceWholeText(new)

        return self._get_element_text()

    def html(self, new=None):
        if isinstance(new, basestring):
            while self.element.childNodes:
                self.element.childNodes.pop()

            html = minidom.parseString(new)
            node = html.childNodes[0]
            self.element.parentNode.replaceChild(node, self.element)
            self.element = node

        return self.element.toxml()

    def _fetch_attributes(self, element):
        keys = element.attributes.keys()
        return dict([(k, element.getAttribute(k)) for k in keys])

class ElementSet(list):
    def __init__(self, items):
        super(ElementSet, self).__init__(map(Element, items))

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

    @property
    def length(self):
        return len(self)

class Element(BaseHandler):
    def __init__(self, element):
        self.element = element
        self.attribute = self._fetch_attributes(element)
        self.tag = element.tagName

class DOM(BaseHandler):
    def __init__(self, raw):
        self.raw = raw
        self.document = minidom.parseString(raw)
        self.element = self.document.childNodes[0]
