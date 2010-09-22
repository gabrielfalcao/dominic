#!/usr/bin/env python

import unittest
import xml.dom.minidom
from dominic import xpath

class TestAbbreviations(unittest.TestCase):
    """Section 2.5: Abbreviated Syntax"""

    def test_para_children(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" />
                <div id="2" />
                <para id="3" />
            </doc>
        """).documentElement
        result = xpath.find('para', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "3"])

    def test_all_children(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" />
                <div id="2" />
                <para id="3" />
            </doc>
        """).documentElement
        result = xpath.find('*', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "3"])

    def test_text_children(self):
        doc = xml.dom.minidom.parseString("""
            <doc>This is <i>some</i> text.</doc>
        """).documentElement
        result = xpath.find('text()', doc)
        self.failUnlessEqual([x.data for x in result],
                             ["This is ", " text."])

    def test_named_attribute(self):
        doc = xml.dom.minidom.parseString("""
            <doc name="foo" value="bar" />
        """).documentElement
        result = xpath.find('@name', doc)
        self.failUnlessEqual([(x.name, x.value) for x in result],
                             [('name', 'foo')])

    def test_all_attributes(self):
        doc = xml.dom.minidom.parseString("""
            <doc name="foo" value="bar" />
        """).documentElement
        result = xpath.find('@*', doc)
        self.failUnlessEqual([(x.name, x.value) for x in result],
                             [('name', 'foo'), ('value', 'bar')])

    def test_first_child(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" /><para id="2" /><para id="3" />
            </doc>
        """).documentElement
        result = xpath.find('para[1]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1"])

    def test_last_child(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" /><para id="2" /><para id="3" />
            </doc>
        """).documentElement
        result = xpath.find('para[last()]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["3"])

    def test_grandchildren(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter><para id="1" /><para id="2" /></chapter>
                <section><para id="3" /><sub><para id="4" /></sub></section>
                <para id="4" />
            </doc>
        """).documentElement
        result = xpath.find('*/para', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "3"])

    def test_section_5_2(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter id="1" /><chapter id="2" /><chapter id="3" />
                <chapter id="4">
                  <section id="4.1" /><section id="4.2" /><section id="4.3" />
                </chapter>
                <chapter id="5">
                  <section id="5.1" /><section id="5.2" /><section id="5.3" />
                </chapter>
            </doc>
        """).documentElement
        result = xpath.find('/doc/chapter[5]/section[2]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["5.2"])

    def test_child_descendant(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter><para id="1" /><para id="2" /></chapter>
                <chapter><section><para id="3" /></section></chapter>
                <para id="4" />
            </doc>
        """).documentElement
        result = xpath.find('chapter//para', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "3"])

    def test_absolute_descendant_or_self(self):
        doc = xml.dom.minidom.parseString("""
            <para id="0">
                <div id="1" />
                <para id="2">
                    <para id="3" />
                </para>
            </para>
        """).documentElement
        node = xpath.findnode('//para[@id="2"]', doc)
        result = xpath.find('//para', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["0", "2", "3"])

    def test_olist_item(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <item id="1">
                    <context />
                    <olist><item id="2" /></olist>
                </item>
                <olist><item id="3" /></olist>
            </doc>
        """).documentElement
        node = xpath.findnode('//context', doc)
        result = xpath.find('//olist/item', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3"])

    def test_self(self):
        doc = xml.dom.minidom.parseString("""
            <doc id="0">
                <para id="1"/>
            </doc>
        """).documentElement
        result = xpath.find('.', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["0"])

    def test_relative_descendant_or_self(self):
        doc = xml.dom.minidom.parseString("""
            <para id="0">
                <div id="1" />
                <para id="2">
                    <para id="3" />
                </para>
            </para>
        """).documentElement
        node = xpath.findnode('//para[@id="2"]', doc)
        result = xpath.find('.//para', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["3"])

    def test_parent(self):
        doc = xml.dom.minidom.parseString("""
            <doc id="0">
                <chapter id="1">
                    <item id="2" />
                    <item id="3"><subitem id="4" /></item>
                </chapter>
            </doc>
        """).documentElement
        node = xpath.findnode('//item[@id="3"]', doc)
        result = xpath.find('..', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1"])

    def test_parent_attr(self):
        doc = xml.dom.minidom.parseString("""
            <doc id="0">
                <chapter id="1" lang="en">
                    <item id="2" />
                    <item id="3"><subitem id="4" /></item>
                </chapter>
            </doc>
        """).documentElement
        node = xpath.findnode('//item[@id="3"]', doc)
        result = xpath.find('../@lang', node)
        self.failUnlessEqual([x.value for x in result],
                             ["en"])

    def test_attr_equal(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" type="info" />
                <para id="2" type="warning" />
                <para id="3" type="warning" />
                <para id="4" type="error" />
            </doc>
        """).documentElement
        result = xpath.find('para[@type="warning"]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3"])

    def test_fifth_warning(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" type="info" />
                <para id="2" type="warning" />
                <para id="3" type="warning" />
                <para id="4" type="warning" />
                <para id="5" type="error" />
                <para id="6" type="warning" />
                <para id="7" type="warning" />
            </doc>
        """).documentElement
        result = xpath.find(
                'para[@type="warning"][5]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["7"])

    def test_fifth_if_warning(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" type="info" />
                <para id="2" type="warning" />
                <para id="3" type="warning" />
                <para id="4" type="warning" />
                <para id="5" type="error" />
                <para id="6" type="warning" />
                <para id="7" type="warning" />
            </doc>
        """).documentElement
        result = xpath.find(
                'para[5][@type="warning"]', doc)
        self.failUnlessEqual(result, [])

    def test_introductions(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter id="1" />
                <chapter id="2"><title>Introduction</title></chapter>
                <chapter id="3"><title>Body</title></chapter>
                <chapter id="4">
                    <title>Another</title>
                    <title>Introduction</title>
                </chapter>
            </doc>
        """).documentElement
        result = xpath.find("chapter[title='Introduction']", doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "4"])

    def test_titles(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter id="1" />
                <chapter id="2"><title /></chapter>
                <chapter id="3"><title /><title /></chapter>
            </doc>
        """).documentElement
        result = xpath.find("chapter[title]", doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3"])

    def test_secretary_and_assistant(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <employee name="Alice" />
                <employee name="Bob" secretary="Cathy" />
                <employee name="Dianne" secretary="Edward" assistant="Fran" />
            </doc>
        """).documentElement
        result = xpath.find("employee[@secretary and @assistant]", doc)
        self.failUnlessEqual([x.getAttribute("name") for x in result],
                             ["Dianne"])

if __name__ == '__main__':
    unittest.main()
