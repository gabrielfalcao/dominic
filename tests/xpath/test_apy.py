#!/usr/bin/env python

import unittest
import traceback
import xml.dom.minidom
from dominic import xpath

class TestAPI(unittest.TestCase):
    """Module API."""

    xml = """
<doc xmlns:pydomxpath="http://code.google.com/p/py-dom-xpath/">
    <item id="1">argument</item>
    <item id="2">lumberjack</item>
    <item id="3">parrot</item>
    <item id="4" xmlns="http://porcupine.example.org/">porcupine</item>
</doc>
"""
    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)
        self.context = xpath.XPathContext()

    def test_api_decorator_raises_exception_to_trim_trace(self):
        "xpath.api decorator trims the trace for xpath functions"

        def throw_away():
            raise xpath.XPathError('oh yeah, original trace here!')

        try:
            throw_away()
        except xpath.XPathError, error1:
            trace1 = traceback.format_exc(error1)

        try:
            xpath.api(throw_away)()
        except xpath.XPathError, error2:
            trace2 = traceback.format_exc(error2)

        self.failIfEqual(trace1, trace2)

    def test_context_clonning(self):
        "XPathContext.clone carbon copies default_namespace, namespaces and variables"
        cloned = self.context.clone()
        assert cloned is not self.context
        self.failUnlessEqual(cloned.__class__, self.context.__class__)
        self.failUnlessEqual(
            cloned.default_namespace,
            self.context.default_namespace
        )
        self.failUnlessEqual(cloned.namespaces, self.context.namespaces)
        self.failUnlessEqual(cloned.variables, self.context.variables)

    def multitest(self, expr, **kwargs):
        functions = ['find', 'findnode', 'findvalue', 'findvalues']
        results = {}
        context = xpath.XPathContext(**kwargs)
        compiled = xpath.XPath(expr)

        def invoke(obj, func, *args, **kwargs):
            try:
                return getattr(obj, func)(*args, **kwargs)
            except xpath.XPathError, e:
                return e.__class__

        for f in functions:
            results[f] = invoke(xpath, f, expr, self.doc, **kwargs)
            self.failUnlessEqual(results[f],
                                 invoke(compiled, f, self.doc, **kwargs))
            self.failUnlessEqual(results[f],
                                 invoke(context, f, expr, self.doc, **kwargs))

            #results[f] = getattr(xpath, f)(expr, self.doc, **kwargs)

            #self.failUnlessEqual(results[f],
            #                     getattr(compiled, f)(self.doc, **kwargs))

            #self.failUnlessEqual(results[f],
            #                     getattr(context, f)(expr, self.doc, **kwargs))

        return results

    def test_empty_result(self):
        results = self.multitest('//item[@id=9]')
        self.failUnlessEqual(results['find'], [])
        self.failUnlessEqual(results['findnode'], None)
        self.failUnlessEqual(results['findvalue'], None)
        self.failUnlessEqual(results['findvalues'], [])

    def test_one_result(self):
        results = self.multitest('//item[@id=2]')
        self.failUnlessEqual([x.getAttribute("id") for x in results['find']],
                             ["2"])
        self.failUnlessEqual(results['findnode'].getAttribute("id"), "2")
        self.failUnlessEqual(results['findvalue'], 'lumberjack')
        self.failUnlessEqual(results['findvalues'], ['lumberjack'])

    def test_multiple_results(self):
        results = self.multitest('//item')
        self.failUnlessEqual([x.getAttribute("id") for x in results['find']],
                             ["1", "2", "3"])
        self.failUnlessEqual(results['findnode'].getAttribute("id"), "1")
        self.failUnlessEqual(results['findvalue'], 'argument')
        self.failUnlessEqual(results['findvalues'],
                             ['argument', 'lumberjack', 'parrot'])

    def test_variables(self):
        variables = {}
        variables['a'] = 90
        variables[('http://var.example.org/', 'b')] = 10

        namespaces = {}
        namespaces['var'] = 'http://var.example.org/'

        results = self.multitest('//item[@id=$a div($var:b*$c)]',
                                 namespaces=namespaces,
                                 variables=variables, c=3)
        self.failUnlessEqual([x.getAttribute("id") for x in results['find']],
                             ["3"])
        self.failUnlessEqual(results['findnode'].getAttribute("id"), "3")
        self.failUnlessEqual(results['findvalue'], 'parrot')
        self.failUnlessEqual(results['findvalues'], ['parrot'])

    def test_default_namespace(self):
        results = self.multitest('//item',
                        default_namespace="http://porcupine.example.org/")
        self.failUnlessEqual([x.getAttribute("id") for x in results['find']],
                             ["4"])
        self.failUnlessEqual(results['findnode'].getAttribute("id"), "4")
        self.failUnlessEqual(results['findvalue'], 'porcupine')
        self.failUnlessEqual(results['findvalues'], ['porcupine'])

    def test_compiled_expr_argument(self):
        expr = xpath.XPath('//item[3]')
        result = xpath.findvalue(expr, self.doc)
        self.failUnlessEqual(result, 'parrot')

    def test_nonnode_result(self):
        results = self.multitest('1')
        self.failUnlessEqual(results['find'], 1)
        self.failUnlessEqual(results['findnode'], xpath.XPathTypeError)
        self.failUnlessEqual(results['findvalue'], 1)
        self.failUnlessEqual(results['findvalues'], xpath.XPathTypeError)

    def test_parse_error(self):
        self.failUnlessRaises(xpath.XPathParseError,
                              xpath.find, 'child/parent', self.doc)

class TestNamespacesAPI(unittest.TestCase):
    """Namespaces in the module API."""

    xml = """
<doc xmlns="http://parrot.example.org/">
    <item id="1">argument</item>
    <item id="2">lumberjack</item>
    <item id="3">parrot</item>
    <item id="4" xmlns="http://porcupine.example.org/">porcupine</item>
</doc>
"""

    def setUp(self):
        self.doc = xml.dom.minidom.parseString(self.xml)

    def test_empty_context(self):
        context = xpath.XPathContext()
        result = context.findvalues('//item', self.doc)
        self.failUnlessEqual(result, [])

    def test_explicit_document_context(self):
        nsdoc = xml.dom.minidom.parseString(
            """<doc xmlns="http://porcupine.example.org/" />""")
        context = xpath.XPathContext(nsdoc)
        result = context.findvalues('//item', self.doc)
        self.failUnlessEqual(result, ['porcupine'])

    def test_explicit_document_context_prefix(self):
        nsdoc = xml.dom.minidom.parseString(
            """<doc xmlns:pork="http://porcupine.example.org/" />""")
        context = xpath.XPathContext(nsdoc)
        result = context.findvalues('//pork:item', self.doc)
        self.failUnlessEqual(result, ['porcupine'])

if __name__ == '__main__':
    unittest.main()
