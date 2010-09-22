#!/usr/bin/env python

import unittest
import xml.dom.minidom
from dominic import xpath

class TestDataModel(unittest.TestCase):
    """Section 5: Data Model"""

    xml = """
<doc xmlns:a="http://www.example.com/a">
    <element attribute="&quot;value&quot;">&lt;text&gt;</element>
    followed
    <?processing  instruction ?>
    by
    <!-- comment -->
    more text
    <a:item attribute="1" a:attribute="2" />
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)
        self.context = xpath.XPathContext(
            namespaces={'a':'http://www.example.com/a'})

    #
    # 5.1 - Root Node
    #

    def test_root_string_value(self):
        result = self.context.find('normalize-space(/)', self.doc)
        self.failUnlessEqual(result, "<text> followed by more text")

    def test_root_expanded_name(self):
        result = self.context.find('name(/)', self.doc)
        self.failUnlessEqual(result, "")

    def test_root_local_name(self):
        result = self.context.find('local-name(/)', self.doc)
        self.failUnlessEqual(result, "")

    #
    # 5.2 - Element Nodes
    #

    def test_element_string_value(self):
        result = self.context.find('normalize-space(/doc)', self.doc)
        self.failUnlessEqual(result, "<text> followed by more text")

    def test_element_expanded_name(self):
        result = self.context.find('name(//a:item)', self.doc)
        self.failUnlessEqual(result, "a:item")

    def test_element_local_name(self):
        result = self.context.find('local-name(//a:item)', self.doc)
        self.failUnlessEqual(result, "item")

    #
    # 5.3 - Attribute Nodes
    #

    def test_attribute_string_value(self):
        result = self.context.find('string(//@attribute)', self.doc)
        self.failUnlessEqual(result, '"value"')

    def test_attribute_expanded_name(self):
        result = self.context.find('name(//@a:attribute)', self.doc)
        self.failUnlessEqual(result, "a:attribute")

    def test_attribute_local_name(self):
        result = self.context.find('local-name(//@a:attribute)', self.doc)
        self.failUnlessEqual(result, "attribute")

    #
    # 5.5 - Processing Instruction Nodes
    #

    def test_pi_string_value(self):
        result = self.context.find('string(//processing-instruction())',
                                   self.doc)
        self.failUnlessEqual(result, 'instruction ')

    def test_pi_expanded_name(self):
        result = self.context.find('name(//processing-instruction())',
                                   self.doc)
        self.failUnlessEqual(result, "processing")

    def test_pi_local_name(self):
        result = self.context.find('local-name(//processing-instruction())',
                                   self.doc)
        self.failUnlessEqual(result, "processing")

    #
    # 5.6 - Comment Nodes
    #

    def test_comment_string_value(self):
        result = self.context.find('string(//comment())', self.doc)
        self.failUnlessEqual(result, ' comment ')

    def test_comment_expanded_name(self):
        result = self.context.find('name(//comment())', self.doc)
        self.failUnlessEqual(result, "")

    def test_comment_local_name(self):
        result = self.context.find('local-name(//comment())', self.doc)
        self.failUnlessEqual(result, "")

    #
    # 5.7 - Text Nodes
    #

    def test_text_string_value(self):
        result = self.context.find('string(//element/text())', self.doc)
        self.failUnlessEqual(result, '<text>')

    def test_text_expanded_name(self):
        result = self.context.find('name(//element/text())', self.doc)
        self.failUnlessEqual(result, "")

    def test_text_local_name(self):
        result = self.context.find('local-name(//element/text())', self.doc)
        self.failUnlessEqual(result, "")

if __name__ == '__main__':
    unittest.main()
