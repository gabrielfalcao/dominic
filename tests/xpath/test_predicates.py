#!/usr/bin/env python

import unittest
import xml.dom.minidom
from dominic import xpath

class TestPredicates(unittest.TestCase):
    """Section 2.4: Predicates"""

    xml = """
<doc id="0">
    <item id="1" />
    <group id="g1">
        <item id="2" />
        <group id="g2">
            <item id="3" />
        </group>
        <item id="4" />
        <item id="5" />
    </group>
    <item id="6" />
    <choice index="2" />
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_boolean_predicate(self):
        result = xpath.find('//item[@id >= 2 and @id <= 4]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3", "4"])

    def test_child_axis(self):
        result = xpath.find('/doc/child::item[1]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1"])

    def test_ancestor_axis(self):
        result = xpath.find('//group[@id="g2"]/ancestor::*[1]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["g1"])

    def test_following_sibling_axis(self):
        result = xpath.find('//item[@id="2"]/following-sibling::item[1]',
                            self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["4"])

    def test_preceding_sibling_axis(self):
        result = xpath.find('//item[@id="5"]/preceding-sibling::item[1]',
                            self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["4"])

    def test_following_axis(self):
        result = xpath.find('//group[@id="g2"]/following::item[1]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["4"])

    def test_preceding_axis(self):
        result = xpath.find('//group[@id="g2"]/preceding::item[1]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

    def test_descendant_or_self_axis(self):
        result = xpath.find('//group[@id="g1"]/descendant-or-self::item[1]',
                            self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

    def test_ancestor_or_self_axis(self):
        result = xpath.find('//group[@id="g2"]/ancestor-or-self::*[1]',
                            self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["g2"])

    def test_numeric_expression(self):
        result = xpath.find(
            '//group/descendant::item[number(//choice/@index)*2]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["5"])

    def test_implicit_child_axis(self):
        result = xpath.find('(//item[@id="5"]/preceding-sibling::item)[1]',
                            self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

if __name__ == '__main__':
    unittest.main()
