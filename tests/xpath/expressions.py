#!/usr/bin/env python

import unittest
import xml.dom.minidom
from dominic import xpath

class TestVariables(unittest.TestCase):
    """Section 3.1: Basics (Variable References)"""

    xml = """
<doc>
    <item id="1" />
    <item id="2" />
    <item id="3" />
    <item id="4" />
    <item id="5" />
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)
        self.context = xpath.XPathContext()
        self.context.variables['start'] = 2
        self.context.variables['end'] = '4'
        self.context.variables[('http://anaconda.python.org', 'start')] = 3
        self.context.namespaces['ana'] = 'http://anaconda.python.org'

    def test_persistant_variables(self):
        result = self.context.find('//item[@id >= $start and @id <= $end]',
                                   self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3", "4"])

    def test_temporary_variables(self):
        result = self.context.find('//item[@id >= $start and @id <= $end]',
                                   self.doc, end=3)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3"])
        result = self.context.find('//item[@id >= $start and @id <= $end]',
                                   self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3", "4"])

    def test_unknown_variable(self):
        self.failUnlessRaises(xpath.XPathUnknownVariableError,
                              xpath.find,
                              '//item[@id >= $start and @id <= $end]',
                              self.doc)

    def test_unknown_variable_with_temporary(self):
        self.failUnlessRaises(xpath.XPathUnknownVariableError,
                              xpath.find,
                              '//item[@id >= $start and @id <= $end]',
                              self.doc, start=1)

    def test_variable_namespace(self):
        result = self.context.find('//item[@id >= $ana:start and @id <= $end]',
                                   self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["3", "4"])

    def test_variable_unknown_namespace(self):
        self.failUnlessRaises(xpath.XPathUnknownPrefixError,
                              self.context.find,
                              '//item[@id >= $a:start and @id <= $end]',
                              self.doc)

    def test_unknown_namespace_variable(self):
        self.failUnlessRaises(xpath.XPathUnknownVariableError,
                              self.context.find,
                              '//item[@id >= $ana:foo and @id <= $end]',
                              self.doc)

class TestFunctionCalls(unittest.TestCase):
    """Section 3.2: Function Calls"""

    xml = """
<doc />
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_function_too_many_arguments(self):
        self.failUnlessRaises(xpath.XPathTypeError,
                              xpath.find, 'position(1)', self.doc)

    def test_function_too_few_arguments(self):
        self.failUnlessRaises(xpath.XPathTypeError,
                              xpath.find, 'not()', self.doc)

    def test_function_cast_success(self):
        result = xpath.find('string-length(100)', self.doc)
        self.failUnlessEqual(result, 3)

    def test_function_cast_failure(self):
        self.failUnlessRaises(xpath.XPathTypeError,
                              xpath.find, 'count(100)', self.doc)

    def test_unknown_function(self):
        self.failUnlessRaises(xpath.XPathUnknownFunctionError,
                              xpath.find, 'adumbrate()', self.doc)

class TestNodeSets(unittest.TestCase):
    """Section 3.3: Node-sets"""

    xml = """
<doc>
    <item id="1" />
    <item id="2" />
    <item id="3" />
    <item id="4" />
    <item id="5" />
    <item id="6" />
    <item id="7" />
    <item id="8" />
    <item id="9" />
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_union(self):
        result = xpath.find('//item[@id mod 2 = 0] | //item[@id mod 3 = 0]',
                            self.doc)
        self.failUnlessEqual([x.getAttribute("id") for x in result],
                             ["2", "3", "4", "6", "8", "9"])

    def test_union_type_error(self):
        self.failUnlessRaises(xpath.XPathTypeError,
                              xpath.find, '//item | 42', self.doc)

    def test_expression_path_element(self):
        result = xpath.find('/doc/(item[@id = 2] | item[@id = 6])/@id',
                            self.doc)
        self.failUnlessEqual([x.value for x in result],
                             ["2", "6"])

    def test_invalid_path_start(self):
        self.failUnlessRaises(xpath.XPathTypeError,
                              xpath.find, '"monty"/anaconda',
                              self.doc)

    def test_invalid_path_element(self):
        self.failUnlessRaises(xpath.XPathTypeError,
                              xpath.find, '/doc/string(item[@id = 2])/@id',
                              self.doc)

    def test_invalid_filter_expression(self):
        self.failUnlessRaises(xpath.XPathTypeError,
                              xpath.find, '(1)[1]', self.doc)

class TestBooleans(unittest.TestCase):
    """Section 3.4: Booleans"""

    xml = """
<doc>
    <set id="1">
        <item>1</item>
        <item>2</item>
        <item>3</item>
        <item>4</item>
    </set>
    <set id="2">
        <item>5</item>
        <item>6</item>
        <item>7</item>
        <item>8</item>
    </set>
    <set id="3">
        <item>0</item>
        <item>3</item>
        <item>6</item>
        <item>9</item>
    </set>
    <set id="4">
        <item>42.0</item>
    </set>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_or_true_true(self):
        result = xpath.find('1 or 1', self.doc)
        self.failUnlessEqual(result, True)

    def test_or_true_false(self):
        result = xpath.find('1 or 0', self.doc)
        self.failUnlessEqual(result, True)

    def test_or_false_true(self):
        result = xpath.find('0 or 1', self.doc)
        self.failUnlessEqual(result, True)

    def test_or_false_false(self):
        result = xpath.find('0 or 0', self.doc)
        self.failUnlessEqual(result, False)

    def test_and_true_true(self):
        result = xpath.find('1 and 1', self.doc)
        self.failUnlessEqual(result, True)

    def test_and_true_false(self):
        result = xpath.find('1 and 0', self.doc)
        self.failUnlessEqual(result, False)

    def test_and_false_true(self):
        result = xpath.find('0 and 1', self.doc)
        self.failUnlessEqual(result, False)

    def test_and_false_false(self):
        result = xpath.find('0 and 0', self.doc)
        self.failUnlessEqual(result, False)

    def test_nodeset_positive_equality(self):
        result = xpath.find('(//set[@id=1]/*) = (//set[@id=3]/*)', self.doc)
        self.failUnlessEqual(result, True)

    def test_nodeset_negative_equality(self):
        result = xpath.find('(//set[@id=1]/*) = (//set[@id=2]/*)', self.doc)
        self.failUnlessEqual(result, False)

    def test_nodeset_positive_inequality(self):
        result = xpath.find('(//set[@id=1]/*) != (//set[@id=1]/*)', self.doc)
        self.failUnlessEqual(result, True)

    def test_nodeset_negative_inequality(self):
        result = xpath.find('(//set[@id=4]/*) != (//set[@id=4]/*)', self.doc)
        self.failUnlessEqual(result, False)

    def test_nodeset_positive_le(self):
        result = xpath.find('(//set[@id=1]/*) <= (//set[@id=2]/*)', self.doc)
        self.failUnlessEqual(result, True)

    def test_nodeset_negative_le(self):
        result = xpath.find('(//set[@id=2]/*) <= (//set[@id=1]/*)', self.doc)
        self.failUnlessEqual(result, False)

    def test_nodeset_positive_lt(self):
        result = xpath.find('(//set[@id=1]/*) < (//set[@id=2]/*)', self.doc)
        self.failUnlessEqual(result, True)

    def test_nodeset_negative_lt(self):
        result = xpath.find('(//set[@id=2]/*) < (//set[@id=1]/*)', self.doc)
        self.failUnlessEqual(result, False)

    def test_nodeset_positive_ge(self):
        result = xpath.find('(//set[@id=2]/*) > (//set[@id=1]/*)', self.doc)
        self.failUnlessEqual(result, True)

    def test_nodeset_negative_ge(self):
        result = xpath.find('(//set[@id=1]/*) > (//set[@id=2]/*)', self.doc)
        self.failUnlessEqual(result, False)

    def test_nodeset_positive_gt(self):
        result = xpath.find('(//set[@id=2]/*) > (//set[@id=1]/*)', self.doc)
        self.failUnlessEqual(result, True)

    def test_nodeset_negative_gt(self):
        result = xpath.find('(//set[@id=1]/*) > (//set[@id=2]/*)', self.doc)
        self.failUnlessEqual(result, False)

    def test_boolean_positive_equality(self):
        result = xpath.find('(//set[@id=4]/*) = (1 = 1)', self.doc)
        self.failUnlessEqual(result, True)

    def test_boolean_negative_equality(self):
        result = xpath.find('(//set[@id=4]/*) = (1 = 0)', self.doc)
        self.failUnlessEqual(result, False)

    def test_boolean_positive_inequality(self):
        result = xpath.find('(//set[@id=4]/*) != (1 = 0)', self.doc)
        self.failUnlessEqual(result, True)

    def test_boolean_negative_inequality(self):
        result = xpath.find('(//set[@id=4]/*) != (1 = 1)', self.doc)
        self.failUnlessEqual(result, False)

    def test_number_positive_equality(self):
        result = xpath.find('(//set[@id=4]/*) = 42', self.doc)
        self.failUnlessEqual(result, True)

    def test_number_negative_equality(self):
        result = xpath.find('(//set[@id=4]/*) = 43', self.doc)
        self.failUnlessEqual(result, False)

    def test_number_positive_inequality(self):
        result = xpath.find('(//set[@id=4]/*) != 43', self.doc)
        self.failUnlessEqual(result, True)

    def test_number_negative_inequality(self):
        result = xpath.find('(//set[@id=4]/*) != 42', self.doc)
        self.failUnlessEqual(result, False)

    def test_string_positive_equality(self):
        result = xpath.find('(//set[@id=4]/*) = "42.0"', self.doc)
        self.failUnlessEqual(result, True)

    def test_string_negative_equality(self):
        result = xpath.find('(//set[@id=4]/*) = "42"', self.doc)
        self.failUnlessEqual(result, False)

    def test_string_positive_inequality(self):
        result = xpath.find('(//set[@id=4]/*) != "42"', self.doc)
        self.failUnlessEqual(result, True)

    def test_string_negative_inequality(self):
        result = xpath.find('(//set[@id=4]/*) != "42.0"', self.doc)
        self.failUnlessEqual(result, False)

    def test_numeric_coercion_le(self):
        result = xpath.find('"a" <= "a"', self.doc)
        self.failUnlessEqual(result, False)

    def test_numeric_coercion_lt(self):
        result = xpath.find('"a" <= "b"', self.doc)
        self.failUnlessEqual(result, False)

    def test_numeric_coercion_ge(self):
        result = xpath.find('"a" >= "a"', self.doc)
        self.failUnlessEqual(result, False)

    def test_numeric_coercion_gt(self):
        result = xpath.find('"b" > "a"', self.doc)
        self.failUnlessEqual(result, False)

    def test_number_positive_le(self):
        result = xpath.find('1 <= 1', self.doc)
        self.failUnlessEqual(result, True)

    def test_number_negative_le(self):
        result = xpath.find('2 <= 1', self.doc)
        self.failUnlessEqual(result, False)

    def test_number_positive_lt(self):
        result = xpath.find('1 < 2', self.doc)
        self.failUnlessEqual(result, True)

    def test_number_negative_lt(self):
        result = xpath.find('1 < 1', self.doc)
        self.failUnlessEqual(result, False)

    def test_number_positive_ge(self):
        result = xpath.find('1 >= 1', self.doc)
        self.failUnlessEqual(result, True)

    def test_number_negative_ge(self):
        result = xpath.find('1 >= 2', self.doc)
        self.failUnlessEqual(result, False)

    def test_number_positive_gt(self):
        result = xpath.find('2 > 1', self.doc)
        self.failUnlessEqual(result, True)

    def test_number_negative_gt(self):
        result = xpath.find('1 > 1', self.doc)
        self.failUnlessEqual(result, False)

class TestNumbers(unittest.TestCase):
    """Section 3.5: Numbers"""

    xml = """
<doc>
    <x>42</x>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_addition(self):
        result = xpath.find('//x + 2.2', self.doc)
        self.failUnlessEqual(result, 44.2)

    def test_subtraction(self):
        result = xpath.find('//x - 2.2', self.doc)
        self.failUnlessEqual(result, 39.8)

    def test_multiplication(self):
        result = xpath.find('//x * 1.5', self.doc)
        self.failUnlessEqual(result, 63)

    def test_division(self):
        result = xpath.find('//x div 5', self.doc)
        self.failUnlessEqual(result, 8.4)

    def test_modulo_positive_positive(self):
        result = xpath.find('5 mod 2', self.doc)
        self.failUnlessEqual(result, 1)

    def test_modulo_positive_negative(self):
        result = xpath.find('5 mod -2', self.doc)
        self.failUnlessEqual(result, 1)

    def test_modulo_negative_positive(self):
        result = xpath.find('-5 mod 2', self.doc)
        self.failUnlessEqual(result, -1)

    def test_modulo_negative_negative(self):
        result = xpath.find('-5 mod -2', self.doc)
        self.failUnlessEqual(result, -1)

    def test_negation(self):
        result = xpath.find('-//x', self.doc)
        self.failUnlessEqual(result, -42)

class TestPrecedence(unittest.TestCase):
    """Operator precedence"""

    xml = """
<doc/>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_or_and(self):
        result = xpath.find('1 or 0 and 0', self.doc)
        self.failUnlessEqual(result, True)

    def test_and_eq(self):
        result = xpath.find('1 and 2 = 2', self.doc)
        self.failUnlessEqual(result, True)

    def test_eq_rel(self):
        result = xpath.find('0 = 1 > 2', self.doc)
        self.failUnlessEqual(result, True)

    def test_rel_assoc(self):
        result = xpath.find('3 > 2 > 1', self.doc)
        self.failUnlessEqual(result, False)

    def test_rel_math(self):
        result = xpath.find('1 < 1 + 1', self.doc)
        self.failUnlessEqual(result, True)

    def test_math(self):
        result = xpath.find('3 + 4 div 2 - 4 * 1 div 2', self.doc)
        self.failUnlessEqual(result, 3)

if __name__ == '__main__':
    unittest.main()
