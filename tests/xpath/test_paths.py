#!/usr/bin/env python

import unittest
import xml.dom.minidom
from dominic import xpath

class PathsTestCase(unittest.TestCase):
    """Test all the example paths given in section 2 of
    http://www.w3.org/TR/xpath.

    """
    def test_para_children(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" />
                <div id="2" />
                <para id="3" />
            </doc>
        """).documentElement
        result = xpath.find('child::para', doc)
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
        result = xpath.find('child::*', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "3"])

    def test_text_children(self):
        doc = xml.dom.minidom.parseString("""
            <doc>This is <i>some</i> text.</doc>
        """).documentElement
        result = xpath.find('child::text()', doc)
        self.failUnlessEqual([x.data for x in result],
                             ["This is ", " text."])

    def test_node_children(self):
        doc = xml.dom.minidom.parseString("""
            <doc>This is <i>some</i> text.</doc>
        """).documentElement
        result = xpath.find('child::node()', doc)
        self.failUnlessEqual([x.nodeType for x in result],
                             [xml.dom.Node.TEXT_NODE,
                              xml.dom.Node.ELEMENT_NODE,
                              xml.dom.Node.TEXT_NODE])

    def test_named_attribute(self):
        doc = xml.dom.minidom.parseString("""
            <doc name="foo" value="bar" />
        """).documentElement
        result = xpath.find('attribute::name', doc)
        self.failUnlessEqual([(x.name, x.value) for x in result],
                             [('name', 'foo')])

    def test_all_attributes(self):
        doc = xml.dom.minidom.parseString("""
            <doc name="foo" value="bar" />
        """).documentElement
        result = xpath.find('attribute::*', doc)
        self.failUnlessEqual([(x.name, x.value) for x in result],
                             [('name', 'foo'), ('value', 'bar')])

    def test_descendants(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1">
                    <div id="2" />
                    <para id="3" />
                </para>
            </doc>
        """).documentElement
        result = xpath.find('descendant::para', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "3"])

    def test_ancestors(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <div id="1">
                    <div id="2">
                        <context />
                    </div>
                    <div id="3" />
                </div>
                <div id="4" />
            </doc>
        """).documentElement
        node = xpath.findnode('//context', doc)
        result = xpath.find('ancestor::div', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2"])

    def test_ancestor_or_self(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <div id="1">
                    <div id="2" />
                    <div id="3" />
                </div>
                <div id="4" />
            </doc>
        """).documentElement
        node = xpath.findnode('//div[@id="3"]', doc)
        result = xpath.find('ancestor-or-self::div', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "3"])

    def test_descendant_or_self(self):
        doc = xml.dom.minidom.parseString("""
            <para id="0">
                <div id="1" />
                <para id="2">
                    <para id="3" />
                </para>
            </para>
        """).documentElement
        result = xpath.find('descendant-or-self::para', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["0", "2", "3"])

    def test_self(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para />
            </doc>
        """).documentElement
        para_node = xpath.findnode('para', doc)
        self.failUnlessEqual(len(xpath.find('self::para', doc)), 0)
        self.failUnlessEqual(len(xpath.find('self::para', para_node)), 1)

    def test_child_descendant(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter><para id="1" /><para id="2" /></chapter>
                <chapter><section><para id="3" /></section></chapter>
                <para id="4" />
            </doc>
        """).documentElement
        result = xpath.find('child::chapter/descendant::para', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "3"])

    def test_grandchildren(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter><para id="1" /><para id="2" /></chapter>
                <section><para id="3" /><sub><para id="4" /></sub></section>
                <para id="4" />
            </doc>
        """).documentElement
        result = xpath.find('child::*/child::para', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "3"])

    def test_root(self):
        doc = xml.dom.minidom.parseString("""
            <doc><a><b><context /></b></a></doc>
        """).documentElement
        node = xpath.findnode('//context', doc)
        result = xpath.find('/', node)
        self.failUnlessEqual([x.nodeType for x in result],
                             [xml.dom.Node.DOCUMENT_NODE])

    def test_root_descendant(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1"><context /></para>
                <para id="2" />
            </doc>
        """).documentElement
        node = xpath.findnode('//context', doc)
        result = xpath.find('/descendant::para', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2"])

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
        result = xpath.find('/descendant::olist/child::item', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3"])

    def test_first_child(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <div id="1" />
                <para id="2" />
                <para id="3" />
            </doc>
        """).documentElement
        result = xpath.find('child::para[position()=1]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

    def test_last_child(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" />
                <para id="2" />
                <div id="3" />
            </doc>
        """).documentElement
        result = xpath.find('child::para[position()=last()]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

    def test_last_but_one_child(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" />
                <para id="2" />
                <para id="3" />
                <div id="4" />
            </doc>
        """).documentElement
        result = xpath.find('child::para[position()=last()-1]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

    def test_all_but_first(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <div id="1" /><para id="2" />
                <div id="3" /><para id="4" />
                <div id="5" /><para id="6" />
            </doc>
        """).documentElement
        result = xpath.find('child::para[position()>1]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["4", "6"])

    def test_next_sibling(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter id="1" /><chapter id="2" />
                <context />
                <chapter id="3" /><chapter id="4" />
            </doc>
        """).documentElement
        node = xpath.findnode('//context', doc)
        result = xpath.find('following-sibling::chapter[position()=1]', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["3"])

    def test_previous_sibling(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter id="1" /><chapter id="2" />
                <context />
                <chapter id="3" /><chapter id="4" />
            </doc>
        """).documentElement
        node = xpath.findnode('//context', doc)
        result = xpath.find('preceding-sibling::chapter[position()=1]', node)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

    def test_figure_42(self):
        x = '<doc>'
        for i in xrange(10):
            for j in xrange(10):
                x += '<figure id="%d">' % ((i*10)+j)
            for j in xrange(10):
                x += '</figure>'
            x += '\n'
        x += '</doc>'
        doc = xml.dom.minidom.parseString(x).documentElement
        result = xpath.find('/descendant::figure[position()=42]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["41"])

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
        result = xpath.find(
                    '/child::doc/child::chapter[position()=5]/'
                    'child::section[position()=2]', doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["5.2"])

    def test_attr_equal(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <para id="1" type="info" />
                <para id="2" type="warning" />
                <para id="3" type="warning" />
                <para id="4" type="error" />
            </doc>
        """).documentElement
        result = xpath.find('child::para[attribute::type="warning"]', doc)
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
                'child::para[attribute::type="warning"][position()=5]', doc)
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
                'child::para[position()=5][attribute::type="warning"]', doc)
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
        result = xpath.find("child::chapter[child::title='Introduction']", doc)
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
        result = xpath.find("child::chapter[child::title]", doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3"])

    def test_chapter_and_appendix(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter id="1" />
                <appendix id="2" />
                <para id="3" />
                <chapter id="4" />
            </doc>
        """).documentElement
        result = xpath.find("child::*[self::chapter or self::appendix]", doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "2", "4"])

    def test_last_chapter_or_appendix(self):
        doc = xml.dom.minidom.parseString("""
            <doc>
                <chapter id="1" />
                <appendix id="2" />
                <para id="3" />
                <chapter id="4" />
                <para id="5" />
            </doc>
        """).documentElement
        result = xpath.find(
           "child::*[self::chapter or self::appendix][position()=last()]", doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["4"])

if __name__ == '__main__':
    unittest.main()
