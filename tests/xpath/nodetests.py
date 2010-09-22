#!/usr/bin/env python

import unittest
import xml.dom.minidom
from dominic import xpath

class TestNameTests(unittest.TestCase):
    """Section 2.3: Node Tests (Name Tests)"""

    xml = """
<doc>
    <item id="1" color="red" />
    <chapter id="c1">
        <item id="2" color="blue" />
    </chapter>
</doc>
"""

    xmlns = """
<doc xmlns="http://a.example.com" xmlns:b="http://b.example.com">
    <item id="1" color="red"/>
    <a:item id="2" xmlns:a="http://a.example.com" a:color="orange"/>
    <b:item id="3" color="yellow" />
    <item id="4" xmlns="http://a.example.com" color="green"/>
    <chapter id="c1" xmlns="http://b.example.com">
        <item id="5" color="blue" />
        <b:item id="6" b:color="indigo"/>
    </chapter>
    <chapter id="c2" xmlns="http://b.example.com" xmlns:b="http://a.example.com">
        <item id="7" b:color="violet"/>
        <b:item id="8" a:color="brown" xmlns:a="http://b.example.com"/>
    </chapter>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)
        self.docns = xml.dom.minidom.parseString(self.xmlns)

        self.context = xpath.XPathContext(
            default_namespace='http://a.example.com',
            namespaces={ 'b' : 'http://b.example.com' })

    def test_element_name_no_namespace(self):
        result = xpath.find('/descendant::item', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2"])

    def test_element_name_default_namespace(self):
        result = self.context.find('/descendant::item', self.docns)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "4", "8"])

    def test_element_name_wildcard_namespace(self):
        # This is an XPath 2.0 feature.
        result = self.context.find('/descendant::*:item', self.docns)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "3", "4", "5", "6", "7", "8"])

    def test_element_name_wildcard_name(self):
        result = self.context.find('/descendant::b:*', self.docns)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["3", "c1", "5", "6", "c2", "7"])

    def test_element_name_invalid_prefix(self):
        self.failUnlessRaises(xpath.XPathUnknownPrefixError,
                              self.context.find, '//a:*', self.docns)

    def test_element_wildcard_no_namespace(self):
        result = xpath.find('doc/child::*', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "c1"])

    def test_element_wildcard_with_namespace(self):
        result = self.context.find('doc/child::*', self.docns)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "3", "4", "c1", "c2"])

    def test_attribute_name_no_namespace(self):
        result = xpath.find('//attribute::color', self.doc)
        self.failUnlessEqual([x.value for x in result],
                             ["red", "blue"])

    def test_attribute_name_default_namespace(self):
        result = self.context.find('//attribute::color', self.docns)
        self.failUnlessEqual([x.value for x in result],
                             ["red", "yellow", "green", "blue"])

    def test_attribute_name_wildcard_namespace(self):
        result = self.context.find('//attribute::*:color', self.docns)
        self.failUnlessEqual([x.value for x in result],
                             ["red", "orange", "yellow", "green", "blue",
                              "indigo", "violet", "brown"])

    def test_attribute_name_wildcard_name(self):
        result = self.context.find('//attribute::b:*', self.docns)
        self.failUnlessEqual([x.value for x in result],
                             ["indigo", "brown"])

    def test_attribute_name_no_namespace(self):
        result = xpath.find('//attribute::*', self.doc)
        self.failUnlessEqual([x.value for x in result if x.localName=='color'],
                             ["red", "blue"])

    def test_attribute_name_with_namespace(self):
        result = self.context.find('//attribute::*', self.docns)
        self.failUnlessEqual([x.value for x in result if x.localName=='color'],
                             ["red", "orange", "yellow", "green", "blue",
                              "indigo", "violet", "brown"])

class TestKindTests(unittest.TestCase):
    """Section 2.3: Node Tests (Kind Tests)"""

    xml = """
<doc><element />text<?one pi?><?two pi?><!--comment--></doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_text(self):
        result = xpath.find('doc/child::text()', self.doc)
        self.failUnlessEqual([x.data for x in result],
                             ['text'])

    def test_comment(self):
        result = xpath.find('doc/child::comment()', self.doc)
        self.failUnlessEqual([x.data for x in result],
                             ['comment'])

    def test_processing_instruction(self):
        result = xpath.find('doc/child::processing-instruction()', self.doc)
        self.failUnlessEqual([x.target for x in result],
                             ['one', 'two'])

    def test_processing_instruction_literal(self):
        result = xpath.find('doc/child::processing-instruction("one")',
                            self.doc)
        self.failUnlessEqual([x.target for x in result],
                             ['one'])

    def test_processing_instruction_ncname(self):
        # This is an XPath 2.0 feature.
        result = xpath.find('doc/child::processing-instruction(two)',
                            self.doc)
        self.failUnlessEqual([x.target for x in result],
                             ['two'])

if __name__ == '__main__':
    unittest.main()

