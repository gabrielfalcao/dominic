#!/usr/bin/env python

import unittest
import xml.dom.minidom
from dominic import xpath

class TestAxes(unittest.TestCase):
    """Section 2.2: Axes"""

    xml = """
<doc id="0">
    <chapter id="1">
        <section id="1.1">
            <item id="1.1.1" />
        </section>
    </chapter>
    <chapter id="2">
        <section id="2.1">
            <item id="2.1.1" />
        </section>
        <section id="2.2">
            <item id="2.2.1" /><item id="2.2.2" /><item id="2.2.3" />
        </section>
        <section id="2.3">
            <item id="2.3.1" />
        </section>
    </chapter>
    <chapter id="3">
        <section id="3.1">
            <item id="3.1.1" />
        </section>
    </chapter>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_child_axis(self):
        result = xpath.find('//*[@id="2"]/child::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2.1", "2.2", "2.3"])

    def test_parent_axis(self):
        result = xpath.find('//*[@id="2.2"]/parent::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

    def test_ancestor_axis(self):
        result = xpath.find('//*[@id="2.2"]/ancestor::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["0", "2"])

    def test_following_sibling_axis(self):
        result = xpath.find('//*[@id="2.2"]/following-sibling::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2.3"])

    def test_preceding_sibling_axis(self):
        result = xpath.find('//*[@id="2.2"]/preceding-sibling::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2.1"])

    def test_following_axis(self):
        result = xpath.find('//*[@id="2.2"]/following::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2.3", "2.3.1", "3", "3.1", "3.1.1"])

    def test_preceding_axis(self):
        result = xpath.find('//*[@id="2.2"]/preceding::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "1.1", "1.1.1", "2.1", "2.1.1"])

    def test_attribute_axis(self):
        result = xpath.find('//*[@id="2.2"]/attribute::*', self.doc)
        self.failUnlessEqual([x.value for x in result],
                             ['2.2'])

    def test_namespace_axis(self):
        self.failUnlessRaises(xpath.XPathNotImplementedError,
                              xpath.find,
                              '//*[@id="2.2"]/namespace::*', self.doc)

    def test_self_axis(self):
        result = xpath.find('//*[@id="2.2"]/self::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2.2"])

    def test_descendant_or_self_axis(self):
        result = xpath.find('//*[@id="1"]/descendant-or-self::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "1.1", "1.1.1"])

    def test_ancestor_or_self_axis(self):
        result = xpath.find('//*[@id="2.2"]/ancestor-or-self::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["0", "2", "2.2"])

    def test_partition(self):
        """Test that the ancestor, descendant, following, preceding, and
        self axes partition the document.

        """
        a = xpath.find('//*', self.doc)
        a.sort()

        b = []
        node = xpath.findnode('//*[@id="2.2"]', self.doc)
        for axis in ('ancestor','descendant','following','preceding','self'):
            b.extend(xpath.find('%s::*' % axis, node))
        b.sort()

        self.failUnlessEqual(a, b)

if __name__ == '__main__':
    unittest.main()

