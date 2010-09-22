#!/usr/bin/env python

import unittest
import xml.dom.minidom
from dominic import xpath

class TestNodeSetFunctions(unittest.TestCase):
    """Section 4.1: Node Set Functions"""

    xml = """
<!DOCTYPE doc [<!ATTLIST item identifier ID #IMPLIED>]>
<doc>
    <item id="1" identifier="a" />
    <item id="2" identifier="b" />
    <item id="3" identifier="c" />
    <item id="4" identifier="d" />
    <item id="5" identifier="e" />
    <reference>a</reference>
    <reference>c</reference>
    <reference>e</reference>
    <namespace xmlns="http://www.example.com/a"
               xmlns:b="http://www.example.com/b">
        <item id="6" />
        <b:item id="7" b:value="42" />
    </namespace>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_last(self):
        result = xpath.find('//item[@id=last()]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["5"])

    def test_position(self):
        result = xpath.find('//item[position()=3]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["3"])

    def test_count(self):
        result = xpath.find('count(//item)', self.doc)
        self.failUnlessEqual(result, 5)

    def test_id_string(self):
        result = xpath.find('id("c")', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["3"])

    def test_id_nodeset(self):
        result = xpath.find('id(//reference)', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1", "3", "5"])

    def test_id_scope(self):
        result = xpath.find('//reference/id("a")', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["1"])

    def test_local_name(self):
        result = xpath.find('local-name(//.[@id=7])', self.doc)
        self.failUnlessEqual(result, 'item')

    def test_local_name_implicit(self):
        result = xpath.find(
            'number(//.[@id=7]/attribute::*[local-name()="value"])', self.doc)
        self.failUnlessEqual(result, 42)

    def test_local_name_empty(self):
        result = xpath.find('local-name(/absent)', self.doc)
        self.failUnlessEqual(result, '')

    def test_namespace_uri(self):
        result = xpath.find('namespace-uri(//.[@id>5])', self.doc)
        self.failUnlessEqual(result, 'http://www.example.com/a')

    def test_namespace_uri_implicit(self):
        result = xpath.find(
           '//.[@id and namespace-uri()="http://www.example.com/b"]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["7"])

    def test_namespace_uri_empty(self):
        result = xpath.find('namespace-uri(/absent)', self.doc)
        self.failUnlessEqual(result, '')

    def test_name(self):
        result = xpath.find('name(//.[@id=7])', self.doc)
        self.failUnlessEqual(result, 'b:item')

    def test_name_implicit(self):
        result = xpath.find('//.[name()="b:item"]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["7"])

    def test_name_empty(self):
        result = xpath.find('name(/absent)', self.doc)
        self.failUnlessEqual(result, '')

class TestStringFunctions(unittest.TestCase):
    """Section 4.2: String Functions"""

    xml = """
<doc>
    <para id="1">One</para>
    <para id="2">Two</para>
    <para id="3">Three</para>
    <para id="4">
        Four
    </para>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_string_nodeset(self):
        result = xpath.find('string(//para)', self.doc)
        self.failUnlessEqual(result, 'One')

    def test_string_empty_nodeset(self):
        result = xpath.find('string(//inconceivable)', self.doc)
        self.failUnlessEqual(result, '')

    def test_string_number_nan(self):
        result = xpath.find('string(0 div 0)', self.doc)
        self.failUnlessEqual(result, 'NaN')

    def test_string_number_infinity(self):
        result = xpath.find('string(1 div 0)', self.doc)
        self.failUnlessEqual(result, 'Infinity')

    def test_string_number_negative_infinity(self):
        result = xpath.find('string(-1 div 0)', self.doc)
        self.failUnlessEqual(result, '-Infinity')

    def test_string_number_integer(self):
        result = xpath.find('string(2.5 * 2)', self.doc)
        self.failUnlessEqual(result, '5')

    def test_string_number_float(self):
        result = xpath.find('string(1 div -2)', self.doc)
        self.failUnlessEqual(result, '-0.5')

    def test_string_boolean_true(self):
        result = xpath.find('string(1 = 1)', self.doc)
        self.failUnlessEqual(result, 'true')

    def test_string_boolean_false(self):
        result = xpath.find('string(1 = 2)', self.doc)
        self.failUnlessEqual(result, 'false')

    def test_string_string(self):
        result = xpath.find('string("string")', self.doc)
        self.failUnlessEqual(result, 'string')

    def test_string_implicit(self):
        result = xpath.find('//para[string()="Two"]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2"])

    def test_string_concat(self):
        result = xpath.find('concat(//para, ":", //para[2])', self.doc)
        self.failUnlessEqual(result, 'One:Two')

    def test_string_starts_with_true(self):
        result = xpath.find('starts-with("foo-bar", "foo")', self.doc)
        self.failUnlessEqual(result, True)

    def test_string_starts_with_false(self):
        result = xpath.find('starts-with("foo-bar", "bar")', self.doc)
        self.failUnlessEqual(result, False)

    def test_string_ends_with_true(self):
        result = xpath.find('ends-with("foo-bar", "bar")', self.doc)
        self.failUnlessEqual(result, True)

    def test_string_ends_with_false(self):
        result = xpath.find('ends-with("foo-bar", "foo")', self.doc)
        self.failUnlessEqual(result, False)

    def test_string_contains_true(self):
        result = xpath.find('contains("foo-bar", "o-b")', self.doc)
        self.failUnlessEqual(result, True)

    def test_string_contains_false(self):
        result = xpath.find('contains("foo-bar", "b-o")', self.doc)
        self.failUnlessEqual(result, False)

    def test_string_substring_before(self):
        result = xpath.find('substring-before("foo::bar", "::")', self.doc)
        self.failUnlessEqual(result, 'foo')

    def test_string_substring_before_no_match(self):
        result = xpath.find('substring-before("foo::bar", "--")', self.doc)
        self.failUnlessEqual(result, '')

    def test_string_substring_after(self):
        result = xpath.find('substring-after("foo::bar", "::")', self.doc)
        self.failUnlessEqual(result, 'bar')

    def test_string_substring_after_no_match(self):
        result = xpath.find('substring-after("foo::bar", "--")', self.doc)
        self.failUnlessEqual(result, '')

    def test_string_substring_two_arg(self):
        result = xpath.find('substring("12345", 2)', self.doc)
        self.failUnlessEqual(result, '2345')

    def test_string_substring_three_arg(self):
        result = xpath.find('substring("12345", 2, 3)', self.doc)
        self.failUnlessEqual(result, '234')

    def test_string_substring_floats(self):
        result = xpath.find('substring("12345", 1.5, 2.6)', self.doc)
        self.failUnlessEqual(result, '234')

    def test_string_substring_offset_start(self):
        result = xpath.find('substring("12345", 0, 3)', self.doc)
        self.failUnlessEqual(result, '12')

    def test_string_substring_nan_start(self):
        result = xpath.find('substring("12345", 0 div 0, 3)', self.doc)
        self.failUnlessEqual(result, '')

    def test_string_substring_nan_length(self):
        result = xpath.find('substring("12345", 1, 0 div 0)', self.doc)
        self.failUnlessEqual(result, '')

    def test_string_substring_inf_length(self):
        result = xpath.find('substring("12345", -42, 1 div 0)', self.doc)
        self.failUnlessEqual(result, '12345')

    def test_string_substring_inf_to_inf(self):
        result = xpath.find('substring("12345", -1 div 0, 1 div 0)', self.doc)
        self.failUnlessEqual(result, '')

    def test_string_substring_start_after_end(self):
        result = xpath.find('substring("12345", 6, 1)', self.doc)
        self.failUnlessEqual(result, '')

    def test_string_substring_zero_length(self):
        result = xpath.find('substring("12345", 1, 0)', self.doc)
        self.failUnlessEqual(result, '')

    def test_string_length(self):
        result = xpath.find('string-length("12345")', self.doc)
        self.failUnlessEqual(result, 5)

    def test_string_length_implicit(self):
        result = xpath.find('//para[string-length()=5]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["3"])

    def test_normalize_space(self):
        result = xpath.find('normalize-space("   one   two   ")', self.doc)
        self.failUnlessEqual(result, "one two")

    def test_normalize_space_implicit(self):
        result = xpath.find('//para[normalize-space() = "Four"]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["4"])

    def test_translate(self):
        result = xpath.find('translate("abcdef", "abcde", "xyz")', self.doc)
        self.failUnlessEqual(result, "xyzf")

class TestBooleanFunctions(unittest.TestCase):
    """Section 4.3: Boolean Functions"""

    xml = """
<doc id="0">
    <para id="1" />
    <para id="2" xml:lang="en">
        <item id="3" />
        English
        <section id="4" xml:lang="jp">
            <item id="5" />
            Nihongo
        </section>
    </para>
    <para id="6" xml:lang="EN">
        ENGLISH
    </para>
    <para id="7" xml:lang="en-us">
        US English
    </para>
    <para id="8" xml:lang="EN-UK">
        UK English
    </para>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_boolean_number_one(self):
        result = xpath.find('boolean(1)', self.doc)
        self.failUnlessEqual(result, True)

    def test_boolean_number_zero(self):
        result = xpath.find('boolean(0)', self.doc)
        self.failUnlessEqual(result, False)

    def test_boolean_number_nan(self):
        result = xpath.find('boolean(0 div 0)', self.doc)
        self.failUnlessEqual(result, False)

    def test_boolean_nodeset_empty(self):
        result = xpath.find('boolean(cod)', self.doc)
        self.failUnlessEqual(result, False)

    def test_boolean_nodeset_nonempty(self):
        result = xpath.find('boolean(doc)', self.doc)
        self.failUnlessEqual(result, True)

    def test_boolean_string_empty(self):
        result = xpath.find('boolean("")', self.doc)
        self.failUnlessEqual(result, False)

    def test_boolean_string_nonempty(self):
        result = xpath.find('boolean("foo")', self.doc)
        self.failUnlessEqual(result, True)

    def test_not(self):
        result = xpath.find('not(1 = 1)', self.doc)
        self.failUnlessEqual(result, False)

    def test_true(self):
        result = xpath.find('true()', self.doc)
        self.failUnlessEqual(result, True)

    def test_false(self):
        result = xpath.find('false()', self.doc)
        self.failUnlessEqual(result, False)

    def test_lang_elements_en(self):
        result = xpath.find('//*[lang("en")]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3", "6", "7", "8"])

    def test_lang_elements_en_us(self):
        result = xpath.find('//*[lang("EN-US")]', self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["7"])

    def test_lang_text_jp(self):
        result = xpath.find(
            'normalize-space((//text()[lang("jp")])[normalize-space()])',
            self.doc)
        self.failUnlessEqual(result, 'Nihongo')

class TestNumberFunctions(unittest.TestCase):
    """Section 4.4: Number Functions"""

    xml = """
<doc>
    <item>1</item>
    <item>2</item>
    <item>3</item>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_number_string(self):
        result = xpath.find('number("-1e5")', self.doc)
        self.failUnlessEqual(result, -100000)

    def test_number_true(self):
        result = xpath.find('number(true())', self.doc)
        self.failUnlessEqual(result, 1)

    def test_number_false(self):
        result = xpath.find('number(false())', self.doc)
        self.failUnlessEqual(result, 0)

    def test_number_nodeset(self):
        result = xpath.find('number(//item)', self.doc)
        self.failUnlessEqual(result, 1)

    def test_number_implicit(self):
        result = xpath.find('string(//item[number()=4 div 2])', self.doc)
        self.failUnlessEqual(result, '2')

    def test_number_sum(self):
        result = xpath.find('sum(//item)', self.doc)
        self.failUnlessEqual(result, 6)

    def test_number_floor_positive(self):
        result = xpath.find('floor(1.99)', self.doc)
        self.failUnlessEqual(result, 1)

    def test_number_floor_negative(self):
        result = xpath.find('floor(-1.99)', self.doc)
        self.failUnlessEqual(result, -2)

    def test_number_ceiling_positive(self):
        result = xpath.find('ceiling(1.99)', self.doc)
        self.failUnlessEqual(result, 2)

    def test_number_ceiling_negative(self):
        result = xpath.find('ceiling(-1.99)', self.doc)
        self.failUnlessEqual(result, -1)

    def test_number_round_positive(self):
        result = xpath.find('round(1.5)', self.doc)
        self.failUnlessEqual(result, 2)

    # Python rounds away from 0.  XPath's round() is specced as rounding
    # towards +Inf.  Thus, this test fails.
    #def test_number_round_negative(self):
    #    result = xpath.find('round(-1.5)', self.doc)
    #    self.failUnlessEqual(result, 1)

    def test_number_round_nan(self):
        result = xpath.find('round(0 div 0)', self.doc)
        self.failIfEqual(result, result)

    def test_number_round_inf(self):
        result = xpath.find('round(1 div 0)', self.doc)
        self.failUnlessEqual(result, float('inf'))

    def test_number_round_neginf(self):
        result = xpath.find('round(-1 div 0)', self.doc)
        self.failUnlessEqual(result, float('-inf'))

if __name__ == '__main__':
    unittest.main()
